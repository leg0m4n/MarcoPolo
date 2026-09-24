"""When the GPU is ours: the window agreed with the server's admin.

    Every night 23:00 -> 08:00, plus all of Friday and Saturday.

So Thursday 23:00 runs straight through to Sunday 08:00; other nights are
23:00 -> 08:00. The admin's pool model runs outside these hours.

vLLM claims all of its GPU memory at startup. If it ran during the day and the
pool model needed more, the pool model would be the one to crash. So the rule is
not "back off under pressure", it is "our server does not exist outside the
window".

No run may straddle the close: runs take up to ~25 min, so none starts within
DRAIN_MIN of closing. A hard stop at close kills and re-queues any straggler.

CLI:
    python -m marcopolo.schedule status      # human-readable
    python -m marcopolo.schedule can-start   # exit 0 iff a new run may start now
    python -m marcopolo.schedule is-open     # exit 0 iff inside the window
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta

OPEN_HOUR, CLOSE_HOUR = 23, 8
ALL_DAY = (4, 5)          # Friday, Saturday (Monday = 0)
DRAIN_MIN = 30


def is_open(t: datetime) -> bool:
    return t.weekday() in ALL_DAY or t.hour >= OPEN_HOUR or t.hour < CLOSE_HOUR


def window_end(t: datetime) -> datetime | None:
    """When the current window closes; None if closed now. Always an 08:00."""
    if not is_open(t):
        return None
    close = t.replace(hour=CLOSE_HOUR, minute=0, second=0, microsecond=0)
    if close <= t:
        close += timedelta(days=1)
    while is_open(close):          # Fri/Sat 08:00 do not close the window
        close += timedelta(days=1)
    return close


def next_open(t: datetime) -> datetime:
    if is_open(t):
        return t
    return t.replace(hour=OPEN_HOUR, minute=0, second=0, microsecond=0)  # closed => 08:00-23:00 Sun-Thu


def can_start(t: datetime) -> bool:
    end = window_end(t)
    return end is not None and t < end - timedelta(minutes=DRAIN_MIN)


def _main(argv: list[str]) -> int:
    now = datetime.now()
    cmd = argv[1] if len(argv) > 1 else "status"
    if cmd == "can-start":
        return 0 if can_start(now) else 1
    if cmd == "is-open":
        return 0 if is_open(now) else 1
    end = window_end(now)
    if end:
        print(f"OPEN until {end:%a %H:%M} | new runs until {end - timedelta(minutes=DRAIN_MIN):%a %H:%M}")
    else:
        print(f"CLOSED | opens {next_open(now):%a %H:%M}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
