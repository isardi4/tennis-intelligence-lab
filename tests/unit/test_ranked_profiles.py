import importlib.util
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from build_ranked_profiles import latest_ranking, challenger_group


def test_roster_uses_latest_pre_cutoff_snapshot_without_backfilling():
    rows = [{"ranking_date": day, "rank": rank, "player": player} for day, rank, player in
            [("20241223", "1", "old"), ("20241230", "350", "pilot"),
             ("20241230", "500", "coverage"), ("20241230", "501", "outside"),
             ("20250106", "1", "future")]]
    day, selected = latest_ranking(rows, "20241231")
    assert day == "20241230"
    assert [row["player"] for row in selected] == ["pilot", "coverage"]


def test_duplicate_player_in_ranking_is_rejected():
    rows = [{"ranking_date": "20241230", "rank": "1", "player": "same"}] * 2
    with pytest.raises(ValueError):
        latest_ranking(rows, "20241231")


def test_challenger_quarterfinal_is_not_qualifying_and_atp_qualifiers_are_not_added():
    assert challenger_group({"tourney_level": "C", "round": "QF"}) == "Challenger_main"
    assert challenger_group({"tourney_level": "C", "round": "Q2"}) == "Challenger_qualifying"
    assert challenger_group({"tourney_level": "A", "round": "Q2"}) is None
