"""Cobertura de registros charted; no convierte fechas declaradas en disponibilidad."""
from collections import Counter, defaultdict
from datetime import date, datetime


def charting_coverage(rows: list[dict], cutoff: date) -> tuple[dict, list[dict], dict]:
    ids = Counter(row.get("match_id", "") for row in rows)
    excluded = Counter()
    players = defaultdict(lambda: {"matches": 0, "surfaces": Counter(), "years": Counter()})
    eligible = {}
    for row in rows:
        identifier = row.get("match_id", "")
        if not identifier or ids[identifier] != 1:
            excluded["missing_or_duplicate_id"] += 1
            continue
        try:
            value = row.get("Date", "")
            if len(value) != 8 or not value.isdigit():
                raise ValueError()
            played = datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            excluded["invalid_date"] += 1
            continue
        if played > cutoff:
            excluded["after_cutoff"] += 1
            continue
        if row.get("Surface") not in ("Hard", "Clay", "Grass", "Carpet"):
            excluded["invalid_or_missing_surface"] += 1
            continue
        names = [row.get("Player 1", "").strip(), row.get("Player 2", "").strip()]
        if not all(names) or names[0] == names[1]:
            excluded["invalid_players"] += 1
            continue
        eligible[identifier] = row
        for name in names:
            player = players[name]
            player["matches"] += 1
            player["surfaces"][row.get("Surface") or "Unknown"] += 1
            player["years"][str(played.year)] += 1
    listing = [{"player": name, **values} for name, values in sorted(players.items())]
    counts = sorted(item["matches"] for item in listing)
    summary = {"cutoff": cutoff.isoformat(), "raw_matches": len(rows), "eligible_metadata_matches": len(eligible),
               "distinct_player_names": len(listing), "excluded_rows": dict(excluded),
               "players_at_least_n_matches": {str(n): sum(value >= n for value in counts) for n in (1, 5, 10, 20, 50)},
               "surfaces": dict(Counter(row.get("Surface") or "Unknown" for row in eligible.values())),
               "years": dict(Counter(row["Date"][:4] for row in eligible.values())),
               "ready_for_training": False}
    return summary, listing, eligible
