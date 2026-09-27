"""One container profile for everything that runs the agent's code.

Three kinds of container execute code the agent wrote: its own workspace, the
`check` grader, and the official SWE-bench evaluator that scores it. All three
get the same limits, so `check` and scoring behave alike and none of them is
a way out:

  --network none          no route anywhere: no web search, no package index,
                          no proxy (the July 2026 escape used a permitted proxy)
  --cap-drop ALL          root inside the grader/evaluator keeps its uid but none
                          of root's kernel privileges (no mount, no raw sockets,
                          no reading other users' files); the stock evaluator
                          even ADDS CAP_SYS_ADMIN, the classic escape capability
  no-new-privileges       setuid binaries (su, sudo) cannot raise privileges
  --pids-limit, --memory  a runaway or fork-bombing script cannot starve the
                          shared host

The agent additionally works as the image's unprivileged `nonroot` user: it
can edit /testbed (world-writable in every SWE-bench image) but not the Python
environment, /usr/local/bin/check, or anything else outside it. The grader and
evaluator stay root, as in the official harness, so tests behave as they do
there.
"""
from __future__ import annotations

import subprocess

AGENT_USER = "nonroot"
MEMORY = "8g"
PIDS = 4096

HARDEN = ["--network", "none", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
          "--pids-limit", str(PIDS), "--memory", MEMORY]
AGENT_RUN_ARGS = ["--rm", *HARDEN, "--user", AGENT_USER]
# The harness runs each command with `bash -c`, which reads only $BASH_ENV. The
# stock config points it at /root/.bashrc, unreadable to the agent's user; this
# root-owned copy of its activation line is readable but not writable by it.
BASH_ENV = "/etc/marcopolo_testbed_env.sh"


def evaluator_kwargs() -> dict:
    """HARDEN in docker-py's terms, for the official evaluator's containers."""
    return {"network_mode": "none", "cap_drop": ["ALL"], "security_opt": ["no-new-privileges"],
            "pids_limit": PIDS, "mem_limit": MEMORY}


def harden_evaluator_create(kwargs: dict) -> dict:
    """The official evaluator's container arguments, sandboxed. Drops its cap_add."""
    out = {k: v for k, v in kwargs.items() if k != "cap_add"}
    out.update(evaluator_kwargs())
    return out


def _exec(container, script, user, input=None, timeout=120):
    return subprocess.run(["docker", "exec", "-i", "-u", user, "-w", "/testbed", container, "bash", "-c", script],
                          input=input, capture_output=True, text=True, timeout=timeout)


# Download caches, never used at run time, that can hold FUTURE releases of the
# task's own package: xarray images ship xarray 2025.4.0 in conda's cache, with
# the fixes to four of our tasks in it (found by marcopolo.leakcheck).
CACHES = ["/opt/miniconda3/pkgs", "/root/.cache"]


def sanitize(container: str) -> None:
    """Delete package caches before the leak check and before the agent starts."""
    r = _exec(container, "rm -rf " + " ".join(f"{c}/* {c}/.[!.]*" for c in CACHES), "root", timeout=600)
    left = _exec(container, "ls -A " + " ".join(CACHES) + " 2>/dev/null | grep -v ':$' | grep -c .", "root").stdout.strip()
    if left not in ("", "0"):
        raise RuntimeError(f"caches not emptied ({left} entries left): {r.stderr[-300:]}")


def prepare_user(container: str) -> None:
    """Give the unprivileged user root's view of the project: its conda env and git.

    SWE-bench images activate the `testbed` env in /root/.bashrc only, so without
    this the agent's python would be the bare base interpreter, silently.
    """
    # /testbed is world-writable except what the image's last build step wrote as
    # root (a few hundred loose git objects, logs, egg-info). Root owns those, so
    # it may chmod them without any capability. Pack files are skipped: git never
    # rewrites them, and touching them would copy hundreds of MB up the overlay.
    # (files some other uid owns, e.g. matplotlib's unpacked freetype build, are left as they are)
    r = _exec(container, "find /testbed -user root ! -perm -o+w ! -path '/testbed/.git/objects/pack/*' "
                         "-exec chmod a+rwX {} +", "root")
    if r.returncode:
        raise RuntimeError(f"could not open /testbed to {AGENT_USER}: {r.stderr[-300:]}")
    r = _exec(container, f"grep -h 'conda activate' /root/.bashrc > {BASH_ENV} && chmod 644 {BASH_ENV}", "root")
    if r.returncode:
        raise RuntimeError(f"no conda activation line in /root/.bashrc: {r.stderr[-300:]}")
    r = _exec(container, "git config --global --add safe.directory /testbed", AGENT_USER)
    if r.returncode:
        raise RuntimeError(f"could not set up {AGENT_USER}: {r.stderr[-300:]}")
    # exactly how the harness will run the agent's commands
    probe = subprocess.run(["docker", "exec", "-u", AGENT_USER, "-e", f"BASH_ENV={BASH_ENV}", "-w", "/testbed",
                            container, "bash", "-c", "id -un; python -c 'import sys; print(sys.prefix)'; "
                            "git rev-parse -q --verify HEAD >/dev/null && echo GIT_OK"],
                           capture_output=True, text=True, timeout=120).stdout.split()
    if probe[:1] != [AGENT_USER] or not probe[1:2] or not probe[1].endswith("/envs/testbed") or "GIT_OK" not in probe:
        raise RuntimeError(f"{AGENT_USER} does not see the testbed env: {probe}")
