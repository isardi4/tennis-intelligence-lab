import csv
from datetime import date
import json
from pathlib import Path
import duckdb
import pytest
from tennis_lab.experiments import Experiment
from tennis_lab.ingestion.dataset import build_exploration_dataset, checked_files
from tennis_lab.ingestion.download import fingerprints


def write_csv(path, columns, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def raw_fixture(root):
    for source in ("sackmann", "tml"):
        directory = root / source
        directory.mkdir(parents=True)
        for year, dates in ((2024, ["20241230"]), (2025, ["20250101", "20241230"]),
                            (2026, ["20260101"])):
            name = f"atp_matches_{year}.csv" if source == "sackmann" else f"{year}.csv"
            rows = [{"tourney_id": f"{year}-580", "tourney_date": d, "winner_id": "1", "loser_id": "2"} for d in dates]
            write_csv(directory / name, list(rows[0]), rows)
        if source == "sackmann":
            write_csv(directory / "atp_players.csv",
                      ["player_id", "name_first", "name_last", "hand", "dob", "ioc", "height", "wikidata_id"],
                      [{"player_id": "1", "name_first": "Player", "name_last": "One", "dob": "not-a-date"}])
            write_csv(directory / "atp_rankings_20s.csv", ["ranking_date", "rank", "player", "points"],
                      [{"ranking_date": d, "rank": "1", "player": "1", "points": ""}
                       for d in ("20241230", "20250106", "20260105")])
        files = [{"name": p.name, **fingerprints(p)} for p in directory.glob("*.csv")]
        (directory / "manifest.json").write_text(json.dumps({"files": files}))


def test_training_parquet_and_rankings_exclude_evaluation_and_future(tmp_path):
    raw = tmp_path / "raw"
    raw_fixture(raw)
    output = tmp_path / "output"
    counts = build_exploration_dataset(raw, output, Experiment("stage_1_2025", date(2024, 12, 31), 2025))
    assert counts["sackmann"] == {"train": 1, "evaluation": 1, "quarantine": 1, "future": 1}
    with duckdb.connect() as con:
        training = con.read_parquet(str(output / "sackmann_training.parquet"))
        assert training.project("source_season").fetchall() == [(2024,)]
        assert counts["rankings"]["max_date"] == "2024-12-30"
        assert counts["rankings"]["rows"] == 1
        assert con.read_parquet(str(output / "rankings.parquet")).project("ranking_points").fetchone() == (None,)
        assert con.read_parquet(str(output / "players_snapshot.parquet")).project("birth_date").fetchone() == (None,)


def test_altered_or_untracked_raw_data_rejected(tmp_path):
    raw_fixture(tmp_path)
    directory = tmp_path / "sackmann"
    file = directory / "atp_matches_2024.csv"
    file.write_text(file.read_text() + "tampered\n")
    with pytest.raises(ValueError, match="Integridad"):
        checked_files(directory, "atp_matches_*.csv")


def test_missing_file_rejected(tmp_path):
    raw_fixture(tmp_path)
    (tmp_path / "sackmann" / "atp_matches_2024.csv").unlink()
    with pytest.raises(ValueError, match="conjunto"):
        checked_files(tmp_path / "sackmann", "atp_matches_*.csv")
