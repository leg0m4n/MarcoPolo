"""Parse pytest's text output into the structure the rungs render from.

`check` runs the task's test files the way the official evaluator does:
    pytest -rA --tb=long --showlocals -p no:cacheprovider <test files>
with COLUMNS=250 so the summary is not truncated. Statuses come from the -rA
summary; everything a rung may reveal comes from the FAILURES/ERRORS sections.

Per failing test we keep:
    message   the raised error, e.g. "AssertionError: assert 100.0 == 99.0"  (rung 3)
    path/line where it was raised — the last repo frame                       (rung 3)
    frames    the call path through repo files, test -> source                 (rung 4)
    values    pytest's introspection ("where 100.0 = f(...)") and the locals
              at each repo frame                                             (rung 4)

Frames outside the repository (site-packages, <frozen ...>) are dropped: they are
noise, and they would expose the harness layout. `self`/`cls` and reprs holding
memory addresses are dropped so identical code gives identical feedback.
"""
from __future__ import annotations

import re

from marcopolo.rungs import CheckResult

PASS = ("PASSED", "XFAIL")          # swebench grading counts both as passing
_SECTION = re.compile(r"^={5,} (FAILURES|ERRORS|PASSES|short test summary info|warnings summary) ={5,}\s*$")
_END = re.compile(r"^={5,} .*\b(passed|failed|error|errors|skipped|no tests ran)\b.* ={5,}\s*$")
_HEADER = re.compile(r"^_{3,} (.+?) _{3,}\s*$")
_FRAME_SEP = re.compile(r"^(_ ){5,}_?\s*$")
_LOC = re.compile(r"^(\S+?\.py):(\d+):(?: (.*))?$")
_FILE_LINE = re.compile(r'File "([^"]+)", line (\d+)')
_LOCAL = re.compile(r"^([A-Za-z_]\w*)\s+= (.*)$")
_STATUS = re.compile(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS) (.+?)(?: - (.*))?$")
MAX_VALUE = 200


def _repo_path(p: str) -> str | None:
    """Repo-relative path, or None for frames outside the repository."""
    if p.startswith("<") or "site-packages" in p or "/lib/python" in p:
        return None
    if p.startswith("/testbed/"):
        return p[len("/testbed/"):]
    return None if p.startswith("/") else p


def statuses(output: str) -> dict[str, tuple[str, str]]:
    """{node_id: (STATUS, short message)} from the -rA summary."""
    out, in_summary = {}, False
    for line in output.splitlines():
        if _SECTION.match(line):
            in_summary = "short test summary" in line
            continue
        if in_summary:
            m = _STATUS.match(line)
            if m and "::" in m.group(2):
                out[m.group(2).strip()] = (m.group(1), (m.group(3) or "").strip())
    return out


def _sections(output: str) -> dict[str, str]:
    """{header: body} for every block in FAILURES and ERRORS."""
    blocks, cur, body, active = {}, None, [], False
    for line in output.splitlines():
        if _SECTION.match(line) or _END.match(line):
            if cur is not None:
                blocks[cur] = "\n".join(body)
            cur, body = None, []
            active = bool(re.search(r"FAILURES|ERRORS", line))
            continue
        if not active:
            continue
        h = _HEADER.match(line)
        if h and not _FRAME_SEP.match(line):
            if cur is not None:
                blocks[cur] = "\n".join(body)
            cur, body = h.group(1).strip(), []
        elif cur is not None:
            body.append(line)
    if cur is not None:
        blocks[cur] = "\n".join(body)
    return blocks


def _detail(body: str) -> dict:
    """message, raise location, repo call path and values from one failure block."""
    frames, values, messages = [], [], []
    for frame in re.split(r"\n(?:_ ){5,}_?\s*\n", "\n" + body):
        loc, locals_, emsgs = None, [], []
        for line in frame.splitlines():
            if line.startswith("E "):
                t = line[1:].strip()
                emsgs.append(t)
                fm = _FILE_LINE.search(t)                      # SyntaxError & co.
                if fm and _repo_path(fm.group(1)):
                    loc = (_repo_path(fm.group(1)), int(fm.group(2)))
                if t.lstrip("+ ").startswith("where"):
                    values.append(t.lstrip("+ ").strip())
                continue
            m = _LOC.match(line)
            if m and _repo_path(m.group(1)):
                loc = (_repo_path(m.group(1)), int(m.group(2)))
                continue
            lm = _LOCAL.match(line)
            if lm and lm.group(1) not in ("self", "cls") and " at 0x" not in lm.group(2):
                v = lm.group(2).strip()
                locals_.append(f"{lm.group(1)} = {v[:MAX_VALUE]}{'...' if len(v) > MAX_VALUE else ''}")
        if loc:
            frames.append(f"{loc[0]}:{loc[1]}")
            values.extend(v for v in locals_ if v not in values)
        if emsgs:
            messages = emsgs
    # The error line plus its continuation: numpy's assert_allclose, pytest's
    # string/list diffs and similar put expected-vs-actual on the lines AFTER
    # "AssertionError:". `where ...` introspection is rung 4's, not rung 3's.
    exc = re.compile(r"^[A-Za-z_][\w.]*(Error|Exception|Warning|Exit|Interrupt)\b")
    idx = next((k for k in range(len(messages) - 1, -1, -1) if exc.match(messages[k])), 0 if messages else None)
    if idx is None:
        msg = ""
    else:
        cont = [m for m in messages[idx + 1:] if m.strip() and not m.lstrip("+ ").startswith("where")]
        msg = "\n".join([messages[idx].rstrip()] + cont)
    path, line = (frames[-1].rsplit(":", 1) if frames else (None, None))
    return {"message": msg, "path": path, "lineno": int(line) if line else None,
            "frames": list(dict.fromkeys(frames)), "values": values}


def _key(node_id: str) -> str:
    """Node id -> the name pytest prints in a section header."""
    return node_id.split("::", 1)[1].replace("::", ".") if "::" in node_id else node_id


def parse(output: str, relevant: list[str], status_parser=None) -> CheckResult:
    """CheckResult over the task's tests only (FAIL_TO_PASS + PASS_TO_PASS).

    status_parser: the official SWE-bench log parser for the task (the dataset's
    `log_parser`). Pass it whenever available: it decides pass/fail exactly as
    scoring will. It also truncates test ids at the first space — SWE-bench's
    FAIL_TO_PASS/PASS_TO_PASS ids are truncated the same way — so matching
    against the dataset's ids only works with the official parser.
    """
    own = statuses(output)
    if status_parser is not None:
        from swebench.harness.grading import _resolve_case
        sm = status_parser(output, None)
    else:
        sm, _resolve_case = {k: v[0] for k, v in own.items()}, None

    def resolve(nid):
        """(status, full id) exactly as official grading resolves the dataset's id.

        676 SWE-bench Verified ids are truncated mid-parameter (SWE-bench #290);
        grading prefix-matches those when the candidates agree on pass/fail, and
        treats ambiguous ones as not passing. We use the same function.
        """
        key = _resolve_case(nid, sm) if _resolve_case else (nid if nid in sm else None)
        return (sm[key], key) if key else ("NOT RUN", nid)
    blocks = _sections(output)
    by_name = {}
    for header, body in blocks.items():
        name = re.sub(r"^ERROR at (setup|teardown) of ", "", header)
        by_name.setdefault(name, body)

    def body_for(nid):
        key = _key(nid)
        if key in by_name:
            return by_name[key]
        # a dataset id truncated at a space: match the full name by prefix
        return next((b for n, b in by_name.items() if n.startswith(key)), None)
    collect = {h[len("ERROR collecting "):].strip(): b for h, b in blocks.items() if h.startswith("ERROR collecting ")}

    res = CheckResult()
    for nid in relevant:
        status, full = resolve(nid)
        short = own.get(full, ("", ""))[1]
        if status in PASS:
            res.passed += 1
            continue
        res.failed += 1
        body = body_for(full)
        if body is None:                                   # never ran: collection error in its file
            f = nid.split("::")[0]
            body = collect.get(f) or next(iter(collect.values()), "")
        d = _detail(body) if body else {"message": short, "path": None, "lineno": None, "frames": [], "values": []}
        if not d["message"]:
            d["message"] = short or ("not run: the test file failed to load" if status == "NOT RUN" else status)
        res.failures.append({"test": nid, "status": status, **d})
    return res
