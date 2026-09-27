"""Memorisation probe: can the model write a task's real fix without seeing the code?

The model gets only the repository name and the GitHub issue (the text the agent
also gets), no code and no tools, and is asked for the patch. If it reproduces
the real fix's lines, it has most likely seen the fix in training.

Scoring, per task:
  gold lines   lines the real fix adds, whitespace-normalised, >= MIN_LINE chars,
               and NOT already in the issue text (a fix the issue spells out
               proves nothing about memory)
  recall       share of gold lines that appear verbatim in the model's answer
  chance       the same recall against the answers for OTHER tasks of the same
               repository: how much overlap common code lines give by chance

Pre-registered flag: recall >= FLAG_RECALL over at least MIN_GOLD gold lines.
Tasks with fewer gold lines cannot be assessed and are reported as such. A flag
is evidence, not proof: a small, obvious fix can be re-derived from the issue.
Flagged tasks feed a sensitivity analysis (primary result with and without them).
"""
from __future__ import annotations

import re

MIN_LINE = 10
MIN_GOLD = 2
FLAG_RECALL = 0.5

PROMPT = """Repository: {repo}

This issue was reported on the repository's GitHub:

<issue>
{issue}
</issue>

You cannot see the code. From your own knowledge of this repository, write the \
patch that fixed this issue, as a unified diff with file paths (git format). \
Output only the diff."""


def norm(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def gold_lines(patch: str, issue: str) -> list[str]:
    """Distinct lines the real fix adds that the issue does not already contain."""
    text = norm(issue)
    out = []
    for line in patch.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            s = norm(line[1:])
            if len(s) >= MIN_LINE and s not in text and s not in out:
                out.append(s)
    return out


def answer_lines(answer: str) -> set[str]:
    """Normalised lines of the model's answer, diff markers removed."""
    out = set()
    for line in answer.splitlines():
        if line.startswith(("+++", "---")):
            continue
        out.add(norm(line[1:] if line[:1] in "+- " else line))
    return out


def recall(gold: list[str], answer: str) -> float | None:
    if not gold:
        return None
    have = answer_lines(answer)
    return sum(g in have for g in gold) / len(gold)


def files_named(patch: str, answer: str) -> float | None:
    files = [l[6:].strip() for l in patch.splitlines() if l.startswith("+++ b/")]
    return sum(f in answer for f in files) / len(files) if files else None


def verdict(gold: list[str], r: float | None) -> str:
    if r is None or len(gold) < MIN_GOLD:
        return "unassessable"
    return "flagged" if r >= FLAG_RECALL else "clear"
