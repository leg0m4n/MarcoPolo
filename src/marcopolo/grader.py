"""The `check` tool: tests run in a separate grader container, feedback at one rung.

Agent container (set up once per run):
  - the task's tests are applied and committed, so the agent can read them and
    so its diffs are against the same base as the grader's
  - pytest is uninstalled, so the agent cannot run the suite and see more than
    its rung allows (probe scripts remain possible; they are counted)
  - /usr/local/bin/check prints the latest result the harness placed for it

When a command runs `check`, BEFORE executing it the harness:
  1. snapshots the agent's working tree as a diff (via a scratch git index, so
     the agent's own staging area is untouched)
  2. applies it in the grader container on the same base
  3. runs the task's test files as the official evaluator does
  4. renders the result at this run's rung, and writes it + an exit code into
     the agent's container for the `check` script to print

The grader has pytest; the agent does not; neither has network. The grader runs
the tests as they are in the agent's workspace — edits included — as a real repo
would. Scoring later uses the original test files (patches.py).
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from marcopolo.check import parse
from marcopolo.rungs import RUNGS, render

ACT = "source /opt/miniconda3/bin/activate testbed"
# `check` in command position: start, or after ; && || | ( $( — not `grep check`
CHECK_RE = re.compile(r"(?:^|[;&|(]\s*|\$\(\s*)check(?=\s|$|[;&|)<>])")
SHIM = """#!/bin/sh
if [ -f /tmp/.mp_check_out ]; then cat /tmp/.mp_check_out; exit "$(cat /tmp/.mp_check_rc)"; fi
echo "check: no result. Run \\`check\\` as its own command (e.g. \\`check\\` or \\`cd /testbed && check\\`)."
exit 2
"""
SNAPSHOT = ("cd /testbed && cp .git/index /tmp/.mp_index && GIT_INDEX_FILE=/tmp/.mp_index git add -A >/dev/null 2>&1 "
            "&& GIT_INDEX_FILE=/tmp/.mp_index git diff --cached --binary HEAD; rm -f /tmp/.mp_index")


def _run(args, input=None, timeout=900):
    return subprocess.run(args, input=input, capture_output=True, text=True, timeout=timeout)


def dexec(container, script, input=None, timeout=900):
    return _run(["docker", "exec", "-i", "-w", "/testbed", container, "bash", "-c", script], input, timeout)


def test_files(eval_script: str) -> list[str]:
    """The files the official evaluator runs (same rule as scripts/preflight.py)."""
    a = eval_script.find(">>>>> Start Test Output")
    b = eval_script.find(">>>>> End Test Output", a)
    return [t for t in eval_script[a:b].splitlines()[1].split() if ".py" in t]


def _as_list(v):
    return json.loads(v) if isinstance(v, str) else list(v)


def _commit_tests(container, test_patch):
    r = dexec(container, "cat > /tmp/.mp_test.patch && git apply /tmp/.mp_test.patch && git add -A "
                         "&& git -c user.email=mp@local -c user.name=marcopolo commit -qm 'task tests' "
                         "&& rm -f /tmp/.mp_test.patch", input=test_patch)
    if r.returncode:
        raise RuntimeError(f"could not apply the task's tests: {r.stderr[-300:]}")


class Grader:
    def __init__(self, instance: dict, rung: str, image: str):
        if rung not in RUNGS:
            raise ValueError(f"unknown rung {rung!r}")
        self.rung, self.image = rung, image
        self.files = test_files(instance["eval_script"])
        self.relevant = _as_list(instance["FAIL_TO_PASS"]) + _as_list(instance["PASS_TO_PASS"])
        self.test_patch = instance["test_patch"]
        # decide pass/fail exactly as scoring will (see check.parse)
        from swebench.harness.log_parsers import PARSER_REGISTRY
        self.status_parser = PARSER_REGISTRY.get(instance.get("log_parser", ""))
        self.container = None
        self.log: list[dict] = []

    def start(self):
        r = _run(["docker", "run", "-d", "--network", "none", "-w", "/testbed", self.image, "sleep", "4h"], timeout=600)
        if r.returncode:
            raise RuntimeError(f"grader container failed: {r.stderr[-300:]}")
        self.container = r.stdout.strip()
        _commit_tests(self.container, self.test_patch)

    def prepare_agent(self, agent_container: str):
        """Tests in, pytest out, `check` script in place."""
        _commit_tests(agent_container, self.test_patch)
        r = dexec(agent_container, f"{ACT} && pip uninstall -y -q pytest >/dev/null 2>&1; "
                                   "cat > /usr/local/bin/check && chmod +x /usr/local/bin/check", input=SHIM)
        if r.returncode:
            raise RuntimeError(f"could not prepare agent container: {r.stderr[-300:]}")

    def grade(self, agent_container: str) -> tuple[str, int]:
        """Run the tests on the agent's current code; (rendered feedback, exit code)."""
        res = self.run_tests(agent_container)
        if res is None:
            return "check: could not apply your changes to a clean copy of the repository.", 2
        text = render(res, self.rung)
        self.log[-1]["chars"] = len(text)
        return text, 0 if res.ok else 1

    def run_tests(self, agent_container: str):
        """CheckResult for the agent's current code, or None if its changes won't apply."""
        t0 = time.time()
        diff = dexec(agent_container, SNAPSHOT).stdout
        # -fd, never -x: ignored files include compiled extensions (astropy's C modules);
        # removing them breaks every import. The base commit already holds whatever
        # was untracked in the image, so -fd removes exactly what a previous check added.
        dexec(self.container, "git reset -q --hard HEAD && git clean -qfd")
        if diff.strip():
            ap = dexec(self.container, "git apply --binary --whitespace=nowarn -", input=diff)
            if ap.returncode:
                self.log.append({"t": time.time(), "error": "apply failed", "detail": ap.stderr[-300:]})
                return None
        quoted = " ".join(f"'{f}'" for f in self.files)
        out = dexec(self.container, f"{ACT} && COLUMNS=250 python -m pytest -rA --tb=long --showlocals "
                                    f"--color=no -p no:cacheprovider {quoted} 2>&1").stdout
        res = parse(out, self.relevant, self.status_parser)
        self.log.append({"t": round(t0, 2), "seconds": round(time.time() - t0, 1), "passed": res.passed,
                         "failed": res.failed, "all_passed": res.ok, "chars": None, "diff_chars": len(diff)})
        return res

    def stop(self):
        if self.container:
            _run(["docker", "rm", "-f", self.container], timeout=120)
            self.container = None


def intercept(env, grader: Grader):
    """Wrap env.execute: run the grader whenever a command invokes `check`."""
    original = env.execute
    agent = env.container_id

    def execute(action: dict, cwd: str = "", *, timeout: int | None = None):
        if CHECK_RE.search(action.get("command", "")):
            text, rc = grader.grade(agent)
            dexec(agent, "cat > /tmp/.mp_check_out", input=text + "\n")
            dexec(agent, f"echo {rc} > /tmp/.mp_check_rc")
            try:
                return original(action, cwd, timeout=timeout)
            finally:
                dexec(agent, "rm -f /tmp/.mp_check_out /tmp/.mp_check_rc")
        return original(action, cwd, timeout=timeout)

    env.execute = execute
