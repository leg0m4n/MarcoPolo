"""Model adapters for mini-swe-agent: keep North Mini Code's reasoning across turns.

The model card asks harnesses to keep reasoning between tool calls; the research
plan notes that dropping it forces replanning, sandbagging the model. Each
backend reads prior-turn reasoning from exactly ONE field and silently ignores
the other — and the two backends disagree:

    backend          returns reasoning as   reads it back from   ignores
    vLLM (local)     reasoning              reasoning            reasoning_content
    Cohere API       reasoning_content      reasoning_content    reasoning

litellm normalises responses to `reasoning_content` and mini-swe-agent sends
messages back unchanged. So on vLLM the stock pipeline drops reasoning every
turn, and a vLLM fix applied to Cohere would drop it there instead.

Evidence: vLLM — /tokenize shows a `reasoning_content` marker never reaches the
prompt. Cohere — a codename invented only in turn-1 reasoning is recalled on
turn 2 when sent back as `reasoning_content` ("Nebulova"), not when sent as
`reasoning` or omitted ("Nebulon"). FINDINGS.md has both.
"""
from __future__ import annotations

import os

from minisweagent.models.litellm_model import LitellmModel

_FIELDS = ("reasoning", "reasoning_content")


def move_reasoning(messages: list[dict], to: str) -> list[dict]:
    """Put each assistant message's reasoning under `to`, the field the backend reads."""
    assert to in _FIELDS
    other = _FIELDS[1 - _FIELDS.index(to)]
    out = []
    for msg in messages:
        if msg.get("role") == "assistant" and msg.get(other) and not msg.get(to):
            reasoning = msg[other]
            msg = {k: v for k, v in msg.items() if k != other}
            msg[to] = reasoning
        out.append(msg)
    return out


def restore_reasoning_key(messages: list[dict]) -> list[dict]:
    """vLLM's field. Kept for callers and tests written against the first version."""
    return move_reasoning(messages, "reasoning")


class NorthVLLMModel(LitellmModel):
    """North Mini Code served locally by vLLM."""

    def _prepare_messages_for_api(self, messages: list[dict]) -> list[dict]:
        return super()._prepare_messages_for_api(move_reasoning(messages, "reasoning"))


class NorthCohereModel(LitellmModel):
    """North Mini Code on Cohere's hosted API (OpenAI-compatible endpoint).

    The API key comes only from the COHERE_API_KEY environment variable — never
    from a config file, so it cannot end up in the repository.
    """

    def __init__(self, **kwargs):
        mk = dict(kwargs.get("model_kwargs") or {})
        if not mk.get("api_key"):
            key = os.environ.get("COHERE_API_KEY")
            if not key:
                raise RuntimeError("COHERE_API_KEY is not set (source ~/.config/marcopolo/cohere.env)")
            mk["api_key"] = key
        # mini-swe-agent's SWE-bench config sets parallel_tool_calls: true; Cohere's
        # API rejects the parameter outright ("parallel_tool_calls is not supported").
        # A real harness difference from the vLLM runs, recorded in FINDINGS.md.
        mk.pop("parallel_tool_calls", None)
        kwargs["model_kwargs"] = mk
        super().__init__(**kwargs)

    def _prepare_messages_for_api(self, messages: list[dict]) -> list[dict]:
        return super()._prepare_messages_for_api(move_reasoning(messages, "reasoning_content"))
