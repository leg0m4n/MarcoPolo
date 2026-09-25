"""The four feedback rungs from Leg 1 of the research plan.

One bug can be reported at four levels of precision. Each rung narrows where
the fault could be:

    1 outcome   pass/fail only              "3 tests failed"
    2 location  which test failed           "test_checkout_total failed"
    3 diff      expected vs actual + line   "expected 104.50, got 110.00 at cart.py:88"
    4 trace     execution path / probe      "discount branch never executed"

Plus `padded`: rung 1 with filler sized to match rung 4, so that what varies
between conditions is *precision*, not volume. The plan calls for this control
because more precise feedback is also more text, and token count alone could
explain a rung effect.

Rung boundaries are partly arbitrary. Per the plan's rigor checklist they are
pre-registered here and must not be adjusted after the first real run.
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

RUNGS = ("outcome", "location", "diff", "trace", "padded")

# Deterministic filler for the `padded` control. It must be *neutral*, not just
# fault-free: nothing in it may claim anything about the test run. An earlier
# version included "no tests ran" and "collected N items", which contradict
# "2 tests failed" and could mislead the agent, so the padded condition would
# differ from rung 1 by more than length.
_FILLER = [
    "platform linux -- Python 3, pytest",
    "cachedir: .pytest_cache",
    "rootdir: {root}",
    "configfile: setup.cfg",
    "plugins: none",
]


@dataclass
class CheckResult:
    """Outcome of one `check` invocation, before rung filtering."""

    passed: int = 0
    failed: int = 0
    errors: int = 0
    failures: list[dict] = field(default_factory=list)
    uncovered: list[str] = field(default_factory=list)
    raw_returncode: int = 0

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.errors == 0


def run_tests(repo: Path, test_cmd: list[str] | None = None,
              with_trace: bool = False) -> CheckResult:
    """Run the suite and collect structured results.

    `with_trace` additionally measures which lines never executed, which is the
    only extra information rung 4 is allowed to expose.
    """
    report = repo / ".mp_report.json"
    pytest_args = ["-q", "--json-report", f"--json-report-file={report}"]
    if with_trace:
        # --showlocals is rung 4's other signal: variable values at the failure
        # frame. Without it, rung 4 collapses into rung 3 for any bug that is a
        # wrong value rather than an unexecuted branch.
        pytest_args += ["--showlocals", "--tb=long"]
        cmd = [sys.executable, "-m", "coverage", "run", "--branch",
               "-m", "pytest", *pytest_args]
    else:
        cmd = test_cmd or [sys.executable, "-m", "pytest", *pytest_args]

    proc = subprocess.run(cmd, cwd=repo, capture_output=True, text=True,
                          timeout=600)
    res = CheckResult(raw_returncode=proc.returncode)

    if report.exists():
        data = json.loads(report.read_text())
        summary = data.get("summary", {})
        res.passed = summary.get("passed", 0)
        res.failed = summary.get("failed", 0)
        res.errors = summary.get("error", 0)
        for t in data.get("tests", []):
            if t.get("outcome") not in ("passed", "skipped"):
                call = t.get("call") or {}
                crash = (call.get("crash") or {})
                res.failures.append({
                    "test": t.get("nodeid", "?"),
                    "message": (crash.get("message") or "").strip(),
                    "path": crash.get("path"),
                    "lineno": crash.get("lineno"),
                    "longrepr": (call.get("longrepr") or ""),
                })
        report.unlink(missing_ok=True)

    if with_trace:
        res.uncovered = _uncovered_lines(repo)
    return res


def _uncovered_lines(repo: Path) -> list[str]:
    """Source lines the test run never executed. Rung 4's extra signal."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "coverage", "json", "-o", "-", "--quiet"],
            cwd=repo, capture_output=True, text=True, timeout=120)
        data = json.loads(proc.stdout or "{}")
    except Exception:
        return []

    out: list[str] = []
    for fname, info in (data.get("files") or {}).items():
        if "test" in Path(fname).name:
            continue
        for ln in (info.get("missing_lines") or []):
            out.append(f"{fname}:{ln} never executed")
    return out


MAX_LISTED = 20    # failing tests shown individually; the rest summarised
MAX_DETAILED = 5   # at rungs 3-4, failing tests given full detail; the rest by name
MAX_VALUES = 12    # rung-4 values shown per failing test
MAX_MESSAGE_LINES = 6   # lines of the error message (rungs 3 and 4 alike)


def render(res: CheckResult, rung: str, repo: Path | None = None,
           seed: int = 0) -> str:
    """Render a CheckResult at one rung. This is all the agent ever sees.

    Every rung shows at most MAX_LISTED failing tests individually, so an agent
    that breaks hundreds of tests does not flood its context, and the cap is the
    same for every rung. At rungs 3 and 4 only the first MAX_DETAILED of those
    get full detail; the rest are named, as at rung 2 — so with 20 failing tests
    rung 4 costs ~1-2K tokens per check rather than ~5K.
    """
    if rung not in RUNGS:
        raise ValueError(f"unknown rung {rung!r}; expected one of {RUNGS}")

    if res.ok:
        return "All tests passed."

    n = res.failed + res.errors
    head = f"{n} test{'s' if n != 1 else ''} failed."

    if rung == "outcome":
        return head

    if rung == "padded":
        target = len(render(res, "trace", repo))
        return head + "\n" + _pad(target - len(head) - 1, repo, seed)

    shown = res.failures[:MAX_LISTED]
    more = len(res.failures) - len(shown)
    tail = [f"... and {more} more failing test{'s' if more != 1 else ''}"] if more > 0 else []

    if rung == "location":
        return "\n".join([f"{n} failed:"] + [f"{f['test']} failed" for f in shown] + tail)

    lines = [f"{n} failed:"]
    for k, f in enumerate(shown):
        if k >= MAX_DETAILED:                 # beyond the detail cap: named, as at rung 2
            lines.append(f"{f['test']} failed")
            continue
        loc = _rel(f.get("path"), repo)
        loc = f"{loc}:{f['lineno']}" if loc and f.get("lineno") else "?"
        msg = [m for m in (f.get("message") or "").splitlines() if m.strip()][:MAX_MESSAGE_LINES]
        lines.append(f"{f['test']} failed at {loc}")
        lines.extend(f"  {m}" for m in msg)
        if rung == "trace":
            frames = f.get("frames") or []
            values = f.get("values")
            if values is None:        # CheckResult built by run_tests(): derive from longrepr
                values = _introspection_of(f.get("longrepr", "")).splitlines()
            if len(frames) > 1:
                lines.append("  call path: " + " -> ".join(frames))
            if values:
                lines.append("  values at failure:")
                lines.extend(f"    {v}" for v in values[:MAX_VALUES])
    if rung == "trace" and res.uncovered:
        lines.append("")
        lines.append("Execution trace:")
        lines.extend(f"  {_rel_line(u, repo)}" for u in res.uncovered[:40])
    return "\n".join(lines + tail)


def _rel(path: str | None, repo: Path | None) -> str:
    if not path:
        return ""
    if repo is None:
        return path
    try:
        return str(Path(path).relative_to(repo))
    except ValueError:
        return Path(path).name


def _rel_line(entry: str, repo: Path | None) -> str:
    fname, _, rest = entry.partition(":")
    return f"{_rel(fname, repo) or fname}:{rest}"


def _introspection_of(longrepr: str) -> str:
    """Rung 4's probe: pytest's assertion introspection and --showlocals block.

    Rung 3 shows only the headline ("assert 100.0 == 99.0"). The introspection
    lines ("+ where 100.0 = cart_total(...)") name the call that produced the
    wrong value, plus any locals, which is what makes rung 4 a probe rather
    than a restatement.
    """
    out = []
    for line in (longrepr or "").splitlines():
        t = line.strip()
        if t.startswith("E") and ("where" in t or "and" in t):
            out.append(t.lstrip("E").strip().lstrip("+").strip())
        elif t and not t.startswith(("E", ">", "def ", "@")) and " = " in t:
            out.append(t)          # --showlocals entries
    return "\n".join(list(dict.fromkeys(out))[:25])


def rung_deltas(res: CheckResult, repo: Path | None = None) -> dict:
    """Diagnostic: are the rungs actually distinct for this task?

    Rung 4 only adds signal when the bug leaves a trace — an unexecuted branch,
    a revealing intermediate value, informative locals. For a bug with none of
    those, rung 4 collapses into rung 3 and the top of the curve flattens for
    reasons that have nothing to do with the agent. Run this over the task set
    before the real runs and report how many tasks collapse.
    """
    bodies = {r: render(res, r, repo) for r in RUNGS}
    return {
        "chars": {r: len(b) for r, b in bodies.items()},
        "trace_adds_over_diff": bodies["trace"] != bodies["diff"],
        "padded_matches_trace": abs(
            len(bodies["padded"]) - len(bodies["trace"])) <= 2,
    }


def _pad(nchars: int, repo: Path | None, seed: int) -> str:
    """Information-free filler of roughly `nchars` characters."""
    if nchars <= 0:
        return ""
    rng = random.Random(seed)
    root = str(repo) if repo else "/testbed"
    out: list[str] = []
    total = 0
    while total < nchars:
        line = rng.choice(_FILLER).format(root=root)
        out.append(line)
        total += len(line) + 1
    return "\n".join(out)[:nchars]
