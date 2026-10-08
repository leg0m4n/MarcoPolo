# Item 53

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


## The agent's commands, in order (138; outputs omitted)

1. `pwd && ls -la`
2. `find . -name "*.py" -type f | grep -E "(unused|import)" | head -20`
3. `ls -la pylint/`
4. `ls -la pylint/checkers/`
5. `grep -n "W0611" pylint/checkers/imports.py`
6. `grep -r "unused-import" pylint/`
7. `head -100 pylint/checkers/variables.py`
8. `grep -n "unused-import" pylint/checkers/variables.py | head -20`
9. `sed -n '1600,2200p' pylint/checkers/variables.py`
10. `grep -n "_check_if_usage" pylint/checkers/variables.py`
11. `grep -n "class VariablesChecker" pylint/checkers/variables.py`
12. `sed -n '578,1000p' pylint/checkers/variables.py`
13. `grep -n "_store_type_annotation_names" pylint/checkers/variables.py`
14. `sed -n '1845,2000p' pylint/checkers/variables.py`
15. `grep -n "class NamesConsumer" pylint/checkers/variables.py`
16. `sed -n '510,577p' pylint/checkers/variables.py`
17. `grep -n "class ScopeConsumer" pylint/checkers/variables.py`
18. `grep -r "class ScopeConsumer" pylint/`
19. `grep -n "ScopeConsumer" pylint/checkers/variables.py`
20. `grep -n "visit_import" pylint/checkers/variables.py`
21. `sed -n '1174,1250p' pylint/checkers/variables.py`
22. `sed -n '800,950p' pylint/checkers/variables.py`
23. `grep -r "visit_import" pylint/ --include="*.py" | grep -v ".pyc" | head -20`
24. `sed -n '720,800p' pylint/checkers/variables.py`
25. `grep -n "_check_globals" pylint/checkers/variables.py`
26. `sed -n '2011,2100p' pylint/checkers/variables.py`
27. `grep -n "_store_type_annotation_node" pylint/checkers/variables.py`
28. `sed -n '1823,1850p' pylint/checkers/variables.py`
29. `grep -n "type_comment" pylint/checkers/variables.py`
30. `grep -r "type_comment" pylint/ --include="*.py" | head -30`
31.
```
cd /testbed && cat > test_issue.py << 'EOF'
"""Docstring."""

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
EOF
```
32. `cd /testbed && python -m pylint test_issue.py --reports=no`
33.
```
cd /testbed && python -c "import astroid; module = astroid.parse('''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''); print(module.body)"
```
34.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
module = astroid.parse(code)
for node in module.body:
    if isinstance(node, astroid.Assign):
        print('Assign:', node)
        print('  type_comment:', node.type_comment)
        print('  value:', node.value)
        print('  targets:', node.targets)
"
```
35.
```
cd /testbed && python -c "
import ast
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
tree = ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        print('Assign:', ast.dump(node, indent=2))
        if hasattr(node, 'type_comment'):
            print('  type_comment:', node.type_comment)
"
```
36.
```
cd /testbed && python -c "
import ast
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
tree = ast.parse(code)
for node in tree.body:
    print(type(node).__name__, node.lineno)
    if hasattr(node, 'type_comment'):
        print('  type_comment:', node.type_comment)
"
```
37. `grep -r "type_comment" pylint/ --include="*.py" -B2 -A2`
38.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
module = astroid.parse(code)
assign = module.body[2]
print('Assign class:', assign.__class__)
print('Assign dir:', [a for a in dir(assign) if not a.startswith('_')])
"
```
39.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
module = astroid.parse(code)
assign = module.body[2]
print('type_annotation:', assign.type_annotation)
if assign.type_annotation:
    print('value:', assign.type_annotation)
    print('type:', type(assign.type_annotation))
"
```
40. `sed -n '1240,1260p' pylint/checkers/variables.py`
41. `grep -A 20 "def _store_type_annotation_node" pylint/checkers/variables.py`
42.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X: abc.ABC = ...
Y: ABC = ...'''
module = astroid.parse(code)
for node in module.body:
    if isinstance(node, astroid.Assign):
        print('Assign:', node)
        print('  type_annotation:', node.type_annotation)
"
```
43.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X: abc.ABC = ...
Y: ABC = ...'''
module = astroid.parse(code)
for node in module.body:
    print(type(node).__name__, node.lineno, node)
    if hasattr(node, 'type_annotation'):
        print('  type_annotation:', node.type_annotation)
"
```
44. `grep -n "annotation" pylint/checkers/variables.py | head -30`
45. `grep -n "visit_annassign" pylint/checkers/variables.py`
46. `grep -n "leave_annassign" pylint/checkers/variables.py`
47. `find /testbed/tests -name "*.py" -exec grep -l "type.*comment" {} \;`
48. `grep -n "type.*comment" /testbed/tests/functional/u/unused/unused_typing_imports.py`
49. `cat /testbed/tests/functional/u/unused/unused_typing_imports.py`
50. `grep -n "type.*comment" /testbed/tests/checkers/unittest_variables.py -B2 -A2`
51. `sed -n '190,250p' /testbed/tests/checkers/unittest_variables.py`
52. `cd /testbed && python -m pytest tests/checkers/unittest_variables.py::TestVariablesChecker::test_attribute_in_type_comment -xvs 2>&1 | head -50`
53. `ls -la /testbed/script/`
54. `which check 2>/dev/null || echo "not found"`
55. `python -c "import pytest; print(pytest.__version__)" 2>&1 | head -5`
56. `head -30 /usr/local/bin/check`
57. `pip install pytest -q 2>&1 | tail -5`
58. `cd /testbed && python -m unittest tests.checkers.unittest_variables.TestVariablesChecker.test_attribute_in_type_comment -v 2>&1`
59. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -5`
60. `cat /usr/local/bin/check`
61. `grep -i check README.rst 2>/dev/null | head -5`
62. `cat /testbed/tox.ini`
63. `find /testbed -name "check" -type f 2>/dev/null | head -10`
64. `ls -la /usr/local/bin/ | grep check`
65. `cd /testbed && check 2>&1 | head -30`
66. `cd /testbed && check -k test_attribute_in_type_comment 2>&1 | tail -30`
67. `cd /testbed && check -k test_attribute_in_type_comment -v 2>&1 | grep -A 10 -B 2 "test_attribute_in_type_comment"`
68.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
module = astroid.parse(code)
assign = module.body[2]
print('type_annotation:', assign.type_annotation)
print('type:', type(assign.type_annotation))
print('is Subscript?', isinstance(assign.type_annotation, astroid.Subscript))
print('is Attribute?', isinstance(assign.t …[cut]
```
69.
```
cd /testbed && python -c "
import astroid
code = '''import abc
from abc import ABC
X = ...  # type: abc.ABC
Y = ...  # type: ABC'''
module = astroid.parse(code)
for node in module.body:
    if hasattr(node, 'type_annotation'):
        print(node.lineno, node.type_annotation, type(node.type_annotation).__name__)
"
```
70. `sed -n '1823,1840p' pylint/checkers/variables.py`
71. `sed -n '1823,1860p' pylint/checkers/variables.py`
72. `grep -n "TYPING_MODULE" pylint/checkers/variables.py | head -5`
73.
```
cd /testbed && cat > fix_type_annotation.py << 'EOF'
import sys
import re

with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the function _store_type_annotation_node
pattern = r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to"""\n        if isinstance\(type_annotation, astroid …[cut]
```
74. `cd /testbed && python fix_type_annotation.py`
75. `sed -n '1823,1900p' pylint/checkers/variables.py`
76.
```
cd /testbed && python -c "
import astroid
attr = astroid.extract_node('abc.ABC')
print('attr:', attr)
print('dir:', [a for a in dir(attr) if 'attr' in a])
print('attr.attrname:', attr.attrname)
"
```
77. `cd /testbed && python -m pylint test_issue.py --reports=no 2>&1`
78. `cd /testbed && check -k TestVariablesChecker -v 2>&1 | head -100`
79. `cd /testbed && check tests/checkers/unittest_variables.py 2>&1 | tail -30`
80. `cd /testbed && pip install -e . -q 2>&1 | tail -10`
81. `cd /testbed && python -m pytest tests/checkers/unittest_variables.py::TestVariablesChecker::test_attribute_in_type_comment -xvs 2>&1 | tail -50`
82. `ls -l /usr/local/bin/check`
83. `grep -r "def check" /testbed --include="*.py" 2>/dev/null | head -5`
84. `cd /testbed && python -m unittest discover -s tests/checkers -p unittest_variables.py -v 2>&1 | head -100`
85. `grep -r "IS_PYPY" /testbed/pylint/`
86. `grep -n "IS_PYPY" /testbed/pylint/constants.py`
87.
```
cd /testbed && cat > test_var_annotation.py << 'EOF'
import abc
from abc import ABC

X: abc.ABC = ...
Y: ABC = ...
EOF
```
88. `cd /testbed && python -m pylint test_var_annotation.py --reports=no 2>&1`
89. `cd /testbed && python -c "import pylint; print(pylint.__version__)"`
90. `grep -r "IS_PYPY" /testbed/ 2>/dev/null | head -5`
91. `sed -n '197,210p' /testbed/tests/checkers/unittest_variables.py`
92.
```
cd /testbed && cat > test_type_comment_attribute.py << 'EOF'
import foo
from foo import Bar, Boo

a = ... # type: foo.Bar
b = ... # type: foo.Bar[Boo]
c = ... # type: Bar.Boo
EOF
```
93. `cd /testbed && python -m pylint test_type_comment_attribute.py --reports=no 2>&1`
94. `python -c "import pylint.constants; print(dir(pylint.constants))" 2>&1 | grep -i pypy`
95. `grep -r "IS_PYPY" /testbed/pylint/ 2>/dev/null`
96. `cd /testbed && python -m pylint tests/functional/u/unused/unused_typing_imports.py --reports=no 2>&1 | grep -v "E0401" | head -30`
97. `cd /testbed && python -m pylint tests/functional/u/unused/unused_typing_imports.py --reports=no 2>&1 | tail -30`
98.
```
cd /testbed && cat > fix_type_annotation2.py << 'EOF'
import sys
import re

with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the function _store_type_annotation_node and replace with corrected version
new_content = re.sub(
    r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to …[cut]
```
99. `cd /testbed && python fix_type_annotation2.py`
100. `sed -n '1823,1900p' pylint/checkers/variables.py`
101. `cd /testbed && python -m pylint tests/functional/u/unused/unused_typing_imports.py --reports=no 2>&1 | grep -E "W0611|unused-import" | head -10`
102. `cd /testbed && python -m pylint tests/functional/u/unused/unused_typing_imports.py --reports=no 2>&1 | tail -20`
103. `grep -r "from pylint.constants import" /testbed/pylint/ 2>/dev/null | head -5`
104. `grep -n "^IS_PYPY" /testbed/pylint/constants.py`
105. `head -100 /testbed/pylint/constants.py`
106. `cd /testbed && sed -i '10aIS_PYPY = sys.implementation.name == "pypy"' pylint/constants.py`
107. `cd /testbed && python -c "from pylint.constants import IS_PYPY; print(IS_PYPY)"`
108. `cd /testbed && python -m pytest tests/checkers/unittest_variables.py::TestVariablesChecker::test_attribute_in_type_comment -xvs 2>&1 | tail -50`
109. `cd /testbed && pip install pytest --break-system-packages -q 2>&1 | tail -5`
110. `ls -l /usr/local/bin/check | cat`
111.
```
cd /testbed && cat > test_typing_module.py << 'EOF'
import typing
x = ...  # type: typing.Optional
EOF
```
112. `cd /testbed && python -m pylint test_typing_module.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
113.
```
cd /testbed && cat > test_typing_import.py << 'EOF'
from typing import Optional
x = ...  # type: Optional[int]
EOF
```
114. `cd /testbed && python -m pylint test_typing_import.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
115.
```
cd /testbed && cat > test_unused.py << 'EOF'
import abc
from abc import ABC
x = 1
EOF
```
116. `cd /testbed && python -m pylint test_unused.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
117. `cd /testbed && git diff HEAD -- pylint/checkers/variables.py 2>&1 | head -100`
118. `cd /testbed && git diff HEAD -- pylint/constants.py 2>&1`
119. `cd /testbed && git diff -- pylint/checkers/variables.py pylint/constants.py > patch.txt 2>&1`
120. `cat /testbed/patch.txt`
121.
```
cd /testbed && cat > fix_type_annotation3.py << 'EOF'
import sys
import re

with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the function _store_type_annotation_node and replace with improved version
new_content = re.sub(
    r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to" …[cut]
```
122. `cd /testbed && python fix_type_annotation3.py`
123. `sed -n '1823,1950p' pylint/checkers/variables.py`
124.
```
cd /testbed && cat > fix_type_annotation4.py << 'EOF'
import sys
import re

with open('pylint/checkers/variables.py', 'r') as f:
    content = f.read()

# Find the function _store_type_annotation_node and replace with corrected version
new_content = re.sub(
    r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to …[cut]
```
125. `cd /testbed && python fix_type_annotation4.py`
126. `cd /testbed && python -m pylint test_issue.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
127.
```
cd /testbed && cat > test_var_annotation2.py << 'EOF'
import abc
from abc import ABC

X: abc.ABC = ...
Y: ABC = ...
EOF
```
128. `cd /testbed && python -m pylint test_var_annotation2.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
129.
```
cd /testbed && cat > test_subscript.py << 'EOF'
from typing import List
x = ...  # type: List[int]
EOF
```
130. `cd /testbed && python -m pylint test_subscript.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
131.
```
cd /testbed && cat > test_typing_special.py << 'EOF'
import typing
x = ...  # type: typing.Optional
EOF
```
132. `cd /testbed && python -m pylint test_typing_special.py --reports=no 2>&1 | grep -E "W0611|unused-import"`
133. `sed -n '1823,1900p' /testbed/pylint/checkers/variables.py | head -30`
134.
```
cd /testbed && cat > final_fix.py << 'EOF'
import sys

with open('pylint/checkers/variables.py', 'r') as f:
    lines = f.readlines()

# Find the start of _store_type_annotation_node
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def _store_type_annotation_node'):
        start = i
        break
if start is None:
    sys.exit(1)

# Find the line where the function en …[cut]
```
135. `cd /testbed && python final_fix.py`
136. `sed -n '1823,1900p' /testbed/pylint/checkers/variables.py | head -40`
137. `cd /testbed && git diff -- pylint/checkers/variables.py pylint/constants.py > patch.txt 2>&1`
138. `cat /testbed/patch.txt`

## The agent's last reasoning (last 3 turns)

```
Now verify the function.
...
Great. Now we have the final version. Now we need to regenerate the patch file.
...
Check patch content.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/final_fix.py b/final_fix.py
new file mode 100644
index 00000000..0659517f
--- /dev/null
+++ b/final_fix.py
@@ -0,0 +1,76 @@
+import sys
+
+with open('pylint/checkers/variables.py', 'r') as f:
+    lines = f.readlines()
+
+# Find the start of _store_type_annotation_node
+start = None
+for i, line in enumerate(lines):
+    if line.strip().startswith('def _store_type_annotation_node'):
+        start = i
+        break
+if start is None:
+    sys.exit(1)
+
+# Find the line where the function ends (next def or end of class)
+# We'll just replace from start to the line before next function with same indent
+# Let's find the line with 'def ' at same indent level (4 spaces)
+indent = 0
+for ch in lines[start]:
+    if ch == ' ':
+        indent += 1
+    else:
+        break
+
+# Find next line that starts with exactly indent spaces and 'def '
+end = start + 1
+while end < len(lines):
+    if lines[end].strip() == '':
+        end += 1
+        continue
+    if lines[end].startswith(' ' * indent) and lines[end].lstrip().startswith('def '):
+        break
+    end += 1
+
+# Now we have lines[start:end] as the function
+# We'll replace that block with our corrected version
+new_function = '''    def _store_type_annotation_node(self, type_annotation):
+        """Given a type annotation, store all the name nodes it refers to"""
+        if type_annotation is None:
+            return
+        if isinstance(type_annotation, astroid.Name):
+            self._type_annotation_names.append(type_annotation.name)
+            return
+
+        if isinstance(type_annotation, astroid.Attribute):
+            # For attribute accesses like abc.ABC, add both the module and the attribute
+            expr = type_annotation.expr
+            if isinstance(expr, astroid.Name):
+                self._type_annotation_names.append(expr.name)
+            self._type_annotation_names.append(type_annotation.attrname)
+            # continue to generic fallback to also capture any name in expr
+            # (e.g., if expr is another Attribute, we'll capture its name via nodes_of_class)
+
+        if isinstance(type_annotation, astroid.Subscript):
+            if (
+                isinstance(type_annotation.value, astroid.Attribute)
+                and isinstance(type_annotation.value.expr, astroid.Name)
+                and type_annotation.value.expr.name == TYPING_MODULE
+            ):
+                self._type_annotation_names.append(TYPING_MODULE)
+                return
+            # fall through to generic name extraction
+
+        # For any other node type, extract all name nodes
+        self._type_annotation_names.extend(
+            annotation.name
+            for annotation in type_annotation.nodes_of_class(astroid.Name)
+        )
+'''
+
+# Replace
+lines[start:end] = new_function.splitlines(keepends=True)
+
+with open('pylint/checkers/variables.py', 'w') as f:
+    f.writelines(lines)
+print('Function updated')
diff --git a/fix_type_annotation.py b/fix_type_annotation.py
new file mode 100644
index 00000000..2f7b298c
--- /dev/null
+++ b/fix_type_annotation.py
@@ -0,0 +1,49 @@
+import sys
+import re
+
+with open('pylint/checkers/variables.py', 'r') as f:
+    content = f.read()
+
+# Find the function _store_type_annotation_node
+pattern = r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to"""\n        if isinstance\(type_annotation, astroid\.Name\):\n            self\._type_annotation_names\.append\(type_annotation\.name\)\n            return\n\n        if not isinstance\(type_annotation, astroid\.Subscript\):\n            return\n\n        if \(\n            isinstance\(type_annotation\.value, astroid\.Attribute\)\n            and isinstance\(type_annotation\.value\.expr, astroid\.Name\)\n            and type_annotation\.value\.expr\.name == TYPING_MODULE\n        \):\n            self\._type_annotation_names\.append\(TYPING_MODULE\)\n            return\n\n        self\._type_annotation_names\.extend\(\n            annotation\.name\n            for annotation in type_annotation\.nodes_of_class\(astroid\.Name\)\n        \)'
+
+replacement = '''    def _store_type_annotation_node(self, type_annotation):
+        """Given a type annotation, store all the name nodes it refers to"""
+        if isinstance(type_annotation, astroid.Name):
+            self._type_annotation_names.append(type_annotation.name)
+            return
+
+        if isinstance(type_annotation, astroid.Attribute):
+            # For attribute accesses like abc.ABC, add both the module and the attribute
+            expr = type_annotation.expr
+            if isinstance(expr, astroid.Name):
+                self._type_annotation_names.append(expr.name)
+            self._type_annotation_names.append(type_annotation.attrname)
+            return
+
+        if isinstance(type_annotation, astroid.Subscript):
+            if (
+                isinstance(type_annotation.value, astroid.Attribute)
+                and isinstance(type_annotation.value.expr, astroid.Name)
+                and type_annotation.value.expr.name == TYPING_MODULE
+            ):
+                self._type_annotation_names.append(TYPING_MODULE)
+                return
+            # fall through to generic name extraction
+
+        # For any other node type, extract all name nodes
+        self._type_annotation_names.extend(
+            annotation.name
+            for annotation in type_annotation.nodes_of_class(astroid.Name)
+        )'''
+
+# Replace using re.DOTALL to match across lines
+new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
+
+if new_content == content:
+    print("Pattern not found")
+    sys.exit(1)
+
+with open('pylint/checkers/variables.py', 'w') as f:
+    f.write(new_content)
+print("File updated")
diff --git a/fix_type_annotation2.py b/fix_type_annotation2.py
new file mode 100644
index 00000000..b5418e41
--- /dev/null
+++ b/fix_type_annotation2.py
@@ -0,0 +1,51 @@
+import sys
+import re
+
+with open('pylint/checkers/variables.py', 'r') as f:
+    content = f.read()
+
+# Find the function _store_type_annotation_node and replace with corrected version
+new_content = re.sub(
+    r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to"""\n        if isinstance\(type_annotation, astroid\.Name\):\n            self\._type_annotation_names\.append\(type_annotation\.name\)\n            return\n\n        if isinstance\(type_annotation, astroid\.Attribute\):\n            # For attribute accesses like abc.ABC, add both the module and the attribute\n            expr = type_annotation\.expr\n            if isinstance\(expr, astroid\.Name\):\n                self\._type_annotation_names\.append\(expr\.name\)\n            self\._type_annotation_names\.append\(type_annotation\.attrname\)\n            return\n\n        if isinstance\(type_annotation, astroid\.Subscript\):\n            if \(\n                isinstance\(type_annotation\.value, astroid\.Attribute\)\n                and isinstance\(type_annotation\.value\.expr, astroid\.Name\)\n                and type_annotation\.value\.expr\.name == TYPING_MODULE\n            \):\n                self\._type_annotation_names\.append\(TYPING_MODULE\)\n                return\n            # fall through to generic name extraction\n\n        # For any other node type, extract all name nodes\n        self\._type_annotation_names\.extend\(\n            annotation\.name\n            for annotation in type_annotation\.nodes_of_class\(astroid\.Name\)\n        \)',
+    '''    def _store_type_annotation_node(self, type_annotation):
+        """Given a type annotation, store all the name nodes it refers to"""
+        if type_annotation is None:
+            return
+        if isinstance(type_annotation, astroid.Name):
+            self._type_annotation_names.append(type_annotation.name)
+            return
+
+        if isinstance(type_annotation, astroid.Attribute):
+            # For attribute accesses like abc.ABC, add both the module and the attribute
+            expr = type_annotation.expr
+            if isinstance(expr, astroid.Name):
+                self._type_annotation_names.append(expr.name)
+            self._type_annotation_names.append(type_annotation.attrname)
+            return
+
+        if isinstance(type_annotation, astroid.Subscript):
+            if (
+                isinstance(type_annotation.value, astroid.Attribute)
+                and isinstance(type_annotation.value.expr, astroid.Name)
+                and type_annotation.value.expr.name == TYPING_MODULE
+            ):
+                self._type_annotation_names.append(TYPING_MODULE)
+                return
+            # fall through to generic name extraction
+
+        # For any other node type, extract all name nodes
+        self._type_annotation_names.extend(
+            annotation.name
+            for annotation in type_annotation.nodes_of_class(astroid.Name)
+        )''',
+    content,
+    flags=re.DOTALL
+)
+
+if new_content == content:
+    print("Pattern not found")
+    sys.exit(1)
+
+with open('pylint/checkers/variables.py', 'w') as f:
+    f.write(new_content)
+print("File updated")
diff --git a/fix_type_annotation3.py b/fix_type_annotation3.py
new file mode 100644
index 00000000..47157c68
--- /dev/null
+++ b/fix_type_annotation3.py
@@ -0,0 +1,49 @@
+import sys
+import re
+
+with open('pylint/checkers/variables.py', 'r') as f:
+    content = f.read()
+
+# Find the function _store_type_annotation_node and replace with improved version
+new_content = re.sub(
+    r'    def _store_type_annotation_node\(self, type_annotation\):\n        """Given a type annotation, store all the name nodes it refers to"""\n        if type_annotation is None:\n            return\n        if isinstance\(type_annotation, astroid\.Name\):\n            self\._type_annotation_names\.append\(type_annotation\.name\)\n            return\n\n        if isinstance\(type_annotation, astroid\.Attribute\):\n            # For attribute accesses like abc.ABC, add both the module and the attribute\n            expr = type_annotation\.expr\n            if isinstance\(expr, astroid\.Name\):\n                self\._type_annotation_names\.append\(expr\.name\)\n            self\._type_annotation_names\.append\(type_annotation\.attrname\)\n            return\n\n        if isinstance\(type_annotation, astroid\.Subscript\):\n            if \(\n                isinstance\(type_annotation\.value, astroid\.Attribute\)\n                and isinstance\(type_annotation\.value\.expr, astroid\.Name\)\n                and type_annotation\.value\.expr\.name == TYPING_MODULE\n            \):\n                self\._type_annotation_names\.append\(TYPING_MODULE\)\n                return\n            # fall through to generic name extraction\n\n        # For any other node type, extract all name nodes\n        self\._type_annotation_names\.extend\(\n            annotation\.name\n            for annotation in type_annotation\.nodes_of_class\(astroid\.Name\)\n        \)',
+    '''    def _store_type_annotation_node(self, type_annotation):
+        """Given a type annotation, store all the name nodes it refers to"""
+        if type_annotation is None:
+            return
+        if isinstance(type_annotation, astroid.Name):
+            self._type_annotation_names.append(type_annotation.name)
+            return
+
+        if isinstance(type_annotation, astroid.Attribute):
+            # For attribute accesses like abc.ABC, add both the module and the attribute
+            self._type_annotation_names.append(type_annotation.attrname)
+            # continue to generic fallback to also capture any name in expr
+            # (e.g., if expr is another Attribute, we'll capture its name via nodes_of_class)
+
+        if isinstance(type_annotation, astroid.Subscript
…[cut, 12221 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
