"""The analysis must find an effect that is there and not find one that is not."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo import analysis as an  # noqa: E402


def fake(slope: float, n_tasks: int = 39, attempts: int = 3, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for t in range(n_tasks):
        base = rng.uniform(0.05, 0.6)                       # tasks differ a lot, as in the real data
        for c in an.CONDITIONS:
            r = an.RUNG.get(c, 1)                           # padded behaves like outcome here
            p = min(max(base + slope * (r - 1), 0), 1)
            for a in range(attempts):
                rows.append({"task": f"t{t}", "condition": c, "resolved": rng.random() < p})
    return pd.DataFrame(rows)


def test_planted_effect_is_recovered():
    t = an.trend(fake(0.10), "resolved", n_boot=200)
    assert 0.05 < t["slope_per_rung"] < 0.15
    assert t["ci95"][0] > 0, "a 10-point-per-rung effect must be detected"


def test_no_effect_gives_an_interval_around_zero():
    t = an.trend(fake(0.0), "resolved", n_boot=200)
    assert t["ci95"][0] < 0 < t["ci95"][1]
    assert an.no_effect_larger_than(t) < 0.1


def test_within_task_slope_ignores_task_difficulty():
    df = pd.DataFrame({"task": ["a"] * 4 + ["b"] * 4, "rung": [1, 2, 3, 4] * 2,
                       "y": [0, 0, 1, 1] + [1, 1, 1, 1]})
    assert abs(an.within_slope(df, "y") - 0.2) < 1e-9


def test_contrast_pairs_conditions_within_task():
    df = fake(0.10)
    c = an.contrast(df, "resolved", "trace", "outcome", n_boot=200)
    assert c["n_tasks"] == 39 and c["diff"] > 0.15


def test_rates_have_intervals():
    r = an.rates(fake(0.0), "resolved", n_boot=100)
    assert set(r) == set(an.CONDITIONS) and all(v["ci95"][0] <= v["mean"] <= v["ci95"][1] for v in r.values())
