# Item 9

**Repository:** pydata/xarray  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** xarray/tests/test_rolling.py

## The issue

"center" kwarg ignored when manually iterating over DataArrayRolling
### Discussed in https://github.com/pydata/xarray/discussions/6738

<div type='discussions-op-text'>

<sup>Originally posted by **ckingdon95** June 29, 2022</sup>
Hello, I am trying to manually iterate over a DataArrayRolling object, as described [here ](https://docs.xarray.dev/en/stable/user-guide/computation.html#rolling-window-operations)in the documentation. 

I am confused why the following two code chunks do not produce the same sequence of values. I would like to be able to manually iterate over a DataArrayRolling object, and still be given center-justified windows. Is there a way to do this?

```python
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")

# Option 1: take a center-justified rolling average
result1 = my_data.rolling(x=3, center=True).mean().values
result1
```
This returns the following values, as expected:
```
array([nan,  2.,  3.,  4.,  5.,  6.,  7.,  8., nan])
```

Whereas when I do it manually, it is not equivalent:

```python
# Option 2: try to manually iterate, but the result is not centered
my_data_rolling = my_data.rolling(x=3, center=True)
result2 = [window.mean().values.item() for label, window in my_data_rolling]
result2
```
This returns
```
[nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
```
Is this an issue with the window iterator? If it is not an issue, then is there a way for me to get the center-justified windows in the manual iteration? </div>


## The agent's commands, in order (111; outputs omitted)

1. `cd /testbed && find . -type f -name "*.py" | head -20`
2. `cd /testbed && ls -la`
3. `cd /testbed && find xarray -type f -name "*.py" | grep -E "rolling|rolling_window" | head -20`
4. `cd /testbed && cat xarray/core/rolling.py`
5. `cd /testbed && grep -n "__iter__\|__getitem__" xarray/core/rolling.py`
6. `cd /testbed && sed -n '260,350p' xarray/core/rolling.py`
7. `cd /testbed && grep -n "class DataArrayRolling" xarray/core/rolling.py`
8. `cd /testbed && sed -n '225,270p' xarray/core/rolling.py`
9. `cd /testbed && grep -n "_reduce_window" xarray/core/rolling.py`
10. `cd /testbed && grep -n "center" xarray/core/rolling.py | head -30`
11. `cd /testbed && grep -n "_construct" xarray/core/rolling.py`
12. `cd /testbed && sed -n '359,500p' xarray/core/rolling.py`
13. `cd /testbed && grep -r "rolling_window" --include="*.py" | head -20`
14. `cd /testbed && grep -n "def rolling_window" xarray/core/variable.py`
15. `cd /testbed && sed -n '2210,2350p' xarray/core/variable.py`
16. `cd /testbed && grep -r "center.*iter" xarray/tests/ --include="*.py"`
17. `cd /testbed && head -200 xarray/tests/test_rolling.py`
18. `cd /testbed && check 2>&1 | head -30`
19. `cd /testbed && python -m pytest xarray/tests/test_rolling.py::TestDataArrayRolling::test_rolling_iter -xvs 2>&1 | head -80`
20. `cd /testbed && pip install pytest -q 2>&1 | tail -5`
21. `cd /testbed && cat setup.cfg | grep -A5 "^commands"`
22. `cd /testbed && grep -A 30 "^\[aliases\]" setup.cfg`
23. `cd /testbed && python -c "import sys; print(sys.executable)"`
24. `cd /testbed && python -c "import pytest; print(pytest.__version__)" 2>&1`
25. `cd /testbed && cat requirements.txt`
26. `cd /testbed && grep -A 20 "^\[tool:pytest\]" setup.cfg`
27. `cd /testbed && ls -la | grep check`
28. `cd /testbed && find . -name "check" -type f 2>/dev/null | head -5`
29. `cd /testbed && cat setup.py`
30. `cd /testbed && grep -r "^check" . 2>/dev/null | head -5`
31. `cd /testbed && conda install -y pytest -c conda-forge 2>&1 | tail -10`
32. `cd /testbed && pip list 2>&1 | grep pytest`
33. `cd /testbed && python -c "import sys; sys.path.insert(0, '/opt/conda/lib/python3.12/site-packages'); import pytest; print(pytest.__version__)" 2>&1`
34. `cd /testbed && conda env list`
35. `cd /testbed && conda activate testbed && pip list | grep pytest`
36. `cd /testbed && conda activate testbed && python -m pytest --collect-only xarray/tests/test_rolling.py::TestDataArrayRolling::test_rolling_iter 2>&1 | head -30`
37. `which python`
38. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python -m pip list | grep pytest`
39. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python -m pip --version 2>&1`
40. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python -c "import sys; print(sys.path)" | head -5`
41. `ls /opt/miniconda3/envs/testbed/lib/python3.10/site-packages/ | grep pytest`
42. `cd /testbed && grep -r "^check" . --include="*.sh" --include="*.py" --include="*.mk" 2>/dev/null | head -5`
43. `cd /testbed && grep -A5 -B5 "test" README.md | head -30`
44.
```
cd /testbed && cat > /tmp/reproduce.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")

# Option 1: take a center-justified rolling average
result1 = my_data.rolling(x=3, center=True).mean().values
print("result1:", result1)

# Option 2: try to manually iterate, but the result is not centered
my_data_rolling = my_data.rolling(x=3, center=True)
res …[cut]
```
45. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/reproduce.py 2>&1`
46.
```
cd /testbed && cat > /tmp/expected.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=True)

# Let's compute expected windows manually
def expected_windows(da, window, center):
    N = len(da)
    for i in range(N):
        if center:
            start = i - window//2
            end = i + window//2 +  …[cut]
```
47. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/expected.py 2>&1`
48.
```
cd /testbed && cat > /tmp/debug.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=True)
print("window_labels:", my_data_rolling.window_labels.values)
print("dim:", my_data_rolling.dim)
print("window:", my_data_rolling.window)
print("center:", my_data_rolling.center)

for label, window in my_data_rolli …[cut]
```
49. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug.py 2>&1`
50.
```
cd /testbed && cat > /tmp/debug2.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=False)
print("Iteration windows:")
for label, window in my_data_rolling:
    print(f"label={label}, window={window.values}")

print("\nReduction mean:", my_data_rolling.mean().values)
print("Iteration means:", [window.m …[cut]
```
51. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug2.py 2>&1`
52.
```
cd /testbed && cat > /tmp/debug3.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
print("center=False reduction:", my_data.rolling(x=3, center=False).mean().values)
print("center=True reduction:", my_data.rolling(x=3, center=True).mean().values)
EOF
```
53. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug3.py 2>&1`
54. `cd /testbed && grep -r "manually iterate" . --include="*.rst" --include="*.md" 2>/dev/null | head -5`
55. `cd /testbed && sed -n '/manually iterate/,/Examples/p' doc/user-guide/computation.rst | head -30`
56. `cd /testbed && grep -B2 -A5 "for label, arr_window in r:" doc/user-guide/computation.rst`
57.
```
cd /testbed && cat > /tmp/construct.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=True)
constructed = rolling.construct("window")
print("constructed shape:", constructed.shape)
print("constructed dims:", constructed.dims)
print("constructed coords x:", constructed.coords['x'].values)
print("constructed co …[cut]
```
58. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/construct.py 2>&1`
59.
```
cd /testbed && cat > /tmp/debug4.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=True)
for label, window in my_data_rolling:
    print(f"label={label}, window dims={window.dims}, window={window.values}")
    break
EOF
```
60. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug4.py 2>&1`
61.
```
cd /testbed && cat > /tmp/construct2.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=False)
constructed = rolling.construct("window")
print("constructed shape:", constructed.shape)
print("constructed dims:", constructed.dims)
print("constructed coords x:", constructed.coords['x'].values)
print("constructed  …[cut]
```
62. `cd /testbed && /opt/miniconda3/envs/envs/testbed/bin/python /tmp/construct2.py 2>&1`
63. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/construct2.py 2>&1`
64.
```
cd /testbed && cat > /tmp/debug5.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=True)
for label, window in my_data_rolling:
    print(f"label={label}, window dims={window.dims}, window shape={window.shape}, window values={window.values}")
    # also check if window has coordinate
    print(f"  coor …[cut]
```
65. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug5.py 2>&1`
66. `cd /testbed && grep -r "for label, arr_window in r:" . --include="*.py" --include="*.rst" --include="*.md" 2>/dev/null | head -5`
67. `cd /testbed && sed -n '/for label, arr_window in r:/,+10p' doc/user-guide/computation.rst`
68. `cd /testbed && grep -A 20 "def test_rolling_iter" xarray/tests/test_rolling.py`
69. `cd /testbed && git log --oneline -20 -- xarray/core/rolling.py 2>&1 | head -20`
70. `cd /testbed && sed -n '1,100p' xarray/core/rolling.py`
71. `cd /testbed && sed -n '225,310p' xarray/core/rolling.py`
72.
```
cd /testbed && cat > /tmp/compare.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=True)
reduction = rolling.mean()
print("Reduction values:", reduction.values)
print("Reduction indices:", reduction.coords['x'].values)

for i, (label, window) in enumerate(rolling):
    window_mean = window.mean().values.item …[cut]
```
73. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/compare.py 2>&1`
74. `cd /testbed && grep -n "from . import dtypes" xarray/core/rolling.py`
75. `cd /testbed && cp xarray/core/rolling.py xarray/core/rolling.py.backup`
76. `cd /testbed && sed -n '270,295p' xarray/core/rolling.py`
77.
```
cd /testbed && cat > /tmp/patch_iter.py << 'EOF'
import sys
import re

with open('xarray/core/rolling.py', 'r') as f:
    content = f.read()

# Find the __iter__ method pattern
pattern = r'(\s+def __iter__\(self\) -> Iterator\[tuple\[RollingKey, DataArray\]\]:\n.*?\n\s+\n)'
# We'll replace using a more robust approach: find the method and replace between def __iter__ and next method
# Let's split  …[cut]
```
78. `cd /testbed && grep -n "def __iter__" xarray/core/rolling.py`
79. `cd /testbed && awk 'NR >= 270 && /^[[:space:]]*def / && NR > 270 {print NR ": " $0; exit}' xarray/core/rolling.py`
80. `cd /testbed && sed -n '270,283p' xarray/core/rolling.py`
81.
```
cd /testbed && cat > /tmp/replace_iter.py << 'EOF'
import sys

with open('xarray/core/rolling.py', 'r') as f:
    lines = f.readlines()

# Find start and end of __iter__ method
start = -1
for i, line in enumerate(lines):
    if line.strip().startswith('def __iter__') and '-> Iterator[tuple[RollingKey, DataArray]]' in line:
        start = i
        break
if start == -1:
    sys.exit('__iter__ not  …[cut]
```
82. `cd /testbed && sed -n '265,270p' xarray/core/rolling.py`
83.
```
cd /testbed && cat > /tmp/fix_iter.py << 'EOF'
import sys

with open('xarray/core/rolling.py', 'r') as f:
    content = f.read()

# We'll split by lines to find the exact range
lines = content.splitlines(keepends=True)

# Find start line index (0-based)
start_idx = -1
for i, line in enumerate(lines):
    if line.strip().startswith('def __iter__') and '-> Iterator[tuple[RollingKey, DataArray]]' in  …[cut]
```
84. `cd /testbed && python /tmp/fix_iter.py 2>&1`
85. `cd /testbed && sed -n '270,350p' xarray/core/rolling.py`
86. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/reproduce.py 2>&1`
87. `cd /testbed && grep -n "NA" xarray/core/dtypes.py | head -5`
88. `cd /testbed && grep -n "maybe_promote" xarray/core/dtypes.py`
89. `cd /testbed && sed -n '47,80p' xarray/core/dtypes.py`
90. `cd /testbed && sed -n '270,310p' xarray/core/rolling.py`
91.
```
cd /testbed && cat > /tmp/new_iter.py << 'EOF'
import sys

with open('xarray/core/rolling.py', 'r') as f:
    content = f.read()

# We'll write the new method as a string with proper indentation.
# First, we need to know the indentation of the class method.
# Let's find the line numbers of the class and method.
lines = content.splitlines(keepends=True)
# Find start of DataArrayRolling class? Not n …[cut]
```
92. `cd /testbed && python /tmp/new_iter.py 2>&1`
93. `cd /testbed && sed -n '270,340p' xarray/core/rolling.py`
94. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/reproduce.py 2>&1`
95. `cd /testbed && find . -type f -name "check" -executable 2>/dev/null | head -5`
96. `which check 2>&1`
97. `head -20 /usr/local/bin/check`
98. `rm -f /tmp/.mp_check_out /tmp/.mp_check_rc 2>&1`
99. `check --help 2>&1 | head -10`
100.
```
cd /testbed && cat > /tmp/test_iter_fixed.py << 'EOF'
import xarray as xr
import numpy as np
import sys

# Test center=False
print("Testing center=False")
my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=False)
rolling_mean = rolling.mean()
for i, (label, window) in enumerate(rolling):
    assert label == my_data.coords['x'].values[i]
    actual = rolling_mea …[cut]
```
101. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/test_iter_fixed.py 2>&1`
102. `cd /testbed && timeout 30 check 2>&1 | head -30`
103. `cat /usr/local/bin/check`
104. `cd /testbed && ls -la | grep -E "tox|nox|pytest.ini"`
105.
```
cd /testbed && cat > /tmp/verify_construct.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=True)
constructed = rolling.construct("window")
print("constructed shape:", constructed.shape)
print("constructed dims:", constructed.dims)
print("constructed coords window:", constructed.coords['window'].values)

# F …[cut]
```
106. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/verify_construct.py 2>&1`
107.
```
cd /testbed && cat > /tmp/debug_iter.py << 'EOF'
import xarray as xr
import numpy as np

my_data = xr.DataArray(np.arange(1,10), dims="x")
rolling = my_data.rolling(x=3, center=True)
win = rolling.window[0]
dtype = my_data.dtype
fill_value = xr.core.dtypes.NA
if fill_value is xr.core.dtypes.NA:
    dtype, fill_value = xr.core.dtypes.maybe_promote(dtype)
start_pad = win // 2
end_pad = win - 1 - sta …[cut]
```
108. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/debug_iter.py 2>&1`
109. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python /tmp/reproduce.py 2>&1`
110. `cd /testbed && python -c "import xarray as xr; import inspect; print(inspect.getsource(xr.core.rolling.DataArrayRolling.__iter__))" 2>&1 | head -30`
111. `cd /testbed && python -c "from xarray.core.rolling import DataArrayRolling; import inspect; print(inspect.getsource(DataArrayRolling.__iter__))" 2>&1 | head -40`

## The agent's last reasoning (last 3 turns)

```
Great! The window_vals are correct. So why did our earlier verification show mismatch? Because we compared `it_window.values` with `window_da.values`. But note that `it_window` is a DataArray with dimension `self.dim[0]` (size win). Its values should match window_vals. However, earlier we printed `window=[nan nan nan]`. That suggests that our iteration didn't produce the correct window. Wait, we printed from the iteration earlier (the reproduce script). That output showed label=0 window=[nan nan nan]. That indicates our fix didn't apply? But we later ran reproduce.py and got result2 matching result1. That suggests the iteration actually works (since result2 matched). Let's double-check by running reproduce.py again.
...
Now we see that the iteration windows are still incorrect! The window means (result2) are correct, but the printed windows show label=0 window all nan, label=1 window [1,2,3], etc. That suggests that the window values are not matching the window_vals we computed (they should be [nan,1,2] for label=0). Wait, result2 shows label=0 mean = nan, label=1 mean = 2.0, label=2 mean = 3.0, etc. That's exactly the reduction result. That means the iteration windows are being reduced to produce those means, but the raw windows are not matching? Let's examine: If label=0 window is [nan, nan, nan], its mean is nan. That matches result2[0] = nan. Good. If label=1 window is [1,2,3], its mean is 2.0, matches result2[1] = 2.0. That matches. But the reduction result expects label=1 window to be [1,2,3]? Wait, the reduction result at label=1 is 2.0 (mean of window [1,2,3]). That's consistent. But the constructed array window for label=1 is [1,2,3] (as we saw earlier). That matches our iteration window for label=1. However, iteration window for label=0 is all nans, while constructed window for label=0 is [nan,1,2]. That's a discrepancy. Why does the iteration window for label=0 differ from constructed? Let's examine the iteration logic again: For center=True, we produce windows of size win with padding. That should produce the same as constructed windows. However, our iteration window for label=0 is all nans. That indicates that our algorithm incorrectly handled label=0. But our debug script shows that window_vals for label=0 is [nan,1,2]. Something is off. Maybe the iteration we are looking at is not using the updated code? Did we maybe edit the wrong file? Let's check the __iter__ method again but look at the actual lines in the file (maybe we have a syntax error causing the method to be skipped?). Let's print the method source from the file.
...
Let's import correctly.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/xarray/core/rolling.py b/xarray/core/rolling.py
index aef290f6..8dfa9d44 100644
--- a/xarray/core/rolling.py
+++ b/xarray/core/rolling.py
@@ -270,17 +270,38 @@ class DataArrayRolling(Rolling["DataArray"]):
     def __iter__(self) -> Iterator[tuple[RollingKey, DataArray]]:
         if self.ndim > 1:
             raise ValueError("__iter__ is only supported for 1d-rolling")
-        stops = np.arange(1, len(self.window_labels) + 1)
-        starts = stops - int(self.window[0])
-        starts[: int(self.window[0])] = 0
-        for (label, start, stop) in zip(self.window_labels, starts, stops):
-            window = self.obj.isel({self.dim[0]: slice(start, stop)})
-
-            counts = window.count(dim=self.dim[0])
-            window = window.where(counts >= self.min_periods)
-
-            yield (label, window)
-
+        win = self.window[0]
+        if self.center[0]:
+            # center=True: windows of constant size with padding
+            dtype = self.obj.dtype
+            fill_value = dtypes.NA
+            if fill_value is dtypes.NA:
+                dtype, fill_value = dtypes.maybe_promote(dtype)
+            start_pad = win // 2
+            end_pad = win - 1 - start_pad
+            for idx, label in enumerate(self.window_labels):
+                # create array of window values
+                window_vals = np.full(win, fill_value, dtype=dtype)
+                for offset in range(win):
+                    data_idx = idx - start_pad + offset
+                    if 0 <= data_idx < len(self.obj.coords[self.dim[0]]):
+                        window_vals[offset] = self.obj.values[data_idx]
+                # create DataArray with dimension self.dim[0] (size win)
+                from .dataarray import DataArray
+                window = DataArray(window_vals, dims=[self.dim[0]])
+                counts = window.count(dim=self.dim[0])
+                window = window.where(counts >= self.min_periods)
+                yield (label, window)
+        else:
+            # center=False: keep original behavior (truncated windows)
+            stops = np.arange(1, len(self.window_labels) + 1)
+            starts = stops - int(self.window[0])
+            starts[: int(self.window[0])] = 0
+            for (label, start, stop) in zip(self.window_labels, starts, stops):
+                window = self.obj.isel({self.dim[0]: slice(start, stop)})
+                counts = window.count(dim=self.dim[0])
+                window = window.where(counts >= self.min_periods)
+                yield (label, window)
     def construct(
         self,
         window_dim: Hashable | Mapping[Any, Hashable] | None = None,
diff --git a/xarray/core/rolling.py.backup b/xarray/core/rolling.py.backup
new file mode 100644
index 00000000..aef290f6
--- /dev/null
+++ b/xarray/core/rolling.py.backup
@@ -0,0 +1,1144 @@
+from __future__ import annotations
+
+import functools
+import itertools
+import math
+import warnings
+from typing import (
+    TYPE_CHECKING,
+    Any,
+    Callable,
+    Generic,
+    Hashable,
+    Iterator,
+    Mapping,
+    TypeVar,
+)
+
+import numpy as np
+
+from . import dtypes, duck_array_ops, utils
+from .arithmetic import CoarsenArithmetic
+from .options import OPTIONS, _get_keep_attrs
+from .pycompat import is_duck_dask_array
+from .types import CoarsenBoundaryOptions, SideOptions, T_Xarray
+from .utils import either_dict_or_kwargs
+
+try:
+    import bottleneck
+except ImportError:
+    # use numpy methods instead
+    bottleneck = None
+
+if TYPE_CHECKING:
+    from .dataarray import DataArray
+    from .dataset import Dataset
+
+    RollingKey = Any
+    _T = TypeVar("_T")
+
+_ROLLING_REDUCE_DOCSTRING_TEMPLATE = """\
+Reduce this object's data windows by applying `{name}` along its dimension.
+
+Parameters
+----------
+keep_attrs : bool, default: None
+    If True, the attributes (``attrs``) will be copied from the original
+    object to the new one. If False, the new object will be returned
+    without attributes. If None uses the global default.
+**kwargs : dict
+    Additional keyword arguments passed on to `{name}`.
+
+Returns
+-------
+reduced : same type as caller
+    New object with `{name}` applied along its rolling dimension.
+"""
+
+
+class Rolling(Generic[T_Xarray]):
+    """A object that implements the moving window pattern.
+
+    See Also
+    --------
+    xarray.Dataset.groupby
+    xarray.DataArray.groupby
+    xarray.Dataset.rolling
+    xarray.DataArray.rolling
+    """
+
+    __slots__ = ("obj", "window", "min_periods", "center", "dim")
+    _attributes = ("window", "min_periods", "center", "dim")
+
+    def __init__(
+        self,
+        obj: T_Xarray,
+        windows: Mapping[Any, int],
+        min_periods: int | None = None,
+        center: bool | Mapping[Any, bool] = False,
+    ) -> None:
+        """
+        Moving window object.
+
+        Parameters
+        ----------
+        obj : Dataset or DataArray
+            Object to window.
+        windows : mapping of hashable to int
+            A mapping from the name of the dimension to create the rolling
+            window along (e.g. `time`) to the size of the moving window.
+        min_periods : int or None, default: None
+            Minimum number of observations in window required to have a value
+            (otherwise result is NA). The default, None, is equivalent to
+            setting min_periods equal to the size of the window.
+        center : bool or dict-like Hashable to bool, default: False
+            Set the labels at the center of the window. If dict-like, set this
+            property per rolling dimension.
+
+        Returns
+        -------
+        rolling : type of input argument
+        """
+        self.dim: list[Hashable] = []
+        self.window: list[int] = []
+        for d, w in windows.items():
+            self.dim.append(d)
+            if w <= 0:
+                raise ValueError("window must be > 0")
+            self.window.append(w)
+
+        self.center = self._mapping_to_list(center, default=False)
+        self.obj: T_Xarray = obj
+
+        # attributes
+        if min_periods is not None and min_periods <= 0:
+            raise ValueError("min_periods must be greater than zero or None")
+
+        self.min_periods = (
+            math.prod(self.window) if min_periods is None else min_periods
+        )
+
+    def __repr__(self) -> str:
+        """provide a nice str repr of our rolling object"""
+
+        attrs = [
+            "{k}->{v}{c}".format(k=k, v=w, c="(center)" if c else "")
+            for k, w, c in zip(self.dim, self.window, self.center)
+        ]
+        return "{klass} [{attrs}]".format(
+            klass=self.__class__.__name__, attrs=",".join(attrs)
+        )
+
+    def __len__(self) -> int:
+        return math.prod(self.obj.sizes[d] for d in self.dim)
+
+    @property
+    def ndim(self) -> int:
+        return len(self.dim)
+
+    def _reduce_method(  # type: ignore[misc]
+        name: str, fillna: Any, rolling_agg_func: Callable | None = None
+    ) -> Callable[..., T_Xarray]:
+        """Constructs reduction methods built on a numpy reduction function (e.g. sum),
+        a bottleneck reduction function (e.g. move_sum), or a Rolling reduction (_mean)."""
+        if rolling_agg_func:
+            array_agg_func = None
+        else:
+            array_agg_func = getattr(duck_array_ops, name)
+
+        bottleneck_move_func = getattr(bottleneck, "move_" + name, None)
+
+        def method(self, keep_attrs=None, **kwargs):
+
+            keep_attrs = self._get_keep_attrs(keep_attrs)
+
+            return self._numpy_or_bottleneck_reduce(
+                array_agg_func,
+                bottleneck_move_func,
+                rolling_agg_func,
+                keep_attrs=keep_attrs,
+                fillna=fillna,
+                **kwargs,
+            )
+
+        method.__name__ = name
+        method.__doc__ = _ROLLING_REDUCE_DOCSTRING_TEMPLATE.format(name=name)
+        return method
+
+    def _mean(self, keep_attrs, **kwargs):
+        result = self.sum(keep_attrs=False, **kwargs) / self.count(keep_attrs=False)
+        if keep_attrs:
+            result.attrs = self.obj.attrs
+        return result
+
+    _mean.__doc__ = _ROLLING_REDUCE_DOCSTRING_TEMPLATE.format(name="mean")
+
+    argmax = _reduce_method("argmax", dtypes.NINF)
+    argmin = _reduce_method("argmin", dtypes.INF)
+    max = _reduce_method("max", dtypes.NINF)
+    min = _reduce_method("min", dtypes.INF)
+    prod = _reduce_method("prod", 1)
+    sum = _reduce_method("sum", 0)
+    mean = _reduce_method("mean", None, _mean)
+    std = _reduce_method("std", None)
+    var = _reduce_method("var", None)
+    median = _reduce_method("median", None)
+
+    def _counts(self, keep_attrs: bool | None) -> T_Xarray:
+        raise NotImplementedError()
+
+    def count(self, keep_attrs: bool | None = None) -> T_Xarray:
+        keep_attrs = self._get_keep_attrs(keep_attrs)
+        rolling_count = self._counts(keep_attrs=keep_attrs)
+        enough_periods = rolling_count >= self.min_periods
+        return rolling_count.where(enough_periods)
+
+    count.__doc__ = _ROLLING_REDUCE_DOCSTRING_TEMPLATE.format(name="count")
+
+    def _mapping_to_list(
+        self,
+        arg: _T | Mapping[Any, _T],
+        default: _T | None = None,
+        allow_default: bool = True,
+        allow_allsame: bool = True,
+    ) -> list[_T]:
+        if utils.is_dict_like(arg):
+            if allow_default:
+                return [arg.get(d, default) for d in self.dim]
+            for d in self.dim:
+                if d not in arg:
+                    raise KeyError(f"Argument has no dimension key {d}.")
+            return [arg[d] for d in self.dim]
+        if allow_allsame:  # for single argument
+            return [arg] * self.ndim  # type: ignore[list-item]  # no check for negatives
+        if self.ndim == 1:
+            return [arg]  # type: ignore[list-item]  # no check for negatives
+        raise ValueError(f"Mapping argument is necessary for {self.ndim}d-rolling.")
+
+    def _get_keep_attrs(self, keep_attrs):
+        if keep_attrs is None:
+            keep_attrs = _get_keep_attrs(default=True)
+
+        return keep_attrs
+
+
+class DataArrayRolling(Rolling["DataArray"]):
+    __slots__ = ("window_labels",)
+
+    def __init__(
+        self,
+        obj: DataArray,
+        windows: Mapping[Any, int],
+        min_periods: int | None = None,
+        center: bool | Mapping[Any, bool] = False,
+    ) -> None:
+        """
+        Moving window object for DataArray.
+        You should use DataArray.rolling() method to construct this object
+        instead of the class constructor.
+
+        Parameters
+        ----------
+        obj : DataArray
+            Object to window.
+        windows : mapping of hashable to int
+            A mapping from the name of the dimension to create the rolling
+            exponential window along (e.g. `time`) to the size of the moving window.
+        min_periods : int, default: None
+            Minimum number of observations in window required to have a value
+            (otherwise result is NA). The default, None, is equivalent to
+            setting min_periods equal to the size of the window.
+        center : bool, default: False
+            Set the labels at the center of the window.
+
+        Returns
+        -------
+        rolling : type of input argument
+
+        See Also
+        --------
+        xarray.DataArray.rolling
+        xarray.DataArray.groupby
+        xarray.Dataset.rolling
+        xarray.Dataset.groupby
+        """
+        super().__init__(obj, windows, min_periods=min_periods, center=center)
+
+        # TODO legacy attribute
+        self.window_labels = self.obj[self.dim[0]]
+
+    def __iter__(self) -> Iterator[tuple[RollingKey, DataArray]]:
+        if self.ndim > 1:
+            raise ValueError("__iter__ is only supported for 1d-r
…[cut, 31826 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
