"""Read mini-swe-agent trajectories and surface what the runner hides.

mini-swe-agent persists the full API response per turn under
`message["extra"]["response"]`, but never surfaces `finish_reason`. That field
decides whether a run is usable:

A turn with `finish_reason == "length"` was cut off mid-generation. Because
North Mini Code emits reasoning before content, a truncated turn can return
EMPTY content while the model was working correctly — and a harness scores that
as a failure.

This matters for Leg 1 specifically. Richer feedback rungs produce longer
reasoning, so a fixed completion budget truncates high rungs more often than
low ones. That manufactures a rung effect pointing the same direction as the
hypothesis. Any resolve-rate curve must be reported alongside the truncation
rate per rung, or it cannot be distinguished from a budget artifact.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Turn:
    index: int
    finish_reason: str | None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    content_chars: int = 0
    reasoning_chars: int = 0
    n_tool_calls: int = 0

    @property
    def truncated(self) -> bool:
        return self.finish_reason == "length"

    @property
    def empty_content(self) -> bool:
        """No text AND no action: the turn produced nothing usable.

        North Mini Code routinely leaves `content` blank on tool-call turns, so
        blank content alone is normal and must not be counted.
        """
        return self.content_chars == 0 and self.n_tool_calls == 0


@dataclass
class Trajectory:
    path: Path
    turns: list[Turn] = field(default_factory=list)

    @property
    def n_truncated(self) -> int:
        return sum(t.truncated for t in self.turns)

    @property
    def n_empty(self) -> int:
        return sum(t.empty_content for t in self.turns)

    @property
    def total_completion_tokens(self) -> int:
        return sum(t.completion_tokens for t in self.turns)

    @property
    def usable(self) -> bool:
        """A run with any truncated turn cannot be scored at face value."""
        return self.n_truncated == 0


def load(path: Path) -> Trajectory:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    messages = data.get("messages") or data.get("trajectory") or []

    traj = Trajectory(path=Path(path))
    idx = 0
    for msg in messages:
        extra = (msg or {}).get("extra") or {}
        resp = extra.get("response")
        if not isinstance(resp, dict):
            continue
        choice = (resp.get("choices") or [{}])[0]
        m = choice.get("message") or {}
        usage = resp.get("usage") or {}
        traj.turns.append(Turn(
            index=idx,
            finish_reason=choice.get("finish_reason"),
            prompt_tokens=usage.get("prompt_tokens", 0) or 0,
            completion_tokens=usage.get("completion_tokens", 0) or 0,
            content_chars=len(m.get("content") or ""),
            reasoning_chars=len(
                m.get("reasoning") or m.get("reasoning_content") or ""),
            n_tool_calls=len(m.get("tool_calls") or []),
        ))
        idx += 1
    return traj


def summarize(paths: list[Path]) -> dict:
    """Aggregate over many trajectories. Report this next to any resolve rate."""
    trajs = [load(p) for p in paths]
    reasons: Counter = Counter()
    for t in trajs:
        reasons.update(turn.finish_reason or "unknown" for turn in t.turns)

    n = len(trajs) or 1
    return {
        "trajectories": len(trajs),
        "usable": sum(t.usable for t in trajs),
        "with_truncation": sum(not t.usable for t in trajs),
        "truncation_rate": round(sum(not t.usable for t in trajs) / n, 4),
        "turns": sum(len(t.turns) for t in trajs),
        "finish_reasons": dict(reasons),
        "completion_tokens_total": sum(t.total_completion_tokens for t in trajs),
        "empty_content_turns": sum(t.n_empty for t in trajs),
    }
