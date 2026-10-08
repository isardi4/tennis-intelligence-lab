from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from tennis_lab.ingestion.temporal import ResultTiming


def test_overnight_result_is_not_known_on_scheduled_day():
    timing = ResultTiming(date(2024, 6, 2), "Europe/Paris")
    assert not timing.known_before(datetime(2024, 6, 2, 23, 59, tzinfo=ZoneInfo("Europe/Paris")))
    assert timing.known_before(datetime(2024, 6, 3, tzinfo=ZoneInfo("Europe/Paris")))


def test_resumed_match_uses_completion_day():
    timing = ResultTiming(date(2024, 5, 30), "Europe/Paris")
    assert not timing.known_before(datetime(2024, 5, 30, 12, tzinfo=timezone.utc))
    assert timing.usable_from == datetime(2024, 5, 30, 22, tzinfo=timezone.utc)


@pytest.mark.parametrize("zone,expected", [("Australia/Melbourne", "2024-01-28T13:00:00+00:00"),
                                          ("America/New_York", "2024-01-29T05:00:00+00:00")])
def test_event_timezone_controls_availability(zone, expected):
    assert ResultTiming(date(2024, 1, 28), zone).usable_from.isoformat() == expected


def test_dst_transition_uses_next_calendar_midnight():
    assert ResultTiming(date(2024, 3, 31), "Europe/Paris").usable_from == datetime(2024, 3, 31, 22, tzinfo=timezone.utc)


def test_unknown_completion_cannot_enter_history():
    timing = ResultTiming(None, "Europe/Paris")
    assert not timing.known_before(datetime(2025, 1, 1, tzinfo=timezone.utc))
    assert not timing.training_eligible(2024, date(2024, 12, 31))


def test_naive_prediction_time_is_rejected():
    with pytest.raises(ValueError):
        ResultTiming(date(2024, 1, 1), "Europe/Paris").known_before(datetime(2024, 1, 3))


def test_next_season_is_excluded_even_if_played_in_december():
    timing = ResultTiming(date(2024, 12, 31), "Australia/Brisbane")
    assert timing.training_eligible(2024, date(2024, 12, 31))
    assert not timing.training_eligible(2025, date(2024, 12, 31))


def test_result_available_after_cutoff_is_excluded():
    assert not ResultTiming(date(2024, 12, 31), "America/New_York").training_eligible(2024, date(2024, 12, 31))
