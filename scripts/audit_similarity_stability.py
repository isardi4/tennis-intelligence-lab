"""Retirar un año por vez; diagnóstico retrospectivo del piloto, no backtest."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.download import verify
from tennis_lab.profiles import profile_observations
from tennis_lab.stability import compare_windows
from build_style_pilot import main as style_profiles
from build_ranked_profiles import challenger_group
from build_similarities import BASIC, STYLE


def write_report(report, roster, output):
    summary = {}
    queue = {row["player_id"]: {"player_id": row["player_id"], "name": row["name"], "rank": row["rank"],
                                "identity_status": row["identity_status"], "diagnostics": {}} for row in roster}
    for group in ("basic/ATP/All", "basic/Challenger_main/All", "basic/Challenger_qualifying/All", "style/MCP/All"):
        views = [report["comparisons"][f"{group}/without_{year}"]["players"] for year in (2022, 2023, 2024)]
        common = set(views[0]) & set(views[1]) & set(views[2])
        retained = {key for key in common if all(view[key]["retained_of_five"] >= 3 for view in views)}
        summary[group] = {"compared_in_all_three": len(common), "retaining_three_in_all_three": len(retained),
                          "sensitive_to_year_removed": len(common - retained), "insufficient_for_all_three": len(roster) - len(common)}
        for key, row in queue.items():
            row["diagnostics"][group] = "retention_criterion_met" if key in retained else "sensitive" if key in common else "insufficient_comparison"
    report["summary"] = summary
    (output / "similarity_stability.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "profile_review_queue.json").write_text(json.dumps(list(queue.values()), ensure_ascii=False, indent=2) + "\n")


def main():
    output = ROOT / "data/processed/stage_1_2025"
    roster_path = output / "top350_profiles.json"
    roster = json.loads(roster_path.read_text())
    ids = {row["player_id"] for row in roster}
    raw_rows = []
    for source, pattern in (("sackmann", "atp_matches_{year}.csv"), ("challenger", "atp_matches_qual_chall_{year}.csv")):
        directory = ROOT / "data/raw" / source
        locked = {item["name"]: item for item in json.loads((directory / "manifest.json").read_text())["files"]}
        for year in (2022, 2023, 2024):
            name = pattern.format(year=year)
            verify(directory / name, locked[name])
            for row in read_rows(directory / name):
                level = "ATP" if source == "sackmann" else challenger_group(row)
                if level and "20220101" <= row["tourney_date"] <= "20241231":
                    raw_rows.append((year, level, row))
    def encounter(row):
        return row["tourney_id"], row["round"], *sorted((row["winner_id"], row["loser_id"]))
    counts = Counter(encounter(row) for _, _, row in raw_rows)
    raw_rows = [(year, level, row) for year, level, row in raw_rows if counts[encounter(row)] == 1]
    report = {"ready_for_prediction": False, "input_sha256": hashlib.sha256(roster_path.read_bytes()).hexdigest(),
              "method": "Retirar 2022, 2023 o 2024; misma población común en cada comparación. Umbrales exploratorios.", "comparisons": {}}
    for excluded in (2022, 2023, 2024):
        buckets = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0])))
        for year, level, row in raw_rows:
            if year == excluded:
                continue
            for side, label in (("w", "winner"), ("l", "loser")):
                identifier = row[f"{label}_id"]
                if identifier not in ids:
                    continue
                for feature, (numerator, denominator) in profile_observations(row, side).items():
                    for surface in ("All", row["surface"]):
                        values = buckets[(level, surface)][identifier][feature]
                        values[0] += numerator
                        values[1] += denominator
                        values[2] += 1
        styles = style_profiles([row["mcp_name"] for row in roster if row["mcp_name"]], f"style_without_{excluded}.json", False, excluded)
        indexed = {(profile["player"], profile["surface"]): profile["metrics"] for profile in styles}
        for surface in ("All", "Hard", "Clay", "Grass"):
            for level in ("ATP", "Challenger_main", "Challenger_qualifying"):
                original = {row["player_id"]: row["basic_profile_by_level"].get(level, {}).get(surface, {}) for row in roster}
                perturbed = {key: {feature: {"rate": values[0] / values[1], "denominator": values[1], "matches": values[2]} for feature, values in metrics.items()} for key, metrics in buckets[(level, surface)].items()}
                report["comparisons"][f"basic/{level}/{surface}/without_{excluded}"] = compare_windows(original, perturbed, BASIC)
            if surface != "All":
                continue
            original = {row["player_id"]: next((p["metrics"] for p in row["style_profiles"] if p["surface"] == surface), {}) for row in roster}
            perturbed = {row["player_id"]: indexed.get((row["mcp_name"], surface), {}) for row in roster}
            report["comparisons"][f"style/MCP/{surface}/without_{excluded}"] = compare_windows(original, perturbed, STYLE)
    write_report(report, roster, output)
    for key, comparison in report["comparisons"].items():
        if "/All/" in key:
            print(key, {k: v for k, v in comparison.items() if k != "players"})


if __name__ == "__main__":
    main()
