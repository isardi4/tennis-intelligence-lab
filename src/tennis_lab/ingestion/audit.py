"""Auditoría de cobertura, coherencia y coincidencia; no adjudica qué fuente tiene razón."""
from __future__ import annotations
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

from tennis_lab.ingestion.dataset import checked_files
from tennis_lab.ingestion.quality import (
    STAT_FIELDS, match_issues, match_key, normalize_name, normalized_score, number,
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_profile(paths: list[str], training_year: int) -> dict:
    years = []
    problems: Counter = Counter()
    schemas: dict[str, list[str]] = {}
    issue_examples = []
    for filename in paths:
        path = Path(filename)
        year = int(path.stem[-4:])
        rows = read_rows(path)
        schemas[str(year)] = list(rows[0]) if rows else []
        missing: Counter = Counter()
        surfaces: Counter = Counter()
        levels: Counter = Counter()
        with_stats = 0
        seen = set()
        affected = 0
        for row in rows:
            surfaces[row.get("surface") or "missing"] += 1
            levels[row.get("tourney_level") or "missing"] += 1
            for field, value in row.items():
                if not value:
                    missing[field] += 1
            with_stats += all(row.get(field) not in (None, "") for field in STAT_FIELDS)
            # Only pre-evaluation outcomes feed the quality investigation.
            if year <= training_year:
                issues = match_issues(row)
                key = (row.get("tourney_id"), row.get("match_num"))
                if key in seen:
                    issues.append("duplicate_source_match_key")
                seen.add(key)
                problems.update(issues)
                affected += bool(issues)
                if issues:
                    issue_examples.append({"year": year, "tournament": row.get("tourney_name"),
                                           "winner": row.get("winner_name"), "loser": row.get("loser_name"),
                                           "issues": issues,
                                           "statistics": {field: row.get(field) for field in STAT_FIELDS}})
        years.append({"year": year, "rows": len(rows), "complete_stats_rows": with_stats,
                      "surfaces": dict(surfaces), "levels": dict(levels),
                      "missing_by_field": dict(missing),
                      "rows_with_internal_issues": affected if year <= training_year else None})
    return {"years": years, "schemas": schemas, "internal_issues": dict(problems),
            "issue_examples": issue_examples}


def align(rows: list[dict], season: int) -> dict[tuple, list[dict]]:
    index: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("winner_name") and row.get("loser_name"):
            index[match_key(row, season)].append(row)
    return index


def field_differences(a: dict, b: dict) -> list[dict]:
    differences = []
    reversed_winner = normalize_name(a.get("winner_name", "")) != normalize_name(b.get("winner_name", ""))
    for field in ("winner_name", "score", "surface", "best_of", "minutes", *STAT_FIELDS,
                  "winner_rank", "loser_rank", "winner_rank_points", "loser_rank_points"):
        other_field = field
        # Align statistics to the same player, even if the winner disagrees.
        if reversed_winner:
            if field.startswith("w_"):
                other_field = "l_" + field[2:]
            elif field.startswith("l_"):
                other_field = "w_" + field[2:]
            elif field.startswith("winner_") and field != "winner_name":
                other_field = "loser_" + field[7:]
            elif field.startswith("loser_"):
                other_field = "winner_" + field[6:]
        left, right = a.get(field), b.get(other_field)
        if not left or not right:
            continue
        if field == "winner_name":
            same = normalize_name(left) == normalize_name(right)
        elif field == "score":
            same = normalized_score(left) == normalized_score(right)
        elif field == "surface":
            same = left.lower() == right.lower()
        else:
            same = number(left) is not None and number(left) == number(right)
        if not same:
            differences.append({"field": field, "sackmann": left, "tml": right})
    return differences


def compare_sources(raw_root: Path, cutoff_year: int, output: Path) -> dict:
    counts: Counter = Counter()
    fields: Counter = Counter()
    years = []
    unmatched_samples = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as discrepancies:
        for year in range(1968, cutoff_year + 1):
            a_path = raw_root / "sackmann" / f"atp_matches_{year}.csv"
            b_path = raw_root / "tml" / f"{year}.csv"
            if not a_path.exists() or not b_path.exists():
                continue
            a, b = align(read_rows(a_path), year), align(read_rows(b_path), year)
            unique_a = {key for key, rows in a.items() if len(rows) == 1}
            unique_b = {key for key, rows in b.items() if len(rows) == 1}
            common = unique_a & unique_b
            summary = {"year": year, "matched": len(common),
                       "sackmann_unmatched": len(unique_a - unique_b),
                       "tml_unmatched": len(unique_b - unique_a),
                       "ambiguous_keys": len(set(a) - unique_a) + len(set(b) - unique_b)}
            year_fields: Counter = Counter()
            counts.update({key: value for key, value in summary.items() if key != "year"})
            for key in sorted(common):
                differences = field_differences(a[key][0], b[key][0])
                if differences:
                    summary["matches_with_differences"] = summary.get("matches_with_differences", 0) + 1
                    counts["matches_with_differences"] += 1
                    fields.update(item["field"] for item in differences)
                    year_fields.update(item["field"] for item in differences)
                    discrepancies.write(json.dumps({"key": key, "differences": differences}, ensure_ascii=False) + "\n")
            summary["differences_by_field"] = dict(year_fields)
            years.append(summary)
            # Name/tournament mismatches are explicitly unresolved, never fuzzy-joined.
            for source, index, keys in (("sackmann", a, unique_a - unique_b), ("tml", b, unique_b - unique_a)):
                if year >= cutoff_year - 1:
                    for key in sorted(keys)[:5]:
                        row = index[key][0]
                        unmatched_samples.append({"source": source, "year": year,
                                                  "tournament": row.get("tourney_name"),
                                                  "winner": row.get("winner_name"),
                                                  "loser": row.get("loser_name")})
    return {"counts": dict(counts), "differences_by_field": dict(fields), "years": years,
            "unmatched_samples": unmatched_samples}


def official_checks(raw_root: Path, checks: list[dict], cutoff_year: int) -> list[dict]:
    results = []
    for check in checks:
        if check["season"] > cutoff_year:
            raise ValueError("La auditoría oficial no puede leer resultados del año de evaluación")
        target = {"tourney_id": str(check["tournament_code"]), **check}
        target_key = match_key(target, check["season"])
        for source, name in (("sackmann", f"atp_matches_{check['season']}.csv"), ("tml", f"{check['season']}.csv")):
            matches = [row for row in read_rows(raw_root / source / name)
                       if match_key(row, check["season"]) == target_key]
            passed = len(matches) == 1
            if passed:
                row = matches[0]
                passed = (normalize_name(row["winner_name"]) == normalize_name(check["winner_name"])
                          and normalized_score(row["score"]) == normalized_score(check["score"]))
                if "minutes" in check:
                    passed = passed and number(row.get("minutes")) == check["minutes"]
            results.append({"source": source, "season": check["season"],
                            "tournament_code": check["tournament_code"],
                            "passed": passed, "candidates": len(matches),
                            "source_url": check["source_url"]})
    return results


def audit_sources(raw_root: Path, cutoff_year: int, output: Path, checks: list[dict]) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    profiles = {}
    for source, pattern in (("sackmann", "atp_matches_[0-9][0-9][0-9][0-9].csv"),
                            ("tml", "[0-9][0-9][0-9][0-9].csv")):
        paths = checked_files(raw_root / source, pattern)
        profiles[source] = source_profile(paths, cutoff_year)
    result = {"cutoff_year": cutoff_year, "profiles": profiles,
              "comparison": compare_sources(raw_root, cutoff_year, output / "discrepancies.jsonl"),
              "official_checks": official_checks(raw_root, checks, cutoff_year),
              "temporal_ready": False,
              "temporal_warning": "tourney_date no es la fecha exacta de cada partido; match_num no es orden cronológico garantizado."}
    (output / "audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result
