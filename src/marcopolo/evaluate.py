"""The official SWE-bench evaluator, run inside the same sandbox as the agent.

Scoring executes the agent's patch, so its container is as much a place for the
agent's code to reach out from as the agent's own. Stock, it has the network
and adds CAP_SYS_ADMIN; here it gets marcopolo.sandbox's limits instead. The
evaluator is otherwise untouched: same images, scripts, parser and verdicts.

Usage: identical to `python -m swebench.harness.run_evaluation ...`
"""
from __future__ import annotations

import runpy

from docker.models.containers import ContainerCollection

from marcopolo.sandbox import harden_evaluator_create

_create = ContainerCollection.create


def _hardened_create(self, *args, **kwargs):
    if str(kwargs.get("name", "")).startswith("sweb.eval."):
        kwargs = harden_evaluator_create(kwargs)
    return _create(self, *args, **kwargs)


def install() -> None:
    ContainerCollection.create = _hardened_create


if __name__ == "__main__":
    install()
    runpy.run_module("swebench.harness.run_evaluation", run_name="__main__", alter_sys=True)
