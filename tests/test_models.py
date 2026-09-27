"""The reasoning-preservation fix. If this regresses, every multi-turn run
silently loses the model's reasoning between steps."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.models import restore_reasoning_key  # noqa: E402


def test_assistant_reasoning_moves_to_key_vllm_reads():
    out = restore_reasoning_key([{"role": "assistant", "content": "", "reasoning_content": "because X"}])
    assert out[0]["reasoning"] == "because X"
    assert "reasoning_content" not in out[0]


def test_existing_reasoning_key_is_not_overwritten():
    msg = {"role": "assistant", "reasoning": "keep", "reasoning_content": "other"}
    assert restore_reasoning_key([msg])[0]["reasoning"] == "keep"


def test_non_assistant_messages_untouched():
    msgs = [{"role": "user", "content": "hi", "reasoning_content": "x"},
            {"role": "tool", "content": "1 test failed."}]
    assert restore_reasoning_key(msgs) == msgs


def test_input_not_mutated():
    msg = {"role": "assistant", "reasoning_content": "because X"}
    restore_reasoning_key([msg])
    assert msg == {"role": "assistant", "reasoning_content": "because X"}


def test_cohere_gets_reasoning_content_and_vllm_gets_reasoning():
    """The two backends read opposite fields; each must get its own."""
    from marcopolo.models import move_reasoning
    from_vllm = {"role": "assistant", "reasoning": "because X"}
    from_litellm = {"role": "assistant", "reasoning_content": "because X"}
    assert move_reasoning([from_vllm], "reasoning_content")[0] == {"role": "assistant", "reasoning_content": "because X"}
    assert move_reasoning([from_litellm], "reasoning")[0] == {"role": "assistant", "reasoning": "because X"}


def test_cohere_model_key_only_from_environment(monkeypatch):
    import pytest
    from marcopolo.models import NorthCohereModel
    monkeypatch.delenv("COHERE_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        NorthCohereModel(model_name="openai/north-mini-code-1-0", cost_tracking="ignore_errors", model_kwargs={})
    monkeypatch.setenv("COHERE_API_KEY", "test-key")
    m = NorthCohereModel(model_name="openai/north-mini-code-1-0", cost_tracking="ignore_errors", model_kwargs={})
    assert m.config.model_kwargs["api_key"] == "test-key"
