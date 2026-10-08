"""Auditoría reproducible de cobertura MCP hasta 2024, sin entrenar ni leer resultados futuros."""
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.charting import charting_coverage
from tennis_lab.ingestion.download import verify


def main():
    directory = ROOT / "data/raw/mcp"
    config_path = ROOT / "configs/mcp_source.json"
    config = json.loads(config_path.read_text())
    for item in config["files"]:
        verify(directory / item["name"], item)
    summary, players, eligible = charting_coverage(read_rows(directory / "charting-m-matches.csv"), date(2024, 12, 31))
    for table in ("ShotTypes", "Rally", "NetPoints"):
        pairs = Counter()
        labels = Counter()
        for row in read_rows(directory / f"charting-m-stats-{table}.csv"):
            match = eligible.get(row["match_id"])
            if match is None:
                continue
            names = (match["Player 1"], match["Player 2"])
            if table == "Rally":
                if set((row["server"], row["returner"])) != set(names):
                    raise ValueError("Participantes inconsistentes en Rally")
                for name in names:
                    pairs[(row["match_id"], name)] += 1
            else:
                if row["player"] not in names:
                    raise ValueError(f"Participante inconsistente en {table}")
                pairs[(row["match_id"], row["player"])] += 1
            labels[row["row"]] += 1
        per_player = defaultdict(int)
        for _, name in pairs:
            per_player[name] += 1
        for player in players:
            player[f"matches_with_{table}"] = per_player[player["player"]]
        summary.setdefault("aggregate_tables", {})[table] = {"player_match_pairs_present": len(pairs), "row_labels": dict(labels)}
    summary["revision"] = config["revision"]
    summary["config_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    summary["examples"] = [player for player in players if player["player"] in ("Carlos Alcaraz", "Fabio Fognini", "Novak Djokovic", "Jannik Sinner")]
    output = ROOT / "data/processed/stage_1_2025"
    output.mkdir(parents=True, exist_ok=True)
    (output / "charting_coverage.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    (output / "charting_players.json").write_text(json.dumps(players, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "aggregate_tables"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
