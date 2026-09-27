import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo import memorisation as mem  # noqa: E402

GOLD = """diff --git a/pkg/mod.py b/pkg/mod.py
--- a/pkg/mod.py
+++ b/pkg/mod.py
@@ -1,3 +1,5 @@
 def f(x):
-    return old(x)
+    value = compute_properly(x, strict=True)
+    return normalise(value)
+    y = 1
"""
ISSUE = "f() is wrong. I think it should end with `return normalise(value)`."


def test_lines_the_issue_already_gives_do_not_count():
    assert mem.gold_lines(GOLD, ISSUE) == ["value = compute_properly(x, strict=True)"]
    assert mem.gold_lines(GOLD, "") == ["value = compute_properly(x, strict=True)", "return normalise(value)"]


def test_reproduced_fix_scores_full_recall_whatever_the_indentation():
    answer = "--- a/pkg/mod.py\n+++ b/pkg/mod.py\n@@\n+        value = compute_properly(x,  strict=True)\n"
    assert mem.recall(mem.gold_lines(GOLD, ISSUE), answer) == 1.0


def test_a_different_fix_scores_zero():
    assert mem.recall(mem.gold_lines(GOLD, ""), "+    return new_function(x)\n") == 0.0


def test_verdicts():
    two = ["line one is long", "line two is long"]
    assert mem.verdict(two, 0.5) == "flagged"
    assert mem.verdict(two, 0.0) == "clear"
    assert mem.verdict(two[:1], 1.0) == "unassessable", "one line is too little to call memory"
    assert mem.verdict([], None) == "unassessable"


def test_files_named():
    assert mem.files_named(GOLD, "I would edit pkg/mod.py") == 1.0
    assert mem.files_named(GOLD, "no idea") == 0.0
