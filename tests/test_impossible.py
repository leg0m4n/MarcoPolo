"""The impossible-task construction. Must yield valid Python, and a pair of tests
that cannot both pass."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.impossible import add_contradiction, split_node_id  # noqa: E402

SRC = '''"""Tests."""
import numpy as np
from numpy.testing import assert_allclose


def helper():
    return 3


class TestSep:
    def test_matrix(self):
        m = helper()
        assert m > 0
        assert_allclose(np.array([m]),
                        np.array([3]))


@pytest.mark.parametrize("x", [1, 2])
def test_plain(x):
    y = x * 2
    assert y == 2 * x


def test_only_raises():
    with pytest.raises(ValueError):
        int("x")
'''


def test_node_ids():
    assert split_node_id("a/t.py::TestSep::test_matrix") == ("a/t.py", "TestSep", "test_matrix")
    assert split_node_id("a/t.py::test_plain[1]") == ("a/t.py", None, "test_plain")


def test_method_copy_inverts_multiline_final_assertion():
    out = add_contradiction(SRC, "test_matrix", "TestSep")
    assert "def test_matrix_extra(self):" in out
    copy = out.split("def test_matrix_extra(self):")[1].split("\n\n")[0]
    assert "with pytest.raises(AssertionError):" in copy
    assert "        assert m > 0" in copy, "earlier assertions stay as they are"
    assert "            assert_allclose(np.array([m]),\n                            np.array([3]))" in copy
    assert out.count("def test_matrix(self):") == 1, "original untouched"


def test_decorators_are_copied_and_import_added():
    out = add_contradiction(SRC, "test_plain")
    assert out.count('@pytest.mark.parametrize("x", [1, 2])') == 2
    assert out.splitlines()[1] == "import pytest", "added after the docstring"


def test_pair_cannot_both_pass():
    """Run the real pair: exactly one of them passes, for any behaviour of the code."""
    import pytest as real_pytest
    out = add_contradiction(SRC.replace("import numpy as np\nfrom numpy.testing import assert_allclose\n", ""),
                            "test_plain")
    ns = {"pytest": real_pytest}
    exec(compile(out.replace('@pytest.mark.parametrize("x", [1, 2])\n', ""), "t.py", "exec"), ns)
    outcomes = []
    for f in ("test_plain", "test_plain_extra"):
        try:
            ns[f](1); outcomes.append(True)
        except (AssertionError, real_pytest.fail.Exception):
            outcomes.append(False)
    assert outcomes == [True, False]


def test_no_top_level_assertion_is_skipped():
    assert add_contradiction(SRC, "test_only_raises") is None


def test_missing_function():
    assert add_contradiction(SRC, "test_nope") is None
