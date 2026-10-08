# Item 7

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



## The agent's commands, in order (137; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed`
3. `find /testbed/xarray -name "nanops.py" -type f`
4. `grep -n "min_count" /testbed/xarray/core/nanops.py`
5. `sed -n '20,60p' /testbed/xarray/core/nanops.py`
6. `sed -n '111,120p' /testbed/xarray/core/nanops.py`
7. `sed -n '1,30p' /testbed/xarray/core/nanops.py`
8. `grep -r "min_count" /testbed/xarray/tests --include="*.py" | head -20`
9. `grep -B5 -A10 "def test_min_count_nd" /testbed/xarray/tests/test_duck_array_ops.py`
10. `cd /testbed && python -m pytest xarray/tests/test_duck_array_ops.py::test_min_count_nd -xvs 2>&1 | head -50`
11. `cd /testbed && check 2>&1 | head -30`
12. `which pytest`
13. `find /testbed -name "check" -type f`
14. `ls -la /testbed/Makefile`
15. `cat /testbed/conftest.py`
16.
```
cd /testbed && python -c "
import xarray as xr
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
try:
    result = da.sum(['dim_0', 'dim_1'], min_count=1)
    print('Success:', result)
except Exception as e:
    print('Error:', e)
"
```
17. `grep -r "pandas.core.nanops" /testbed/xarray`
18. `find /testbed/xarray/tests -name "*nanops*" -type f`
19. `cd /testbed && pip install pytest -q 2>&1 | tail -5`
20. `ls -la /testbed/ | grep -E "check|pytest"`
21. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -5`
22. `sed -n '/def test_min_count_nd/,/^def /p' /testbed/xarray/tests/test_duck_array_ops.py | head -30`
23. `sed -n '/def test_min_count/,/^def /p' /testbed/xarray/tests/test_duck_array_ops.py | head -40`
24. `grep -n "series_reduce" /testbed/xarray/tests/test_duck_array_ops.py`
25. `sed -n '259,270p' /testbed/xarray/tests/test_duck_array_ops.py`
26. `find /testbed -type f -name "pytest" -path "*/site-packages/*" 2>/dev/null | head -5`
27. `ls -la /opt/miniconda3/envs/testbed/`
28. `/opt/miniconda3/envs/testbed/bin/pytest --version 2>&1 | head -5`
29. `ls -la /opt/miniconda3/envs/testbed/bin/ | grep pytest`
30. `/opt/miniconda3/envs/testbed/bin/python -m pytest --version 2>&1 | head -5`
31. `find /testbed -type f -name "pytest" -o -name "pytest.py" 2>/dev/null`
32. `grep -r "check" /testbed/.github --include="*.yml" | head -5`
33. `cd /testbed && check 2>&1 | head -10`
34. `which check`
35. `head -30 /usr/local/bin/check`
36. `sed -n '/def test_multiple_dims/,/^def /p' /testbed/xarray/tests/test_duck_array_ops.py | head -50`
37. `head -20 /testbed/xarray/core/nanops.py`
38.
```
cd /testbed && python -c "
import numpy as np
import xarray as xr
# Let's examine the mask and axis
mask = np.array([[True, False, False], [False, True, False]])
print('mask shape:', mask.shape)
axis = (0,1)
print('axis:', axis)
print('mask.sum(axis):', mask.sum(axis))
print('mask.shape:', mask.shape)
print('np.take(mask.shape, axis):', np.take(mask.shape, axis))
print('np.take(mask.shape, axis).p …[cut]
```
39. `sed -n '25,55p' /testbed/xarray/core/nanops.py`
40.
```
cd /testbed && python -c "
import numpy as np
shape = (2,3,4)
axis = 1
print('shape[axis]:', shape[axis])
print('np.take(shape, axis):', np.take(shape, axis))
print('type:', type(np.take(shape, axis)))
print('np.take(shape, axis).prod():', np.take(shape, axis).prod())
"
```
41. `cd /testbed && cp xarray/core/nanops.py xarray/core/nanops.py.backup`
42.
```
cd /testbed && cat > /tmp/modify_nanops.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find the function _maybe_null_out
in_func = False
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        in_func = True
    if in_func and line.strip() == '':
        # maybe end of function? we'll just replace specific l …[cut]
```
43. `cd /testbed && python /tmp/modify_nanops.py 2>&1`
44. `sed -n '25,55p' /testbed/xarray/core/nanops.py`
45.
```
cd /testbed && python -c "
import xarray as xr
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
try:
    result = da.sum(['dim_0', 'dim_1'], min_count=1)
    print('Success:', result)
except Exception as e:
    print('Error:', e)
"
```
46.
```
cd /testbed && python -c "
import xarray as xr
import numpy as np
# Case 1: no NaN, min_count=1, should succeed
da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
print('Case 1:', da.sum(['dim_0', 'dim_1'], min_count=1).values)
# Case 2: one NaN, min_count=1, total non-null = 5, should succeed
import copy
da2 = da.copy()
da2[0,0] = np.nan
print('Case 2:', da2.sum(['dim_0', 'dim_1'], min_count=1).values)
# …[cut]
```
47.
```
cd /testbed && python -c "
import xarray as xr
import numpy as np
allnan = xr.DataArray([[np.nan, np.nan], [np.nan, np.nan]])
print('allnan sum:', allnan.sum())
print('type:', type(allnan.sum().values))
"
```
48.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from xarray.core.nanops import _maybe_null_out
import numpy as np
import xarray as xr
# Simulate the case where axis reduces all dimensions
da = xr.DataArray([[np.nan, np.nan], [np.nan, np.nan]])
from xarray.core.nanops import _replace_nan
result, mask = _replace_nan(da.values, 0)
print('result shape:', result.shape)
print('mask shape:' …[cut]
```
49. `find /opt/miniconda3/envs/testbed -name "pytest*" -type f 2>/dev/null | head -5`
50. `cd /testbed && python -c "import sys; print(sys.executable)"`
51. `/opt/miniconda3/envs/testbed/bin/python -m pip list 2>&1 | grep pytest`
52. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python -m pytest xarray/tests/test_duck_array_ops.py::test_min_count_nd -xvs 2>&1 | head -80`
53. `/opt/miniconda3/envs/testbed/bin/python -c "import pytest; print(pytest.__version__)" 2>&1`
54. `/opt/miniconda3/envs/testbed/bin/python -m pip freeze | grep -E "^pytest" 2>&1 | head -10`
55. `cat /usr/local/bin/check`
56. `cat /tmp/.mp_check_out 2>&1 | head -5`
57. `which -a check`
58. `cd /testbed && cat /usr/local/bin/check 2>&1 | wc -l`
59. `type check`
60. `find /opt/miniconda3/envs/testbed -name "pytest-*.dist-info" -o -name "pytest*.egg-info" 2>/dev/null`
61. `find /opt/miniconda3/envs/testbed/lib/python3.10/site-packages -name "pytest" -type d 2>/dev/null | head -5`
62. `ls /opt/miniconda3/envs/testbed/lib/python3.10/site-packages/ | grep pytest`
63. `which pytest 2>/dev/null || echo "not found"`
64. `ls -la /usr/local/bin/ | grep pytest`
65. `ls -l /usr/local/bin/check`
66. `echo $PS1`
67. `/usr/bin/python3 -m pytest --version 2>&1 | head -5`
68.
```
cd /testbed && cat > /tmp/test_nanops.py << 'EOF'
import sys
sys.path.insert(0, '.')
import numpy as np
import xarray as xr
from xarray.core.nanops import _maybe_null_out, nansum, nanprod

print("Testing _maybe_null_out with single axis")
# Create dummy data
result = np.array([[1., 2., 3.], [4., 5., 6.]])
mask = np.array([[False, True, False], [False, False, True]])  # True where null
axis = 1  #  …[cut]
```
69. `grep -n "_dask_or_eager_func" /testbed/xarray/core/duck_array_ops.py | head -5`
70. `sed -n '26,70p' /testbed/xarray/core/duck_array_ops.py`
71. `grep -r "nansum" /testbed/xarray/core/ --include="*.py" | grep -v "\.pyc" | head -10`
72. `grep -n "def reduce" /testbed/xarray/core/variable.py`
73. `sed -n '1580,1700p' /testbed/xarray/core/variable.py`
74. `grep -n "def sum" /testbed/xarray/core/dataarray.py`
75. `grep -r "nansum" /testbed/xarray --include="*.py" | grep -v "\.pyc" | grep -v "def nansum" | head -10`
76. `grep -n "sum" /testbed/xarray/core/dataarray.py | head -20`
77. `grep -r "def sum" /testbed/xarray --include="*.py" | grep -v "\.pyc" | head -10`
78. `grep -r "min_count" /testbed/xarray --include="*.py" | grep -v "\.pyc" | grep -v "test" | head -30`
79. `grep -r "min_count" /testbed/xarray --include="*.py" 2>/dev/null | head -30`
80. `grep -n "sum" /testbed/xarray/core/duck_array_ops.py | head -20`
81. `grep -n "_create_nan_agg_method" /testbed/xarray/core/duck_array_ops.py -A 20`
82. `grep -r "class _Reduce" /testbed/xarray --include="*.py"`
83. `grep -n "skipna" /testbed/xarray/core/dataarray.py | head -10`
84. `head -50 /testbed/xarray/core/dataarray.py`
85. `grep -n "sum" /testbed/xarray/core/common.py | head -20`
86. `grep -n "_Reduce" /testbed/xarray/core/dataarray.py`
87. `grep -r "class _Reduce" /testbed/xarray --include="*.py"`
88. `grep -n "__array_function__" /testbed/xarray/core/ops.py`
89. `grep -n "sum" /testbed/xarray/core/ops.py | head -20`
90. `sed -n '1,100p' /testbed/xarray/core/ops.py`
91. `grep -n "def inject" /testbed/xarray/core/ops.py`
92. `sed -n '253,279p' /testbed/xarray/core/ops.py`
93. `grep -n "_reduce_method" /testbed/xarray/core/ops.py -A 30`
94. `grep -n "_reduce_method" /testbed/xarray/core/common.py -A 50`
95. `grep -n "class ImplementsArrayReduce" /testbed/xarray/core/common.py -A 100`
96. `grep -n "def reduce" /testbed/xarray/core/common.py -A 30`
97. `grep -n "^class" /testbed/xarray/core/common.py`
98. `sed -n '113,200p' /testbed/xarray/core/common.py`
99. `grep -n "def reduce" /testbed/xarray/core/dataarray.py -A 30`
100. `ls -l /usr/local/bin/check 2>&1`
101. `type -a check`
102. `ls -l /tmp/.mp_check* 2>&1`
103. `cd /testbed && /usr/local/bin/check 2>&1 | head -5`
104. `find /testbed -name "check" -type f 2>/dev/null`
105.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
import numpy as np
from xarray.core.nanops import _maybe_null_out

# Simulate axis = (0,1) and result scalar (0-d array)
# In nansum, result is the output of _dask_or_eager_func('sum') which returns a scalar? Let's assume.
# For all NaN, result = 0 (as we saw). That's what we got.
# Let's just call _maybe_null_out with result = 0 (scala …[cut]
```
106.
```
cd /testbed && python -c "
result = np.array(0.)
axis = (0,1)
print('axis is not None:', axis is not None)
print('getattr(result, \"ndim\", False):', getattr(result, 'ndim', False))
print('bool(getattr(...)):', bool(getattr(result, 'ndim', False)))
print('Condition:', axis is not None and getattr(result, 'ndim', False))
"
```
107. `cd /testbed && cp xarray/core/nanops.py xarray/core/nanops.py.backup2`
108.
```
cd /testbed && cat > /tmp/debug_nanops.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find the function _maybe_null_out
in_func = False
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        in_func = True
    if in_func and line.strip().startswith('return result'):
        # Insert before return
        in …[cut]
```
109. `sed -n '25,70p' /testbed/xarray/core/nanops.py`
110.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
import numpy as np
from xarray.core.nanops import _maybe_null_out

result = np.array(0.)
mask = np.array([[True, True], [True, True]])
axis = (0,1)
min_count = 1
print('Calling...')
new_result = _maybe_null_out(result, axis, mask, min_count)
print('new_result:', new_result)
" 2>&1
```
111. `sed -n '25,80p' /testbed/xarray/core/nanops.py | cat -n`
112. `cd /testbed && cp xarray/core/nanops.py.backup2 xarray/core/nanops.py`
113.
```
cd /testbed && cat > /tmp/fix_nanops.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Remove the error line block
# Find line with "if hasattr(axis, "__len__"):"
for i, line in enumerate(lines):
    if 'if hasattr(axis, "__len__"):' in line:
        # Find the next few lines until the line after the raise ValueError
        # We'll delete from i to  …[cut]
```
114. `sed -n '25,60p' /testbed/xarray/core/nanops.py`
115.
```
cd /testbed && cat > /tmp/add_debug.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find the function _maybe_null_out
for i, line in enumerate(lines):
    if line.strip().startswith('def _maybe_null_out'):
        # Insert after docstring
        j = i
        while j < len(lines) and not lines[j].strip().startswith('    if axis is not None'):
     …[cut]
```
116. `sed -n '111,120p' /testbed/xarray/core/nanops.py`
117. `sed -n '111,130p' /testbed/xarray/core/nanops.py`
118. `grep -n "def nansum" /testbed/xarray/core/nanops.py`
119. `sed -n '107,125p' /testbed/xarray/core/nanops.py`
120. `cd /testbed && cp xarray/core/nanops.py xarray/core/nanops.py.backup3`
121.
```
cd /testbed && cat > /tmp/patch_debug.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    content = f.read()

# Find the function definition and insert after docstring
# Simple approach: replace the line after the docstring with a print.
# We'll locate "def _maybe_null_out(result, axis, mask, min_count=1):"
# then find the next line that is not empty and not a docstring line.
 …[cut]
```
122. `sed -n '25,80p' /testbed/xarray/core/nanops.py`
123. `cd /testbed && cp xarray/core/nanops.py.backup3 xarray/core/nanops.py`
124.
```
cd /testbed && cat > /tmp/debug2.py << 'EOF'
import sys
sys.path.insert(0, '.')
import xarray.core.nanops as nanops
import numpy as np

original = nanops._maybe_null_out

def debug_maybe_null_out(result, axis, mask, min_count=1):
    print("DEBUG: axis=", axis)
    print("DEBUG: result.ndim=", getattr(result, 'ndim', False))
    print("DEBUG: result.dtype=", getattr(result, 'dtype', None))
    pri …[cut]
```
125.
```
cd /testbed && cat > /tmp/patch_elif.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if line.strip().startswith('elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:'):
        # Insert debug prints after this line, with same indentation as the next  …[cut]
```
126.
```
cd /testbed && python -c "
import numpy as np
mask = np.array([[True, True], [True, True]])
print('mask.size:', mask.size)
print('mask.sum():', mask.sum())
null_mask = mask.size - mask.sum()
print('null_mask:', null_mask)
print('type:', type(null_mask))
min_count = 1
print('null_mask < min_count:', null_mask < min_count)
print('bool:', bool(null_mask < min_count))
"
```
127.
```
cd /testbed && cat > /tmp/insert_print.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Find the line with "if null_mask < min_count:"
for i, line in enumerate(lines):
    if 'if null_mask < min_count:' in line:
        indent = len(line) - len(line.lstrip())
        indent_str = ' ' * indent
        # Insert after this line, before the next line at …[cut]
```
128. `cd /testbed && python /tmp/debug2.py 2>&1`
129. `sed -n '25,70p' /testbed/xarray/core/nanops.py`
130. `grep -n "null_mask = mask.size - mask.sum()" /testbed/xarray/core/nanops.py`
131.
```
cd /testbed && cat > /tmp/insert_print2.py << 'EOF'
import sys
with open('xarray/core/nanops.py', 'r') as f:
    lines = f.readlines()

# Insert after line 38 (0-indexed 37)
indent = len(lines[37]) - len(lines[37].lstrip())
indent_str = ' ' * indent
lines.insert(38, indent_str + '    print("DEBUG: null_mask =", null_mask)\n')

with open('xarray/core/nanops.py', 'w') as f:
    f.writelines(lines)
E …[cut]
```
132. `cd /testbed && python /tmp/debug2.py 2>&1`
133. `sed -n '38p' /testbed/xarray/core/nanops.py | cat -A`
134.
```
cd /testbed && cat > /tmp/final_test.py << 'EOF'
import sys
sys.path.insert(0, '.')
# Monkey-patch before importing xarray
import xarray.core.nanops as nanops
original = nanops._maybe_null_out

def patched(result, axis, mask, min_count=1):
    print("DEBUG: axis=", axis)
    print("DEBUG: result.ndim=", getattr(result, 'ndim', False))
    print("DEBUG: result.dtype=", getattr(result, 'dtype', None …[cut]
```
135. `sed -n '35,45p' /testbed/xarray/core/nanops.py`
136. `grep -n "NAT_TYPES" /testbed/xarray/core/dtypes.py`
137.
```
cd /testbed && python -c "
import numpy as np
# Simulate the second branch logic
mask = np.array([[True, True], [True, True]])
null_mask = mask.size - mask.sum()
print('null_mask:', null_mask)
print('null_mask < 1:', null_mask < 1)
print('bool:', bool(null_mask < 1))
"
```

## The agent's last reasoning (last 3 turns)

```
The indentation error is blocking any import. We must fix it. Let's restore the file from backup3 and apply a proper fix. We'll also fix the min_count bug. We need to understand why the assignment didn't happen. Let's examine the original pandas _maybe_null_out (maybe we can find a reference). But we can also look at the xarray source code on GitHub. However, we can infer from the existing code that the second branch is intended for scalar reduction (axis reduces all dimensions). The condition `null_mask < min_count` uses `<` between a scalar and an integer. That should work. But maybe the `null_mask` variable is not a scalar? Let's check: `mask.size - mask.sum()` returns a numpy scalar (int64). That's fine. Maybe the issue is that `result` is not a numpy array but a dask array? In our test, it's a numpy array. The assignment `result = np.nan` changes the local variable, but maybe the caller expects a numpy array and assigns it back? Actually nansum returns the result of _maybe_null_out, which is the local variable `result`. That should be fine. Let's look at the actual call chain: nansum -> _maybe_null_out -> returns result. That's it. Thus the bug must be in the condition `null_mask < min_count` evaluating to False. Let's compute with the actual values inside the function. We'll need to see the actual values. Since we cannot import due to indentation error, we must fix the indentation first. Let's restore the file again and then apply a proper edit using a more robust method: we'll write a new version of the function with prints and replace the entire function. But we need to be careful not to break other functions. Alternatively, we can fix the indentation by checking the line numbers. Let's open the file and see line 39.
...
Ah! The indentation is wrong. The print line is indented more than it should be (extra spaces). It's aligned with the if block? Actually it's aligned with the null_mask line? It's indented by 12 spaces? This is because our insert script inserted with the indentation of the next line (which is 12 spaces?). This broke the syntax. We need to fix the indentation. Let's restore from backup3 and start over with a clean fix that also fixes the bug (maybe the bug is that the second branch is never executed because axis is not None but result.ndim == 0? Wait, we already determined that condition is false, so we go to elif branch. That branch is executed (since we saw the print lines from our debug wrapper? Actually we didn't see prints, meaning the elif branch didn't execute. That's because the condition `getattr(result, "dtype", None) not in dtypes.NAT_TYPES` might be False? But result.dtype is float64, which is not NAT_TYPES. So it should be True. Unless dtypes.NAT_TYPES includes float? Let's check. We can quickly look at dtypes.NAT_TYPES.
...
So NAT_TYPES only contains datetime64 NaT and timedelta64 NaT. So float is not in there. So condition is True. Thus the elif branch should execute. Yet our prints didn't show. That means the elif branch didn't execute because the previous condition `if axis is not None and getattr(result, "ndim", False):` evaluated to True? Wait, we already determined that condition is False because result.ndim == 0. But maybe `getattr(result, "ndim", False)` returns something else? Let's double-check: `result` is a numpy array with shape (). Its ndim attribute is 0. So `getattr(result, "ndim", False)` returns 0, which is falsy. So condition is False. Thus the elif branch should be executed. Something else is happening: maybe the function we are calling is not the one we edited because the module is cached. Our debug wrapper replaced the function in the module, but the debug wrapper printed the debug lines we added? Actually we added prints to the original file, but the debug wrapper calls the original function (which is the one we edited). However, the debug wrapper printed its own debug lines, not the ones from the file. That's fine. But we didn't see the prints from the file because 
…[cut, 540 more chars]
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/xarray/core/nanops.py b/xarray/core/nanops.py
index 41c8d258..0559a4e9 100644
--- a/xarray/core/nanops.py
+++ b/xarray/core/nanops.py
@@ -26,13 +26,9 @@ def _maybe_null_out(result, axis, mask, min_count=1):
     """
     xarray version of pandas.core.nanops._maybe_null_out
     """
-    if hasattr(axis, "__len__"):  # if tuple or list
-        raise ValueError(
-            "min_count is not available for reduction with more than one dimensions."
-        )
 
     if axis is not None and getattr(result, "ndim", False):
-        null_mask = (mask.shape[axis] - mask.sum(axis) - min_count) < 0
+        null_mask = (np.take(mask.shape, axis).prod() - mask.sum(axis) - min_count) < 0
         if null_mask.any():
             dtype, fill_value = dtypes.maybe_promote(result.dtype)
             result = result.astype(dtype)
@@ -40,7 +36,10 @@ def _maybe_null_out(result, axis, mask, min_count=1):
 
     elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:
         null_mask = mask.size - mask.sum()
+            print("DEBUG: null_mask =", null_mask)
         if null_mask < min_count:
+            print("DEBUG: entering if block")
+            print("DEBUG: result before assignment:", result)
             result = np.nan
 
     return result
diff --git a/xarray/core/nanops.py.backup b/xarray/core/nanops.py.backup
new file mode 100644
index 00000000..41c8d258
--- /dev/null
+++ b/xarray/core/nanops.py.backup
@@ -0,0 +1,199 @@
+import numpy as np
+
+from . import dtypes, nputils, utils
+from .duck_array_ops import _dask_or_eager_func, count, fillna, isnull, where_method
+from .pycompat import dask_array_type
+
+try:
+    import dask.array as dask_array
+
+    from . import dask_array_compat
+except ImportError:
+    dask_array = None
+    dask_array_compat = None  # type: ignore
+
+
+def _replace_nan(a, val):
+    """
+    replace nan in a by val, and returns the replaced array and the nan
+    position
+    """
+    mask = isnull(a)
+    return where_method(val, mask, a), mask
+
+
+def _maybe_null_out(result, axis, mask, min_count=1):
+    """
+    xarray version of pandas.core.nanops._maybe_null_out
+    """
+    if hasattr(axis, "__len__"):  # if tuple or list
+        raise ValueError(
+            "min_count is not available for reduction with more than one dimensions."
+        )
+
+    if axis is not None and getattr(result, "ndim", False):
+        null_mask = (mask.shape[axis] - mask.sum(axis) - min_count) < 0
+        if null_mask.any():
+            dtype, fill_value = dtypes.maybe_promote(result.dtype)
+            result = result.astype(dtype)
+            result[null_mask] = fill_value
+
+    elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:
+        null_mask = mask.size - mask.sum()
+        if null_mask < min_count:
+            result = np.nan
+
+    return result
+
+
+def _nan_argminmax_object(func, fill_value, value, axis=None, **kwargs):
+    """ In house nanargmin, nanargmax for object arrays. Always return integer
+    type
+    """
+    valid_count = count(value, axis=axis)
+    value = fillna(value, fill_value)
+    data = _dask_or_eager_func(func)(value, axis=axis, **kwargs)
+
+    # TODO This will evaluate dask arrays and might be costly.
+    if (valid_count == 0).any():
+        raise ValueError("All-NaN slice encountered")
+
+    return data
+
+
+def _nan_minmax_object(func, fill_value, value, axis=None, **kwargs):
+    """ In house nanmin and nanmax for object array """
+    valid_count = count(value, axis=axis)
+    filled_value = fillna(value, fill_value)
+    data = getattr(np, func)(filled_value, axis=axis, **kwargs)
+    if not hasattr(data, "dtype"):  # scalar case
+        data = fill_value if valid_count == 0 else data
+        # we've computed a single min, max value of type object.
+        # don't let np.array turn a tuple back into an array
+        return utils.to_0d_object_array(data)
+    return where_method(data, valid_count != 0)
+
+
+def nanmin(a, axis=None, out=None):
+    if a.dtype.kind == "O":
+        return _nan_minmax_object("min", dtypes.get_pos_infinity(a.dtype), a, axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanmin(a, axis=axis)
+
+
+def nanmax(a, axis=None, out=None):
+    if a.dtype.kind == "O":
+        return _nan_minmax_object("max", dtypes.get_neg_infinity(a.dtype), a, axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanmax(a, axis=axis)
+
+
+def nanargmin(a, axis=None):
+    if a.dtype.kind == "O":
+        fill_value = dtypes.get_pos_infinity(a.dtype)
+        return _nan_argminmax_object("argmin", fill_value, a, axis=axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanargmin(a, axis=axis)
+
+
+def nanargmax(a, axis=None):
+    if a.dtype.kind == "O":
+        fill_value = dtypes.get_neg_infinity(a.dtype)
+        return _nan_argminmax_object("argmax", fill_value, a, axis=axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanargmax(a, axis=axis)
+
+
+def nansum(a, axis=None, dtype=None, out=None, min_count=None):
+    a, mask = _replace_nan(a, 0)
+    result = _dask_or_eager_func("sum")(a, axis=axis, dtype=dtype)
+    if min_count is not None:
+        return _maybe_null_out(result, axis, mask, min_count)
+    else:
+        return result
+
+
+def _nanmean_ddof_object(ddof, value, axis=None, dtype=None, **kwargs):
+    """ In house nanmean. ddof argument will be used in _nanvar method """
+    from .duck_array_ops import _dask_or_eager_func, count, fillna, where_method
+
+    valid_count = count(value, axis=axis)
+    value = fillna(value, 0)
+    # As dtype inference is impossible for object dtype, we assume float
+    # https://github.com/dask/dask/issues/3162
+    if dtype is None and value.dtype.kind == "O":
+        dtype = value.dtype if value.dtype.kind in ["cf"] else float
+
+    data = _dask_or_eager_func("sum")(value, axis=axis, dtype=dtype, **kwargs)
+    data = data / (valid_count - ddof)
+    return where_method(data, valid_count != 0)
+
+
+def nanmean(a, axis=None, dtype=None, out=None):
+    if a.dtype.kind == "O":
+        return _nanmean_ddof_object(0, a, axis=axis, dtype=dtype)
+
+    if isinstance(a, dask_array_type):
+        return dask_array.nanmean(a, axis=axis, dtype=dtype)
+
+    return np.nanmean(a, axis=axis, dtype=dtype)
+
+
+def nanmedian(a, axis=None, out=None):
+    # The dask algorithm works by rechunking to one chunk along axis
+    # Make sure we trigger the dask error when passing all dimensions
+    # so that we don't rechunk the entire array to one chunk and
+    # possibly blow memory
+    if axis is not None and len(np.atleast_1d(axis)) == a.ndim:
+        axis = None
+    return _dask_or_eager_func(
+        "nanmedian", dask_module=dask_array_compat, eager_module=nputils
+    )(a, axis=axis)
+
+
+def _nanvar_object(value, axis=None, ddof=0, keepdims=False, **kwargs):
+    value_mean = _nanmean_ddof_object(
+        ddof=0, value=value, axis=axis, keepdims=True, **kwargs
+    )
+    squared = (value.astype(value_mean.dtype) - value_mean) ** 2
+    return _nanmean_ddof_object(ddof, squared, axis=axis, keepdims=keepdims, **kwargs)
+
+
+def nanvar(a, axis=None, dtype=None, out=None, ddof=0):
+    if a.dtype.kind == "O":
+        return _nanvar_object(a, axis=axis, dtype=dtype, ddof=ddof)
+
+    return _dask_or_eager_func("nanvar", eager_module=nputils)(
+        a, axis=axis, dtype=dtype, ddof=ddof
+    )
+
+
+def nanstd(a, axis=None, dtype=None, out=None, ddof=0):
+    return _dask_or_eager_func("nanstd", eager_module=nputils)(
+        a, axis=axis, dtype=dtype, ddof=ddof
+    )
+
+
+def nanprod(a, axis=None, dtype=None, out=None, min_count=None):
+    a, mask = _replace_nan(a, 1)
+    result = _dask_or_eager_func("nanprod")(a, axis=axis, dtype=dtype, out=out)
+    if min_count is not None:
+        return _maybe_null_out(result, axis, mask, min_count)
+    else:
+        return result
+
+
+def nancumsum(a, axis=None, dtype=None, out=None):
+    return _dask_or_eager_func("nancumsum", eager_module=nputils)(
+        a, axis=axis, dtype=dtype
+    )
+
+
+def nancumprod(a, axis=None, dtype=None, out=None):
+    return _dask_or_eager_func("nancumprod", eager_module=nputils)(
+        a, axis=axis, dtype=dtype
+    )
diff --git a/xarray/core/nanops.py.backup2 b/xarray/core/nanops.py.backup2
new file mode 100644
index 00000000..bc7dc510
--- /dev/null
+++ b/xarray/core/nanops.py.backup2
@@ -0,0 +1,195 @@
+import numpy as np
+
+from . import dtypes, nputils, utils
+from .duck_array_ops import _dask_or_eager_func, count, fillna, isnull, where_method
+from .pycompat import dask_array_type
+
+try:
+    import dask.array as dask_array
+
+    from . import dask_array_compat
+except ImportError:
+    dask_array = None
+    dask_array_compat = None  # type: ignore
+
+
+def _replace_nan(a, val):
+    """
+    replace nan in a by val, and returns the replaced array and the nan
+    position
+    """
+    mask = isnull(a)
+    return where_method(val, mask, a), mask
+
+
+def _maybe_null_out(result, axis, mask, min_count=1):
+    """
+    xarray version of pandas.core.nanops._maybe_null_out
+    """
+
+    if axis is not None and getattr(result, "ndim", False):
+        null_mask = (np.take(mask.shape, axis).prod() - mask.sum(axis) - min_count) < 0
+        if null_mask.any():
+            dtype, fill_value = dtypes.maybe_promote(result.dtype)
+            result = result.astype(dtype)
+            result[null_mask] = fill_value
+
+    elif getattr(result, "dtype", None) not in dtypes.NAT_TYPES:
+        null_mask = mask.size - mask.sum()
+        if null_mask < min_count:
+            result = np.nan
+
+    return result
+
+
+def _nan_argminmax_object(func, fill_value, value, axis=None, **kwargs):
+    """ In house nanargmin, nanargmax for object arrays. Always return integer
+    type
+    """
+    valid_count = count(value, axis=axis)
+    value = fillna(value, fill_value)
+    data = _dask_or_eager_func(func)(value, axis=axis, **kwargs)
+
+    # TODO This will evaluate dask arrays and might be costly.
+    if (valid_count == 0).any():
+        raise ValueError("All-NaN slice encountered")
+
+    return data
+
+
+def _nan_minmax_object(func, fill_value, value, axis=None, **kwargs):
+    """ In house nanmin and nanmax for object array """
+    valid_count = count(value, axis=axis)
+    filled_value = fillna(value, fill_value)
+    data = getattr(np, func)(filled_value, axis=axis, **kwargs)
+    if not hasattr(data, "dtype"):  # scalar case
+        data = fill_value if valid_count == 0 else data
+        # we've computed a single min, max value of type object.
+        # don't let np.array turn a tuple back into an array
+        return utils.to_0d_object_array(data)
+    return where_method(data, valid_count != 0)
+
+
+def nanmin(a, axis=None, out=None):
+    if a.dtype.kind == "O":
+        return _nan_minmax_object("min", dtypes.get_pos_infinity(a.dtype), a, axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanmin(a, axis=axis)
+
+
+def nanmax(a, axis=None, out=None):
+    if a.dtype.kind == "O":
+        return _nan_minmax_object("max", dtypes.get_neg_infinity(a.dtype), a, axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanmax(a, axis=axis)
+
+
+def nanargmin(a, axis=None):
+    if a.dtype.kind == "O":
+        fill_value = dtypes.get_pos_infinity(a.dtype)
+        return _nan_argminmax_object("argmin", fill_value, a, axis=axis)
+
+    module = dask_array if isinstance(a, dask_array_type) else nputils
+    return module.nanargmin(a, axis=axis)
+
+
+def nanargmax(a, axis=None):
+    if a.dtype.kind == "O":
+        fill_value = dtypes.get_neg_infinity(a.dtype)
+        return _nan_argminmax_object("argmax", fill_value, a, axis=axis)
+
+    module = dask_array if i
…[cut, 10318 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
