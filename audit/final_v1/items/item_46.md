# Item 46

**Repository:** pylint-dev/pylint  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** tests/checkers/unittest_variables.py

## The issue

unused-import false positive for a module used in a type comment
### Steps to reproduce

```python
"""Docstring."""

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
```

### Current behavior

```
************* Module a
/tmp/a.py:3:0: W0611: Unused import abc (unused-import)

-----------------------------------
Your code has been rated at 7.50/10
```

### Expected behavior

`unused-import` should not be emitted.

### pylint --version output

Result of `pylint --version` output:

```
pylint 2.8.3
astroid 2.5.6
Python 3.9.2 (default, Feb 28 2021, 17:03:44) 
[GCC 10.2.1 20210110]
```

This is a follow up to #3112.


## The agent's commands, in order (134; outputs omitted)

1. `find /testbed -type f -name "*.py" | grep -E "(unused-import|import)" | head -30`
2. `ls -la /testbed/`
3. `grep -r "unused_import\|W0611" /testbed/pylint --include="*.py" | head -20`
4. `grep -B5 -A5 "W0611" /testbed/pylint/checkers/variables.py`
5. `grep -r "Unused import" /testbed/pylint --include="*.py" | head -10`
6. `head -n 200 /testbed/pylint/checkers/variables.py`
7. `grep -n "class.*Import\|class.*Unused" /testbed/pylint/checkers/variables.py`
8. `grep -r "W0611" /testbed/pylint --include="*.py" -B2 -A2`
9. `grep -r "unused_import" /testbed/pylint/checkers --include="*.py" -i`
10. `find /testbed/pylint/checkers -name "*.py" -exec grep -l "UnusedImport" {} \;`
11. `ls -la /testbed/pylint/checkers/`
12. `grep -n "unused" /testbed/pylint/checkers/imports.py -i`
13. `grep -n "class.*Checker" /testbed/pylint/checkers/variables.py`
14. `sed -n '578,1000p' /testbed/pylint/checkers/variables.py`
15. `grep -n "visit_import\|visit_importfrom" /testbed/pylint/checkers/variables.py`
16. `sed -n '1174,1250p' /testbed/pylint/checkers/variables.py`
17. `grep -n "_check_is_unused\|_check_import\|_check_module_attrs" /testbed/pylint/checkers/variables.py | head -20`
18. `sed -n '2018,2100p' /testbed/pylint/checkers/variables.py`
19. `grep -n "_store_type_annotation" /testbed/pylint/checkers/variables.py`
20. `sed -n '1,200p' /testbed/pylint/checkers/variables.py | grep -A 20 -B 5 "_type_annotation_names"`
21. `grep -n "_type_annotation_names" /testbed/pylint/checkers/variables.py | head -30`
22. `sed -n '1823,1850p' /testbed/pylint/checkers/variables.py`
23. `grep -n "type_comment" /testbed/pylint/checkers/variables.py | head -30`
24. `sed -n '845,870p' /testbed/pylint/checkers/variables.py`
25. `grep -r "type_comment" /testbed/pylint --include="*.py" | grep -v ".pyc" | head -30`
26. `grep -n "type_comment" /testbed/pylint/checkers/variables.py -B2 -A2`
27. `cd /testbed && python -m pytest tests/ -xvs -k unused_import 2>&1 | head -50`
28. `cd /testbed && ./check 2>&1 | head -20`
29. `ls -la /testbed/*.py`
30. `find /testbed -name "check" -type f`
31. `cat /testbed/README.rst | head -100`
32. `cat /testbed/tox.ini`
33. `pip install pytest 2>&1 | tail -5`
34. `find /testbed -type f -name "check" 2>/dev/null`
35. `ls -la /testbed/`
36. `ls -la /testbed/script/`
37. `grep -r "unused-import" /testbed/tests --include="*.py" | head -5`
38. `find /testbed/tests -name "*import*.py" -type f | head -10`
39. `ls -la /testbed/tests/functional/`
40. `ls -la /testbed/tests/functional/w/ | head -20`
41. `python -c "import sys; print(sys.executable)"`
42. `pip list | grep pytest`
43. `python -c "import pytest; print(pytest.__version__)" 2>&1`
44. `cat /testbed/requirements_test.txt`
45. `grep -r "check" /testbed --include="*.py" --include="*.sh" --include="*.mk" | grep -v ".pyc" | grep -v "test" | head -20`
46. `find /testbed/.github/workflows -type f -name "*.yml" -o -name "*.yaml" | head -5`
47. `head -100 /testbed/.github/workflows/ci.yaml`
48. `echo $VIRTUAL_ENV`
49. `python setup.py --help-commands | grep test`
50. `cat /testbed/setup.py`
51. `which apt-get`
52. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -20`
53. `python -c "import sys; print([p for p in sys.path if 'site' in p])"`
54. `ls /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/ | grep pytest`
55. `find /testbed -maxdepth 1 -type f -name "*.sh" -o -name "*.bash" 2>/dev/null`
56. `grep -n "test" /testbed/.github/workflows/ci.yaml | head -30`
57. `apt-get clean 2>&1`
58. `whoami`
59. `ls -la /testbed/ | grep check`
60.
```
cd /testbed && cat > test_issue.py << 'EOF'
"""Docstring."""

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
EOF
```
61. `cd /testbed && python -m pylint test_issue.py 2>&1 | head -20`
62. `grep -r "type_comment" /testbed/pylint --include="*.py" | grep -v ".pyc" | grep -v "type_comment_args\|type_comment_returns"`
63. `sed -n '1200,1300p' /testbed/pylint/checkers/variables.py`
64. `grep -r "\.type_comment" /testbed/pylint --include="*.py" | head -10`
65.
```
cd /testbed && python -c "
import astroid
code = '''import abc
X = ...  # type: abc.ABC
'''
tree = astroid.parse(code)
for node in tree.body:
    print(node)
    if hasattr(node, 'type_comment'):
        print('type_comment:', node.type_comment)
    if hasattr(node, 'value'):
        print('value:', node.value)
"
```
66. `ls -la /testbed/ | grep -i astroid`
67. `grep -r "type:" /testbed/tests --include="*.py" | head -5`
68. `cat /testbed/tests/functional/u/unused/unused_typing_imports.py`
69. `grep -r "abc" /testbed/tests --include="*.py" | head -10`
70. `python -c "import astroid; import inspect; print(inspect.getfile(astroid))"`
71. `grep -r "type_comment" /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astroid --include="*.py" | head -5`
72. `grep -n "class Assign" /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astroid/node_classes.py -A 30`
73. `grep -n "class AnnAssign" /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astroid/node_classes.py -A 30`
74.
```
python -c "
import ast
code = '''import abc
X = ...  # type: abc.ABC
'''
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
"
```
75.
```
cd /testbed && python -c "
import astroid
code = '''import abc
X = ...  # type: abc.ABC
'''
tree = astroid.parse(code)
for node in tree.body:
    print(type(node).__name__, hasattr(node, 'type_comment'))
    if hasattr(node, 'type_comment'):
        print(node.type_comment)
"
```
76. `grep -r "type:" /testbed/pylint --include="*.py" | head -5`
77. `python -c "import astroid; print(astroid.__version__)"`
78. `grep -r "3112" /testbed --include="*.py" --include="*.rst" --include="*.txt"`
79. `ls -la /testbed/tests/regrtest_data/`
80. `cat /testbed/tests/regrtest_data/import_something.py`
81. `find /testbed/tests/functional/u -name "*.py" -exec grep -l "type:" {} \;`
82. `pip install pytest --break-system-packages 2>&1 | tail -10`
83. `find /testbed -type f -name "*.py" -exec grep -l "def test" {} \; | head -5`
84. `grep -r "type_comment" /testbed/pylint --include="*.py" | grep -v "type_comment_args\|type_comment_returns" | head -20`
85.
```
python -c "
import ast
code = '''import abc
X = ...  # type: abc.ABC
'''
tree = ast.parse(code)
print(ast.dump(tree))
"
```
86. `grep -r "tokenize" /testbed/pylint --include="*.py" | head -5`
87. `grep -B5 -A20 "def tokenize_module" /testbed/pylint/utils/utils.py`
88. `grep -n "tokenize_module" /testbed/pylint/checkers/variables.py`
89. `grep -r "tokenize_module" /testbed/pylint --include="*.py" | head -10`
90. `grep -B5 -A5 "utils.tokenize_module" /testbed/pylint/lint/pylinter.py`
91. `grep -r "type_comment" /testbed --include="*.py" | grep -v "type_comment_args\|type_comment_returns" | head -30`
92. `grep -n "test_attribute_in_type_comment" /testbed/tests/checkers/unittest_variables.py -A 30`
93. `grep -B10 "class TestVariablesChecker" /testbed/tests/checkers/unittest_variables.py | head -30`
94. `grep -n "@set_config" /testbed/tests/checkers/unittest_variables.py | head -10`
95. `ls -la /testbed/ | grep venv`
96. `grep -r "type_comment" /testbed/pylint/checkers/base.py`
97.
```
cd /testbed && python -c "
import astroid
node = astroid.extract_node('''X = ...  # type: abc.ABC
''')
print(type(node))
print(node)
print(node.__dict__ if hasattr(node, '__dict__') else '')
"
```
98. `sed -n '1845,1860p' /testbed/pylint/checkers/variables.py`
99. `grep -n "_check_imports" /testbed/pylint/checkers/variables.py -B5 -A5`
100. `sed -n '730,770p' /testbed/pylint/checkers/variables.py`
101.
```
cd /testbed && cat > debug.py << 'EOF'
import astroid
from pylint.checkers import variables
from pylint.testutils import CheckerTestCase

module = astroid.parse("""
import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
""")

checker = variables.VariablesChecker()
checker.open()
checker.visit_module(module)
for node in module.body:
    node.accept(checker)
checker.leave_modu …[cut]
```
102.
```
cd /testbed && cat > debug2.py << 'EOF'
import astroid
from pylint.checkers import variables

module = astroid.parse("""
import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
""")

checker = variables.VariablesChecker()
# We need to set up the checker's internal state
checker._to_consume = [variables.NamesConsumer(module, "module")]
checker._type_annotation_names = []

# Wa …[cut]
```
103. `grep -n "_fix_dot_imports" /testbed/pylint/checkers/variables.py -B2 -A20`
104. `sed -n '261,350p' /testbed/pylint/checkers/variables.py`
105. `grep -n "class NamesConsumer" /testbed/pylint/checkers/variables.py -A 30`
106. `grep -n "\.consumed\[" /testbed/pylint/checkers/variables.py | head -10`
107. `sed -n '540,560p' /testbed/pylint/checkers/variables.py`
108. `grep -n "mark_as_consumed" /testbed/pylint/checkers/variables.py`
109. `sed -n '1100,1200p' /testbed/pylint/checkers/variables.py`
110. `grep -n "_type_annotation_names.append" /testbed/pylint/checkers/variables.py`
111. `sed -n '1820,1850p' /testbed/pylint/checkers/variables.py`
112. `sed -n '2030,2080p' /testbed/pylint/checkers/variables.py`
113. `cp /testbed/pylint/checkers/variables.py /testbed/pylint/checkers/variables.py.backup`
114. `grep "from pylint.testutils" /testbed/pylint/checkers/variables.py`
115. `grep -n "self._type_annotation_names" /testbed/pylint/checkers/variables.py | grep -v "\.append\|\.extend\|\.name"`
116. `grep -n "def _store_type_annotation_node" /testbed/pylint/checkers/variables.py`
117.
```
cd /testbed && cat > edit_debug.py << 'EOF'
import sys
with open('pylint/checkers/variables.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if line.strip() == 'self._type_annotation_names.append(type_annotation.name)':
        new_lines.append('            print(f"DEBUG: adding {type_annotation.name}")\n')
    elif line.strip() == 'self._ …[cut]
```
118. `cd /testbed && python -m pylint test_issue.py 2>&1 | head -30`
119. `cp /testbed/pylint/checkers/variables.py.backup /testbed/pylint/checkers/variables.py`
120. `grep -n "import pytest" /testbed/pylint/testutils/__init__.py`
121. `head -100 /testbed/pylint/testutils/__init__.py`
122. `grep -n "import pytest" /testbed/pylint/testutils/checker_test_case.py`
123. `which pytest`
124. `which tox`
125. `cd /testbed && git log --oneline -n 20 --grep="type" 2>&1 | head -20`
126. `cd /testbed && git log --oneline -n 100 --grep="unused-import" 2>&1 | head -20`
127. `cd /testbed && git show e918f96f --stat 2>&1 | head -30`
128. `cd /testbed && git show e918f96f --no-stat 2>&1 | head -200`
129. `cd /testbed && git show e918f96f pylint/checkers/variables.py 2>&1 | head -200`
130.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
'''
module = astroid.parse(code)
for node in module.body:
    if isinstance(node, astroid.Assign):
        print('Assign:', node)
        print('type_annotation:', node.type_annotation)
        if node.type_annotation:
            print('type_annotation type:', type(nod …[cut]
```
131.
```
cd /testbed && cat > patch_debug.py << 'EOF'
import re
with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the line with "def _check_imports(self, not_consumed):"
pattern = r'(def _check_imports\(self, not_consumed\):)'
match = re.search(pattern, content)
if match:
    # Insert after the def line but before the next line
    lines = content.split('\n')
    for i, li …[cut]
```
132. `cd /testbed && python -m pylint test_issue.py 2>&1 | head -50`
133. `grep -n "def _store_type_annotation_node" /testbed/pylint/checkers/variables.py`
134.
```
cd /testbed && cat > patch_debug2.py << 'EOF'
import re
with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the method
pattern = r'(def _store_type_annotation_node\(self, type_annotation\):)'
match = re.search(pattern, content)
if match:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == 'def _store_type_annotation_node(s …[cut]
```

## The agent's last reasoning (last 3 turns)

```
Now we need to also import print? It's already there. However, we need to ensure that `print` is available (it is). Now run pylint on our test file again.
...
Aha! The `_type_annotation_names` only contains `['ABC']`. It does NOT contain `'abc'`. That's the bug! Why is `abc` missing? Let's examine why `_store_type_annotation_node` didn't add `abc`. Let's add more debug to see what's happening inside `_store_type_annotation_node`. We'll patch `_store_type_annotation_node` to print what it receives. We need to edit `_store_type_annotation_node`. Let's find its line number.
...
Now we'll edit that method to add debug prints. Let's write another script.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/debug.py b/debug.py
new file mode 100644
index 00000000..c08ae6cf
--- /dev/null
+++ b/debug.py
@@ -0,0 +1,21 @@
+import astroid
+from pylint.checkers import variables
+from pylint.testutils import CheckerTestCase
+
+module = astroid.parse("""
+import abc
+from abc import ABC
+
+X = ...  # type: abc.ABC
+Y = ...  # type: ABC
+""")
+
+checker = variables.VariablesChecker()
+checker.open()
+checker.visit_module(module)
+for node in module.body:
+    node.accept(checker)
+checker.leave_module(module)
+checker.close()
+
+print("_type_annotation_names:", checker._type_annotation_names)
diff --git a/debug2.py b/debug2.py
new file mode 100644
index 00000000..ee0a1906
--- /dev/null
+++ b/debug2.py
@@ -0,0 +1,25 @@
+import astroid
+from pylint.checkers import variables
+
+module = astroid.parse("""
+import abc
+from abc import ABC
+
+X = ...  # type: abc.ABC
+Y = ...  # type: ABC
+""")
+
+checker = variables.VariablesChecker()
+# We need to set up the checker's internal state
+checker._to_consume = [variables.NamesConsumer(module, "module")]
+checker._type_annotation_names = []
+
+# Walk the tree and call visit/leave methods
+for node in module.body:
+    node.accept(checker)
+    if hasattr(node, 'value'):
+        node.value.accept(checker)
+
+checker.leave_module(module)
+
+print("_type_annotation_names:", checker._type_annotation_names)
diff --git a/edit_debug.py b/edit_debug.py
new file mode 100644
index 00000000..d7f0ddcf
--- /dev/null
+++ b/edit_debug.py
@@ -0,0 +1,16 @@
+import sys
+with open('pylint/checkers/variables.py', 'r') as f:
+    lines = f.readlines()
+
+new_lines = []
+for line in lines:
+    new_lines.append(line)
+    if line.strip() == 'self._type_annotation_names.append(type_annotation.name)':
+        new_lines.append('            print(f"DEBUG: adding {type_annotation.name}")\n')
+    elif line.strip() == 'self._type_annotation_names.append(TYPING_MODULE)':
+        new_lines.append('            print(f"DEBUG: adding {TYPING_MODULE}")\n')
+    elif line.strip().startswith('self._type_annotation_names.extend('):
+        new_lines.append('            print(f"DEBUG: adding from type_annotation {type_annotation}")\n')
+
+with open('pylint/checkers/variables.py', 'w') as f:
+    f.writelines(new_lines)
diff --git a/patch_debug.py b/patch_debug.py
new file mode 100644
index 00000000..0ff2a64c
--- /dev/null
+++ b/patch_debug.py
@@ -0,0 +1,24 @@
+import re
+with open('pylint/checkers/variables.py', 'r') as f:
+    content = f.read()
+
+# Find the line with "def _check_imports(self, not_consumed):"
+pattern = r'(def _check_imports\(self, not_consumed\):)'
+match = re.search(pattern, content)
+if match:
+    # Insert after the def line but before the next line
+    lines = content.split('\n')
+    for i, line in enumerate(lines):
+        if line.strip() == 'def _check_imports(self, not_consumed):':
+            # Insert two lines
+            indent = len(line) - len(line.lstrip())
+            lines.insert(i+1, ' ' * indent + '    # DEBUG')
+            lines.insert(i+2, ' ' * indent + '    print("DEBUG: _type_annotation_names:", self._type_annotation_names)')
+            lines.insert(i+3, ' ' * indent + '    print("DEBUG: not_consumed:", not_consumed)')
+            break
+    content = '\n'.join(lines)
+    with open('pylint/checkers/variables.py', 'w') as f:
+        f.write(content)
+        print('Patched')
+else:
+    print('Pattern not found')
diff --git a/patch_debug2.py b/patch_debug2.py
new file mode 100644
index 00000000..173b5643
--- /dev/null
+++ b/patch_debug2.py
@@ -0,0 +1,33 @@
+import re
+with open('pylint/checkers/variables.py', 'r') as f:
+    content = f.read()
+
+# Find the method
+pattern = r'(def _store_type_annotation_node\(self, type_annotation\):)'
+match = re.search(pattern, content)
+if match:
+    lines = content.split('\n')
+    for i, line in enumerate(lines):
+        if line.strip() == 'def _store_type_annotation_node(self, type_annotation):':
+            # Insert after the docstring? Actually we can insert after the method signature.
+            # Find the next line that is not empty and has less indentation than the method body.
+            # We'll insert after the line "\"\"\"Given a type annotation, store all the name nodes it refers to\"\"\"
+            # but we can just insert after the first line of the method body.
+            # Let's find the line where the body starts (indentation > signature).
+            j = i + 1
+            while j < len(lines) and (lines[j].strip() == '' or len(lines[j]) - len(lines[j].lstrip()) <= len(line) - len(line.lstrip())):
+                j += 1
+            # Now j points to the first line of the method body.
+            # Insert before that line.
+            indent = len(lines[j]) - len(lines[j].lstrip())
+            lines.insert(j, ' ' * indent + '    # DEBUG: type_annotation:', type_annotation, 'node_type:', type(type_annotation).__name__)
+            lines.insert(j+1, ' ' * indent + '    if isinstance(type_annotation, astroid.Name):')
+            lines.insert(j+2, ' ' * indent + '        self._type_annotation_names.append(type_annotation.name)')
+            lines.insert(j+3, ' ' * indent + '        print(f"DEBUG: added {type_annotation.name}")')
+            lines.insert(j+4, ' ' * indent + '        return')
+            # Actually we need to replace the whole method? This is too messy.
+            # Let's do a simpler approach: replace the whole method with a debug version.
+            break
+    # Let's instead replace the method using regex substitution (risky)
+    # We'll just manually edit using a temporary file.
+    print('Need to manually edit')
diff --git a/pylint/checkers/variables.py b/pylint/checkers/variables.py
index 3ddafd59..fddb3d7d 100644
--- a/pylint/checkers/variables.py
+++ b/pylint/checkers/variables.py
@@ -2016,6 +2016,9 @@ class VariablesChecker(BaseChecker):
                 self.add_message("unused-variable", args=(name,), node=node)
 
     def _check_imports(self, not_consumed):
+        # DEBUG
+        print("DEBUG: _type_annotation_names:", self._type_annotation_names)
+        print("DEBUG: not_consumed:", not_consumed)
         local_names = _fix_dot_imports(not_consumed)
         checked = set()
         for name, stmt in local_names:
diff --git a/pylint/checkers/variables.py.backup b/pylint/checkers/variables.py.backup
new file mode 100644
index 00000000..3ddafd59
--- /dev/null
+++ b/pylint/checkers/variables.py.backup
@@ -0,0 +1,2152 @@
+# Copyright (c) 2006-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
+# Copyright (c) 2009 Mads Kiilerich <mads@kiilerich.com>
+# Copyright (c) 2010 Daniel Harding <dharding@gmail.com>
+# Copyright (c) 2011-2014, 2017 Google, Inc.
+# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
+# Copyright (c) 2013-2020 Claudiu Popa <pcmanticore@gmail.com>
+# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
+# Copyright (c) 2014 Brett Cannon <brett@python.org>
+# Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
+# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
+# Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
+# Copyright (c) 2015 Radu Ciorba <radu@devrandom.ro>
+# Copyright (c) 2015 Simu Toni <simutoni@gmail.com>
+# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
+# Copyright (c) 2016, 2018-2019 Ashley Whetter <ashley@awhetter.co.uk>
+# Copyright (c) 2016, 2018 Jakub Wilk <jwilk@jwilk.net>
+# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
+# Copyright (c) 2016-2017 Łukasz Rogalski <rogalski.91@gmail.com>
+# Copyright (c) 2016 Grant Welch <gwelch925+github@gmail.com>
+# Copyright (c) 2017-2018, 2020 hippo91 <guillaume.peillex@gmail.com>
+# Copyright (c) 2017-2018 Ville Skyttä <ville.skytta@iki.fi>
+# Copyright (c) 2017 Dan Garrette <dhgarrette@gmail.com>
+# Copyright (c) 2018-2019 Jim Robertson <jrobertson98atx@gmail.com>
+# Copyright (c) 2018 Mike Miller <mtmiller@users.noreply.github.com>
+# Copyright (c) 2018 Lucas Cimon <lucas.cimon@gmail.com>
+# Copyright (c) 2018 Drew <drewrisinger@users.noreply.github.com>
+# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
+# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
+# Copyright (c) 2018 Bryce Guinta <bryce.guinta@protonmail.com>
+# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
+# Copyright (c) 2018 Mike Frysinger <vapier@gmail.com>
+# Copyright (c) 2018 Marianna Polatoglou <mpolatoglou@bloomberg.net>
+# Copyright (c) 2018 mar-chi-pan <mar.polatoglou@gmail.com>
+# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
+# Copyright (c) 2019 Nick Drozd <nicholasdrozd@gmail.com>
+# Copyright (c) 2019 Djailla <bastien.vallet@gmail.com>
+# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
+# Copyright (c) 2020 Andrew Simmons <anjsimmo@gmail.com>
+# Copyright (c) 2020 Andrew Simmons <a.simmons@deakin.edu.au>
+# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
+# Copyright (c) 2020 Ashley Whetter <ashleyw@activestate.com>
+# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
+# Copyright (c) 2021 haasea <44787650+haasea@users.noreply.github.com>
+# Copyright (c) 2021 Alexander Kapshuna <kapsh@kap.sh>
+
+# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
+# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
+
+"""variables checkers for Python code
+"""
+import collections
+import copy
+import itertools
+import os
+import re
+from functools import lru_cache
+
+import astroid
+
+from pylint.checkers import BaseChecker, utils
+from pylint.checkers.utils import is_postponed_evaluation_enabled
+from pylint.constants import PY39_PLUS
+from pylint.interfaces import HIGH, INFERENCE, INFERENCE_FAILURE, IAstroidChecker
+from pylint.utils import get_global_option
+
+SPECIAL_OBJ = re.compile("^_{2}[a-z]+_{2}$")
+FUTURE = "__future__"
+# regexp for ignored argument name
+IGNORED_ARGUMENT_NAMES = re.compile("_.*|^ignored_|^unused_")
+# In Python 3.7 abc has a Python implementation which is preferred
+# by astroid. Unfortunately this also messes up our explicit checks
+# for `abc`
+METACLASS_NAME_TRANSFORMS = {"_py_abc": "abc"}
+TYPING_TYPE_CHECKS_GUARDS = frozenset({"typing.TYPE_CHECKING", "TYPE_CHECKING"})
+BUILTIN_RANGE = "builtins.range"
+TYPING_MODULE = "typing"
+TYPING_NAMES = frozenset(
+    {
+        "Any",
+        "Callable",
+        "ClassVar",
+        "Generic",
+        "Optional",
+        "Tuple",
+        "Type",
+        "TypeVar",
+        "Union",
+        "AbstractSet",
+        "ByteString",
+        "Container",
+        "ContextManager",
+        "Hashable",
+        "ItemsView",
+        "Iterable",
+        "Iterator",
+        "KeysView",
+        "Mapping",
+        "MappingView",
+        "MutableMapping",
+        "MutableSequence",
+        "MutableSet",
+        "Sequence",
+        "Sized",
+        "ValuesView",
+        "Awaitable",
+        "AsyncIterator",
+        "AsyncIterable",
+        "Coroutine",
+        "Collection",
+        "AsyncGenerator",
+        "AsyncContextManager",
+        "Reversible",
+        "SupportsAbs",
+        "SupportsBytes",
+        "SupportsComplex",
+        "SupportsFloat",
+        "SupportsInt",
+        "SupportsRound",
+        "Counter",
+        "Deque",
+        "Dict",
+        "DefaultDict",
+        "List",
+        "Set",
+        "FrozenSet",
+        "NamedTuple",
+        "Generator",
+        "AnyStr",
+        "Text",
+        "Pattern",
+        "BinaryIO",
+    }
+)
+
+
+def _is_from_future_import(stmt, name):
+    """Check if the name is a future import from another module."""
+    try:
+        module = stmt.do_import_module(stmt.modname)
+    except astroid.AstroidBuildingException:
+        return None
+
+    for local_node in module.locals.get(name, []):
+        if isinstance(local_node, astroid.ImportFrom) and local_node.modname == FUTURE:
+  
…[cut, 80440 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
