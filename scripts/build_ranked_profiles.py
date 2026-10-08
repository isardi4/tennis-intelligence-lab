"""Universo histórico top 500; piloto top 350, con cobertura explícita y sin imputación."""
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tennis_lab.ingestion.audit import read_rows
from tennis_lab.ingestion.charting import charting_coverage
from tennis_lab.ingestion.download import verify
from tennis_lab.ingestion.quality import normalize_name
from tennis_lab.profiles import profile_observations
from build_style_pilot import main as style_profiles


def latest_ranking(rows, cutoff):
    dated = [row for row in rows if row["ranking_date"].isdigit() and len(row["ranking_date"]) == 8 and row["ranking_date"] <= cutoff]
    latest = max(row["ranking_date"] for row in dated)
    selected = [row for row in dated if row["ranking_date"] == latest and 1 <= int(row["rank"]) <= 500]
    if len({row["player"] for row in selected}) != len(selected):
        raise ValueError("Jugador duplicado en ranking")
    return latest, sorted(selected, key=lambda row: (int(row["rank"]), row["player"]))


def challenger_group(row):
    if row["tourney_level"] != "C":
        return None
    return "Challenger_qualifying" if row["round"] in ("Q1", "Q2", "Q3") else "Challenger_main"


def main():
    raw = ROOT / "data/raw/sackmann"
    locked = {item["name"]: item for item in json.loads((raw / "manifest.json").read_text())["files"]}
    names = ["atp_rankings_20s.csv", "atp_players.csv"] + [f"atp_matches_{year}.csv" for year in range(2022, 2025)]
    for name in names:
        verify(raw / name, locked[name])
    ranking_day, ranking = latest_ranking(read_rows(raw / names[0]), "20241231")
    players = {row["player_id"]: row for row in read_rows(raw / "atp_players.csv")}
    ids = {row["player"] for row in ranking}
    aliases = defaultdict(set)
    metrics = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0])))
    by_level = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))))
    admissions = Counter()
    rows_to_process = []
    for year in range(2022, 2025):
        rows_to_process.extend(("ATP", row) for row in read_rows(raw / f"atp_matches_{year}.csv"))
    challenger = ROOT / "data/raw/challenger"
    config = json.loads((ROOT / "configs/challenger_source.json").read_text())
    for item in config["files"]:
        verify(challenger / item["name"], item)
        for row in read_rows(challenger / item["name"]):
            level = challenger_group(row)
            if level is None:
                admissions["non_challenger_rows_not_added"] += 1
                continue
            rows_to_process.append((level, row))
    def encounter_key(row):
        return row["tourney_id"], row["round"], *sorted((row["winner_id"], row["loser_id"]))
    duplicates = Counter(encounter_key(row) for _, row in rows_to_process)
    for level, row in rows_to_process:
            if duplicates[encounter_key(row)] != 1:
                admissions["duplicate_rows_quarantined"] += 1
                continue
            if not "20220101" <= row.get("tourney_date", "") <= "20241231":
                admissions["outside_window"] += 1
                continue
            admissions[f"{level}_rows_in_window"] += 1
            for side, label in (("w", "winner"), ("l", "loser")):
                identifier = row[f"{label}_id"]
                if identifier not in ids:
                    continue
                aliases[identifier].add(normalize_name(row[f"{label}_name"]))
                observations = profile_observations(row, side)
                for surface in ("All", row["surface"]):
                    for key, (numerator, denominator) in observations.items():
                        bucket = metrics[identifier][surface][key]
                        bucket[0] += numerator
                        bucket[1] += denominator
                        bucket[2] += 1
                        level_bucket = by_level[identifier][level][surface][key]
                        level_bucket[0] += numerator
                        level_bucket[1] += denominator
                        level_bucket[2] += 1
    mcp = ROOT / "data/raw/mcp"
    for item in json.loads((ROOT / "configs/mcp_source.json").read_text())["files"]:
        verify(mcp / item["name"], item)
    _, _, eligible = charting_coverage(read_rows(mcp / "charting-m-matches.csv"), date(2024, 12, 31))
    charted_names = defaultdict(set)
    for row in eligible.values():
        if row["Date"] >= "20220101":
            for key in ("Player 1", "Player 2"):
                charted_names[normalize_name(row[key])].add(row[key])
    roster = []
    for row in ranking:
        identifier = row["player"]
        player = players.get(identifier, {})
        display = " ".join((player.get("name_first", ""), player.get("name_last", ""))).strip()
        candidates = set().union(*(charted_names.get(alias, set()) for alias in aliases[identifier] | {normalize_name(display)}))
        roster.append({"rank": int(row["rank"]), "player_id": identifier, "name": display,
                       "mcp_name": next(iter(candidates)) if len(candidates) == 1 else None,
                       "identity_status": "exact_normalized_candidate" if len(candidates) == 1 else "unmatched_or_ambiguous",
                       "basic_profile": {surface: {key: {"numerator": values[0], "denominator": values[1], "matches": values[2], "rate": values[0] / values[1]} for key, values in group.items()} for surface, group in metrics[identifier].items()},
                       "basic_profile_by_level": {level: {surface: {key: {"numerator": values[0], "denominator": values[1], "matches": values[2], "rate": values[0] / values[1]} for key, values in group.items()} for surface, group in surfaces.items()} for level, surfaces in by_level[identifier].items()}})
    # No compartir una identidad MCP entre dos jugadores del ranking.
    collisions = defaultdict(list)
    for row in roster:
        if row["mcp_name"]:
            collisions[row["mcp_name"]].append(row)
    for group in collisions.values():
        if len(group) > 1:
            for row in group:
                row["mcp_name"] = None
                row["identity_status"] = "ambiguous_shared_name"
    selected = [row for row in roster if row["rank"] <= 350]
    styles = style_profiles([row["mcp_name"] for row in selected if row["mcp_name"]], "top350_styles.json", False)
    indexed = {(profile["player"], profile["surface"]): profile for profile in styles}
    pilot = [{**row, "style_profiles": [indexed[(row["mcp_name"], surface)] for surface in ("All",)] if row["mcp_name"] else []} for row in selected]
    summary = {"ranking_date": ranking_day, "window": ["2022-01-01", "2024-12-31"], "ready_for_training": False, "row_admissions": dict(admissions)}
    for label, group in (("top500", roster), ("top350", selected)):
        summary[label] = {"players": len(group), "with_basic_observations": sum(bool(row["basic_profile"]) for row in group),
                          "with_mcp_name_candidate": sum(bool(row["mcp_name"]) for row in group),
                          "with_ATP_observations": sum(bool(row["basic_profile_by_level"].get("ATP")) for row in group),
                          "newly_covered_by_challenger": sum(bool(row["basic_profile"]) and not bool(row["basic_profile_by_level"].get("ATP")) for row in group)}
    summary["top350"]["with_style_metrics"] = sum(bool(profile["metrics"]) for profile in styles if profile["surface"] == "All")
    output = ROOT / "data/processed/stage_1_2025"
    for name, payload in (("top500_coverage.json", roster), ("top350_profiles.json", pilot), ("ranked_profiles_summary.json", summary)):
        (output / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
