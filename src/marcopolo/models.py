"""Model adapters for mini-swe-agent.

North Mini Code's model card asks harnesses to keep reasoning between tool
calls; the research plan notes that dropping it forces replanning, which would
sandbag the model and fake a finding.

The stock mini-swe-agent + litellm + vLLM pipeline drops it silently:

    vLLM returns reasoning as        `reasoning`
    litellm renames it to            `reasoning_content`
    mini-swe-agent sends it back as  `reasoning_content`
    vLLM's server discards incoming  `reasoning_content`  (keeps only `reasoning`)

Verified with vLLM's /tokenize endpoint: a marker sent under
`reasoning_content` never reaches the prompt; under `reasoning` it does.
"""
from __future__ import annotations

from minisweagent.models.litellm_model import LitellmModel


def restore_reasoning_key(messages: list[dict]) -> list[dict]:
    """Move assistant reasoning to the key vLLM's server actually reads."""
    out = []
    for msg in messages:
        if msg.get("role") == "assistant" and msg.get("reasoning_content") and not msg.get("reasoning"):
            reasoning = msg["reasoning_content"]
            msg = {k: v for k, v in msg.items() if k != "reasoning_content"}
            msg["reasoning"] = reasoning
        out.append(msg)
    return out


class NorthVLLMModel(LitellmModel):
    """LitellmModel that keeps North Mini Code's reasoning across turns on vLLM."""

    def _prepare_messages_for_api(self, messages: list[dict]) -> list[dict]:
        return super()._prepare_messages_for_api(restore_reasoning_key(messages))
