# Item 17

**Repository:** pydata/xarray  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** xarray/tests/test_duck_array_ops.py

## The issue

sum: min_count is not available for reduction with more than one dimensions
**Is your feature request related to a problem? Please describe.**

`sum` with `min_count` errors when passing more than one dim:

```python
import xarray as xr
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
da.sum(["dim_0", "dim_1"], min_count=1)
```

**Describe the solution you'd like**
The logic to calculate the number of valid elements is here:
https://github.com/pydata/xarray/blob/1be777fe725a85b8cc0f65a2bc41f4bc2ba18043/xarray/core/nanops.py#L35

I *think* this can be fixed by replacing

`mask.shape[axis]` with `np.take(a.shape, axis).prod()`

**Additional context**
Potentially relevant for #4351



## The agent's commands, in order (118; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed/`
3. `find /testbed/xarray -type f -name "*.py" | grep -E "nanops|sum"`
4. `head -n 100 /testbed/xarray/core/nanops.py`
5. `grep -n "min_count" /testbed/xarray/core/nanops.py`
6. `sed -n '100,130p' /testbed/xarray/core/nanops.py`
7. `sed -n '180,190p' /testbed/xarray/core/nanops.py`
8. `sed -n '25,50p' /testbed/xarray/core/nanops.py`
9. `grep -r "min_count" /testbed/xarray --include="*.py" | head -30`
10. `grep -A 20 -B 5 "test_min_count_nd" /testbed/xarray/tests/test_duck_array_ops.py`
11. `grep -n "def sum" /testbed/xarray/core/dataarray.py`
12. `grep -r "\.sum" /testbed/xarray/core/dataarray.py | head -5`
13. `cd /testbed && python -c "import xarray as xr; import inspect; print(inspect.getsourcefile(xr.DataArray))"`
14. `grep -n "sum" /testbed/xarray/core/dataarray.py | head -20`
15. `grep -r "def sum" /testbed/xarray/core/ --include="*.py"`
16. `grep -n "class DataArray" /testbed/xarray/core/dataarray.py`
17. `grep -n "from ." /testbed/xarray/core/dataarray.py | head -30`
18. `grep -n "class AbstractArray" /testbed/xarray/core/common.py`
19. `grep -n "class ImplementsArrayReduce" /testbed/xarray/core/common.py`
20. `sed -n '38,200p' /testbed/xarray/core/common.py`
21. `sed -n '200,400p' /testbed/xarray/core/common.py`
22. `grep -r "def reduce" /testbed/xarray/core/ --include="*.py" | head -10`
23. `grep -n "def reduce" /testbed/xarray/core/dataarray.py -A 30`
24. `sed -n '2305,2400p' /testbed/xarray/core/dataarray.py`
25. `grep -n "def reduce" /testbed/xarray/core/variable.py -A 30`
26. `sed -n '1580,1700p' /testbed/xarray/core/variable.py`
27. `grep -n "@" /testbed/xarray/core/dataarray.py | grep -B2 -A2 "sum"`
28. `grep -n "def sum" /testbed/xarray/core/dataarray.py`
29. `grep -r "_reduce_method" /testbed/xarray/core/ --include="*.py"`
30. `grep -n "def sum" /testbed/xarray/core/duck_array_ops.py`
31. `grep -n "inject_reduce_methods" /testbed/xarray/core/ops.py -A 30`
32. `grep -n "REDUCE_METHODS\|NAN_REDUCE_METHODS" /testbed/xarray/core/ops.py`
33. `sed -n '49,70p' /testbed/xarray/core/ops.py`
34. `grep -n "^def sum" /testbed/xarray/core/duck_array_ops.py`
35. `grep -n "sum" /testbed/xarray/core/duck_array_ops.py | head -20`
36. `grep -n "_create_nan_agg_method" /testbed/xarray/core/duck_array_ops.py -A 30`
37. `cd /testbed && ls -la`
38. `find /testbed -name "check" -type f`
39. `ls /testbed/*.mk`
40. `ls -la /testbed/*.sh`
41. `ls /testbed/.github/workflows/`
42. `cd /testbed && python -m pytest xarray/tests/test_duck_array_ops.py::test_min_count_nd -xvs 2>&1 | head -50`
43. `grep -r "def check" /testbed/`
44. `grep -A5 -B5 "test" /testbed/setup.cfg`
45. `cd /testbed && python setup.py test 2>&1 | head -30`
46. `ls /testbed/*.ini`
47. `grep -r "pytest" /testbed/setup.cfg`
48. `find /testbed -maxdepth 1 -type f -name "*" | grep -v ".git" | grep -v ".pyc" | head -30`
49. `ls -la /testbed/ci/`
50. `head -30 /testbed/ci/min_deps_check.py`
51. `pip install pytest 2>&1 | tail -5`
52. `python -m pytest --version 2>&1 | head -5`
53. `cat /testbed/requirements.txt`
54. `pip list | grep pytest`
55. `cd /testbed && python -c "import pytest; print(pytest.__version__)"`
56. `python -c "import sys; print(sys.path)"`
57. `which pytest`
58. `find /testbed/.github -type f -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -5`
59. `grep -n "pytest" /testbed/azure-pipelines.yml`
60. `head -100 /testbed/azure-pipelines.yml`
61. `find /testbed/ci/azure -name "unit-tests.yml" -exec cat {} \;`
62. `which conda`
63. `conda install -y pytest 2>&1 | tail -10`
64. `find /opt/miniconda3/envs/testbed/lib/python3.10/site-packages -name "pytest" -type d 2>/dev/null | head -5`
65. `python -c "import pkgutil; print([name for name, _ in pkgutil.iter_modules()])" | grep pytest`
66. `grep -n "test_min_count_nd" /testbed/xarray/tests/test_duck_array_ops.py -B2 -A30`
67. `grep -n "def construct_dataarray" /testbed/xarray/tests/test_duck_array_ops.py -A 20`
68.
```
cd /testbed && python -c "
import xarray as xr
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
print('DataArray shape:', da.shape)
print('DataArray dims:', da.dims)
try:
    result = da.sum(['dim_0', 'dim_1'], min_count=1)
    print('Success:', result)
except Exception as e:
    print('Error:', e)
"
```
69. `sed -n '1,40p' /testbed/xarray/core/nanops.py`
70. `sed -n '25,60p' /testbed/xarray/core/nanops.py`
71. `head -20 /testbed/xarray/core/nanops.py`
72. `cp /testbed/xarray/core/nanops.py /testbed/xarray/core/nanops.py.backup`
73.
```
cd /testbed && python -c "
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()
# find start and end of _maybe_null_out
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        start = i
        break
if start is None:
    sys.exit(1)
# find end of function (next def with same indentation)
indent = len(lines[start])  …[cut]
```
74. `sed -n '25,80p' /testbed/xarray/core/nanops.py`
75.
```
cd /testbed && python -c "
import xarray as xr
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
print('DataArray shape:', da.shape)
print('DataArray dims:', da.dims)
try:
    result = da.sum(['dim_0', 'dim_1'], min_count=1)
    print('Success:', result)
    print('Result shape:', result.shape)
except Exception as e:
    import traceback
    traceback.print_exc()
"
```
76.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
import numpy as np
from xarray.core import dtypes
from xarray.tests.test_duck_array_ops import construct_dataarray

# parameters from test_min_count_nd
dtype = float
dask = False
func = 'sum'
min_count = 3
dim_num = 3
da = construct_dataarray(dim_num, dtype, contains_nan=True, dask=dask)
print('da shape:', da.shape)
print('da dims:', da …[cut]
```
77. `conda env list 2>&1 | head -20`
78. `python -c "import sys; print(sys.executable)"`
79. `python -c "import site; print(site.getsitepackages())"`
80. `ls /opt/miniconda3/envs/testbed/lib/python3.10/site-packages/ | grep pytest`
81. `find /opt/miniconda3/envs/testbed/lib/python3.10/site-packages -type d -name "pytest*" 2>/dev/null`
82. `grep -n "def maybe_promote" /testbed/xarray/core/dtypes.py -A 10`
83. `sed -n '45,80p' /testbed/xarray/core/dtypes.py`
84.
```
cd /testbed && cat > test_min_count.py << 'EOF'
import numpy as np
import xarray as xr

print("Testing min_count with single axis reduction")
# Create a 2D array with NaNs
da = xr.DataArray([[1., np.nan, 3.],
                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
print("DataArray:", da.values)
print("NaN positions:", np.isnan(da.values))

# min_count = 1, there is at least one non-NaN in eac …[cut]
```
85.
```
cd /testbed && cat > test_min_count.py << 'EOF'
import numpy as np
import xarray as xr

print("Testing min_count with single axis reduction")
# Create a 2D array with NaNs
da = xr.DataArray([[1., np.nan, 3.],
                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
print("DataArray:", da.values)
print("NaN positions:", np.isnan(da.values))

# min_count = 1, there is at least one non-NaN in eac …[cut]
```
86.
```
cd /testbed && cat > debug_min_count.py << 'EOF'
import xarray as xr
import xarray.core.nanops as nanops
import numpy as np

original = nanops._maybe_null_out
def debug_maybe_null_out(result, axis, mask, min_count=1):
    print(f"DEBUG: result={result}, axis={axis}, mask shape={mask.shape}, min_count={min_count}")
    print(f"  result.ndim={getattr(result, 'ndim', 'no ndim')}")
    print(f"  resul …[cut]
```
87. `cd /testbed && cp xarray/core/nanops.py xarray/core/nanops.py.bak2`
88.
```
cd /testbed && python -c "
import sys
with open('xarray/core/nanops.py', 'r') as f:
    content = f.read()
# Find the function definition and replace with debug version
import re
pattern = r'(def _maybe_null_out\(result, axis, mask, min_count=1\):\s*\"\"\"\s*xarray version of pandas.core.nanops._maybe_null_out\s*\"\"\"\s*)'
match = re.search(pattern, content, re.DOTALL)
if match:
    # Insert debu …[cut]
```
89. `grep -n "def _maybe_null_out" /testbed/xarray/core/nanops.py`
90. `sed -n '25,40p' /testbed/xarray/core/nanops.py`
91. `grep -n "def _nan_argminmax_object" /testbed/xarray/core/nanops.py`
92.
```
cd /testbed && python -c "
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find start and end of _maybe_null_out
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        start = i
        break
if start is None:
    sys.exit(1)

# Find end of function (next def with same indentation)
indent = len(lines[start] …[cut]
```
93. `sed -n '25,70p' /testbed/xarray/core/nanops.py`
94.
```
cd /testbed && python -c "
import sys
import xarray as xr
import numpy as np

da = xr.DataArray([[1., np.nan, 3.],
                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
print('Test min_count=5 over both dims:')
result = da.sum(['dim0', 'dim1'], min_count=5)
print('Result:', result.values)
" 2>&1 | head -30
```
95. `cp /testbed/xarray/core/nanops.py.backup /testbed/xarray/core/nanops.py`
96. `sed -n '25,45p' /testbed/xarray/core/nanops.py`
97.
```
cd /testbed && python -c "
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find start and end of _maybe_null_out
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        start = i
        break
if start is None:
    sys.exit(1)

# Find end of function (next def with same indentation)
indent = len(lines[start] …[cut]
```
98. `sed -n '25,50p' /testbed/xarray/core/nanops.py`
99. `cd /testbed && python test_min_count.py 2>&1`
100. `grep -n "NAT_TYPES" /testbed/xarray/core/dtypes.py`
101.
```
cd /testbed && cat > debug2.py << 'EOF'
import sys
import xarray.core.nanops as nanops
import numpy as np

original = nanops._maybe_null_out
def debug_maybe_null_out(result, axis, mask, min_count=1):
    print(f"DEBUG: axis={axis}, min_count={min_count}, result={result}, result.ndim={getattr(result, 'ndim', None)}")
    print(f"  mask shape={mask.shape}, mask.sum()={mask.sum()}, mask.size={mask.si …[cut]
```
102. `grep -n "def _maybe_null_out" /testbed/xarray/core/nanops.py`
103. `sed -n '25,35p' /testbed/xarray/core/nanops.py | cat -n`
104.
```
cd /testbed && cat > patch_with_debug.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    content = f.read()

# Find the function using a simple regex (since the file is not huge)
import re
pattern = r'(def _maybe_null_out\(result, axis, mask, min_count=1\):\s*\"\"\"\s*xarray version of pandas.core.nanops._maybe_null_out\s*\"\"\"\s*)'
match = re.search(pattern, content, re.DOT …[cut]
```
105. `sed -n '25,60p' /testbed/xarray/core/nanops.py`
106. `cp /testbed/xarray/core/nanops.py.bak2 /testbed/xarray/core/nanops.py`
107. `sed -n '25,50p' /testbed/xarray/core/nanops.py`
108.
```
cd /testbed && cat > add_debug.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find line index of elif branch
for i, line in enumerate(lines):
    if line.strip().startswith('elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:'):
        # Insert after this line
        indent = len(line) - len(line.lstrip())
        new_line = ' ' * inden …[cut]
```
109. `sed -n '25,60p' /testbed/xarray/core/nanops.py`
110. `cp /testbed/xarray/core/nanops.py.bak2 /testbed/xarray/core/nanops.py`
111. `sed -n '25,50p' /testbed/xarray/core/nanops.py`
112.
```
cd /testbed && cat > test_with_debug.py << 'EOF'
import sys
import os
# Backup original file
import shutil
shutil.copy('xarray/core/nanops.py', 'xarray/core/nanops.py.debug_backup')
# Read the file
with open('xarray/core/nanops.py', 'r') as f:
    content = f.read()
# Replace the function with debug version
import re
# Find the function using a simple marker
pattern = r'(def _maybe_null_out\(resul …[cut]
```
113. `grep -n "elif getattr(result, \"dtype\", None) not in dtypes.NAT_TYPES:" /testbed/xarray/core/nanops.py`
114. `cd /testbed && sed -i '41i\    import sys\n    print("DEBUG: entering elif branch", file=sys.stderr)' xarray/core/nanops.py`
115. `sed -n '25,50p' /testbed/xarray/core/nanops.py`
116. `cp /testbed/xarray/core/nanops.py.bak2 /testbed/xarray/core/nanops.py`
117.
```
cd /testbed && cat > test_nanops_direct.py << 'EOF'
import sys
sys.path.insert(0, '.')
import numpy as np
import xarray.core.nanops as nanops

# Create a simple array with NaN
a = np.array([[1., np.nan, 3.],
              [4., 5., np.nan]])
print('a:', a)
print('a shape:', a.shape)

# Compute axis as tuple (0,1) (reduce over all dimensions)
axis = (0, 1)
# Call nansum directly
result = nanops.nans …[cut]
```
118.
```
cd /testbed && cat > debug_insert.py << 'EOF'
import sys
import os
# Read file
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()
# Find line index of the line after docstring
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        # find the line after docstring
        j = i + 1
        while j < len(lines) and lines[j].strip().startsw …[cut]
```

## The agent's last reasoning (last 3 turns)

```
Oops, the import sys and print lines are inserted inside the if block? Actually they are inserted after the if block but before the elif, but the indentation is wrong (they are at same level as if?). The line numbers show they are at the same indentation as the if? Actually they are at column 4? Let's examine the raw lines. The issue is that sed inserted lines with no indentation. We need to fix the indentation. Let's revert the file again and start over with a more careful approach. We'll restore from backup again (the corrected version). But we still have the backup at xarray/core/nanops.py.bak2. Let's copy again.
...
Now we need a better debugging strategy. Instead of modifying the source file, we can write a test that directly calls nanops.nansum with our inputs and see what happens. We can import nanops and manually call nansum with axis=tuple, min_count, and inspect the result. That will bypass the DataArray wrapper. Let's write a script that does that and prints intermediate values.
...
So the result is 13.0, not NaN. That means _maybe_null_out didn't set result to NaN. Let's add a print inside _maybe_null_out by monkey-patching at runtime but we need to ensure the patched function is used. Since we imported nanops and then called _maybe_null_out directly (the function object), we can patch it before calling. Let's do that. But we also want to see the debug prints for the elif branch. Let's create a wrapper that prints and then calls original. We'll write a script that patches nanops._maybe_null_out before any other code uses it (except our direct call). However, nanops.nansum already captured the original _maybe_null_out reference. But we can still patch nanops._maybe_null_out and then re-import nanops? That's messy. Instead, we can copy the function logic and instrument it in our test script. Let's just compute manually what should happen. We already have the values: - axis = (0,1) - result2 = 13.0 (scalar) - mask.sum() = 2 (NaN count) - mask.size = 6 - null_mask = mask.size - mask.sum() = 4 - min_count = 5 - null_mask < min_count => True Thus the elif branch should have set result = np.nan. But it didn't. That means either the elif branch wasn't taken, or the assignment didn't happen because result is not the same variable? Wait, _maybe_null_out returns result (which is result2). It modifies result variable locally (reassigns result = np.nan) and returns that. That should have returned np.nan. But the final output is 13.0. So either our assumption about the branch is wrong, or there is another path that returns result2. Let's add a print inside _maybe_null_out by temporarily replacing the function in the module before we import anything else. But we have already imported nanops. However, we can still replace nanops._maybe_null_out and then re-import nansum? Actually nansum is a function inside nanops module; it references nanops._maybe_null_out at the time of its definition (when the module is loaded). If we replace nanops._maybe_null_out after the module is loaded, the reference inside nansum still points to the old function. So we need to reload the nanops module. That's possible but may have side effects. Given the time, we can directly edit the source file with a print that will be included in the patch. Since we need to submit a fix, we can include a small debug print? No, we should not include debug prints in production code. However, we can add a print for debugging only for now, test, and then remove them before finalizing the patch. That's acceptable because we are in a development environment. But we need to ensure we don't break anything else. Let's edit the file again but this time we'll add a simple print that logs when the elif branch is taken, and also log the values. We'll do a careful edit using a Python script that reads the file, finds the elif line, and inserts a print before it, with correct indentation. We'll also need to import sys at the top of the function (but we can import sys inside the br
…[cut, 4171 more chars]
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/add_debug.py b/add_debug.py
new file mode 100644
index 00000000..e3cd2f03
--- /dev/null
+++ b/add_debug.py
@@ -0,0 +1,32 @@
+import sys
+with open('xarray/core/nanops.py', 'r') as f:
+    lines = f.readlines()
+
+# Find line index of elif branch
+for i, line in enumerate(lines):
+    if line.strip().startswith('elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:'):
+        # Insert after this line
+        indent = len(line) - len(line.lstrip())
+        new_line = ' ' * indent + 'import sys\n'
+        new_line2 = ' ' * indent + 'print("DEBUG: scalar null_mask branch", file=sys.stderr)\n'
+        # Insert import sys at the top of the function? We'll just insert before the elif line? Actually we need import sys earlier.
+        # Let's insert import sys at the beginning of the function after the docstring.
+        # Find the function start
+        for j in range(i, -1, -1):
+            if lines[j].strip().startswith('def _maybe_null_out'):
+                # Find the line after docstring
+                k = j + 1
+                while k < len(lines) and lines[k].strip().startswith('\"\"\"'):
+                    k += 1
+                # Now lines[k] is the first line of code after docstring
+                # Insert import sys there if not already present
+                if not any('import sys' in l for l in lines[j:i]):
+                    lines.insert(k, '    import sys\n')
+                break
+        lines.insert(i+1, new_line)
+        lines.insert(i+2, new_line2)
+        break
+
+with open('xarray/core/nanops.py', 'w') as f:
+    f.writelines(lines)
+print('Added debug lines')
diff --git a/debug2.py b/debug2.py
new file mode 100644
index 00000000..9d5c8ae7
--- /dev/null
+++ b/debug2.py
@@ -0,0 +1,52 @@
+import sys
+import xarray.core.nanops as nanops
+import numpy as np
+
+original = nanops._maybe_null_out
+def debug_maybe_null_out(result, axis, mask, min_count=1):
+    print(f"DEBUG: axis={axis}, min_count={min_count}, result={result}, result.ndim={getattr(result, 'ndim', None)}")
+    print(f"  mask shape={mask.shape}, mask.sum()={mask.sum()}, mask.size={mask.size}")
+    if axis is not None and getattr(result, "ndim", False):
+        print("  branch 1")
+        if hasattr(axis, "__len__"):
+            total_elements = np.prod([mask.shape[i] for i in axis])
+        else:
+            total_elements = mask.shape[axis]
+        valid_elements = total_elements - mask.sum(axis)
+        null_mask = (valid_elements - min_count) < 0
+        print(f"    total_elements={total_elements}, valid_elements={valid_elements}, null_mask={null_mask}")
+        if null_mask.any():
+            print("    would replace with fill_value")
+    elif getattr(result, "dtype", None) not in nanops.dtypes.NAT_TYPES:
+        print("  branch 2")
+        null_mask = mask.size - mask.sum()
+        print(f"    scalar null_mask={null_mask}, null_mask < min_count? {null_mask < min_count}")
+        if null_mask < min_count:
+            result = np.nan
+            print(f"    set result = np.nan")
+    else:
+        print("  branch else")
+    out = original(result, axis, mask, min_count)
+    print(f"  output={out}")
+    return out
+
+nanops._maybe_null_out = debug_maybe_null_out
+# Need to also patch nanops.nansum? Actually nansum uses _maybe_null_out directly, but nansum is imported in duck_array_ops.
+# Let's reload duck_array_ops to pick up the patched version? Too complex.
+# Instead, we can directly test the logic by calling nansum with our own inputs but using the patched nanops.
+# However, nansum is imported into duck_array_ops at module level. Changing nanops._maybe_null_out after import may not affect because nansum references the original function.
+# Let's just test using the actual DataArray sum which will go through the whole chain.
+# But we can also directly call nanops.nansum.
+# Let's import nanops again after patching.
+import importlib
+importlib.reload(nanops)
+# Now nansum will use the patched version? Actually nansum is a function in nanops module, not a reference to _maybe_null_out.
+# Since we patched nanops._maybe_null_out, nansum will use the patched version because it imports _maybe_null_out from the same module (which is the patched one).
+# Let's verify.
+import xarray as xr
+
+da = xr.DataArray([[1., np.nan, 3.],
+                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
+print("\nTest min_count=5 over both dims:")
+result = da.sum(['dim0', 'dim1'], min_count=5)
+print("Result:", result.values)
diff --git a/debug_insert.py b/debug_insert.py
new file mode 100644
index 00000000..dff98237
--- /dev/null
+++ b/debug_insert.py
@@ -0,0 +1,54 @@
+import sys
+import os
+# Read file
+with open('xarray/core/nanops.py', 'r') as f:
+    lines = f.readlines()
+# Find line index of the line after docstring
+for i, line in enumerate(lines):
+    if line.strip().startswith('def _maybe_null_out'):
+        # find the line after docstring
+        j = i + 1
+        while j < len(lines) and lines[j].strip().startswith('\"\"\"'):
+            j += 1
+        # now lines[j] is first line of code after docstring
+        # Insert print at j
+        indent = len(lines[j]) - len(lines[j].lstrip())
+        lines.insert(j, ' ' * indent + 'import sys\n')
+        lines.insert(j+1, ' ' * indent + 'print(\"DEBUG: axis=%s, min_count=%s, result.ndim=%s\" % (axis, min_count, getattr(result, \"ndim\", None)), file=sys.stderr)\n')
+        break
+# Write back
+with open('xarray/core/nanops.py', 'w') as f:
+    f.writelines(lines)
+print('Inserted debug print')
+# Run test
+import xarray as xr
+import numpy as np
+da = xr.DataArray([[1., np.nan, 3.],
+                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
+print('\nTest min_count=5 over both dims:')
+result = da.sum(['dim0', 'dim1'], min_count=5)
+print('Result:', result.values)
+# Restore original
+with open('xarray/core/nanops.py', 'r') as f:
+    lines = f.readlines()
+# Find start and end of function again
+for i, line in enumerate(lines):
+    if line.strip().startswith('def _maybe_null_out'):
+        start = i
+        break
+indent = len(lines[start]) - len(lines[start].lstrip())
+end = None
+for i in range(start + 1, len(lines)):
+    if lines[i].strip() == '':
+        continue
+    if len(lines[i]) - len(lines[i].lstrip()) == indent and lines[i].lstrip().startswith('def '):
+        end = i
+        break
+if end is None:
+    end = len(lines)
+# Remove the inserted lines (the two lines we added)
+# We'll just replace the whole function with the corrected version (without debug).
+# Let's copy from backup again.
+import shutil
+shutil.copy('xarray/core/nanops.py.bak2', 'xarray/core/nanops.py')
+print('Restored original')
diff --git a/debug_min_count.py b/debug_min_count.py
new file mode 100644
index 00000000..5c44eab0
--- /dev/null
+++ b/debug_min_count.py
@@ -0,0 +1,39 @@
+import xarray as xr
+import xarray.core.nanops as nanops
+import numpy as np
+
+original = nanops._maybe_null_out
+def debug_maybe_null_out(result, axis, mask, min_count=1):
+    print(f"DEBUG: result={result}, axis={axis}, mask shape={mask.shape}, min_count={min_count}")
+    print(f"  result.ndim={getattr(result, 'ndim', 'no ndim')}")
+    print(f"  result.dtype={getattr(result, 'dtype', 'no dtype')}")
+    if axis is not None and getattr(result, "ndim", False):
+        print("  branch 1")
+    elif getattr(result, "dtype", None) not in nanops.dtypes.NAT_TYPES:
+        print("  branch 2")
+    else:
+        print("  branch else")
+    out = original(result, axis, mask, min_count)
+    print(f"  output={out}")
+    return out
+
+nanops._maybe_null_out = debug_maybe_null_out
+# Now test
+import xarray.core.nanops as nanops2
+# Ensure sum uses our patched version
+import xarray.core.duck_array_ops as daops
+print("daops.sum:", daops.sum)
+print("daops.sum.__module__:", daops.sum.__module__)
+
+# Reset by re-importing? Let's just test using DataArray after monkey patch
+import sys
+sys.modules['xarray.core.nanops'] = nanops2
+# But duck_array_ops already imported nanops, need to reload
+import importlib
+importlib.reload(xarray.core.duck_array_ops)
+
+da = xr.DataArray([[1., np.nan, 3.],
+                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
+print("\nTest min_count=5 over both dims:")
+result = da.sum(['dim0', 'dim1'], min_count=5)
+print("Result:", result.values)
diff --git a/patch_with_debug.py b/patch_with_debug.py
new file mode 100644
index 00000000..1d351316
--- /dev/null
+++ b/patch_with_debug.py
@@ -0,0 +1,43 @@
+import sys
+with open('xarray/core/nanops.py', 'r') as f:
+    content = f.read()
+
+# Find the function using a simple regex (since the file is not huge)
+import re
+pattern = r'(def _maybe_null_out\(result, axis, mask, min_count=1\):\s*\"\"\"\s*xarray version of pandas.core.nanops._maybe_null_out\s*\"\"\"\s*)'
+match = re.search(pattern, content, re.DOTALL)
+if not match:
+    sys.exit('Function not found')
+# Replace with debug version
+new_func = '''def _maybe_null_out(result, axis, mask, min_count=1):
+    \"\"\"
+    xarray version of pandas.core.nanops._maybe_null_out
+    \"\"\"
+    import sys
+    print(\"[_maybe_null_out] axis=%s, min_count=%s, result.ndim=%s\" % (axis, min_count, getattr(result, \"ndim\", None)), file=sys.stderr)
+    if axis is not None and getattr(result, \"ndim\", False):
+        if hasattr(axis, \"__len__\"):  # tuple or list of axes
+            total_elements = np.prod([mask.shape[i] for i in axis])
+        else:
+            total_elements = mask.shape[axis]
+        valid_elements = total_elements - mask.sum(axis)
+        null_mask = (valid_elements - min_count) < 0
+        print(\"  total_elements=%s, valid_elements=%s, null_mask=%s\" % (total_elements, valid_elements, null_mask), file=sys.stderr)
+        if null_mask.any():
+            dtype, fill_value = dtypes.maybe_promote(result.dtype)
+            result = result.astype(dtype)
+            result[null_mask] = fill_value
+
+    elif getattr(result, \"dtype\", None) not in dtypes.NAT_TYPES:
+        null_mask = mask.size - mask.sum()
+        print(\"  scalar null_mask=%s\" % null_mask, file=sys.stderr)
+        if null_mask < min_count:
+            result = np.nan
+
+    return result
+'''
+# Use re.sub with the matched pattern
+new_content = re.sub(pattern, new_func, content, flags=re.DOTALL)
+with open('xarray/core/nanops.py', 'w') as f:
+    f.write(new_content)
+print('Patched with debug prints')
diff --git a/test_min_count.py b/test_min_count.py
new file mode 100644
index 00000000..881b8258
--- /dev/null
+++ b/test_min_count.py
@@ -0,0 +1,68 @@
+import numpy as np
+import xarray as xr
+
+print("Testing min_count with single axis reduction")
+# Create a 2D array with NaNs
+da = xr.DataArray([[1., np.nan, 3.],
+                   [4., 5., np.nan]], dims=['dim0', 'dim1'])
+print("DataArray:", da.values)
+print("NaN positions:", np.isnan(da.values))
+
+# min_count = 1, there is at least one non-NaN in each row and column
+# reduction over dim0 (axis 0) should compute sum over each column
+# column 0: 1+4 =5 (both non-NaN) -> 5
+# column 1: NaN+5 =0+5 =5 (but NaN replaced with 0) ->5
+# column 2: 3+NaN =3 ->3
+# Since min_count=1 satisfied (2 non-NaN per column?), we get those sums
+result = da.sum('dim0', min_count=1)
+print("sum over dim0:", result.values)
+assert np.allclose(result.values, [5., 5., 3.])
+
+# min_count = 2, column 0 has 2 non-NaN -> sum 5, column1 has only 1 non-NaN (5) -> should be NaN
+result2 = da.sum('dim0', min_count=2)
+print("sum over dim0 min_count=2:", result2.values)
+assert np.isnan(result2.values[1])
+assert np.allclose(result2.values[0], 5.)
+# compute non-NaN counts per column
+non_nan_counts = np.sum(~np.isnan(da.values), axis=0)
+print("Non-NaN counts per column:", non_nan_counts)
+# column2 count=1 -> NaN
+assert np.isnan(result2.values[2])
+print("Single axis test passed")
+
+# Test multi-axis reduction (the issue)
+print("\nTesting multi-axis reduc
…[cut, 29803 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
