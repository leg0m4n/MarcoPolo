import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo import sandbox  # noqa: E402
from marcopolo.leakcheck import added_lines, leaking_files, patch_files  # noqa: E402

GOLD = """diff --git a/pkg/mod.py b/pkg/mod.py
--- a/pkg/mod.py
+++ b/pkg/mod.py
@@ -1,4 +1,5 @@
 def f(x):
-    return compute_the_old_way(x, flag=True)
+    return compute_the_old_way(x, flag=True)
+    result = compute_the_new_way(x, strict=False)
+    y = 1
+    return normalise_everything(result, axis=-1)
diff --git a/pkg/new.py b/pkg/new.py
new file mode 100644
--- /dev/null
+++ b/pkg/new.py
@@ -0,0 +1 @@
+HELPER_CONSTANT_FOR_THE_NEW_CODE = 42
diff --git a/pkg/gone.py b/pkg/gone.py
deleted file mode 100644
--- a/pkg/gone.py
+++ /dev/null
@@ -1 +0,0 @@
-x = 1
"""


def test_every_container_is_offline_and_unprivileged():
    for args in (sandbox.HARDEN, sandbox.AGENT_RUN_ARGS):
        assert args[args.index("--network") + 1] == "none"
        assert args[args.index("--cap-drop") + 1] == "ALL"
        assert "no-new-privileges" in args
    assert sandbox.AGENT_RUN_ARGS[sandbox.AGENT_RUN_ARGS.index("--user") + 1] == sandbox.AGENT_USER != "root"


def test_evaluator_loses_sys_admin_and_network():
    stock = {"image": "img", "name": "sweb.eval.x", "user": "root", "cap_add": ["SYS_ADMIN"], "detach": True}
    out = sandbox.harden_evaluator_create(stock)
    assert "cap_add" not in out
    assert out["network_mode"] == "none" and out["cap_drop"] == ["ALL"]
    assert out["user"] == "root" and out["image"] == "img", "the rest of the evaluator is untouched"
    assert out["mem_limit"] == sandbox.MEMORY and out["pids_limit"] == sandbox.PIDS


def test_patch_files_are_post_images_without_deletions():
    assert patch_files(GOLD) == ["pkg/mod.py", "pkg/new.py"]


def test_added_lines_skip_short_and_moved_lines():
    assert added_lines(GOLD) == ["result = compute_the_new_way(x, strict=False)",
                                 "return normalise_everything(result, axis=-1)",
                                 "HELPER_CONSTANT_FOR_THE_NEW_CODE = 42"]


LINES = ["line one of the fix, long enough", "line two of the fix, long enough",
         "line three of the fix, long enough", "a line the source already has"]
TRACKED = {"/testbed/pkg/other.py"}


def test_a_copy_of_the_fix_elsewhere_is_a_leak():
    hits = [("/opt/site-packages/pkg/mod.py", LINES[0]), ("/opt/site-packages/pkg/mod.py", LINES[1]),
            ("/testbed/pkg/other.py", LINES[3])]
    distinctive, files = leaking_files(hits, TRACKED, LINES)
    assert LINES[3] not in distinctive, "a line the task's own source has proves nothing"
    assert list(files) == ["/opt/site-packages/pkg/mod.py"]


def test_one_coincidental_line_is_not_a_leak():
    hits = [("/usr/lib/python3/something.py", LINES[0])]
    assert leaking_files(hits, TRACKED, LINES)[1] == {}


def test_nothing_found_nothing_flagged():
    assert leaking_files([], TRACKED, LINES)[1] == {}
    assert leaking_files([], TRACKED, [])[1] == {}
