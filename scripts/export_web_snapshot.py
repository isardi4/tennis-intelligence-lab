"""Exportar agregados exploratorios para una página estática, sin archivos originales."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / "data/processed/stage_1_2025"
    paths = {key: source / name for key, name in {
        "players": "top350_profiles.json", "similarities": "player_similarities.json",
        "stability": "similarity_stability.json", "coverage": "ranked_profiles_summary.json"}.items()}
    snapshot = {key: json.loads(path.read_text()) for key, path in paths.items()}
    snapshot["source_hashes"] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}
    profile_hash = snapshot["source_hashes"]["players"]
    if any(snapshot[key]["input_sha256"] != profile_hash for key in ("similarities", "stability")):
        raise ValueError("Regenerar similitudes y estabilidad: perfiles de versiones diferentes")
    snapshot["stability"] = snapshot["stability"]["summary"]
    destination = ROOT / "docs/lab-snapshot.js"
    payload = json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    destination.write_text("window.TENNIS_LAB = " + payload + ";\n")
    print(f"Snapshot web: {len(snapshot['players'])} jugadores, {destination.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
