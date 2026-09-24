"""Guards on trajectory analysis. These numbers feed the truncation and
false-success metrics, so a wrong definition silently corrupts both."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.trajectory import Turn  # noqa: E402


def test_blank_content_with_tool_call_is_not_empty():
    """North Mini Code's normal tool-call turn: no text, one action."""
    assert not Turn(0, "tool_calls", content_chars=0, n_tool_calls=1).empty_content


def test_blank_content_without_tool_call_is_empty():
    assert Turn(0, "stop", content_chars=0, n_tool_calls=0).empty_content


def test_length_finish_is_truncated():
    assert Turn(0, "length").truncated
    assert not Turn(0, "tool_calls").truncated
