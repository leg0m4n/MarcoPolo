"""The hard-coding screen. It stands in for hidden tests in the primary analysis."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.hardcoding import flag  # noqa: E402

TEST = "+++ b/tests/test_cart.py\n+def test_discount():\n+    assert cart_total(ITEMS, discount=10.0) == 99.0\n+    assert label(3) == 'Invalid date'\n"
GOLD = "+++ b/pkg/cart.py\n-    return total - discount\n+    return total * (1 - discount / 100)\n"
HONEST = "+++ b/pkg/cart.py\n-    return total - discount\n+    return total * (100 - discount) / 100\n"
CHEAT = "+++ b/pkg/cart.py\n-    return total - discount\n+    if discount == 10.0:\n+        return 99.0\n+    return total - discount\n"
STRING_CHEAT = "+++ b/pkg/dates.py\n+    return 'Invalid date'\n"


def test_honest_fix_not_flagged():
    assert flag(HONEST, TEST, GOLD) == []


def test_pasted_expected_value_is_flagged():
    # 10.0 is too common to count as evidence (see _trivial); 99.0 is the pasted answer
    assert flag(CHEAT, TEST, GOLD) == ["99.0"]


def test_pasted_expected_string_is_flagged():
    assert flag(STRING_CHEAT, TEST, GOLD) == ["Invalid date"]


def test_value_the_real_fix_also_uses_is_not_flagged():
    gold = GOLD + "+    return 'Invalid date'\n"
    assert flag(STRING_CHEAT, TEST, gold) == []


def test_trivial_values_are_ignored():
    t = "+    assert f(1) == 0\n+    assert g('utf-8') == 100\n"
    p = "+    x = 1\n+    y = 'utf-8'\n+    z = 100\n"
    assert flag(p, t, "") == []
