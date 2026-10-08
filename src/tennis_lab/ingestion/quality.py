"""Controles internos: inconsistencias registradas sin alterar la fuente."""
from __future__ import annotations
from datetime import datetime
import re
import unicodedata

STAT_SUFFIXES = ("ace", "df", "svpt", "1stIn", "1stWon", "2ndWon", "SvGms", "bpSaved", "bpFaced")
STAT_FIELDS = tuple(f"{side}_{field}" for side in ("w", "l") for field in STAT_SUFFIXES)


def normalize_name(value: str) -> str:
    unaccented = "".join(c for c in unicodedata.normalize("NFKD", value)
                         if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", unaccented.lower()).split())


def tournament_code(value: str) -> str:
    code = value.split("-", 1)[-1]
    return str(int(code)) if code.isdigit() else code.lower()


def match_key(row: dict[str, str], season: int) -> tuple:
    participants = sorted((normalize_name(row.get("winner_name", "")),
                           normalize_name(row.get("loser_name", ""))))
    return season, tournament_code(row.get("tourney_id", "")), row.get("round", ""), *participants


def normalized_score(value: str) -> str:
    # Formatting alone is not a contradiction; preserve tie-break point information.
    return " ".join(value.replace("–", "-").replace(",", " ").upper().split())


def number(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    try:
        result = float(value)
        return result if result == result and abs(result) != float("inf") else None
    except ValueError:
        return None


def match_issues(row: dict[str, str]) -> list[str]:
    issues: list[str] = []
    winner, loser = row.get("winner_id"), row.get("loser_id")
    if not winner or not loser:
        issues.append("missing_player_id")
    elif winner == loser:
        issues.append("same_player")
    if row.get("surface") not in ("Hard", "Clay", "Grass", "Carpet", ""):
        issues.append("unknown_surface")
    try:
        if not re.fullmatch(r"\d{8}", row.get("tourney_date", "")):
            raise ValueError("La fecha debe tener ocho dígitos")
        datetime.strptime(row.get("tourney_date", ""), "%Y%m%d")
    except ValueError:
        issues.append("invalid_tournament_date")
    if row.get("best_of") not in ("3", "5", ""):
        issues.append("invalid_best_of")
    for side in ("w", "l"):
        stats: dict[str, float | None] = {}
        for suffix in STAT_SUFFIXES:
            field = f"{side}_{suffix}"
            value = row.get(field, "")
            parsed = number(value)
            stats[suffix] = parsed
            if value and (parsed is None or parsed < 0 or not parsed.is_integer()):
                issues.append(f"invalid_{field}")
        for left, right in (("1stIn", "svpt"), ("1stWon", "1stIn"), ("bpSaved", "bpFaced"),
                            ("ace", "svpt"), ("df", "svpt")):
            if stats[left] is not None and stats[right] is not None and stats[left] > stats[right]:
                issues.append(f"{side}_{left}_exceeds_{right}")
        if all(stats[x] is not None for x in ("2ndWon", "svpt", "1stIn")):
            if stats["2ndWon"] > stats["svpt"] - stats["1stIn"]:
                issues.append(f"{side}_second_serve_wins_exceed_opportunities")
        rank_field = "winner_rank" if side == "w" else "loser_rank"
        raw_rank = row.get(rank_field, "")
        rank = number(raw_rank)
        if raw_rank and (rank is None or rank <= 0 or not rank.is_integer()):
            issues.append(f"invalid_{rank_field}")
    return issues
