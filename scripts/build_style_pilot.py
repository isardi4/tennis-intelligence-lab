"""Perfiles descriptivos MCP 2022–2024; no son variables listas para backtest."""
from collections import Counter, defaultdict
from datetime import date
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.charting import charting_coverage
from tennis_lab.ingestion.download import verify


def validated_counts(row, columns):
    values = [int(row[column]) for column in columns]
    if any(value < 0 for value in values):
        raise ValueError("Contador negativo")
    return values


def main(players=("Carlos Alcaraz", "Fabio Fognini"), output_name="style_pilot.json", verbose=True, excluded_year=None):
    directory = ROOT / "data/raw/mcp"
    config = json.loads((ROOT / "configs/mcp_source.json").read_text())
    for item in config["files"]:
        verify(directory / item["name"], item)
    _, _, eligible = charting_coverage(read_rows(directory / "charting-m-matches.csv"), date(2024, 12, 31))
    eligible = {key: row for key, row in eligible.items() if row["Date"] >= "20220101"
                and row["Date"][:4] != str(excluded_year)}
    tables = {}
    for name in ("ShotTypes", "Rally", "NetPoints"):
        selected = [row for row in read_rows(directory / f"charting-m-stats-{name}.csv") if row["match_id"] in eligible]
        counts = Counter((row["match_id"], row.get("player", ""), row["row"]) for row in selected)
        tables[name] = {key: row for row in selected if counts[(key := (row["match_id"], row.get("player", ""), row["row"]))] == 1}
    profiles = []
    rejected = Counter()
    for player in players:
        for surface in ("All",):
            metrics = defaultdict(lambda: [0, 0, 0])
            matches = [row for row in eligible.values() if player in (row["Player 1"], row["Player 2"]) and (surface == "All" or row["Surface"] == surface)]
            for match in matches:
                identifier = match["match_id"]
                previous = deepcopy(metrics)
                def add(metric, numerator, denominator):
                    if not 0 <= numerator <= denominator:
                        raise ValueError("Numerador fuera de rango")
                    if denominator:
                        values = metrics[metric]
                        values[0] += numerator
                        values[1] += denominator
                        values[2] += 1
                try:
                    total = tables["ShotTypes"].get((identifier, player, "Total"))
                    if total:
                        shots, = validated_counts(total, ["shots"])
                        for label in ("Fside", "Bside"):
                            row = tables["ShotTypes"].get((identifier, player, label))
                            if row:
                                n, = validated_counts(row, ["shots"])
                                add(f"{label}_shot_share", n, shots)
                    for label in ("Fside", "Bside"):
                        row = tables["ShotTypes"].get((identifier, player, label))
                        if row:
                            shots, winners, errors = validated_counts(row, ["shots", "winners", "unforced"])
                            add(f"{label}_winner_rate", winners, shots)
                            add(f"{label}_unforced_rate", errors, shots)
                    row = tables["NetPoints"].get((identifier, player, "NetPoints"))
                    if row:
                        points, won = validated_counts(row, ["net_pts", "pts_won"])
                        add("net_points_won", won, points)
                    for label in ("1-3", "4-6", "7-9", "10"):
                        row = tables["Rally"].get((identifier, "", label))
                        if row:
                            if {row["server"], row["returner"]} != {match["Player 1"], match["Player 2"]}:
                                raise ValueError("Identidades inconsistentes")
                            column = "pl1_won" if match["Player 1"] == player else "pl2_won"
                            points, won = validated_counts(row, ["pts", column])
                            if int(row["pl1_won"]) + int(row["pl2_won"]) != points:
                                raise ValueError("Puntos inconsistentes")
                            add(f"rally_{label}_points_won", won, points)
                except (ValueError, KeyError):
                    metrics = previous
                    rejected[identifier] += 1
            profiles.append({"player": player, "surface": surface, "metadata_matches": len(matches),
                             "metrics": {key: {"numerator": value[0], "denominator": value[1], "matches": value[2], "rate": value[0] / value[1]} for key, value in metrics.items()}})
    output = ROOT / "data/processed/stage_1_2025" / output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"window": ["2022-01-01", "2024-12-31"], "excluded_year": excluded_year, "ready_for_training": False,
                                 "revision": config["revision"], "rejected": dict(rejected), "profiles": profiles}, indent=2) + "\n")
    if verbose:
        for profile in profiles:
            print(profile["player"], profile["surface"], profile["metadata_matches"], {key: round(value["rate"] * 100, 1) for key, value in profile["metrics"].items()})
    return profiles


if __name__ == "__main__":
    main()
