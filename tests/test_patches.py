"""What is scored vs kept for the audit. A mistake here either zeroes correct
fixes (test hunks break `git apply`) or lets test tampering count."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.patches import files_in, is_test_file, same_changes, split_patch  # noqa: E402

SRC = "diff --git a/pkg/cart.py b/pkg/cart.py\n--- a/pkg/cart.py\n+++ b/pkg/cart.py\n@@ -1 +1 @@\n-a\n+b\n"
TST = "diff --git a/pkg/tests/test_cart.py b/pkg/tests/test_cart.py\n--- a/pkg/tests/test_cart.py\n+++ b/pkg/tests/test_cart.py\n@@ -1 +1 @@\n-assert x == 99\n+assert True\n"
CONF = "diff --git a/conftest.py b/conftest.py\nnew file mode 100644\n--- /dev/null\n+++ b/conftest.py\n@@ -0,0 +1 @@\n+collect_ignore = ['pkg']\n"


def test_test_edits_are_stripped_from_the_scored_patch():
    src, tst = split_patch(SRC + TST)
    assert files_in(src) == ["pkg/cart.py"] and files_in(tst) == ["pkg/tests/test_cart.py"]


def test_conftest_trick_is_stripped():
    src, tst = split_patch(SRC + CONF)
    assert "conftest.py" in files_in(tst) and "conftest.py" not in files_in(src)


def test_task_test_files_count_even_without_test_naming():
    assert is_test_file("pkg/checks.py", {"pkg/checks.py"})
    assert not is_test_file("pkg/checks.py")


def test_source_files_named_like_tests_are_not_misclassified():
    assert not is_test_file("pkg/testbed_utils.py")
    assert not is_test_file("pkg/attestation.py")


def test_empty_patch():
    assert split_patch("") == ("", "")


def test_same_changes_ignores_headers():
    other = SRC.replace("diff --git", "diff --git").replace("@@ -1 +1 @@", "@@ -1,1 +1,1 @@")
    assert same_changes(SRC, other)
    assert not same_changes(SRC, TST)
