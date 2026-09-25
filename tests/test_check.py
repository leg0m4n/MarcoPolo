"""The check parser, pinned to real pytest output.

Each fixture is verbatim pytest text (local paths replaced by the container's).
If parsing drifts, a rung shows the agent more or less than pre-registered.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.check import parse, statuses  # noqa: E402
from marcopolo.rungs import render  # noqa: E402

FX = Path(__file__).parent / "fixtures"
failures = (FX / "pytest_sample_failures.txt").read_text()
collect = (FX / "pytest_sample_collect_error.txt").read_text()
setup = (FX / "pytest_sample_setup_error.txt").read_text()

DISCOUNT = "test_cart.py::TestCart::test_discount"
PARSE_X = "test_cart.py::test_parse[x]"
PARSE_12 = "test_cart.py::test_parse[12]"


def test_statuses_from_summary():
    st = statuses(failures)
    assert st[PARSE_12][0] == "PASSED" and st[DISCOUNT][0] == "FAILED"


def test_only_the_tasks_tests_are_counted():
    res = parse(failures, [DISCOUNT, PARSE_12])
    assert (res.passed, res.failed) == (1, 1)


def test_assertion_failure_detail():
    f = parse(failures, [DISCOUNT]).failures[0]
    assert f["message"] == "AssertionError: assert 100.0 == 99.0"
    assert (f["path"], f["lineno"]) == ("test_cart.py", 10)
    assert any(v.startswith("where 100.0 = cart_total(") for v in f["values"])
    assert "expected = 99.0" in f["values"]


def test_exception_is_located_where_raised_in_source():
    f = parse(failures, [PARSE_X]).failures[0]
    assert f["message"].startswith("ValueError: invalid literal")
    assert (f["path"], f["lineno"]) == ("pkg/cart.py", 7)
    assert f["frames"] == ["test_cart.py:15", "pkg/cart.py:7"]     # the execution path


def test_nondeterministic_reprs_are_dropped():
    vals = parse(failures, [DISCOUNT]).failures[0]["values"]
    assert not any(v.startswith("self =") or " at 0x" in v for v in vals)


def test_collection_error_fails_every_test_with_the_real_cause():
    res = parse(collect, [DISCOUNT, PARSE_12])
    assert res.failed == 2
    f = res.failures[0]
    assert f["message"] == "SyntaxError: invalid syntax"
    assert f["path"] == "pkg/cart.py"
    assert all("site-packages" not in fr and "<frozen" not in fr for fr in f["frames"])


def test_setup_error():
    f = parse(setup, ["test_fixture.py::test_uses_db"]).failures[0]
    assert f["message"] == "RuntimeError: db unavailable"
    assert (f["path"], f["lineno"]) == ("test_fixture.py", 4)


def test_rendered_rungs_stay_monotonic_on_real_output():
    res = parse(failures, [DISCOUNT, PARSE_X, PARSE_12])
    lens = [len(render(res, r)) for r in ("outcome", "location", "diff", "trace")]
    assert lens == sorted(lens) and len(set(lens)) == 4, lens


def test_expected_vs_actual_on_continuation_lines_reaches_rung_3():
    """numpy puts x/y (actual/expected) after a bare "AssertionError:"."""
    out = (FX / "pytest_astropy_numpy_assert.txt").read_text()
    nid = "astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]"
    f = parse(out, [nid]).failures[0]
    assert "x: array([False, False, False, False])" in f["message"]
    assert "y: array([False, False,  True,  True])" in f["message"]
    diff = render(parse(out, [nid]), "diff")
    assert "y: array(" in diff and "values at failure" not in diff


def test_ids_with_spaces_match_the_datasets_truncated_ids():
    """SWE-bench's ids are cut at the first space; so is its parser's output."""
    from swebench.harness.log_parsers import PARSER_REGISTRY
    out = (FX / "pytest_param_with_spaces.txt").read_text()
    truncated = "test_spaces.py::test_non_mapping_init[ceci"     # as the dataset stores it
    ok = "test_spaces.py::test_non_mapping_init[ok]"
    # without the official parser the truncated id has no status at all; a
    # PASSING test named with a space would then be counted as failing
    assert parse(out, [truncated, ok]).failures[0]["status"] == "NOT RUN"
    # parse_log_pytest truncates too, so exact match; parse_log_pytest_v2 (astropy,
    # sphinx, scikit) keeps the full name, which only official grading's prefix
    # resolution reconciles with the dataset's truncated id. Both must agree.
    for parser in ("parse_log_pytest", "parse_log_astropy"):
        r = parse(out, [truncated, ok], PARSER_REGISTRY[parser])
        assert (r.passed, r.failed) == (1, 1), parser
        assert r.failures[0]["status"] == "FAILED", parser
    res = parse(out, [truncated, ok], PARSER_REGISTRY["parse_log_astropy"])
    assert (res.passed, res.failed) == (1, 1)
    f = res.failures[0]
    assert f["status"] == "FAILED" and "ceci n'est pas un meta" in f["message"]


def test_coloured_output_is_parsed():
    """astropy forces colour: every line starts with escape codes. Without
    stripping them, rung 3 and 4 silently lost all content (found on 8/40 tasks)."""
    from swebench.harness.log_parsers import PARSER_REGISTRY
    out = (FX / "pytest_astropy_ansi_color.txt").read_text()
    assert "\x1b[" in out, "fixture must be the raw coloured output"
    nid = "astropy/units/tests/test_format.py::test_cds_grammar[strings4-unit4]"
    f = parse(out, [nid], PARSER_REGISTRY["parse_log_astropy"]).failures[0]
    assert f["message"] != "FAILED" and f["path"] is not None
    res = parse(out, [nid], PARSER_REGISTRY["parse_log_astropy"])
    assert render(res, "trace") != render(res, "diff")
    assert "\x1b[" not in render(res, "trace"), "no escape codes reach the agent"
    vals = f["values"]
    assert "unit2 = Unit(\"km Mpc / s\")" in vals
    assert not any(", unit = " in v for v in vals), "the combined argument line is not repeated"
