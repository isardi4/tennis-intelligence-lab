from tennis_lab.profiles import profile_observations


def valid_row():
    row = dict(winner_id="1", loser_id="2", tourney_date="20240101", score="6-4 6-4", best_of="3", surface="Hard")
    for side in ("w", "l"):
        for field, value in dict(svpt=100, ace=10, df=3, **{"1stIn": 60, "1stWon": 45, "2ndWon": 20}).items():
            row[f"{side}_{field}"] = str(value)
    return row


def test_return_uses_opponents_service_counts():
    row = valid_row()
    row["l_1stWon"] = "30"
    result = profile_observations(row, "w")
    assert result["serve_points_won"] == (65, 100)
    assert result["first_serve_return_points_won"] == (30, 60)
    assert result["return_points_won"] == (50, 100)


def test_impossible_stats_and_unplayed_matches_are_excluded():
    row = valid_row()
    row["w_2ndWon"] = "41"
    assert profile_observations(row, "l") == {}
    row = valid_row()
    row["score"] = "W/O"
    assert profile_observations(row, "w") == {}
    row["score"] = "6-4 1-0 RET"
    assert profile_observations(row, "w") == {}


def test_missing_data_and_zero_opportunities_do_not_become_zero_rates():
    row = valid_row()
    row["w_ace"] = ""
    row["w_1stIn"] = "100"
    row["w_2ndWon"] = "0"
    result = profile_observations(row, "w")
    assert "ace_rate" not in result
    assert "second_serve_points_won" not in result
    assert "serve_points_won" in result
