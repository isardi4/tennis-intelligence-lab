from datetime import date
from tennis_lab.ingestion.charting import charting_coverage


def row(identifier, day="20241231", surface="Clay"):
    return {"match_id": identifier, "Date": day, "Player 1": "A", "Player 2": "B", "Surface": surface}


def test_future_and_invalid_dates_are_excluded():
    summary, players, eligible = charting_coverage([row("a"), row("b", "20250101"), row("c", "20240230")], date(2024, 12, 31))
    assert set(eligible) == {"a"}
    assert summary["excluded_rows"] == {"after_cutoff": 1, "invalid_date": 1}
    assert players[0]["matches"] == 1
    assert not summary["ready_for_training"]


def test_duplicates_do_not_inflate_player_or_surface_coverage():
    summary, players, eligible = charting_coverage([row("a"), row("a"), row("b", surface="Hard")], date(2024, 12, 31))
    assert set(eligible) == {"b"}
    assert summary["surfaces"] == {"Hard": 1}
    assert summary["players_at_least_n_matches"]["5"] == 0
    assert sum(player["matches"] for player in players) == 2


def test_invalid_surface_is_quarantined_without_guessing():
    summary, players, eligible = charting_coverage([row("a", surface="Eva Asderaki-Moore")], date(2024, 12, 31))
    assert not eligible and not players
    assert summary["excluded_rows"] == {"invalid_or_missing_surface": 1}
