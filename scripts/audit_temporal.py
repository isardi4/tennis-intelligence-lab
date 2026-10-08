"""Vincular evidencia oficial puntual con originales, sin modificar esos datos."""
from pathlib import Path
import hashlib
import json
import sys
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.download import verify
from tennis_lab.ingestion.quality import match_key
from tennis_lab.ingestion.temporal import ResultTiming


def audit_sample(root: Path = ROOT) -> dict:
    config_path = root / "configs/temporal_sample.json"
    config = json.loads(config_path.read_text())
    cases = config["cases"]
    keys = set()
    identifiers = set()
    for case in cases:
        key = match_key({"tourney_id": case["tournament_code"], "round": case["round"],
                         "winner_name": case["players"][0], "loser_name": case["players"][1]}, case["season"])
        if key in keys or case["id"] in identifiers or not case["sources"]:
            raise ValueError("Evidencia duplicada o sin referencia")
        keys.add(key)
        identifiers.add(case["id"])
        finished = date.fromisoformat(case["completed_on"])
        if case.get("started_on") and date.fromisoformat(case["started_on"]) > finished:
            raise ValueError("La finalización precede al inicio")
    records = []
    manifests = {}
    for source in ("sackmann", "tml"):
        directory = root / "data/raw" / source
        manifest_path = directory / "manifest.json"
        manifests[source] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        locked = {item["name"]: item for item in json.loads(manifest_path.read_text())["files"]}
        rows_by_season = {}
        for season in sorted({case["season"] for case in cases}):
            name = f"atp_matches_{season}.csv" if source == "sackmann" else f"{season}.csv"
            verify(directory / name, locked[name])
            rows_by_season[season] = read_rows(directory / name)
        for case in cases:
            season = case["season"]
            key = match_key({"tourney_id": case["tournament_code"], "round": case["round"],
                             "winner_name": case["players"][0], "loser_name": case["players"][1]}, season)
            matches = [row for row in rows_by_season[season] if match_key(row, season) == key]
            if len(matches) != 1:
                raise ValueError(f"{source}/{case['id']}: se esperaba una coincidencia, hay {len(matches)}")
            timing = ResultTiming(date.fromisoformat(case["completed_on"]), case["timezone"])
            usable = timing.usable_from.isoformat()
            if usable != case["expected_usable_from_utc"]:
                raise ValueError(f"Disponibilidad inesperada: {case['id']}")
            records.append({"source": source, "case_id": case["id"], "season": season,
                            "raw_tourney_date": matches[0]["tourney_date"],
                            "completed_on": case["completed_on"], "usable_from_policy_utc": usable,
                            "training_eligible_2024": timing.training_eligible(season, date(2024, 12, 31))})
    return {"sample_cases": len(cases), "provider_links": len(records), "temporal_ready": False,
            "scope": "Muestra dirigida; no mide exactitud del historial ni valida estadísticas/resultados.",
            "historical_publication_timestamp_known": False,
            "configuration_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
            "raw_manifest_sha256": manifests, "records": records}


if __name__ == "__main__":
    result = audit_sample()
    output = ROOT / "data/processed/stage_1_2025/temporal_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"{result['sample_cases']} casos, {result['provider_links']} vínculos verificados. Fase 0 abierta.")
