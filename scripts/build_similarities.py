"""Similitudes exploratorias top 350, 2022–2024; grupos/superficies separados."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.similarity import neighbors

BASIC = ("ace_rate", "double_fault_rate", "first_serve_in_rate", "first_serve_points_won",
         "second_serve_points_won", "first_serve_return_points_won", "second_serve_return_points_won")
STYLE = ("Fside_shot_share", "Fside_winner_rate", "Fside_unforced_rate", "Bside_winner_rate", "Bside_unforced_rate", "net_points_won")


def main():
    output = ROOT / "data/processed/stage_1_2025"
    source = output / "top350_profiles.json"
    roster = json.loads(source.read_text())
    result = {"ready_for_prediction": False, "window": ["2022-01-01", "2024-12-31"],
              "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "roster": {row["player_id"]: row["name"] for row in roster}, "views": {}}
    for surface in ("All", "Hard", "Clay", "Grass"):
        for level in ("ATP", "Challenger_main", "Challenger_qualifying"):
            profiles = {row["player_id"]: row["basic_profile_by_level"].get(level, {}).get(surface, {}) for row in roster}
            result["views"][f"basic/{level}/{surface}"] = neighbors(profiles, BASIC)
        if surface != "All":
            continue
        profiles = {row["player_id"]: next((profile["metrics"] for profile in row["style_profiles"] if profile["surface"] == surface), {}) for row in roster}
        result["views"][f"style/MCP/{surface}"] = neighbors(profiles, STYLE)
    (output / "player_similarities.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for key, view in result["views"].items():
        print(key, view["eligible_players"])
    for row in roster:
        if row["name"] in ("Carlos Alcaraz", "Fabio Fognini"):
            for key in ("basic/ATP/All", "style/MCP/All"):
                print(row["name"], key, [(result["roster"][neighbor["player_id"]], round(neighbor["distance"], 3)) for neighbor in result["views"][key]["neighbors"].get(row["player_id"], [])])


if __name__ == "__main__":
    main()
