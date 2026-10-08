"""The pre-registered analysis (PREREGISTRATION.md, "Primary analysis").

Primary: the trend in resolve rate across rungs 1 -> 4 (outcome, location,
diff, trace), conditions compared within task, task as a random effect:

    resolved ~ rung + (1 | task)        linear mixed model, rung = 1..4

The slope is in resolve-rate points per rung step. Its 95% interval is a
cluster bootstrap over tasks (tasks resampled with replacement, the model refit
each time), so it does not lean on normal theory for a binary outcome or on the
correlation between a task's attempts. A null is reported as "no effect larger
than X", X the larger end of the interval.

Everything else (other metrics, pairwise contrasts, padded vs outcome, the
check subgroup) uses the same machinery and is secondary.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

RUNG = {"outcome": 1, "location": 2, "diff": 3, "trace": 4}
CONDITIONS = ["outcome", "location", "diff", "trace", "padded"]


def _mixed_slope(df: pd.DataFrame, y: str) -> float:
    """Slope of y on rung, random intercept per task. Falls back to the
    within-task (fixed-effects) slope if the mixed model cannot be fit."""
    import statsmodels.formula.api as smf
    d = df[["task", "rung", y]].astype({y: float})
    if d[y].nunique() < 2:
        return 0.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            return float(smf.mixedlm(f"{y} ~ rung", d, groups=d["task"]).fit(reml=True).params["rung"])
        except Exception:
            return within_slope(d, y)


def within_slope(df: pd.DataFrame, y: str) -> float:
    """OLS slope of y on rung after removing each task's mean (task fixed effects)."""
    yc = df[y].astype(float) - df.groupby("task")[y].transform("mean").astype(float)
    xc = df["rung"] - df.groupby("task")["rung"].transform("mean")
    den = float((xc * xc).sum())
    return float((xc * yc).sum() / den) if den else 0.0


def _resample_tasks(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    tasks = df["task"].unique()
    pick = rng.choice(tasks, size=len(tasks), replace=True)
    parts = [df[df["task"] == t].assign(task=f"{t}#{i}") for i, t in enumerate(pick)]
    return pd.concat(parts, ignore_index=True)


def trend(df: pd.DataFrame, y: str, n_boot: int = 1000, seed: int = 0, mixed: bool = True) -> dict:
    """Trend across rungs 1-4 of y: slope per rung step with a cluster-bootstrap 95% CI."""
    d = df[df["condition"].isin(RUNG)].assign(rung=lambda x: x["condition"].map(RUNG))
    est = _mixed_slope if mixed else within_slope
    point = est(d, y)
    rng = np.random.default_rng(seed)
    boots = np.array([est(_resample_tasks(d, rng), y) for _ in range(n_boot)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"metric": y, "slope_per_rung": point, "ci95": [float(lo), float(hi)],
            "rung4_minus_rung1": 3 * point, "ci95_rung4_minus_rung1": [3 * float(lo), 3 * float(hi)],
            "p_boot_two_sided": float(min(1.0, 2 * min((boots <= 0).mean(), (boots >= 0).mean()))),
            "n_runs": int(len(d)), "n_tasks": int(d["task"].nunique()), "model": "mixedlm" if mixed else "within-task OLS"}


def rates(df: pd.DataFrame, y: str, n_boot: int = 1000, seed: int = 0) -> dict:
    """Mean of y per condition, cluster-bootstrap 95% CI."""
    rng = np.random.default_rng(seed)
    out = {}
    for c in CONDITIONS:
        d = df[df["condition"] == c]
        if d.empty:
            continue
        boots = [ _resample_tasks(d, rng)[y].astype(float).mean() for _ in range(n_boot)]
        out[c] = {"mean": float(d[y].astype(float).mean()), "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
                  "n": int(len(d))}
    return out


def contrast(df: pd.DataFrame, y: str, a: str, b: str, n_boot: int = 1000, seed: int = 0) -> dict:
    """Mean of (a - b) over tasks, each task's conditions averaged over its attempts; cluster bootstrap."""
    m = df[df["condition"].isin([a, b])].groupby(["task", "condition"])[y].mean().unstack()
    m = m.dropna()
    diff = (m[a] - m[b]).to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    boots = [rng.choice(diff, size=len(diff), replace=True).mean() for _ in range(n_boot)]
    return {"metric": y, "contrast": f"{a} - {b}", "diff": float(diff.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))], "n_tasks": int(len(diff))}


def no_effect_larger_than(t: dict) -> float:
    """For a null: the largest effect the interval still allows, in points per rung step."""
    return float(max(abs(t["ci95"][0]), abs(t["ci95"][1])))
