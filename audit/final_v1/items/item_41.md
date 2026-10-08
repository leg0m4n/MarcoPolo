# Item 41

**Repository:** sphinx-doc/sphinx  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** NOT resolved  
**The task's test files:** tests/test_domain_py.py, tests/test_pycode_ast.py

## The issue

`IndexError: pop from empty list` for empty tuple type annotation
**Describe the bug**
Following notation for empty tuple from [this mypy issue](https://github.com/python/mypy/issues/4211) like
```python
from typing import Tuple

def foo() -> Tuple[()]:
	"""Sample text."""
    return ()
```
I get
```bash
  File "\path\to\site-packages\sphinx\domains\python.py", line 112, in unparse
    result.pop()
IndexError: pop from empty list
```

**To Reproduce**
Steps to reproduce the behavior:
1. Write contents of snippet to module and set it to be explorable by sphinx.
2. Install dependencies, in my `docs/requirements.txt`:
```txt
Sphinx>=2.0.1
sphinx-rtd-theme>=0.4.3
```
2. Build docs.

**Expected behavior**
Docs are built and there is `foo` with valid type annotations.

**Your project**
https://github.com/lycantropos/robust/tree/1c7b74e0cc39c1843a89583b8c245f08039a3978

**Environment info**
- OS: Windows 10, but also reproduces on [readthedocs](https://readthedocs.org/projects/shewchuk/builds/10817256/).
- Python version: 3.8.0
- Sphinx version: 3.0.1
- Sphinx extensions:  `['sphinx.ext.autodoc', 'sphinx.ext.viewcode']`



## The agent's commands, in order (83; outputs omitted)

1. `cd /testbed && git status`
2. `cd /testbed && find . -type f -name "*.py" | head -20`
3. `cd /testbed && ls -la`
4. `cd /testbed && grep -n "unparse" sphinx/domains/python.py`
5. `cd /testbed && sed -n '100,130p' sphinx/domains/python.py`
6. `cd /testbed && sed -n '91,150p' sphinx/domains/python.py`
7. `cd /testbed && grep -n "result.pop()" sphinx/domains/python.py`
8. `cd /testbed && sed -n '115,130p' sphinx/domains/python.py`
9. `cd /testbed && grep -n "def signature_from_str" sphinx/domains/python.py`
10. `cd /testbed && grep -r "def signature_from_str" sphinx/`
11. `cd /testbed && head -30 sphinx/domains/python.py`
12. `cd /testbed && sed -n '30,80p' sphinx/domains/python.py`
13. `cd /testbed && sed -n '85,160p' sphinx/domains/python.py`
14. `cd /testbed && grep -n "def _parse_annotation" sphinx/domains/python.py`
15. `cd /testbed && sed -n '80,160p' sphinx/domains/python.py`
16. `cd /testbed && python -m pytest --version 2>&1 | head -5`
17. `cd /testbed && ./check 2>&1 | head -30`
18. `cd /testbed && cat Makefile`
19. `cd /testbed && python -m pytest -v 2>&1 | head -50`
20. `cd /testbed && pip list | grep -E "pytest|Sphinx"`
21. `cd /testbed && pip list | grep pytest`
22. `cd /testbed && pip install pytest -q`
23. `cd /testbed && find . -name "check" -type f`
24. `cd /testbed && grep -r "check" .travis.yml .github/ 2>/dev/null | head -5`
25. `cd /testbed && ls -la .circleci/`
26. `cd /testbed && cat .circleci/config.yml`
27. `cd /testbed && make test 2>&1 | head -30`
28. `cd /testbed && grep -r "extras_require" setup.py`
29. `cd /testbed && cat setup.py`
30. `cd /testbed && find . -type f -name "*check*" -o -name "*test*" | grep -v ".pyc" | head -20`
31. `cd /testbed && cat utils/checks.py | head -30`
32. `cd /testbed && cat tox.ini`
33. `cd /testbed && grep -r "Tuple\[()\]" sphinx/`
34. `cd /testbed && grep -r "pop from empty list" tests/ 2>/dev/null | head -5`
35. `cd /testbed && python -c "import sys; sys.path.insert(0, '.'); from sphinx.domains.python import _parse_annotation; print(_parse_annotation('Tuple[int, str]'))" 2>&1`
36. `cd /testbed && python -c "import sys; sys.path.insert(0, '.'); from sphinx.domains.python import _parse_annotation; print(_parse_annotation('Tuple[()]'))" 2>&1`
37. `cd /testbed && python -c "import ast; tree = ast.parse('Tuple[()]', mode='eval'); print(ast.dump(tree))" 2>&1`
38. `cd /testbed && grep -r "4211" . 2>/dev/null | head -5`
39. `cd /testbed && python -c "import ast; tree = ast.parse('()', mode='eval'); print(ast.dump(tree))" 2>&1`
40. `cd /testbed && grep -r "Tuple\[()\]" sphinx/ 2>/dev/null | head -5`
41. `cd /testbed && grep -r "Tuple\[()" . 2>/dev/null | head -5`
42. `cd /testbed && grep -B5 -A10 'Tuple\[()\]' sphinx/domains/python.py 2>/dev/null || true`
43. `cd /testbed && find tests -name "*.py" -exec grep -l "Tuple\[()\]" {} \;`
44. `cd /testbed && grep -n "Tuple\[()\]" tests/test_domain_py.py -B2 -A2`
45. `cd /testbed && sed -n '250,270p' tests/test_domain_py.py`
46. `cd /testbed && grep -n "List\[()\]" tests/test_domain_py.py -B2 -A2`
47. `cd /testbed && sed -n '95,125p' sphinx/domains/python.py`
48. `cd /testbed && cp sphinx/domains/python.py sphinx/domains/python.py.backup`
49.
```
cd /testbed && cat > fix_empty_tuple.py << 'EOF'
import ast
import sys

with open('sphinx/domains/python.py', 'r') as f:
    lines = f.readlines()

# Find the line numbers for the tuple branch
in_tuple = False
start = -1
for i, line in enumerate(lines):
    if 'elif isinstance(node, ast.Tuple):' in line:
        start = i
        in_tuple = True
    if in_tuple and start != -1 and line.strip() ==  …[cut]
```
50.
```
cd /testbed && cat > fix_annotations.py << 'EOF'
import sys

with open('sphinx/domains/python.py', 'r') as f:
    content = f.read()

# We'll replace the tuple branch using a regex that matches the whole branch.
# Since the branch is simple, we can do a multiline regex.
import re

# Pattern for tuple branch
# We'll match from "elif isinstance(node, ast.Tuple):" up to the next "elif" or "else:" or  …[cut]
```
51.
```
cd /testbed && python3 << 'EOF'
import sys
with open('sphinx/domains/python.py', 'r') as f:
    lines = f.readlines()

# Find the start of tuple branch
tuple_start = -1
for i, line in enumerate(lines):
    if 'elif isinstance(node, ast.Tuple):' in line:
        tuple_start = i
        break

if tuple_start == -1:
    sys.exit(1)

# Find the line where the function ends (next elif or else at same i …[cut]
```
52.
```
cd /testbed && python3 << 'EOF'
import sys
with open('sphinx/domains/python.py', 'r') as f:
    lines = f.readlines()

# Find the list branch
list_start = -1
for i, line in enumerate(lines):
    if 'elif isinstance(node, ast.List):' in line:
        list_start = i
        break

if list_start == -1:
    sys.exit(1)

# Find the line where the function ends (next elif or else at same indent level)
# …[cut]
```
53.
```
cd /testbed && cat > fix_annotations.py << 'EOF'
import sys

with open('sphinx/domains/python.py', 'r') as f:
    lines = f.readlines()

# 1. Fix ast.Tuple branch (lines 115-121)
# Find the start line of the branch
for i, line in enumerate(lines):
    if 'elif isinstance(node, ast.Tuple):' in line:
        tuple_start = i
        break

# Determine the indentation of the tuple branch
indent = len( …[cut]
```
54. `cd /testbed && python3 fix_annotations.py`
55. `cd /testbed && sed -n '97,130p' sphinx/domains/python.py`
56.
```
cd /testbed && cat > fix_punctuation.py << 'EOF'
import sys

with open('sphinx/domains/python.py', 'r') as f:
    content = f.read()

# Replace escaped backslashes with actual brackets
# We'll use regex to match patterns like '\\[' and replace with '['
# But careful not to replace other backslashes.
import re

# Replace '\\[' with '['
content = re.sub(r"'\\\\\['", "'['", content)
content = re.sub( …[cut]
```
57. `cd /testbed && python3 fix_punctuation.py`
58. `cd /testbed && grep -n "\\\\" sphinx/domains/python.py | head -20`
59. `cd /testbed && sed -n '115,125p' sphinx/domains/python.py`
60. `cd /testbed && sed -n '97,110p' sphinx/domains/python.py`
61. `cd /testbed && sed -i "s/addnodes.desc_sig_punctuation('', '\\\\\\[')/addnodes.desc_sig_punctuation('', '[')/g" sphinx/domains/python.py`
62. `cd /testbed && sed -i "s/addnodes.desc_sig_punctuation('', '\\\\\\]')/addnodes.desc_sig_punctuation('', ']')/g" sphinx/domains/python.py`
63. `cd /testbed && sed -n '97,110p' sphinx/domains/python.py`
64. `cd /testbed && sed -n '115,125p' sphinx/domains/python.py`
65. `cd /testbed && python3 -c "import pytest; print(pytest.__version__)" 2>&1`
66. `cd /testbed && pip install .[test] 2>&1 | tail -30`
67. `which apt-get`
68. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -20`
69. `cd /testbed && head -50 tests/test_domain_py.py`
70.
```
cd /testbed && python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref, desc_sig_punctuation
from docutils import nodes

result = _parse_annotation('Tuple[()]')
print('Result length:', len(result))
for i, node in enumerate(result):
    print(f'{i}: {type(node).__name__}', end='')
    if isinstance(node, nodes. …[cut]
```
71.
```
cd /testbed && python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import desc_sig_punctuation
from docutils import nodes

result = _parse_annotation('[]')
print('Result length:', len(result))
for i, node in enumerate(result):
    print(f'{i}: {type(node).__name__}', end='')
    if isinstance(node, nodes.Text):
        print( …[cut]
```
72. `cd /testbed && find . -name "check" -type f 2>/dev/null`
73. `cd /testbed && ls -la | grep -E "check|test"`
74. `cd /testbed && git diff sphinx/domains/python.py 2>&1 | head -100`
75. `cd /testbed && git diff --stat sphinx/domains/python.py`
76. `cd /testbed && git diff --no-ext-diff sphinx/domains/python.py > patch.txt`
77. `cd /testbed && cat patch.txt`
78.
```
cd /testbed && python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref, desc_sig_punctuation
from docutils import nodes

def check(annotation, expected_texts):
    result = _parse_annotation(annotation)
    texts = []
    for node in result:
        if isinstance(node, pending_xref):
            texts.append(n …[cut]
```
79.
```
cd /testbed && python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from sphinx.domains.python import _parse_annotation

# Nested empty tuple
result = _parse_annotation('Tuple[Tuple[()], int]')
print('Nested empty tuple length:', len(result))
for node in result:
    print(type(node).__name__, end=' ')
print()
EOF
```
80. `cd /testbed && git log --oneline -1`
81. `cd /testbed && grep -n "result.pop()" sphinx/domains/python.py`
82. `cd /testbed && python3 -m py_compile sphinx/domains/python.py 2>&1`
83. `cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
We are not at that commit. The repository may have additional commits. However, we need to ensure our changes are based on the base commit. Since we are working in a fresh environment, we can assume the source code is as of that commit? Not sure. But the issue is about a bug in the current version, and we are fixing it. The patch we created is based on the current version (which may be ahead). That's fine because we need to fix the bug in the current version. Now we should also check if there are any other places in the codebase that might have similar issues (e.g., other AST node types like `ast.Set`? Not present). Let's search for other `result.pop()` occurrences in the file.
...
Two occurrences: one in list branch (line 106) and one in tuple branch (line 127). Both are now guarded by the empty check. Good. Now we should also check if there are any other branches that might have similar issues (like `ast.Attribute`? Not). We'll trust that the function is only used for parsing annotations. Now we can consider the fix complete. Let's create a final verification by running the test that the user might run: building docs with Sphinx. That's too heavy. Given the constraints, we'll submit our patch. But before we submit, we need to ensure we haven't introduced any syntax errors. Let's run a quick syntax check on the modified file.
...
No errors. Good. Now we can submit.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/fix_annotations.py b/fix_annotations.py
new file mode 100644
index 000000000..399cac0e7
--- /dev/null
+++ b/fix_annotations.py
@@ -0,0 +1,100 @@
+import sys
+
+with open('sphinx/domains/python.py', 'r') as f:
+    lines = f.readlines()
+
+# 1. Fix ast.Tuple branch (lines 115-121)
+# Find the start line of the branch
+for i, line in enumerate(lines):
+    if 'elif isinstance(node, ast.Tuple):' in line:
+        tuple_start = i
+        break
+
+# Determine the indentation of the tuple branch
+indent = len(lines[tuple_start]) - len(lines[tuple_start].lstrip())
+
+# Build new branch lines
+new_tuple_lines = []
+new_tuple_lines.append(' ' * indent + 'elif isinstance(node, ast.Tuple):\n')
+new_tuple_lines.append(' ' * (indent + 4) + 'if not node.elts:\n')
+new_tuple_lines.append(' ' * (indent + 8) + 'return [addnodes.desc_sig_punctuation(\'\', \'(\'),\n')
+new_tuple_lines.append(' ' * (indent + 8) + '            addnodes.desc_sig_punctuation(\'\', \')\')]\n')
+new_tuple_lines.append(' ' * (indent + 4) + 'result = []\n')
+new_tuple_lines.append(' ' * (indent + 4) + 'for elem in node.elts:\n')
+new_tuple_lines.append(' ' * (indent + 8) + 'result.extend(unparse(elem))\n')
+new_tuple_lines.append(' ' * (indent + 8) + 'result.append(addnodes.desc_sig_punctuation(\'\', \', \'))\n')
+new_tuple_lines.append(' ' * (indent + 4) + 'result.pop()\n')
+new_tuple_lines.append(' ' * (indent + 4) + 'return result\n')
+
+# Replace the existing branch lines (from tuple_start to tuple_end)
+# Find tuple_end: next line with same indent that is not part of the branch
+# We'll look for the next line that starts with same indent and is either 'elif', 'else', or 'return' but not indented further.
+# Actually we can replace until we see a line that is not indented more than indent and is not empty.
+# Let's just replace lines[tuple_start:tuple_start+7] (since branch is 7 lines)
+# We'll keep the rest of the file unchanged.
+# However we need to keep the 'else:' line after tuple branch.
+# Let's find the line after tuple branch that is at same indent and starts with 'else:' or 'elif'
+# We'll use a simple approach: we know the exact lines from earlier output (115-123).
+# We'll replace lines 115-121 (0-indexed 114-120) with new_tuple_lines.
+# But we need to keep the 'else:' line and raise line.
+# Actually the branch ends at line 121 (return result). The next line is 'else:'.
+# So we can replace lines[tuple_start:tuple_start+7] (including the line before else?)
+# Let's examine lines indices from earlier output:
+# 115 elif ...
+# 116 result = []
+# 117 for elem in node.elts:
+# 118 result.extend(...)
+# 119 result.append(...)
+# 120 result.pop()
+# 121 return result
+# 122 else:
+# 123 raise SyntaxError
+# So we need to replace lines 115-121 inclusive.
+# Let's do that.
+start_idx = tuple_start
+end_idx = tuple_start + 7  # exclusive (since 7 lines)
+# Ensure we have enough lines
+if end_idx <= len(lines):
+    lines[start_idx:end_idx] = new_tuple_lines
+else:
+    print('Error: not enough lines')
+    sys.exit(1)
+
+# 2. Fix ast.List branch (lines 97-104)
+# Find start line of list branch
+for i, line in enumerate(lines):
+    if 'elif isinstance(node, ast.List):' in line:
+        list_start = i
+        break
+
+# Determine indentation
+indent = len(lines[list_start]) - len(lines[list_start].lstrip())
+
+# Build new branch lines for empty list handling
+new_list_lines = []
+new_list_lines.append(' ' * indent + 'elif isinstance(node, ast.List):\n')
+new_list_lines.append(' ' * (indent + 4) + 'if not node.elts:\n')
+new_list_lines.append(' ' * (indent + 8) + 'return [addnodes.desc_sig_punctuation(\'\', \'\[\'),\n')
+new_list_lines.append(' ' * (indent + 8) + '                addnodes.desc_sig_punctuation(\'\', \'\]\')]\n')
+new_list_lines.append(' ' * (indent + 4) + 'result = [addnodes.desc_sig_punctuation(\'\', \'\[\')]  # type: List[Node]\n')
+new_list_lines.append(' ' * (indent + 4) + 'for elem in node.elts:\n')
+new_list_lines.append(' ' * (indent + 8) + 'result.extend(unparse(elem))\n')
+new_list_lines.append(' ' * (indent + 8) + 'result.append(addnodes.desc_sig_punctuation(\'\', \', \'))\n')
+new_list_lines.append(' ' * (indent + 4) + 'result.pop()\n')
+new_list_lines.append(' ' * (indent + 4) + 'result.append(addnodes.desc_sig_punctuation(\'\', \'\]\'))\n')
+new_list_lines.append(' ' * (indent + 4) + 'return result\n')
+
+# Replace lines 97-104 (0-indexed 96-103)
+list_start_idx = list_start
+list_end_idx = list_start + 8  # exclusive (8 lines)
+if list_end_idx <= len(lines):
+    lines[list_start_idx:list_end_idx] = new_list_lines
+else:
+    print('Error: not enough lines for list branch')
+    sys.exit(1)
+
+# Write back
+with open('sphinx/domains/python.py', 'w') as f:
+    f.writelines(lines)
+
+print('File updated successfully')
diff --git a/fix_empty_tuple.py b/fix_empty_tuple.py
new file mode 100644
index 000000000..1f2843e02
--- /dev/null
+++ b/fix_empty_tuple.py
@@ -0,0 +1,21 @@
+import ast
+import sys
+
+with open('sphinx/domains/python.py', 'r') as f:
+    lines = f.readlines()
+
+# Find the line numbers for the tuple branch
+in_tuple = False
+start = -1
+for i, line in enumerate(lines):
+    if 'elif isinstance(node, ast.Tuple):' in line:
+        start = i
+        in_tuple = True
+    if in_tuple and start != -1 and line.strip() == 'else:' and i > start:
+        # We'll assume the tuple branch ends at the line before 'else:'
+        # Actually we need to find the line that returns result
+        # Let's just replace from start to the line before 'else:' (but there is an else after tuple)
+        pass
+
+# Instead of complex parsing, we'll just replace the whole function using regex.
+# But we need to be careful.
diff --git a/fix_punctuation.py b/fix_punctuation.py
new file mode 100644
index 000000000..cf0ddd039
--- /dev/null
+++ b/fix_punctuation.py
@@ -0,0 +1,45 @@
+import sys
+
+with open('sphinx/domains/python.py', 'r') as f:
+    content = f.read()
+
+# Replace escaped backslashes with actual brackets
+# We'll use regex to match patterns like '\\[' and replace with '['
+# But careful not to replace other backslashes.
+import re
+
+# Replace '\\[' with '['
+content = re.sub(r"'\\\\\['", "'['", content)
+content = re.sub(r"'\\\\\]'", "']'", content)
+content = re.sub(r"'\\\\\('", "'('\", content)
+content = re.sub(r"'\\\\\)'", "')'", content)
+
+# Also need to fix the double backslashes in the list branch where we have '\[' and '\]' inside the string.
+# Actually we can just replace all occurrences of '\\\\' with nothing? That's too risky.
+# Let's do a more targeted fix: replace only those inside addnodes.desc_sig_punctuation arguments.
+# We'll write a small function to parse but we can do simple string replacement for the whole block.
+
+# Let's just replace the entire list branch and tuple branch with corrected versions using the same method but with proper strings.
+# Instead, we can read the file line by line and fix only those lines.
+
+with open('sphinx/domains/python.py', 'r') as f:
+    lines = f.readlines()
+
+# Fix lines that contain '\\[' etc.
+for i, line in enumerate(lines):
+    if '\\\\[' in line:
+        lines[i] = line.replace('\\\\[', '[')
+    if '\\\\]' in line:
+        lines[i] = line.replace('\\\\]', ']')
+    if '\\\\(' in line:
+        lines[i] = line.replace('\\\\(', '(')
+    if '\\\\)' in line:
+        lines[i] = line.replace('\\)', ')')
+
+# Also fix the extra spaces indentation? We'll leave for now.
+
+# Write back
+with open('sphinx/domains/python.py', 'w') as f:
+    f.writelines(lines)
+
+print('Fixed punctuation')
diff --git a/patch.txt b/patch.txt
new file mode 100644
index 000000000..0e883f37e
--- /dev/null
+++ b/patch.txt
@@ -0,0 +1,24 @@
+diff --git a/sphinx/domains/python.py b/sphinx/domains/python.py
+index 3ca730e30..6f28c1e63 100644
+--- a/sphinx/domains/python.py
++++ b/sphinx/domains/python.py
+@@ -96,6 +96,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
+         elif isinstance(node, ast.Index):
+             return unparse(node.value)
+         elif isinstance(node, ast.List):
++            if not node.elts:
++                return [addnodes.desc_sig_punctuation('', '['),
++                                addnodes.desc_sig_punctuation('', ']')]
+             result = [addnodes.desc_sig_punctuation('', '[')]  # type: List[Node]
+             for elem in node.elts:
+                 result.extend(unparse(elem))
+@@ -114,6 +117,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
+             result.append(addnodes.desc_sig_punctuation('', ']'))
+             return result
+         elif isinstance(node, ast.Tuple):
++            if not node.elts:
++                return [addnodes.desc_sig_punctuation('', '('),
++                            addnodes.desc_sig_punctuation('', ')')]
+             result = []
+             for elem in node.elts:
+                 result.extend(unparse(elem))
diff --git a/sphinx/domains/python.py b/sphinx/domains/python.py
index 3ca730e30..6f28c1e63 100644
--- a/sphinx/domains/python.py
+++ b/sphinx/domains/python.py
@@ -96,6 +96,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
         elif isinstance(node, ast.Index):
             return unparse(node.value)
         elif isinstance(node, ast.List):
+            if not node.elts:
+                return [addnodes.desc_sig_punctuation('', '['),
+                                addnodes.desc_sig_punctuation('', ']')]
             result = [addnodes.desc_sig_punctuation('', '[')]  # type: List[Node]
             for elem in node.elts:
                 result.extend(unparse(elem))
@@ -114,6 +117,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
             result.append(addnodes.desc_sig_punctuation('', ']'))
             return result
         elif isinstance(node, ast.Tuple):
+            if not node.elts:
+                return [addnodes.desc_sig_punctuation('', '('),
+                            addnodes.desc_sig_punctuation('', ')')]
             result = []
             for elem in node.elts:
                 result.extend(unparse(elem))
diff --git a/sphinx/domains/python.py.backup b/sphinx/domains/python.py.backup
new file mode 100644
index 000000000..3ca730e30
--- /dev/null
+++ b/sphinx/domains/python.py.backup
@@ -0,0 +1,1356 @@
+"""
+    sphinx.domains.python
+    ~~~~~~~~~~~~~~~~~~~~~
+
+    The Python domain.
+
+    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
+    :license: BSD, see LICENSE for details.
+"""
+
+import builtins
+import inspect
+import re
+import typing
+import warnings
+from inspect import Parameter
+from typing import Any, Dict, Iterable, Iterator, List, NamedTuple, Tuple
+from typing import cast
+
+from docutils import nodes
+from docutils.nodes import Element, Node
+from docutils.parsers.rst import directives
+
+from sphinx import addnodes
+from sphinx.addnodes import pending_xref, desc_signature
+from sphinx.application import Sphinx
+from sphinx.builders import Builder
+from sphinx.deprecation import RemovedInSphinx40Warning, RemovedInSphinx50Warning
+from sphinx.directives import ObjectDescription
+from sphinx.domains import Domain, ObjType, Index, IndexEntry
+from sphinx.environment import BuildEnvironment
+from sphinx.locale import _, __
+from sphinx.pycode.ast import ast, parse as ast_parse
+from sphinx.roles import XRefRole
+from sphinx.util import logging
+from sphinx.util.docfields import Field, GroupedField, TypedField
+from sphinx.util.docutils import SphinxDirective
+from sphinx.util.inspect import signature_from_str
+from sphinx.util.nodes import make_id, make_refnode
+from sphinx.util.typing import TextlikeNode
+
+if False:
+    # For type annotation
+    from typing import Type  # for python3.5.1
+
+
+logger = logging.getLogger(__name__)
+
+
+# REs for Python signatures
+py_sig_re = re.compile(
+    r'''^ ([\w.]*\.)?            # class name(s)
+          (\w+)  \s*             # thing name
+          (?: \(\s*(.*)\s*\)     # op
…[cut, 51744 more chars]
```

## The submitted patch (as submitted)

```diff
diff --git a/sphinx/domains/python.py b/sphinx/domains/python.py
index 3ca730e30..6f28c1e63 100644
--- a/sphinx/domains/python.py
+++ b/sphinx/domains/python.py
@@ -96,6 +96,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
         elif isinstance(node, ast.Index):
             return unparse(node.value)
         elif isinstance(node, ast.List):
+            if not node.elts:
+                return [addnodes.desc_sig_punctuation('', '['),
+                                addnodes.desc_sig_punctuation('', ']')]
             result = [addnodes.desc_sig_punctuation('', '[')]  # type: List[Node]
             for elem in node.elts:
                 result.extend(unparse(elem))
@@ -114,6 +117,9 @@ def _parse_annotation(annotation: str) -> List[Node]:
             result.append(addnodes.desc_sig_punctuation('', ']'))
             return result
         elif isinstance(node, ast.Tuple):
+            if not node.elts:
+                return [addnodes.desc_sig_punctuation('', '('),
+                            addnodes.desc_sig_punctuation('', ')')]
             result = []
             for elem in node.elts:
                 result.extend(unparse(elem))

```
