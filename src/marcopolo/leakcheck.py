"""Before the agent's first command: is the real fix findable anywhere in its container?

SWE-bench builds each image from the repository's full history and resets it to
the commit before the fix. If a later commit survives (a branch, a tag, a
reflog entry, an unreachable object in a pack), or a newer release of the
package sits in site-packages, the agent could read the answer instead of
finding it. This checks every run's container, since images are re-pulled.

Three tests, each against the task's gold patch (which never enters the
container: the patterns arrive on stdin and nothing is written):

  future commits  every commit object in the repository's database, reachable
                  or not, that is not in HEAD's history and is dated after the
                  base commit
  fixed files     the exact contents of each file after the fix (computed on
                  the host), looked up as a git object in every repository on
                  the filesystem
  fix lines       the lines the fix adds that the task's own source does not
                  already contain, searched for across the whole filesystem; a
                  file holding at least half of them is a leak

A leak makes the run invalid and parks it; nothing is scored.
"""
from __future__ import annotations

import io
import math
import subprocess
import tarfile
import tempfile
from pathlib import Path

MIN_LINE = 20   # shorter added lines ("return x", "else:") are too common to mean anything
TOP_EXCLUDE = {"proc", "sys", "dev"}


class TaskLeak(RuntimeError):
    """The task's real fix is readable from inside the agent's container."""


def _exec(container, script, input=None, timeout=300):
    return subprocess.run(["docker", "exec", "-i", "-u", "root", "-w", "/testbed", container, "bash", "-c", script],
                          input=input, capture_output=True, timeout=timeout)


def patch_files(patch: str) -> list[str]:
    """Paths the patch leaves behind (post-image), excluding deletions."""
    out = []
    for line in patch.splitlines():
        if line.startswith("+++ ") and line[4:].strip() != "/dev/null":
            p = line[4:].strip()
            out.append(p[2:] if p.startswith("b/") else p)
    return out


def added_lines(patch: str) -> list[str]:
    """Distinct, stripped lines the patch adds and does not also remove."""
    added, removed = [], set()
    for line in patch.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:].strip())
        elif line.startswith("-") and not line.startswith("---"):
            removed.add(line[1:].strip())
    seen, out = set(), []
    for s in added:
        if len(s) >= MIN_LINE and s not in removed and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def leaking_files(hits: list[tuple[str, str]], tracked: set[str], lines: list[str]) -> tuple[list[str], dict]:
    """(distinctive lines, {file: lines found}) from grep hits (file, matched line).

    A line already in the task's tracked source is not evidence of anything (the
    fix may reuse it), so it is dropped. A file is a leak if it holds at least
    half of the remaining lines.
    """
    in_source = {m for f, m in hits if f in tracked}
    distinctive = [l for l in lines if l not in in_source]
    if not distinctive:
        return distinctive, {}
    need = max(1, math.ceil(len(distinctive) / 2))
    per_file: dict[str, set] = {}
    for f, m in hits:
        if f not in tracked and m in distinctive:
            per_file.setdefault(f, set()).add(m)
    return distinctive, {f: sorted(ms) for f, ms in per_file.items() if len(ms) >= need}


def fixed_blobs(container: str, patch: str) -> dict[str, str]:
    """{path: git blob id} of each file as the gold patch leaves it. Computed on the host."""
    files = patch_files(patch)
    if not files:
        return {}
    listed = _exec(container, 'git ls-tree -r --name-only HEAD --' + "".join(f" '{f}'" for f in files))
    existing = [f for f in listed.stdout.decode().splitlines() if f]
    with tempfile.TemporaryDirectory() as d:
        if existing:
            tar = _exec(container, "git archive HEAD -- " + " ".join(f"'{f}'" for f in existing))
            with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as t:
                t.extractall(d, filter="data")
        r = subprocess.run(["git", "apply", "--whitespace=nowarn", "-"], cwd=d, input=patch.encode(),
                           capture_output=True)
        if r.returncode:
            raise RuntimeError(f"gold patch does not apply to the image's HEAD: {r.stderr.decode()[-300:]}")
        out = {}
        for f in files:
            p = Path(d, f)
            if p.is_file():
                out[f] = subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                                        text=True, check=True).stdout.strip()
        return out


FUTURE_COMMITS = r"""
base_ct=$(git log -1 --format=%ct "$1")
stray=$(git cat-file --batch-all-objects --batch-check='%(objecttype) %(objectname)' | awk '$1=="commit"{print $2}' \
  | sort | comm -23 - <(git rev-list HEAD | sort))
# (guarded: with no revisions, `git log --stdin` would show HEAD)
[ -n "$stray" ] && printf '%s\n' "$stray" | git log --no-walk --stdin --format='%H %ct %s' | awk -v b="$base_ct" '$2 > b'
exit 0
"""

# a fixed blob inside HEAD's own history is not a leak (the fix may restore an old version)
IN_HISTORY = r"""
git rev-list --objects HEAD | awk '{print $1}' | grep -xF -f /dev/stdin
"""

BLOBS_ANYWHERE = r"""
shas=$(cat)
find / -xdev -name .git -type d 2>/dev/null | while read -r g; do
  printf '%s\n' "$shas" | git -c safe.directory='*' --git-dir="$g" cat-file --batch-check 2>/dev/null \
    | awk -v g="$g" '$2!="missing"{print g, $1}'
done
"""

GREP_EVERYWHERE = r"""
cd / && grep -rIFoH -f /dev/stdin $(ls -A / | grep -vxE 'proc|sys|dev') 2>/dev/null | sort -u
"""


def check(container: str, instance: dict) -> dict:
    """Report on the container as the agent will first see it. report['leak'] is the verdict."""
    patch = instance["patch"]
    rep: dict = {}

    fut = _exec(container, f"set -- '{instance['base_commit']}'\n{FUTURE_COMMITS}")
    rep["future_commits"] = [l for l in fut.stdout.decode().splitlines() if l][:20]

    blobs = set(fixed_blobs(container, patch).values())
    found = [l.split() for l in _exec(container, BLOBS_ANYWHERE, input="\n".join(blobs).encode())
             .stdout.decode().splitlines() if l.strip()]
    if found:
        own = set(_exec(container, IN_HISTORY, input="\n".join(blobs).encode(), timeout=900)
                  .stdout.decode().split())
        found = [(g, sha) for g, sha in found if not (g == "/testbed/.git" and sha in own)]
    rep["fixed_files_found"] = [f"{g} {sha}" for g, sha in found]

    lines = added_lines(patch)
    hits = []
    if lines:
        out = _exec(container, GREP_EVERYWHERE, input="\n".join(lines).encode()).stdout.decode(errors="replace")
        for row in out.splitlines():
            f, _, m = row.partition(":")
            hits.append(("/" + f, m))
    tracked = {"/testbed/" + p for p in
               _exec(container, "git ls-files").stdout.decode(errors="replace").splitlines()}
    distinctive, files = leaking_files(hits, tracked, lines)
    rep["fix_lines"] = len(lines)
    rep["fix_lines_distinctive"] = len(distinctive)
    rep["fix_lines_found_in"] = files

    rep["leak"] = bool(rep["future_commits"] or rep["fixed_files_found"] or files)
    return rep
