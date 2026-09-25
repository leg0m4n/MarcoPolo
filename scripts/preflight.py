"""Pre-flight every candidate task before it may enter the frozen set.

Runs through the real `check` machinery (marcopolo.grader): the same grader, a
prepared agent container, and the gold patch applied inside the agent container
the way an agent would edit files. So it validates `check` itself, per task, and
records every rung's output on the unfixed code (the rung-collapse diagnostic).

A task is admitted only if, with NO network (the agent's and grader's condition):
  unfixed code : every FAIL_TO_PASS test fails
  gold patch   : every FAIL_TO_PASS test passes, no PASS_TO_PASS test fails
  pytest removed from the agent's environment, the package still imports

Why: a target test that needs the internet fails whatever the agent does (found
on psf__requests-1724: 0/6 target tests pass even with the real fix), and a
package that needs pytest to import breaks every probe script the agent writes.

CPU and Docker only, no GPU, so it may run outside the GPU window. Pulls,
tests and deletes one image at a time (all 46 at once would need ~150 GB).

    python scripts/preflight.py [tasks/candidates_v2.json] [results/preflight_v2.jsonl]
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from datasets import load_dataset

CANDIDATES = Path(sys.argv[1] if len(sys.argv) > 1 else "tasks/candidates_v2.json")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "results/preflight_v2.jsonl")
PKG = {"astropy/astropy": "astropy", "matplotlib/matplotlib": "matplotlib", "sphinx-doc/sphinx": "sphinx",
       "pydata/xarray": "xarray", "scikit-learn/scikit-learn": "sklearn", "psf/requests": "requests",
       "pylint-dev/pylint": "pylint", "mwaskom/seaborn": "seaborn", "pallets/flask": "flask"}
ACT = "source /opt/miniconda3/bin/activate testbed"


def sh(*args, timeout=1800, check=False):
    return subprocess.run(list(args), capture_output=True, text=True, timeout=timeout, check=check)


def dexec(c, script, *argv, timeout=1800):
    """Run a bash script in the container; argv passed safely as "$@"."""
    return sh("docker", "exec", "-w", "/testbed", c, "bash", "-c", script, "_", *argv, timeout=timeout)


def test_files(eval_script):
    """The test files the official evaluator runs, from its test command line.

    Passing individual node ids is fragile: if pytest cannot find ONE of them
    (parametrized ids vary by environment) it runs nothing at all. Running the
    files and reading each test's status from the -rA summary is what the
    official harness does, so check and scoring agree by construction.
    """
    a = eval_script.find(">>>>> Start Test Output")
    b = eval_script.find(">>>>> End Test Output", a)
    cmd = eval_script[a:b].splitlines()[1]
    return [tok for tok in cmd.split() if ".py" in tok]


def pytest_status(c, files):
    """{node_id: PASSED|FAILED|ERROR|...} from pytest's -rA summary over whole files."""
    if not files:
        return {}, 0.0
    t0 = time.time()
    r = dexec(c, f'{ACT} && COLUMNS=250 exec python -m pytest -rA --tb=no -p no:cacheprovider "$@"', *files)
    dt = time.time() - t0
    st = {}
    for line in r.stdout.splitlines():
        for tag in ("PASSED", "FAILED", "ERROR", "SKIPPED", "XFAIL", "XPASS"):
            if line.startswith(tag + " "):
                st[line[len(tag) + 1:].split(" - ")[0].strip()] = tag
    return st, dt


def put(c, text, dest):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".patch") as f:
        f.write(text)
    sh("docker", "cp", f.name, f"{c}:{dest}", check=True)
    Path(f.name).unlink()


def check_task(t, row):
    """Validate the task through the real `check` machinery, as an agent would meet it."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from marcopolo.grader import ACT as GACT, Grader, dexec as gexec
    from marcopolo.rungs import RUNGS, render

    img = "docker.io/" + t["image"]
    L = lambda v: json.loads(v) if isinstance(v, str) else list(v)
    f2p, p2p = set(L(row["FAIL_TO_PASS"])), set(L(row["PASS_TO_PASS"]))
    rec = {"instance_id": t["instance_id"], "repo": t["repo"], "n_f2p": len(f2p), "n_p2p": len(p2p)}
    pre = sh("docker", "image", "inspect", img).returncode == 0
    t0 = time.time()
    if not pre and sh("docker", "pull", "-q", img, timeout=3600).returncode != 0:
        return {**rec, "admitted": False, "reason": "pull failed"}
    rec["pull_s"] = round(time.time() - t0)
    agent = sh("docker", "run", "-d", "--network", "none", "-w", "/testbed", img, "sleep", "3600", check=True).stdout.strip()
    g = Grader(row, "trace", img)
    try:
        g.start()
        g.prepare_agent(agent)                       # tests committed, pytest removed, check installed
        rec["test_files"] = g.files

        base = g.run_tests(agent)
        failing = {f["test"] for f in base.failures}
        rec["base_f2p_failing"] = len(f2p & failing)
        rec["base_p2p_failing"] = len(p2p & failing)
        rec["check_seconds"] = g.log[-1]["seconds"]
        # rung collapse: what each rung shows on the unfixed code
        bodies = {r: render(base, r) for r in RUNGS}
        rec["rung_chars"] = {r: len(b) for r, b in bodies.items()}
        rec["location_adds_over_outcome"] = bodies["location"] != bodies["outcome"]
        rec["diff_adds_over_location"] = bodies["diff"] != bodies["location"]
        rec["trace_adds_over_diff"] = bodies["trace"] != bodies["diff"]

        if gexec(agent, "cat > /tmp/.gold.patch && git apply /tmp/.gold.patch", input=row["patch"]).returncode:
            return {**rec, "admitted": False, "reason": "gold patch did not apply"}
        gold = g.run_tests(agent)
        if gold is None:
            return {**rec, "admitted": False, "reason": "HARNESS: grader could not apply the agent-side diff"}
        gfail = {f["test"] for f in gold.failures}
        rec["gold_f2p_passing"] = len(f2p - gfail)
        rec["gold_p2p_failing"] = sorted(p2p & gfail)[:10]
        n_gold_p2p_failing = len(p2p & gfail)

        pkg = PKG.get(t["repo"], t["repo"].split("/")[1])
        rec["imports_without_pytest"] = "IMPORT_OK" in gexec(agent, f"{GACT} && python -c 'import {pkg}' && echo IMPORT_OK").stdout

        # HARNESS means the machinery itself failed: nothing ran, or the target
        # tests never ran even with the fix. Distinct from a few regression tests
        # that do not run in THIS environment (e.g. pylint skips its multiprocessing
        # tests when the container reports < 2 cores) — those make the task
        # unwinnable here, since the official evaluator shares the environment.
        not_run = {f["test"] for f in gold.failures if f.get("message", "").startswith("not run")}
        if base.passed + base.failed == 0 or (f2p & not_run):
            return {**rec, "admitted": False, "reason": "HARNESS: tests did not run; investigate, do not trust"}
        reasons = []
        env_skipped = sorted(p2p & not_run)
        if env_skipped:
            rec["regression_tests_not_run_here"] = env_skipped[:10]
            reasons.append(f"{len(env_skipped)} regression tests do not run in this environment (skipped or absent)")
            n_gold_p2p_failing -= len(env_skipped)
        if rec["base_f2p_failing"] != len(f2p): reasons.append(f"{len(f2p) - rec['base_f2p_failing']} target tests already pass unfixed")
        if rec["gold_f2p_passing"] != len(f2p): reasons.append(f"only {rec['gold_f2p_passing']}/{len(f2p)} target tests pass with the real fix")
        if n_gold_p2p_failing: reasons.append(f"{n_gold_p2p_failing} regression tests fail with the real fix")
        if not rec["imports_without_pytest"]: reasons.append(f"{pkg} needs pytest to import")
        return {**rec, "admitted": not reasons, "reason": "; ".join(reasons) or "ok"}
    finally:
        g.stop()
        sh("docker", "rm", "-f", agent)
        if not pre:
            sh("docker", "rmi", img)


def main():
    tasks = json.loads(CANDIDATES.read_text())["tasks"]
    rows = {r["instance_id"]: r for r in load_dataset("SWE-bench/SWE-bench_Verified", split="test")}
    done = {json.loads(l)["instance_id"] for l in OUT.read_text().splitlines()} if OUT.exists() else set()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for i, t in enumerate(tasks, 1):
        if t["instance_id"] in done:
            continue
        t0 = time.time()
        try:
            rec = check_task(t, rows[t["instance_id"]])
        except Exception as e:
            rec = {"instance_id": t["instance_id"], "repo": t["repo"], "admitted": False,
                   "reason": f"preflight error: {type(e).__name__}: {e}"[:300]}
        rec["wall_s"] = round(time.time() - t0)
        with OUT.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"[{i}/{len(tasks)}] {'ADMIT' if rec['admitted'] else 'reject'} {t['instance_id']:36} "
              f"{rec['wall_s']:>4}s  {rec['reason']}", flush=True)


if __name__ == "__main__":
    main()
