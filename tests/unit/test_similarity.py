from tennis_lab.similarity import neighbors


def metric(rate, matches=10):
    return {"x": {"rate": rate, "matches": matches, "denominator": 100}}


def test_missing_or_insufficient_evidence_is_excluded_and_self_is_not_neighbor():
    result = neighbors({"a": metric(.1), "b": metric(.11), "c": metric(.9), "thin": metric(.1, 9), "empty": {}}, ["x"])
    assert result["eligible_players"] == 3
    assert result["neighbors"]["a"][0]["player_id"] == "b"
    assert all(item["player_id"] != "a" for item in result["neighbors"]["a"])


def test_rescaling_does_not_change_distances_and_pair_distance_is_symmetric():
    first = neighbors({"a": metric(.1), "b": metric(.4)}, ["x"])
    scaled = neighbors({"a": metric(10), "b": metric(40)}, ["x"])
    assert first["neighbors"]["a"][0]["distance"] == scaled["neighbors"]["a"][0]["distance"]
    assert first["neighbors"]["a"][0]["distance"] == first["neighbors"]["b"][0]["distance"]


def test_constant_features_do_not_produce_false_similarity():
    result = neighbors({"a": metric(.5), "b": metric(.5)}, ["x"])
    assert result["neighbors"]["a"] == []
