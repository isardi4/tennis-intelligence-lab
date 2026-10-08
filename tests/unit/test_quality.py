from tennis_lab.ingestion.quality import match_issues, match_key, normalize_name, number
from tennis_lab.ingestion.audit import field_differences


def valid_match():
    return {"winner_id": "A", "loser_id": "B", "winner_name": "Jugador A",
            "loser_name": "Jugador B", "tourney_id": "2024-0580", "round": "F",
            "tourney_date": "20240114", "surface": "Hard", "best_of": "5"}


def test_detects_impossible_serve_stats_seen_in_real_data():
    row = valid_match() | {"w_svpt": "135", "w_1stIn": "122", "w_2ndWon": "21"}
    assert "w_second_serve_wins_exceed_opportunities" in match_issues(row)


def test_missing_stats_are_unknown_not_zero_or_invalid():
    row = valid_match()
    assert match_issues(row) == []
    assert number("") is None
    assert number("nan") is None
    assert number("0") == 0


def test_negative_and_non_numeric_values_are_flagged():
    issues = match_issues(valid_match() | {"w_ace": "-1", "l_svpt": "oops", "winner_rank": "0"})
    assert "invalid_w_ace" in issues
    assert "invalid_l_svpt" in issues
    assert "invalid_winner_rank" in issues


def test_match_alignment_does_not_require_same_winner_or_source_ids():
    a = valid_match()
    b = a | {"winner_name": a["loser_name"], "loser_name": a["winner_name"],
             "winner_id": "999", "loser_id": "123", "tourney_id": "2024-580"}
    assert match_key(a, 2024) == match_key(b, 2024)
    assert [d["field"] for d in field_differences(a, b)] == ["winner_name"]


def test_score_formatting_is_not_a_disagreement():
    a = valid_match() | {"score": "6-2 7-6(4)", "w_ace": "10"}
    b = valid_match() | {"score": "6-2, 7-6(4)", "w_ace": "10.0"}
    assert field_differences(a, b) == []
    assert normalize_name("Jan-Lennard Struff") == normalize_name("Jan Lennard Struff")


def test_reversed_winner_statistics_are_aligned_to_each_player():
    a = valid_match() | {"w_ace": "10", "l_ace": "3"}
    b = valid_match() | {"winner_name": a["loser_name"], "loser_name": a["winner_name"],
                        "w_ace": "3", "l_ace": "10"}
    assert [d["field"] for d in field_differences(a, b)] == ["winner_name"]


def test_invalid_date_and_fractional_counters_flagged():
    issues = match_issues(valid_match() | {"tourney_date": "2024011", "w_ace": "2.5"})
    assert "invalid_tournament_date" in issues
    assert "invalid_w_ace" in issues
