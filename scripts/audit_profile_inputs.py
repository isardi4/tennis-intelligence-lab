"""Cobertura exploratoria de métricas de perfil en 2024; no produce perfiles históricos."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.download import verify
from tennis_lab.profiles import profile_observations


if __name__ == "__main__":
    report = {"season": 2024, "ready_for_training": False, "sources": {}}
    for source in ("sackmann", "tml"):
        directory = ROOT / "data/raw" / source
        name = "atp_matches_2024.csv" if source == "sackmann" else "2024.csv"
        manifest = json.loads((directory / "manifest.json").read_text())
        verify(directory / name, next(item for item in manifest["files"] if item["name"] == name))
        rows = read_rows(directory / name)
        coverage = Counter()
        for row in rows:
            for side in ("w", "l"):
                coverage.update(profile_observations(row, side).keys())
        report["sources"][source] = {"matches": len(rows), "player_match_observations": len(rows) * 2,
                                     "usable_observations_by_metric": dict(coverage)}
    output = ROOT / "data/processed/stage_1_2025/profile_input_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
