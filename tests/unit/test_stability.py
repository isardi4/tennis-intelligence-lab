from tennis_lab.stability import compare_windows


def profiles():
    return {str(i): {"x": {"rate": i / 10, "denominator": 100, "matches": 20}} for i in range(8)}


def test_unchanged_profiles_retain_all_neighbors():
    result = compare_windows(profiles(), profiles(), ["x"])
    assert result["median_retained"] == 5
    assert result["retaining_at_least_three"] == 8


def test_insufficient_population_is_unavailable_not_zero_stability():
    result = compare_windows(profiles(), {"0": profiles()["0"]}, ["x"])
    assert result["status"] == "insufficient_population"
    assert "median_retained" not in result


def test_ineligible_player_is_removed_from_both_candidate_populations():
    smaller = profiles()
    smaller["0"]["x"]["matches"] = 9
    result = compare_windows(profiles(), smaller, ["x"])
    assert result["comparable_players"] == 7
    assert "0" not in result["players"]
    assert result["median_retained"] == 5
