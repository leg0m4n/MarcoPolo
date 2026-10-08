# Item 65

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



## The agent's commands, in order (110; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed`
3. `find /testbed/pylint -type f -name "*pyreverse*" | head -30`
4. `grep -r "pyreverse" /testbed --include="*.py" | head -20`
5. `ls -la /testbed/pylint/pyreverse/`
6. `cat /testbed/pylint/pyreverse/inspector.py | head -200`
7. `cat /testbed/pylint/pyreverse/utils.py`
8. `grep -r "get_annotation" /testbed/pylint/pyreverse/`
9. `grep -n "get_annotation" /testbed/tests/unittest_pyreverse_writer.py`
10. `find /testbed/pylint -name "utils.py" -type f`
11. `grep -n "get_annotation" /testbed/pylint/utils/utils.py`
12. `grep -n "get_annotation" /testbed/pylint/lint/utils.py`
13. `grep -A 20 -B 5 "def get_annotation" /testbed/pylint/pyreverse/utils.py`
14. `cat /testbed/pylint/pyreverse/__init__.py`
15. `sed -n '200,500p' /testbed/pylint/pyreverse/inspector.py`
16. `grep -r "def infer_node" /testbed/pylint/`
17. `wc -l /testbed/pylint/pyreverse/utils.py`
18. `cat /testbed/pylint/pyreverse/utils.py | tail -200`
19. `grep -r "def get_annotation" /testbed/`
20. `head -40 /testbed/tests/unittest_pyreverse_writer.py`
21. `grep -r "from .*utils import" /testbed/pylint/pyreverse/`
22. `cd /testbed && python -m pytest --version 2>&1 | head -5`
23. `ls -la /testbed/ | grep -i check`
24. `find /testbed -name "check" -type f`
25. `cat /testbed/setup.cfg`
26. `pip list | grep -i pytest`
27. `grep -r "^check$" /testbed/`
28. `ls -la /testbed/.github/`
29. `ls -la /testbed/.github/workflows/`
30. `cat /testbed/.github/workflows/ci.yaml`
31. `ls -la /testbed/ | grep check`
32. `cat /testbed/.pre-commit-config.yaml | head -50`
33. `grep -r "check" /testbed/setup.py`
34. `ls -la /testbed/script/`
35. `ls -la /testbed/Makefile 2>/dev/null || echo "no Makefile"`
36. `grep -r "annotation" /testbed/pylint/pyreverse/ --include="*.py"`
37. `grep -r "type" /testbed/pylint/pyreverse/ --include="*.py" | head -20`
38. `cat /testbed/pylint/pyreverse/writer.py | head -200`
39. `cat /testbed/pylint/pyreverse/diadefslib.py | head -300`
40. `cat /testbed/pylint/pyreverse/diagrams.py | head -400`
41.
```
cd /testbed && cat > test_type_hints.py << 'EOF'
class C(object):
    def __init__(self, a: str = None):
        self.a = a
EOF
```
42. `cd /testbed && python -m pylint.pyreverse test_type_hints.py 2>&1`
43. `cat /testbed/pylint/pyreverse/main.py`
44. `cd /testbed && python -m pylint.pyreverse.main test_type_hints.py 2>&1 | head -30`
45. `cd /testbed && ls -la *.dot 2>/dev/null || echo "no dot file"`
46. `cat /testbed/classes.dot`
47. `grep -r "get_annotation" /testbed/pylint/ 2>/dev/null | head -20`
48. `grep -r "def get_annotation" /testbed/ 2>/dev/null`
49. `cat /testbed/pylint/pyreverse/utils.py | wc -l`
50. `tail -50 /testbed/pylint/pyreverse/utils.py`
51. `grep -r "infer_node" /testbed/pylint/ 2>/dev/null | head -10`
52. `cat /testbed/pylint/pyreverse/__init__.py`
53. `cd /testbed && git status`
54. `cd /testbed && python -m pytest tests/ -xvs -k pyreverse 2>&1 | head -100`
55. `which pytest`
56. `cd /testbed && python -m pytest --version 2>&1 | head -5`
57. `pip list | grep -i pytest 2>&1`
58. `cd /testbed && pytest --version 2>&1`
59. `find /testbed -type f -name "check" -executable 2>/dev/null`
60. `cd /testbed && python setup.py test 2>&1 | head -30`
61. `pip install pytest -q 2>&1 | tail -5`
62. `find / -name "check" -type f -executable 2>/dev/null | grep -v proc | head -5`
63. `cat /usr/local/bin/check | head -30`
64. `cd /testbed && check 2>&1`
65. `cat /tmp/.mp_check_out 2>/dev/null | head -30`
66. `python -c "import sys; print(sys.path)"`
67. `python -c "import pytest; print(pytest.__version__)" 2>&1`
68. `which python`
69. `cat /usr/local/bin/check | wc -l`
70. `cat /usr/local/bin/check`
71. `grep -r "mp_check" /testbed/ 2>/dev/null`
72. `sed -n '148,182p' /testbed/tests/unittest_pyreverse_writer.py`
73. `sed -n '182,210p' /testbed/tests/unittest_pyreverse_writer.py`
74. `grep -r "get_annotation\|infer_node" /testbed/pylint --include="*.py" 2>/dev/null | grep -v test`
75. `head -40 /testbed/tests/unittest_pyreverse_writer.py | grep -A5 -B5 "import"`
76. `cd /testbed && python -m unittest tests.unittest_pyreverse_writer 2>&1 | head -50`
77. `grep -n "annotation" /testbed/pylint/pyreverse/inspector.py`
78. `grep -r "get_annotation" /testbed/ 2>/dev/null | head -30`
79.
```
cd /testbed && cat > explore_ast.py << 'EOF'
import astroid
code = """
class C(object):
    def __init__(self, a: str = None):
        self.a = a
"""
tree = astroid.parse(code)
class_node = tree.body[0]
print("Class:", class_node.name)
init = class_node.body[0]
print("Method:", init.name)
print("Args:", init.args)
for arg in init.args.args:
    print("  Arg:", arg.name, "annotation:", arg.annotati …[cut]
```
80. `sed -n '150,250p' /testbed/pylint/pyreverse/inspector.py`
81. `cat /testbed/pylint/pyreverse/utils.py | tail -30`
82. `cd /testbed && cp pylint/pyreverse/utils.py pylint/pyreverse/utils.py.backup`
83.
```
cd /testbed && cat >> pylint/pyreverse/utils.py << 'EOF'

# type hint utilities
import astroid

def get_annotation(node):
    """Return the annotation node for the given node.
    
    For AnnAssign nodes, returns node.annotation.
    For AssignAttr nodes, returns the annotation of the value being assigned,
    if the value is a Name that has an annotation in its enclosing scope.
    Otherwise ret …[cut]
```
84. `grep -B 20 "def test_get_annotation_annassign" /testbed/tests/unittest_pyreverse_writer.py`
85.
```
cd /testbed && cat > inspect_annotation.py << 'EOF'
import astroid
from pylint.pyreverse.utils import get_annotation, infer_node

# Test AnnAssign
code = "a: str = None"
node = astroid.extract_node(code)
print("Node type:", type(node))
print("Node annotation:", node.annotation)
print("Node value:", node.value)
print("Node value type:", type(node.value))
print("Calling get_annotation(node.value):", …[cut]
```
86. `cd /testbed && python -c "import astroid; node = astroid.extract_node('Optional[str]'); print(type(node)); print(dir(node))" 2>&1 | head -30`
87. `cd /testbed && git grep -r "get_annotation" -- "*.py" 2>/dev/null | head -20`
88. `grep -n "def get_annotation" /testbed/pylint/pyreverse/utils.py`
89. `wc -l /testbed/pylint/pyreverse/utils.py`
90. `sed -n '215,240p' /testbed/pylint/pyreverse/utils.py`
91. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -10`
92. `ls -la /tmp/.mp_check_out 2>/dev/null | head -5`
93. `cat /testbed/tox.ini`
94. `cat /testbed/requirements_test.txt`
95. `conda list 2>&1 | head -20`
96. `python -c "import sys; print(sys.executable)"`
97. `find /opt/miniconda3/envs/testbed -name "pytest" -type f 2>/dev/null | head -5`
98. `cd /testbed && cp pylint/pyreverse/utils.py pylint/pyreverse/utils.py.new`
99. `sed -n '220,260p' /testbed/pylint/pyreverse/utils.py`
100.
```
cd /testbed && cat > /tmp/replace_utils.py << 'EOF'
import sys
import astroid

def _get_annotation_of_name(name_node):
    """Given an astroid.Name node, return its annotation if it's a function
    parameter, else None."""
    # Walk up to find the enclosing FunctionDef
    node = name_node.parent
    while node is not None:
        if isinstance(node, astroid.FunctionDef):
            # Look for …[cut]
```
101. `cd /testbed && wc -l pylint/pyreverse/utils.py`
102. `cd /testbed && head -219 pylint/pyreverse/utils.py > /tmp/utils_new.py`
103. `head -30 /testbed/pylint/pyreverse/utils.py`
104. `grep -n "import astroid" /testbed/pylint/pyreverse/utils.py`
105. `sed -n '210,230p' /testbed/pylint/pyreverse/utils.py`
106.
```
cd /testbed && cat > /tmp/update_utils.py << 'EOF'
import sys

with open('pylint/pyreverse/utils.py', 'r') as f:
    lines = f.readlines()

# Find the line where import astroid appears (should be line 218)
import_line = None
for i, line in enumerate(lines):
    if line.strip() == 'import astroid':
        import_line = i
        break

if import_line is None:
    # Should not happen
    print('Cou …[cut]
```
107. `tail -80 /testbed/pylint/pyreverse/utils.py`
108. `cd /testbed && python -c "from pylint.pyreverse.utils import get_annotation, infer_node; print('imported')" 2>&1`
109.
```
cd /testbed && cat > /tmp/test_functions.py << 'EOF'
import astroid
from pylint.pyreverse.utils import get_annotation, infer_node

print("Testing get_annotation on AnnAssign...")
# Test cases from test_get_annotation_annassign
test_cases = [
    ("a: str = None", "Optional[str]"),
    ("a: str = 'mystr'", "str"),
    ("a: Optional[str] = 'str'", "Optional[str]"),
    ("a: Optional[str] = None", "O …[cut]
```
110. `cd /testbed && cp pylint/pyreverse/inspector.py pylint/pyreverse/inspector.py.backup`

## The agent's last reasoning (last 3 turns)

```
We have duplicate import astroid lines and duplicate "# type hint utilities". That's fine. However, note that `get_annotation` references `_get_annotation_of_name` which is defined after it (that's okay because Python reads the whole file before execution). However, we have a circular import? Not. Now we need to test our functions with the test expectations. Let's write a small script that imports them and runs the test logic. But first, we need to ensure that the functions are importable. Let's try to import them in a Python shell.
...
Great. Now let's write a script that runs the test logic and see what we get. We'll create a script that replicates the test expectations and prints the results.
...
We see two issues: 1. For the first case `a: str = None`, the result.name is `str` but expected `Optional[str]`. That's because our `get_annotation` returns the annotation `str` (correct), but the test expects `Optional[str]`. That indicates that the test expects the annotation to be `Optional[str]` when default is `None`. That suggests that `get_annotation` should adjust the annotation based on default value. Indeed, the test includes that expectation. 2. For `Optional[str]` annotation, the result is a `Subscript` node which doesn't have a `.name` attribute. The test expects `.name` to be `"Optional[str]"`. That suggests that the test expects a different kind of node (maybe a custom object). This is puzzling. Maybe the test is using a mock? But they are not. However, note that the test imports `get_annotation` from `pylint.pyreverse.utils`. That means the actual `get_annotation` function (which we are implementing) must return something that has a `.name` attribute equal to the label. That could be an `astroid.Name` for simple types, but for `Optional[str]` they might have a custom class? Let's examine the test more: they also have `Optional[str]` as a label. The annotation node in AST is a `Subscript`. The `.name` attribute of a `Subscript` is not present. However, maybe they are using `result.as_string()`? No, they call `.name`. Could be a mistake in the test? But we cannot change the test. We need to see what the actual `get_annotation` function in the original codebase returns. Since we can't see it, we can infer from the test that `get_annotation` returns a node that has a `.name` attribute. That could be an `astroid.Name` for simple types, and for `Optional[str]` they might have a different representation (maybe they return `Optional[str]` as a string?). But they call `.name` on the return value, so it must be an object with a `name` attribute. Let's search for any usage of `.name` in the pyreverse source to see what kind of objects have a `.name` attribute. For example, `astroid.Name` has a `.name` attribute. `astroid.Subscript` does not. So maybe the test expects `get_annotation` to return an `astroid.Name` even for `Optional[str]`? That would be wrong. Alternatively, maybe the test is checking `got = get_annotation(node.value).name` where `get_annotation` returns a tuple or something? Let's look at the test for assignattr: they expect `Optional[str]` as label, and they also call `.name`. So same issue. Given the time, we need to think of a pragmatic solution: we can modify our `get_annotation` to return an object that has a `.name` attribute equal to the label string. That could be a simple class that mimics an AST node but with a `.name` attribute. However, the test also uses `get_annotation` in `infer_node` where they mock it to return `None`. That's fine. But we also need to integrate with the rest of the code. The inspector uses `infer_node`? Actually the inspector uses `node.infer()`. We need to modify the inspector to use `infer_node` for `instance_attrs_type` and `locals_type`. However, we cannot change the inspector's usage because `infer_node` is not used anywhere. We could change the inspector to use `infer_node` (or `get_annotation`) but that would be a larger change. Given the complexity, perhaps we should foc
…[cut, 6784 more chars]
```

## Final state of the repository (git diff vs the starting commit)

### Test files (shown in full)

```diff
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

### All other files

```diff
diff --git a/classes.dot b/classes.dot
new file mode 100644
index 00000000..b9fbf89b
--- /dev/null
+++ b/classes.dot
@@ -0,0 +1,5 @@
+digraph "classes" {
+charset="utf-8"
+rankdir=BT
+"0" [label="{C|a : NoneType\l|}", shape="record"];
+}
diff --git a/explore_ast.py b/explore_ast.py
new file mode 100644
index 00000000..91d56374
--- /dev/null
+++ b/explore_ast.py
@@ -0,0 +1,23 @@
+import astroid
+code = """
+class C(object):
+    def __init__(self, a: str = None):
+        self.a = a
+"""
+tree = astroid.parse(code)
+class_node = tree.body[0]
+print("Class:", class_node.name)
+init = class_node.body[0]
+print("Method:", init.name)
+print("Args:", init.args)
+for arg in init.args.args:
+    print("  Arg:", arg.name, "annotation:", arg.annotation, "type:", type(arg.annotation))
+    if arg.annotation:
+        print("    annotation:", arg.annotation.as_string())
+for assign in class_node.body[1:]:
+    print("Assign:", assign)
+    if isinstance(assign, astroid.Assign):
+        for target, value in zip(assign.targets, assign.value):
+            print("  target:", target, "value:", value)
+    elif isinstance(assign, astroid.AnnAssign):
+        print("  AnnAssign:", assign)
diff --git a/inspect_annotation.py b/inspect_annotation.py
new file mode 100644
index 00000000..6cc5365f
--- /dev/null
+++ b/inspect_annotation.py
@@ -0,0 +1,27 @@
+import astroid
+from pylint.pyreverse.utils import get_annotation, infer_node
+
+# Test AnnAssign
+code = "a: str = None"
+node = astroid.extract_node(code)
+print("Node type:", type(node))
+print("Node annotation:", node.annotation)
+print("Node value:", node.value)
+print("Node value type:", type(node.value))
+print("Calling get_annotation(node.value):", get_annotation(node.value))
+print("Calling get_annotation(node.annotation):", get_annotation(node.annotation))
+print()
+# Test AssignAttr
+code2 = """
+class A:
+    def __init__(self, x: str = None):
+        self.x = x
+"""
+tree = astroid.parse(code2)
+class_node = tree.body[0]
+init = class_node.body[0]
+assign_attr = init.body[0].value  # self.x = x
+print("AssignAttr:", assign_attr)
+print("AssignAttr attrname:", assign_attr.attrname)
+print("AssignAttr value:", assign_attr.value)
+print("Calling get_annotation(assign_attr):", get_annotation(assign_attr))
diff --git a/pylint/pyreverse/inspector.py.backup b/pylint/pyreverse/inspector.py.backup
new file mode 100644
index 00000000..8fa12202
--- /dev/null
+++ b/pylint/pyreverse/inspector.py.backup
@@ -0,0 +1,355 @@
+# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
+# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
+# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
+# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
+# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
+# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
+# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
+# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
+
+# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
+# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
+
+"""
+Visitor doing some postprocessing on the astroid tree.
+Try to resolve definitions (namespace) dictionary, relationship...
+"""
+import collections
+import os
+import traceback
+
+import astroid
+
+from pylint.pyreverse import utils
+
+
+def _iface_hdlr(_):
+    """Handler used by interfaces to handle suspicious interface nodes."""
+    return True
+
+
+def _astroid_wrapper(func, modname):
+    print("parsing %s..." % modname)
+    try:
+        return func(modname)
+    except astroid.exceptions.AstroidBuildingException as exc:
+        print(exc)
+    except Exception:  # pylint: disable=broad-except
+        traceback.print_exc()
+    return None
+
+
+def interfaces(node, herited=True, handler_func=_iface_hdlr):
+    """Return an iterator on interfaces implemented by the given class node."""
+    try:
+        implements = astroid.bases.Instance(node).getattr("__implements__")[0]
+    except astroid.exceptions.NotFoundError:
+        return
+    if not herited and implements.frame() is not node:
+        return
+    found = set()
+    missing = False
+    for iface in astroid.node_classes.unpack_infer(implements):
+        if iface is astroid.Uninferable:
+            missing = True
+            continue
+        if iface not in found and handler_func(iface):
+            found.add(iface)
+            yield iface
+    if missing:
+        raise astroid.exceptions.InferenceError()
+
+
+class IdGeneratorMixIn:
+    """Mixin adding the ability to generate integer uid."""
+
+    def __init__(self, start_value=0):
+        self.id_count = start_value
+
+    def init_counter(self, start_value=0):
+        """init the id counter"""
+        self.id_count = start_value
+
+    def generate_id(self):
+        """generate a new identifier"""
+        self.id_count += 1
+        return self.id_count
+
+
+class Linker(IdGeneratorMixIn, utils.LocalsVisitor):
+    """Walk on the project tree and resolve relationships.
+
+    According to options the following attributes may be
+    added to visited nodes:
+
+    * uid,
+      a unique identifier for the node (on astroid.Project, astroid.Module,
+      astroid.Class and astroid.locals_type). Only if the linker
+      has been instantiated with tag=True parameter (False by default).
+
+    * Function
+      a mapping from locals names to their bounded value, which may be a
+      constant like a string or an integer, or an astroid node
+      (on astroid.Module, astroid.Class and astroid.Function).
+
+    * instance_attrs_type
+      as locals_type but for klass member attributes (only on astroid.Class)
+
+    * implements,
+      list of implemented interface _objects_ (only on astroid.Class nodes)
+    """
+
+    def __init__(self, project, inherited_interfaces=0, tag=False):
+        IdGeneratorMixIn.__init__(self)
+        utils.LocalsVisitor.__init__(self)
+        # take inherited interface in consideration or not
+        self.inherited_interfaces = inherited_interfaces
+        # tag nodes or not
+        self.tag = tag
+        # visited project
+        self.project = project
+
+    def visit_project(self, node):
+        """visit a pyreverse.utils.Project node
+
+        * optionally tag the node with a unique id
+        """
+        if self.tag:
+            node.uid = self.generate_id()
+        for module in node.modules:
+            self.visit(module)
+
+    def visit_package(self, node):
+        """visit an astroid.Package node
+
+        * optionally tag the node with a unique id
+        """
+        if self.tag:
+            node.uid = self.generate_id()
+        for subelmt in node.values():
+            self.visit(subelmt)
+
+    def visit_module(self, node):
+        """visit an astroid.Module node
+
+        * set the locals_type mapping
+        * set the depends mapping
+        * optionally tag the node with a unique id
+        """
+        if hasattr(node, "locals_type"):
+            return
+        node.locals_type = collections.defaultdict(list)
+        node.depends = []
+        if self.tag:
+            node.uid = self.generate_id()
+
+    def visit_classdef(self, node):
+        """visit an astroid.Class node
+
+        * set the locals_type and instance_attrs_type mappings
+        * set the implements list and build it
+        * optionally tag the node with a unique id
+        """
+        if hasattr(node, "locals_type"):
+            return
+        node.locals_type = collections.defaultdict(list)
+        if self.tag:
+            node.uid = self.generate_id()
+        # resolve ancestors
+        for baseobj in node.ancestors(recurs=False):
+            specializations = getattr(baseobj, "specializations", [])
+            specializations.append(node)
+            baseobj.specializations = specializations
+        # resolve instance attributes
+        node.instance_attrs_type = collections.defaultdict(list)
+        for assignattrs in node.instance_attrs.values():
+            for assignattr in assignattrs:
+                if not isinstance(assignattr, astroid.Unknown):
+                    self.handle_assignattr_type(assignattr, node)
+        # resolve implemented interface
+        try:
+            node.implements = list(interfaces(node, self.inherited_interfaces))
+        except astroid.InferenceError:
+            node.implements = ()
+
+    def visit_functiondef(self, node):
+        """visit an astroid.Function node
+
+        * set the locals_type mapping
+        * optionally tag the node with a unique id
+        """
+        if hasattr(node, "locals_type"):
+            return
+        node.locals_type = collections.defaultdict(list)
+        if self.tag:
+            node.uid = self.generate_id()
+
+    link_project = visit_project
+    link_module = visit_module
+    link_class = visit_classdef
+    link_function = visit_functiondef
+
+    def visit_assignname(self, node):
+        """visit an astroid.AssignName node
+
+        handle locals_type
+        """
+        # avoid double parsing done by different Linkers.visit
+        # running over the same project:
+        if hasattr(node, "_handled"):
+            return
+        node._handled = True
+        if node.name in node.frame():
+            frame = node.frame()
+        else:
+            # the name has been defined as 'global' in the frame and belongs
+            # there.
+            frame = node.root()
+        try:
+            if not hasattr(frame, "locals_type"):
+                # If the frame doesn't have a locals_type yet,
+                # it means it wasn't yet visited. Visit it now
+                # to add what's missing from it.
+                if isinstance(frame, astroid.ClassDef):
+                    self.visit_classdef(frame)
+                elif isinstance(frame, astroid.FunctionDef):
+                    self.visit_functiondef(frame)
+                else:
+                    self.visit_module(frame)
+
+            current = frame.locals_type[node.name]
+            values = set(node.infer())
+            frame.locals_type[node.name] = list(set(current) | values)
+        except astroid.InferenceError:
+            pass
+
+    @staticmethod
+    def handle_assignattr_type(node, parent):
+        """handle an astroid.assignattr node
+
+        handle instance_attrs_type
+        """
+        try:
+            values = set(node.infer())
+            current = set(parent.instance_attrs_type[node.attrname])
+            parent.instance_attrs_type[node.attrname] = list(current | values)
+        except astroid.InferenceError:
+            pass
+
+    def visit_import(self, node):
+        """visit an astroid.Import node
+
+        resolve module dependencies
+        """
+        context_file = node.root().file
+        for name in node.names:
+            relative = astroid.modutils.is_relative(name[0], context_file)
+            self._imported_module(node, name[0], relative)
+
+    def visit_importfrom(self, node):
+        """visit an astroid.ImportFrom node
+
+        resolve module dependencies
+        """
+        basename = node.modname
+        context_file = node.root().file
+        if context_file is not None:
+            relative = astroid.modutils.is_relative(basename, context_file)
+        else:
+            relative = False
+        for name in node.names:
+            if name[0] == "*":
+                continue
+            # analyze dependencies
+            fullname = f"{basename}.{name[0]}"
+            if fullname.find(".") > -1:
+                try:
+                    fullname = astroid.modutils.get_module_part(fullname, context_file)
+                except ImportError:
+                    continue
+            if fullname != basename:
+                self._imported_module(node, fullname, relative)
+
+    def compute_module(self, context_name, mod_path):
+   
…[cut, 21628 more chars]
```

## The submitted patch (as submitted)

### Test files (shown in full)

```diff
(none)
```

### All other files

```diff
(nothing submitted)
```
