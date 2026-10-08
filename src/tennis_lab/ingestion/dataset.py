"""Tablas de exploración con fecha de torneo explícita, no fecha de partido inventada."""
from __future__ import annotations
from pathlib import Path
import duckdb
from tennis_lab.experiments import Experiment
from tennis_lab.ingestion.download import verify
import json


def checked_files(directory: Path, pattern: str) -> list[str]:
    manifest = json.loads((directory / "manifest.json").read_text())
    locked = {item["name"]: item for item in manifest["files"]}
    paths = sorted(directory.glob(pattern))
    if not paths:
        raise ValueError(f"No hay archivos para {pattern}")
    expected = {name for name in locked if Path(name).match(pattern)}
    if {path.name for path in paths} != expected:
        raise ValueError("El conjunto de archivos no coincide con el manifiesto")
    for path in paths:
        verify(path, locked[path.name])
    return [str(path.resolve()) for path in paths]


def build_exploration_dataset(raw_root: Path, output: Path, experiment: Experiment) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    database = output / "exploration.duckdb"
    counts: dict[str, dict] = {}
    with duckdb.connect(str(database)) as con:
        for source, pattern in (("sackmann", "atp_matches_[0-9][0-9][0-9][0-9].csv"),
                                ("tml", "[0-9][0-9][0-9][0-9].csv")):
            paths = checked_files(raw_root / source, pattern)
            con.read_csv(paths, header=True, all_varchar=True, union_by_name=True,
                         filename=True).create_view("input_matches", replace=True)
            con.execute(f"""
                CREATE OR REPLACE TABLE {source}_matches AS
                WITH dated AS (
                    SELECT * EXCLUDE (filename), filename AS source_file,
                        CAST(regexp_extract(filename, '([0-9]{{4}})\\.csv$', 1) AS INTEGER) AS source_season,
                        CAST(try_strptime(tourney_date, '%Y%m%d') AS DATE) AS tournament_start_date
                    FROM input_matches
                )
                SELECT *, CASE
                    WHEN tournament_start_date IS NULL OR year(tournament_start_date) != source_season
                        THEN 'quarantine'
                    WHEN source_season < ? AND tournament_start_date <= ? THEN 'train'
                    WHEN source_season = ? THEN 'evaluation'
                    ELSE 'future' END AS dataset_partition
                FROM dated
            """, [experiment.evaluation_year, experiment.training_cutoff, experiment.evaluation_year])
            con.execute(f"CREATE OR REPLACE VIEW {source}_training AS SELECT * FROM {source}_matches WHERE dataset_partition = 'train'")
            con.execute(f"COPY {source}_matches TO ? (FORMAT PARQUET)", [str(output / f"{source}_matches.parquet")])
            con.execute(f"COPY {source}_training TO ? (FORMAT PARQUET)", [str(output / f"{source}_training.parquet")])
            violations = con.execute(f"SELECT count(*) FROM {source}_training WHERE source_season >= ? OR tournament_start_date > ?", [experiment.evaluation_year, experiment.training_cutoff]).fetchone()[0]
            if violations:
                raise ValueError("El entrenamiento contiene datos fuera del corte")
            counts[source] = dict(con.execute(f"SELECT dataset_partition, count(*) FROM {source}_matches GROUP BY 1").fetchall())
            con.execute("DROP VIEW input_matches")
        player_file = checked_files(raw_root / "sackmann", "atp_players.csv")
        con.read_csv(player_file, all_varchar=True, header=True).create_view("raw_players", replace=True)
        con.execute("""CREATE OR REPLACE TABLE players_snapshot AS
            SELECT player_id AS source_player_id, name_first AS first_name,
                name_last AS last_name, hand,
                CAST(try_strptime(dob, '%Y%m%d') AS DATE) AS birth_date,
                ioc AS country_code, TRY_CAST(height AS INTEGER) AS height_cm,
                wikidata_id FROM raw_players""")
        ranking_files = checked_files(raw_root / "sackmann", "atp_rankings_*.csv")
        con.read_csv(ranking_files, all_varchar=True, header=True, union_by_name=True).create_view("raw_rankings", replace=True)
        con.execute("""CREATE OR REPLACE TABLE rankings AS
            WITH dated AS (
                SELECT CAST(try_strptime(ranking_date, '%Y%m%d') AS DATE) AS ranking_date,
                    player AS source_player_id, TRY_CAST(rank AS INTEGER) AS rank,
                    TRY_CAST(points AS INTEGER) AS ranking_points FROM raw_rankings
            ) SELECT * FROM dated WHERE ranking_date <= ?""", [experiment.training_cutoff])
        con.execute("COPY rankings TO ? (FORMAT PARQUET)", [str(output / "rankings.parquet")])
        con.execute("COPY players_snapshot TO ? (FORMAT PARQUET)", [str(output / "players_snapshot.parquet")])
        counts["rankings"] = {"rows": con.execute("SELECT count(*) FROM rankings").fetchone()[0],
                               "max_date": str(con.execute("SELECT max(ranking_date) FROM rankings").fetchone()[0])}
        con.execute("DROP VIEW raw_players")
        con.execute("DROP VIEW raw_rankings")
    return counts
