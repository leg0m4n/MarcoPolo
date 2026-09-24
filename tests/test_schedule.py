"""The GPU-sharing agreement. A bug here runs vLLM while the admin's model needs
the card, and crashes *his* process, not ours."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.schedule import can_start, is_open, next_open, window_end  # noqa: E402

# 2026-09-21 is a Monday
MON, TUE, WED, THU, FRI, SAT, SUN = (datetime(2026, 9, 21 + i) for i in range(7))


def at(day, h, m=0):
    return day.replace(hour=h, minute=m)


def test_weekday_daytime_is_closed():
    for d in (MON, TUE, WED, THU):
        assert not is_open(at(d, 8)) and not is_open(at(d, 13)) and not is_open(at(d, 22, 59))
    assert not is_open(at(SUN, 8)) and not is_open(at(SUN, 22, 59))


def test_nights_are_open():
    assert is_open(at(MON, 23)) and is_open(at(TUE, 3)) and is_open(at(TUE, 7, 59))


def test_friday_and_saturday_open_all_day():
    for h in (0, 8, 12, 18, 23):
        assert is_open(at(FRI, h)) and is_open(at(SAT, h))


def test_weekend_block_runs_thursday_night_to_sunday_morning():
    assert window_end(at(THU, 23)) == at(SUN, 8)
    assert window_end(at(FRI, 9)) == at(SUN, 8)
    assert window_end(at(SAT, 23, 30)) == at(SUN, 8)


def test_weeknight_closes_next_morning():
    assert window_end(at(MON, 23)) == at(TUE, 8)
    assert window_end(at(TUE, 2)) == at(TUE, 8)
    assert window_end(at(SUN, 23)) == datetime(2026, 9, 28, 8)  # the following Monday


def test_closed_has_no_end_and_opens_at_23():
    assert window_end(at(WED, 12)) is None
    assert next_open(at(WED, 12)) == at(WED, 23)


def test_no_new_run_in_the_last_30_minutes():
    assert can_start(at(TUE, 7, 29))
    assert not can_start(at(TUE, 7, 30))
    assert not can_start(at(SUN, 7, 45))
    assert can_start(at(SAT, 7, 45)), "Saturday 07:45 is mid-weekend, not near a close"


def test_weekly_capacity_is_93_hours():
    hours = sum(is_open(at(d, h)) for d in (MON, TUE, WED, THU, FRI, SAT, SUN) for h in range(24))
    assert hours == 93
