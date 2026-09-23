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
