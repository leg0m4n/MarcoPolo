# Item 43

**Repository:** pylint-dev/pylint  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** tests/unittest_pyreverse_writer.py

## The issue

Use Python type hints for UML generation
It seems that pyreverse does not read python type hints (as defined by [PEP 484](https://www.python.org/dev/peps/pep-0484/)), and this does not help when you use `None` as a default value :

### Code example
```
class C(object):
    def __init__(self, a: str = None):
        self.a = a
```

### Current behavior

Output of pyreverse :

![classes_test](https://user-images.githubusercontent.com/22218701/27432305-f10fe03e-574f-11e7-81fa-e2b59e493360.png)

### Expected behavior

I would like to see something like : `a : String` in the output.

### pylint --version output
pylint-script.py 1.6.5,
astroid 1.4.9
Python 3.6.0 |Anaconda custom (64-bit)| (default, Dec 23 2016, 11:57:41) [MSC v.1900 64 bit (AMD64)]



## The agent's commands, in order (137; outputs omitted)

1. `ls -la`
2. `find pylint -type f -name "*.py" | head -20`
3. `grep -r "pyreverse" --include="*.py" . | head -20`
4. `ls -la pylint/pyreverse/`
5. `cd /testbed && python -m pytest --version 2>&1 || echo "pytest not installed"`
6. `cat tox.ini`
7. `ls -la | grep -E "check|run"`
8. `cat .pre-commit-config.yaml`
9. `find . -type f -name "check" 2>/dev/null`
10. `ls -la script/`
11. `find .github -type f -name "*.yml" -o -name "*.yaml" | head -5`
12. `cat .github/workflows/ci.yaml`
13. `find . -type f -name "check" 2>/dev/null -o -name "check.py" 2>/dev/null`
14. `ls -la | grep -i make`
15. `cat setup.cfg`
16. `which check`
17. `file /usr/local/bin/check`
18. `head -c 100 /usr/local/bin/check`
19. `check 2>&1 | head -30`
20. `check 2>&1 | tail -30`
21. `python -m pytest --version 2>&1 || pip install pytest -q`
22. `check 2>&1 | tee /tmp/check_output.txt | head -100`
23. `grep -A 5 -B 5 "FAILED" /tmp/check_output.txt | head -80`
24. `tail -200 /tmp/check_output.txt`
25. `cat /tmp/.mp_check_out 2>/dev/null | head -200`
26. `sed -n '1,200p' /usr/local/bin/check`
27. `ls -la /testbed/`
28. `python -c "import sys; print(sys.executable)"`
29. `/opt/miniconda3/envs/testbed/bin/python -m pytest --version 2>&1`
30. `cat requirements_test.txt`
31. `ls -l /usr/local/bin/check`
32. `grep -r "mp_check" . 2>/dev/null | head -5`
33. `ls -la /testbed/venv 2>/dev/null || echo "no venv"`
34. `grep -A 10 "options.extras_require" /testbed/setup.cfg 2>/dev/null || echo "no extras"`
35. `cat requirements_test_min.txt`
36. `python -c "import pylint; print(pylint.__version__)" 2>&1`
37. `check > /dev/null 2>&1; sleep 2; cat /tmp/.mp_check_out 2>/dev/null | head -100`
38. `wc -l /tmp/.mp_check_out 2>/dev/null || echo "file not found"`
39. `grep -r "mp_check_out" . 2>/dev/null`
40. `pip install -r requirements_test_min.txt 2>&1 | tail -30`
41. `which python3`
42. `apt-get update 2>&1 | tail -5`
43. `conda list | grep pytest 2>/dev/null || echo "not in conda list"`
44. `cd /testbed && python -m pytest -v 2>&1 | head -200`
45. `python -c "import pytest; print(pytest.__version__)" 2>&1`
46. `conda env list`
47. `conda info --envs | grep testbed`
48. `conda prefix`
49. `conda info --base`
50. `/opt/miniconda3/envs/testbed/bin/python -c "import sys; print(sys.path)" | head -5`
51. `ls /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/ | grep pytest`
52. `which python3-system 2>/dev/null || echo "not found"`
53. `check 2>&1 ; echo "Exit code: $?"`
54. `grep -r "annotation" pylint/pyreverse/ --include="*.py"`
55. `cat pylint/pyreverse/utils.py`
56. `wc -l pylint/pyreverse/utils.py`
57. `sed -n '200,215p' pylint/pyreverse/utils.py`
58. `grep -r "def get_annotation" . --include="*.py" 2>/dev/null`
59. `grep -n "get_annotation" tests/unittest_pyreverse_writer.py`
60. `grep -n "get_annotation" pylint/pyreverse/utils.py`
61. `head -30 pylint/pyreverse/utils.py`
62. `cat pylint/pyreverse/utils.py | wc -c`
63. `cat pylint/pyreverse/__init__.py`
64. `grep -r "get_annotation" pylint/ --include="*.py" 2>/dev/null | head -20`
65. `sed -n '30,200p' tests/unittest_pyreverse_writer.py`
66. `grep -n "get_annotation" pylint/pyreverse/inspector.py`
67. `awk '/def get_annotation/ {print NR ": " $0}' pylint/pyreverse/utils.py`
68. `python -c "import pylint.pyreverse.utils; print(dir(pylint.pyreverse.utils))" 2>&1 | head -30`
69. `find pylint/pyreverse -name "*.py" -exec basename {} \;`
70. `tail -100 pylint/pyreverse/utils.py`
71. `grep -c "def " pylint/pyreverse/utils.py`
72. `grep "^def " pylint/pyreverse/utils.py`
73. `grep -r "def get_annotation" . --include="*.py" 2>/dev/null`
74. `grep -n "annotation" pylint/pyreverse/inspector.py`
75. `head -100 pylint/pyreverse/inspector.py`
76. `grep -n "instance_attrs_type" pylint/pyreverse/inspector.py`
77. `sed -n '140,250p' pylint/pyreverse/inspector.py`
78. `grep -n "annotation" pylint/pyreverse/inspector.py -i`
79. `grep -n "instance_attrs_type" pylint/pyreverse/diadefslib.py`
80. `sed -n '90,120p' pylint/pyreverse/diadefslib.py`
81. `grep -n "instance_attrs_type" pylint/pyreverse/writer.py`
82. `head -200 pylint/pyreverse/writer.py`
83. `grep -n "class.*ClassDiadef" pylint/pyreverse/diadefslib.py`
84. `sed -n '179,400p' pylint/pyreverse/diadefslib.py`
85. `grep -n "class DefaultDiadefGenerator" pylint/pyreverse/diadefslib.py`
86. `sed -n '124,178p' pylint/pyreverse/diadefslib.py`
87. `grep -n "class ClassDiagram" pylint/pyreverse/diagrams.py`
88. `sed -n '46,200p' pylint/pyreverse/diagrams.py`
89. `ls -l pylint/pyreverse/utils.py`
90. `grep -r "annotation" . --include="*.py" 2>/dev/null | grep -v ".pyc" | head -30`
91. `tail -200 pylint/pyreverse/inspector.py`
92. `cd /testbed && git grep -n "get_annotation" 2>/dev/null | head -20`
93. `grep -n "def infer_node" pylint/pyreverse/utils.py`
94. `grep -r "AnnAssign" . --include="*.py" 2>/dev/null | head -20`
95. `find tests -name "*.dot" -o -name "*.vcg" | head -10`
96. `head -30 tests/data/classes_No_Name.dot`
97. `find tests -type f -name "*.py" | xargs grep -l "attr : str" 2>/dev/null | head -5`
98. `grep -r "attr : str" . 2>/dev/null | head -5`
99. `find tests/regrtest_data -type f -name "*.py" | head -10`
100. `ls -la tests/regrtest_data/dataclasses_pyreverse/`
101. `cat tests/regrtest_data/dataclasses_pyreverse/__init__.py`
102. `ls -la tests/data/`
103. `cat tests/data/clientmodule_test.py`
104.
```
cd /testbed && cat > test_type_hints.py << 'EOF'
class C(object):
    def __init__(self, a: str = None):
        self.a = a
EOF
```
105. `cd /testbed && pyreverse -p test_type_hints -a -d output 2>&1 | head -30`
106. `cd /testbed && pyreverse --help 2>&1 | head -30`
107. `cd /testbed && rm -rf output && pyreverse -p test_type_hints -d output test_type_hints.py 2>&1 | tail -10`
108. `ls -la output/ 2>/dev/null || echo "no output"`
109. `find /testbed -name "*.dot" -type f 2>/dev/null | grep -v ".git" | head -10`
110. `cat /testbed/classes_test_type_hints.dot`
111. `grep -n "def get_annotation" pylint/pyreverse/utils.py 2>/dev/null || echo "not found"`
112. `grep -r "annotation" pylint/ --include="*.py" 2>/dev/null | grep -v ".pyc" | head -20`
113. `grep -r "AnnAssign" pylint/pyreverse/ 2>/dev/null`
114. `cd /testbed && git log --oneline -n 20 -- pylint/pyreverse/utils.py 2>/dev/null | head -10`
115. `grep -n "annotation" pylint/pyreverse/utils.py`
116. `find /testbed -type f -name "*.py" -exec grep -l "get_annotation" {} \; 2>/dev/null`
117. `sed -n '1,100p' tests/unittest_pyreverse_writer.py`
118. `grep -r "get_annotation" pylint/ --include="*.py" 2>/dev/null`
119. `find /opt/miniconda3/envs/testbed -name "pytest" -type d 2>/dev/null | head -5`
120. `ls /usr/local/lib/python3.9/dist-packages/ 2>/dev/null | grep pytest`
121. `ls -l /usr/local/bin/check`
122. `cat /usr/local/bin/check`
123. `grep -r "Optional" pylint/pyreverse/ 2>/dev/null`
124. `sed -n '200,400p' tests/unittest_pyreverse_writer.py`
125. `grep -n "def infer_node" tests/unittest_pyreverse_writer.py`
126. `grep -n "infer_node" pylint/pyreverse/utils.py 2>/dev/null`
127.
```
cd /testbed && python -c "
import astroid
node = astroid.extract_node('a: str = None')
print(type(node))
print(node.__class__.__name__)
print('annotation:', node.annotation)
print('value:', node.value)
print('target:', node.target)
"
```
128. `cd /testbed && git branch -a 2>&1 | head -20`
129. `pip install --user pytest 2>&1 | tail -10`
130. `tail -20 pylint/pyreverse/utils.py`
131. `head -30 pylint/pyreverse/inspector.py | grep import`
132. `cp pylint/pyreverse/utils.py pylint/pyreverse/utils.py.backup`
133. `tail -30 pylint/pyreverse/utils.py`
134.
```
cd /testbed && python3 -c "
import sys
with open('pylint/pyreverse/utils.py', 'r') as f:
    lines = f.readlines()
# Find the line number of the last line (before newline)
# We'll insert before the end of file (but after the last line)
# Actually we want to insert before the last line if it's empty? Let's just append after the class definition.
# We'll find the line index where the class ends (the …[cut]
```
135.
```
cd /testbed && python3 -c "
import astroid
code = '''
class C:
    def __init__(self, a: str = None):
        self.a = a
'''
tree = astroid.parse(code)
cls = tree.body[0]
for node in cls.body:
    if isinstance(node, astroid.FunctionDef):
        print('Function:', node.name)
        for arg in node.args.args:
            print('  arg:', arg.name, arg.annotation)
        for arg in node.args.poson …[cut]
```
136. `grep -r "\.annotation" pylint/ --include="*.py" | head -5`
137. `grep -n "annotation" pylint/checkers/utils.py -B2 -A2`

## The agent's last reasoning (last 3 turns)

```
Let's write a proper script in a file. But we can also use `sed` to append after the class definition. Let's find the line number of the end of LocalsVisitor. We can use `grep -n 'class LocalsVisitor' pylint/pyreverse/utils.py` and then find the next method after that. But time is limited. Let's take a different approach: we can edit the file using `apply_patch`? Not available. However, we can use `ed` with a script. Let's write a simple ed script to insert after the line containing "return None" that is preceded by a blank line and part of LocalsVisitor. We'll need to be careful. Given the time, I think we should directly edit the file using `cat >` with a heredoc, but we need to replace the whole file. That's risky. Maybe we can find a pre-existing implementation of `get_annotation` and `infer_node` from another branch (maybe in the upstream). Let's search the internet? Not possible. We need to think of another way: maybe the missing functions are not needed; the test is wrong and should be removed? But the issue is about type hints, not about missing functions. However, the test is part of the repository, so it must be fixed. We need to decide: we can comment out the test imports? That would make the tests pass but not solve the issue. However, the user wants type hints for UML generation, not just passing tests. So we must implement type hint support. Given the time constraints, I'm going to implement a minimal fix that at least makes the example work: we'll modify `inspector.py` to extract type hints from `AnnAssign` and function parameters and store them in `instance_attrs_type`. We'll also need to modify `get_attrs` to use those annotations instead of inferred values (maybe combine). We'll also need to implement `get_annotation` and `infer_node` as per test expectations, but we can stub them with minimal functionality that passes the tests (maybe they already pass? No, they are missing). We'll implement them with basic logic. Let's start by editing `inspector.py`. We'll add a visitor for `AnnAssign` and a method to store annotation. We'll also modify `visit_functiondef` to store parameter annotations. We'll need to know how to access parameter annotations in astroid. Let's write a small test to explore.
...
Interesting. The annotation is stored on `Arguments` nodes? Let's check astroid documentation. But we can look at the `pylint.checkers.utils` to see how they handle annotations. However, we can search for `annotation` in inspector.py to see if there is any existing handling. We need to get this done. Let's search for "annotation" in the whole pylint directory to see how they extract annotation nodes.
...
Look at `pylint/checkers/utils.py`. Let's examine that file.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/classes_test_type_hints.dot b/classes_test_type_hints.dot
new file mode 100644
index 00000000..15cf1dea
--- /dev/null
+++ b/classes_test_type_hints.dot
@@ -0,0 +1,5 @@
+digraph "classes_test_type_hints" {
+charset="utf-8"
+rankdir=BT
+"0" [label="{C|a : NoneType\l|}", shape="record"];
+}
diff --git a/pylint/pyreverse/utils.py.backup b/pylint/pyreverse/utils.py.backup
new file mode 100644
index 00000000..a24d227e
--- /dev/null
+++ b/pylint/pyreverse/utils.py.backup
@@ -0,0 +1,215 @@
+# Copyright (c) 2006, 2008, 2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
+# Copyright (c) 2014 Brett Cannon <brett@python.org>
+# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
+# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
+# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
+# Copyright (c) 2017, 2020 hippo91 <guillaume.peillex@gmail.com>
+# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
+# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
+# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
+# Copyright (c) 2020 yeting li <liyt@ios.ac.cn>
+# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
+# Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>
+# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>
+
+# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
+# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
+
+"""Generic classes/functions for pyreverse core/extensions. """
+import os
+import re
+import sys
+
+RCFILE = ".pyreverserc"
+
+
+def get_default_options():
+    """Read config file and return list of options."""
+    options = []
+    home = os.environ.get("HOME", "")
+    if home:
+        rcfile = os.path.join(home, RCFILE)
+        try:
+            with open(rcfile) as file_handle:
+                options = file_handle.read().split()
+        except OSError:
+            pass  # ignore if no config file found
+    return options
+
+
+def insert_default_options():
+    """insert default options to sys.argv"""
+    options = get_default_options()
+    options.reverse()
+    for arg in options:
+        sys.argv.insert(1, arg)
+
+
+# astroid utilities ###########################################################
+SPECIAL = re.compile(r"^__([^\W_]_*)+__$")
+PRIVATE = re.compile(r"^__(_*[^\W_])+_?$")
+PROTECTED = re.compile(r"^_\w*$")
+
+
+def get_visibility(name):
+    """return the visibility from a name: public, protected, private or special"""
+    if SPECIAL.match(name):
+        visibility = "special"
+    elif PRIVATE.match(name):
+        visibility = "private"
+    elif PROTECTED.match(name):
+        visibility = "protected"
+
+    else:
+        visibility = "public"
+    return visibility
+
+
+ABSTRACT = re.compile(r"^.*Abstract.*")
+FINAL = re.compile(r"^[^\W\da-z]*$")
+
+
+def is_abstract(node):
+    """return true if the given class node correspond to an abstract class
+    definition
+    """
+    return ABSTRACT.match(node.name)
+
+
+def is_final(node):
+    """return true if the given class/function node correspond to final
+    definition
+    """
+    return FINAL.match(node.name)
+
+
+def is_interface(node):
+    # bw compat
+    return node.type == "interface"
+
+
+def is_exception(node):
+    # bw compat
+    return node.type == "exception"
+
+
+# Helpers #####################################################################
+
+_CONSTRUCTOR = 1
+_SPECIAL = 2
+_PROTECTED = 4
+_PRIVATE = 8
+MODES = {
+    "ALL": 0,
+    "PUB_ONLY": _SPECIAL + _PROTECTED + _PRIVATE,
+    "SPECIAL": _SPECIAL,
+    "OTHER": _PROTECTED + _PRIVATE,
+}
+VIS_MOD = {
+    "special": _SPECIAL,
+    "protected": _PROTECTED,
+    "private": _PRIVATE,
+    "public": 0,
+}
+
+
+class FilterMixIn:
+    """filter nodes according to a mode and nodes' visibility"""
+
+    def __init__(self, mode):
+        "init filter modes"
+        __mode = 0
+        for nummod in mode.split("+"):
+            try:
+                __mode += MODES[nummod]
+            except KeyError as ex:
+                print("Unknown filter mode %s" % ex, file=sys.stderr)
+        self.__mode = __mode
+
+    def show_attr(self, node):
+        """return true if the node should be treated"""
+        visibility = get_visibility(getattr(node, "name", node))
+        return not self.__mode & VIS_MOD[visibility]
+
+
+class ASTWalker:
+    """a walker visiting a tree in preorder, calling on the handler:
+
+    * visit_<class name> on entering a node, where class name is the class of
+    the node in lower case
+
+    * leave_<class name> on leaving a node, where class name is the class of
+    the node in lower case
+    """
+
+    def __init__(self, handler):
+        self.handler = handler
+        self._cache = {}
+
+    def walk(self, node, _done=None):
+        """walk on the tree from <node>, getting callbacks from handler"""
+        if _done is None:
+            _done = set()
+        if node in _done:
+            raise AssertionError((id(node), node, node.parent))
+        _done.add(node)
+        self.visit(node)
+        for child_node in node.get_children():
+            assert child_node is not node
+            self.walk(child_node, _done)
+        self.leave(node)
+        assert node.parent is not node
+
+    def get_callbacks(self, node):
+        """get callbacks from handler for the visited node"""
+        klass = node.__class__
+        methods = self._cache.get(klass)
+        if methods is None:
+            handler = self.handler
+            kid = klass.__name__.lower()
+            e_method = getattr(
+                handler, "visit_%s" % kid, getattr(handler, "visit_default", None)
+            )
+            l_method = getattr(
+                handler, "leave_%s" % kid, getattr(handler, "leave_default", None)
+            )
+            self._cache[klass] = (e_method, l_method)
+        else:
+            e_method, l_method = methods
+        return e_method, l_method
+
+    def visit(self, node):
+        """walk on the tree from <node>, getting callbacks from handler"""
+        method = self.get_callbacks(node)[0]
+        if method is not None:
+            method(node)
+
+    def leave(self, node):
+        """walk on the tree from <node>, getting callbacks from handler"""
+        method = self.get_callbacks(node)[1]
+        if method is not None:
+            method(node)
+
+
+class LocalsVisitor(ASTWalker):
+    """visit a project by traversing the locals dictionary"""
+
+    def __init__(self):
+        ASTWalker.__init__(self, self)
+        self._visited = set()
+
+    def visit(self, node):
+        """launch the visit starting from the given node"""
+        if node in self._visited:
+            return None
+
+        self._visited.add(node)
+        methods = self.get_callbacks(node)
+        if methods[0] is not None:
+            methods[0](node)
+        if hasattr(node, "locals"):  # skip Instance and other proxy
+            for local_node in node.values():
+                self.visit(local_node)
+        if methods[1] is not None:
+            return methods[1](node)
+        return None
diff --git a/test_type_hints.py b/test_type_hints.py
new file mode 100644
index 00000000..a90f4b2d
--- /dev/null
+++ b/test_type_hints.py
@@ -0,0 +1,3 @@
+class C(object):
+    def __init__(self, a: str = None):
+        self.a = a

```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
