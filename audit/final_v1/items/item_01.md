# Item 1

**Repository:** mwaskom/seaborn  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** tests/_core/test_plot.py, tests/test_relational.py

## The issue

Wrong legend values of large ranges
As of 0.12.1, legends describing large numbers that were created using `ScalarFormatter` with an offset are formatted without their multiplicative offset value. An example:
```python
import seaborn as sns
import seaborn.objects as so

penguins = sns.load_dataset("Penguins")
penguins["body_mass_mg"] = penguins["body_mass_g"]*1000
(
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_mg",
    )
    .add(so.Dot())
)
```
The code creates the following plot:
![image](https://user-images.githubusercontent.com/13831112/205512305-778966db-f8d8-43f3-a2c0-5e5ce95bae39.png)
which is wrong because `body_mass_mg` is in the order of 1E6. The issue also reproduces if you create the mentioned plot using `scatterplot`.
 
I believe the issue stems from not using the offset value of the `ScalarFormatter` used to generate the tick labels:
https://github.com/mwaskom/seaborn/blob/ba786bc14eb255f6b4fb7619c8210c5a8016a26f/seaborn/_core/scales.py#L377-L382
Examining the code of `ScalarFormatter` suggests the issue also depends on the following rcParam settings:
`mpl.rcParams['axes.formatter.useoffset']`
`mpl.rcParams['axes.formatter.offset_threshold']`
However, I did not test it. 

The offset value can be safely retrieved from all formatters and based on that it can be used to create the legend title and/or labels.


## The agent's commands, in order (108; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed`
3. `find /testbed/seaborn -name "scales.py" -type f`
4. `sed -n '370,390p' /testbed/seaborn/_core/scales.py`
5. `grep -n "ScalarFormatter" /testbed/seaborn/_core/scales.py`
6. `sed -n '640,670p' /testbed/seaborn/_core/scales.py`
7. `grep -n "_legend" /testbed/seaborn/_core/scales.py`
8. `head -200 /testbed/seaborn/_core/scales.py`
9. `grep -n "class Continuous" /testbed/seaborn/_core/scales.py`
10. `sed -n '317,450p' /testbed/seaborn/_core/scales.py`
11. `grep -n "_get_formatter" /testbed/seaborn/_core/scales.py`
12. `sed -n '290,310p' /testbed/seaborn/_core/scales.py`
13. `sed -n '421,800p' /testbed/seaborn/_core/scales.py`
14. `grep -B2 -A10 "def _get_formatter" /testbed/seaborn/_core/scales.py`
15. `sed -n '615,660p' /testbed/seaborn/_core/scales.py`
16.
```
cd /testbed && python -c "
import seaborn as sns
import seaborn.objects as so

penguins = sns.load_dataset('Penguins')
penguins['body_mass_mg'] = penguins['body_mass_g'] * 1000
(
    so.Plot(
        penguins, x='bill_length_mm', y='bill_depth_mm',
        color='species', pointsize='body_mass_mg',
    )
    .add(so.Dot())
)
" 2>&1 | head -30
```
17. `cd /testbed && check 2>&1 | head -50`
18. `cd /testbed && python -m pytest -xvs 2>&1 | head -100`
19. `grep -r "check" /testbed --include="*.py" | head -20`
20. `cat /testbed/Makefile`
21. `pip install pytest 2>&1 | tail -5`
22. `find /testbed -type f -name "check" -executable 2>/dev/null`
23. `ls -la /testbed/.github/workflows/`
24. `cat /testbed/.github/workflows/ci.yaml`
25. `which pytest`
26. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -10`
27. `pip list | grep -i pytest`
28. `python -m pytest --version 2>&1`
29. `find /testbed -type f -name "check" 2>/dev/null`
30. `cat /testbed/.pre-commit-config.yaml`
31. `grep -r "^check" /testbed 2>/dev/null | head -5`
32. `grep -r "ScalarFormatter" /testbed/tests 2>/dev/null | head -5`
33. `grep -n "legend" /testbed/tests/test_objects.py | head -10`
34. `ls -la /testbed/seaborn-data 2>/dev/null || echo "not found"`
35. `python -c "import matplotlib.pyplot as plt; from matplotlib.ticker import ScalarFormatter; f = ScalarFormatter(); print(f.offset); f.set_xmargin(0.1); print(f.offset)" 2>&1`
36.
```
cat > /tmp/test_formatter.py << 'EOF'
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
formatter = ScalarFormatter()
ax.yaxis.set_major_formatter(formatter)
print('offset:', formatter.offset)
print('format:', formatter.format_data(1000000))
print('format ticks:', formatter.format_ticks([1000000, 20000 …[cut]
```
37. `python -c "import matplotlib.ticker as mt; import inspect; print(inspect.getsource(mt.ScalarFormatter.format_ticks))" 2>&1 | head -30`
38. `python -c "import matplotlib.ticker as mt; import inspect; print(inspect.getsource(mt.ScalarFormatter.__call__))" 2>&1 | head -40`
39. `sed -n '/class PseudoAxis/,/^class/ p' /testbed/seaborn/_core/scales.py | head -30`
40. `sed -n '80,100p' /testbed/seaborn/_core/scales.py`
41. `grep -r "legend" /testbed/tests --include="*.py" | grep -v ".pyc" | head -20`
42. `grep -B5 -A20 "test_legend_data" /testbed/tests/test_axisgrid.py`
43. `python -c "import matplotlib; print(matplotlib.__version__)" 2>&1`
44. `grep -r "_legend" /testbed/seaborn --include="*.py" | grep -v ".pyc" | head -30`
45. `grep -n "def locator_to_legend_entries" /testbed/seaborn/utils.py -A 30`
46. `grep -n "add_legend_data" /testbed/seaborn/relational.py -B2 -A30`
47. `grep -n "legend_data" /testbed/seaborn/relational.py -B2 -A2`
48. `sed -n '193,350p' /testbed/seaborn/relational.py`
49. `grep -r "\._legend" /testbed/seaborn --include="*.py" | grep -v ".pyc" | head -20`
50. `ls -la /testbed/ | grep -E "check|test"`
51. `python -c "import sys; print('\n'.join(sys.path))" 2>&1 | head -10`
52.
```
cat > /tmp/test_bug.py << 'EOF'
import matplotlib.ticker as mt
import numpy as np
from seaborn.utils import locator_to_legend_entries

# Simulate large numeric values around 1e6
levels = [500000, 1000000, 1500000, 2000000]
limits = (min(levels), max(levels))
print('limits:', limits)

# Create a locator (MaxNLocator)
locator = mt.MaxNLocator(nbins=5)
# Get raw levels
raw_levels = locator.tick_value …[cut]
```
53. `python -c "import matplotlib.ticker as mt; import inspect; print(inspect.getsource(mt.ScalarFormatter.set_locs))" 2>&1 | head -50`
54. `python -c "import matplotlib.ticker as mt; import inspect; print(inspect.getsource(mt.ScalarFormatter._compute_offset))" 2>&1 | head -80`
55. `python -c "import matplotlib.ticker as mt; f = mt.ScalarFormatter(); print('_useOffset:', f._useOffset); print('_offset_threshold:', f._offset_threshold)" 2>&1`
56.
```
cat > /tmp/test_offset.py << 'EOF'
import matplotlib.ticker as mt
import numpy as np

# Simulate locator_to_legend_entries logic
locator = mt.MaxNLocator(nbins=5)
limits = (500000, 2000000)
raw_levels = locator.tick_values(*limits)
print('raw_levels:', raw_levels)

class dummy_axis:
    def get_view_interval(self):
        return limits

formatter = mt.ScalarFormatter()
formatter.axis = dummy_axis …[cut]
```
57.
```
python -c "
import matplotlib.ticker as mt
import numpy as np
formatter = mt.ScalarFormatter()
print('format_data 1000000:', formatter.format_data(1000000))
print('format_data 600000:', formatter.format_data(600000))
print('format_data 1500000:', formatter.format_data(1500000))
" 2>&1
```
58. `grep -r "locator_to_legend_entries" /testbed/tests 2>/dev/null`
59. `sed -n '/def test_locator_to_legend_entries/,/^def /p' /testbed/tests/test_utils.py | head -80`
60. `python -c "import sys; import pkgutil; print([name for name in sys.modules if 'pytest' in name])" 2>&1 | head -5`
61. `grep -n "_legend" /testbed/seaborn/plot.py -B2 -A2`
62. `find /testbed/seaborn -name "plot.py" -type f`
63. `grep -n "_legend" /testbed/seaborn/_core/plot.py -B2 -A2`
64. `python -c "import matplotlib as mpl; print(mpl.rcParams['axes.formatter.offset_threshold'])" 2>&1`
65. `sed -n '370,390p' /testbed/seaborn/_core/scales.py`
66. `cd /testbed && check 2>&1 | tee /tmp/check_output.txt | head -30`
67. `python -c "import sys; print([p for p in sys.path if 'site-packages' in p])" 2>&1`
68. `ls -la /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/ | grep pytest`
69. `ls -la /var/lib/apt/lists/`
70. `apt-get update 2>&1 | tail -5`
71. `ls -ld /var/lib/apt/`
72. `mkdir -p /var/lib/apt/lists/partial && apt-get update 2>&1 | tail -5`
73.
```
cat > /tmp/test_offset2.py << 'EOF'
import matplotlib as mpl
import matplotlib.ticker as mt
import numpy as np

# Temporarily set offset_threshold to 2 (so offset can be used for smaller numbers)
mpl.rcParams['axes.formatter.offset_threshold'] = 2

# Create a formatter
formatter = mt.ScalarFormatter()
print('offset_threshold:', formatter._offset_threshold)
print('useOffset:', formatter._useOffset) …[cut]
```
74.
```
cat > /tmp/test_offset3.py << 'EOF'
import matplotlib as mpl
import matplotlib.ticker as mt
import numpy as np

# Set offset_threshold to 1 (so offset can be used when quotient >=1)
mpl.rcParams['axes.formatter.offset_threshold'] = 1

# Create a formatter
formatter = mt.ScalarFormatter()
print('offset_threshold:', formatter._offset_threshold)
print('useOffset:', formatter._useOffset)

# Simulate a …[cut]
```
75.
```
cat > /tmp/reproduce_bug.py << 'EOF'
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

# Create synthetic dataset
species = ['Adelie', 'Gentoo', 'Chinstrap']
bill_length = [40, 50, 45]
bill_depth = [20, 25, 22]
body_mass_g = [3000, 5000, 4000]

df = pd.DataFrame({
    'species': species,
    'bill_length_mm': bill_length,
    'bill_depth_mm': b …[cut]
```
76. `grep -r "\.plot\(\)" /testbed/tests --include="*.py" | head -5`
77. `grep -A5 -B5 "so.Plot" /testbed/tests/test_objects.py | head -30`
78. `grep -n "class Plotter" /testbed/seaborn/_core/plot.py -A2`
79. `grep -n "\.plot\(" /testbed/tests/test_objects.py | head -5`
80. `dpkg -l | grep pytest 2>&1 | head -5`
81. `cd /testbed && git log --oneline -10 -- seaborn/_core/scales.py 2>&1 | head -10`
82.
```
python -c "
import matplotlib.ticker as mt
import numpy as np
formatter = mt.ScalarFormatter()
formatter.axis = None
print('format_data 0.15:', formatter.format_data(0.15))
print('format_data 0.30:', formatter.format_data(0.30))
" 2>&1
```
83. `cd /testbed && git log --all --oneline --grep="offset" 2>&1 | head -10`
84. `find /testbed -name "penguins.csv" -type f 2>/dev/null`
85.
```
cat > /tmp/test_axis_labels.py << 'EOF'
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
import numpy as np

fig, ax = plt.subplots()
ax.plot([0,1], [0,1])
ax.set_ylim(0, 2000000)
ax.yaxis.set_major_formatter(mt.ScalarFormatter())
ax.yaxis.set_major_locator(mt.AutoLocator())
ax.autoscale(enable=True, axis='y')

# Get tick labels
labels = ax.yaxis.get_ticklabels()
print('Y tick labels …[cut]
```
86. `cd /testbed && check 2>&1 | grep -A5 -B5 "FAILED" | head -30`
87. `cd /testbed && check > /tmp/check.out 2>&1 & sleep 5 && kill $! 2>&1`
88. `cd /testbed && timeout 30 check 2>&1 | tee /tmp/check.out`
89. `which check`
90. `file /usr/local/bin/check`
91. `head -20 /usr/local/bin/check`
92. `rm -f /tmp/.mp_check_out /tmp/.mp_check_rc && /usr/local/bin/check 2>&1 | head -50`
93. `cd /testbed && /usr/local/bin/check 2>&1 | head -100`
94. `cd /testbed && sh -c 'check' 2>&1 | head -100`
95. `grep -n "offset" /testbed/seaborn/_core/scales.py | head -20`
96.
```
python -c "
import matplotlib.ticker as mt
formatter = mt.ScalarFormatter()
print('format_data 1000000:', formatter.format_data(1000000))
print('__call__ 1000000:', formatter(1000000))
print('format_ticks [1000000]:', formatter.format_ticks([1000000]))
" 2>&1
```
97.
```
python -c "
import matplotlib.ticker as mt
formatter = mt.ScalarFormatter()
formatter.axis = None
formatter.set_locs([0.15, 0.30])
print('orderOfMagnitude:', formatter.orderOfMagnitude)
print('offset:', formatter.offset)
print('format_data 0.15:', formatter.format_data(0.15))
print('format_data 0.30:', formatter.format_data(0.30))
" 2>&1
```
98. `cd /testbed && git log --oneline -1`
99. `cd /testbed && git diff 6084ebccd6f8dc503dcacad3e3cb4a7c5f083540 HEAD -- seaborn/_core/scales.py 2>&1 | head -100`
100.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from seaborn.utils import locator_to_legend_entries
import matplotlib.ticker as mt
import numpy as np

# Test cases from test_utils.py
test_cases = [
    (mt.MaxNLocator(nbins=3), (0.09, 0.4), float),
    (mt.MaxNLocator(nbins=3), (0.8, 0.9), float),
    (mt.MaxNLocator(nbins=3), (1, 6), int),
    (mt.LogLocator(numticks=5), (5, 1425),  …[cut]
```
101.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from seaborn.utils import locator_to_legend_entries
import matplotlib.ticker as mt
import numpy as np

# Large numbers
locator = mt.MaxNLocator(nbins=5)
limits = (500000, 2000000)
raw, formatted = locator_to_legend_entries(locator, limits, np.float64)
print('Large limits:', limits)
print('  formatted:', formatted)
print('  raw:', raw)
" …[cut]
```
102.
```
cd /testbed && python -c "
import matplotlib.ticker as mt
import numpy as np

def format_data_all(formatter, ticks):
    # Ensure axis is set (dummy)
    class DummyAxis:
        def get_view_interval(self):
            return (min(ticks), max(ticks))
    formatter.axis = DummyAxis()
    formatter.set_locs(ticks)
    return [formatter.format_data(t) for t in ticks]

# Test cases
test_cases = [
    …[cut]
```
103. `grep -n "def locator_to_legend_entries" /testbed/seaborn/utils.py -A 30`
104. `cp /testbed/seaborn/utils.py /testbed/seaborn/utils.py.backup`
105. `sed -n '680,690p' /testbed/seaborn/utils.py`
106.
```
cat > /tmp/modify_utils.py << 'EOF'
import sys
sys.path.insert(0, '/testbed')
import re

with open('/testbed/seaborn/utils.py', 'r') as f:
    content = f.read()

# Insert helper before locator_to_legend_entries
# Find the line "def locator_to_legend_entries(locator, limits, dtype):"
pattern = r'(\s*)def locator_to_legend_entries\(locator, limits, dtype\):'
match = re.search(pattern, content)
if n …[cut]
```
107.
```
cat > /tmp/modify_scales.py << 'EOF'
import sys
sys.path.insert(0, '/testbed')
import re

with open('/testbed/seaborn/_core/scales.py', 'r') as f:
    content = f.read()

# First, add import after the existing imports if not already present
# Find a good place to add import (after the import block)
# We'll add after the last import line that is not a comment.
# Simple: add after the line "from sea …[cut]
```
108.
```
cat > /tmp/test_fix.py << 'EOF'
import sys
sys.path.insert(0, '/testbed')
import matplotlib.ticker as mt
import numpy as np

# Load original function from backup
import importlib.util
spec = importlib.util.spec_from_file_location('utils_orig', '/testbed/seaborn/utils.py.backup')
utils_orig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils_orig)

# Load modified module
from seab …[cut]
```

## The agent's last reasoning (last 3 turns)

```
We'll insert our helper between the previous function and locator_to_legend_entries. Let's write the helper in a separate file and then insert. But we can do it with a script. Let's create a temporary Python script that will modify the file. However, we can use sed to insert multiple lines. Let's do it step by step. First, let's write the helper function content: ```python def _format_ticks_with_offset(formatter, raw_levels): """ Return formatted tick labels with offset and scientific notation. """ # Ensure axis is set (formatter expects an axis) if not hasattr(formatter, 'axis') or formatter.axis is None: class dummy_axis: def get_view_interval(self): return (min(raw_levels), max(raw_levels)) formatter.axis = dummy_axis() # Compute offset and order of magnitude (already done by set_locs) formatter.set_locs(raw_levels) formatted = [] for x in raw_levels: # Get the offset-corrected string label = formatter(x) # If label contains 'e', keep as is (already offset/scientific aware) if 'e' in label: formatted.append(label) else: # Label does not contain exponent, check if we need to add offset # If offset is non-zero, we need to reconstruct original tick # However, offset is likely zero in this case. # Instead, we can try to format using format_data which includes scientific notation # but we must avoid breaking existing tests. # We'll only replace for large positive numbers where orderOfMagnitude > 0. if formatter.orderOfMagnitude > 0: # Use format_data to include scientific notation label2 = formatter.format_data(x) # Ensure it's not empty if label2: formatted.append(label2) else: formatted.append(label) else: formatted.append(label) return formatted ``` But we need to be careful about side effects (formatter.axis). We'll assume axis already set (it is). Also we need to consider that `formatter(x)` may return empty string? Not likely. We'll keep the existing formatted_levels if they contain 'e' (scientific notation). For large positive numbers without 'e', we replace with format_data. Now we need to modify locator_to_legend_entries to use this helper. Let's edit the file using a Python script.
...
Great! Now we need to also modify the legend labels in scales.py. Let's look at the exact line again. We'll need to decide how to adjust those labels. We could use the same helper function, but scales.py doesn't import utils. We could either import it (adding a dependency) or replicate the logic. Since scales.py is in the same module (seaborn._core), we can import from ..utils? Actually scales.py is in seaborn._core, while utils is in seaborn. We can import `seaborn.utils`. That's okay. But we also need to consider that the axis.major.formatter may be a different type (ScalarFormatter, LogFormatter, etc). The helper we wrote only handles ScalarFormatter (and LogFormatter via isinstance). However, the legend labels in scales.py are generated for continuous scales where the formatter is set in `_get_formatter`. That could be ScalarFormatter, EngFormatter, LogFormatter, etc. We need a generic solution. Given the time, I think we should also apply the same fix to scales.py: replace `labels = axis.major.formatter.format_ticks(locs)` with a call to a helper that uses offset-aware formatting. We can create a similar helper in scales.py (maybe reuse the one from utils by importing). Let's import `locator_to_legend_entries`? That function expects a locator, not a formatter. Not suitable. We'll create a helper inside scales.py that uses the formatter's offset and orderOfMagnitude. We'll also need to consider that the formatter may be EngFormatter (which uses SI prefixes). That formatter also has offset? Probably not. We can just keep the existing labels for non-ScalarFormatter? The bug is about ScalarFormatter with offset. So we can check if the formatter is an instance of ScalarFormatter, and if so, apply offset-aware formatting. Otherwise, keep as is. Let's examine the imports at the top of scales.py: they import ScalarFormatter. Good. Now we ne
…[cut, 1593 more chars]
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/seaborn/_core/scales.py b/seaborn/_core/scales.py
index 55874bf2..b9b8a87d 100644
--- a/seaborn/_core/scales.py
+++ b/seaborn/_core/scales.py
@@ -35,6 +35,7 @@ from matplotlib.scale import ScaleBase
 from pandas import Series
 
 from seaborn._core.rules import categorical_order
+from seaborn.utils import _format_ticks_with_offset
 from seaborn._core.typing import Default, default
 
 from typing import TYPE_CHECKING
@@ -378,7 +379,24 @@ class ContinuousBase(Scale):
             axis.set_view_interval(vmin, vmax)
             locs = axis.major.locator()
             locs = locs[(vmin <= locs) & (locs <= vmax)]
-            labels = axis.major.formatter.format_ticks(locs)
+            formatter = axis.major.formatter
+
+            if isinstance(formatter, mpl.ticker.ScalarFormatter):
+
+                # Use offset-aware formatting
+
+                if formatter.orderOfMagnitude > 0 or formatter.offset != 0:
+
+                    labels = _format_ticks_with_offset(formatter, list(locs))
+
+                else:
+
+                    labels = axis.major.formatter.format_ticks(locs)
+
+            else:
+
+                labels = axis.major.formatter.format_ticks(locs)
+
             new._legend = list(locs), list(labels)
 
         return new
diff --git a/seaborn/utils.py b/seaborn/utils.py
index 2407853c..4a17fed8 100644
--- a/seaborn/utils.py
+++ b/seaborn/utils.py
@@ -684,6 +684,157 @@ def axes_ticklabels_overlap(ax):
             axis_ticklabels_overlap(ax.get_yticklabels()))
 
 
+
+def _format_ticks_with_offset(formatter, raw_levels):
+
+
+
+    """
+
+
+
+    Return formatted tick labels with offset and scientific notation.
+
+
+
+    """
+
+
+
+    # Ensure axis is set (formatter expects an axis)
+
+
+
+    if not hasattr(formatter, 'axis') or formatter.axis is None:
+
+
+
+        class dummy_axis:
+
+
+
+            def get_view_interval(self):
+
+
+
+                return (min(raw_levels), max(raw_levels))
+
+
+
+        formatter.axis = dummy_axis()
+
+
+
+    # Compute offset and order of magnitude (already done by set_locs)
+
+
+
+    formatter.set_locs(raw_levels)
+
+
+
+    formatted = []
+
+
+
+    for x in raw_levels:
+
+
+
+        # Get the offset-corrected string
+
+
+
+        label = formatter(x)
+
+
+
+        # If label contains 'e', keep as is (already offset/scientific aware)
+
+
+
+        if 'e' in label:
+
+
+
+            formatted.append(label)
+
+
+
+        else:
+
+
+
+            # Label does not contain exponent, check if we need to add offset
+
+
+
+            # If offset is non-zero, we need to reconstruct original tick
+
+
+
+            # However, offset is likely zero in this case.
+
+
+
+            # Instead, we can try to format using format_data which includes scientific notation
+
+
+
+            # but we must avoid breaking existing tests.
+
+
+
+            # We'll only replace for large positive numbers where orderOfMagnitude > 0.
+
+
+
+            if formatter.orderOfMagnitude > 0:
+
+
+
+                # Use format_data to include scientific notation
+
+
+
+                label2 = formatter.format_data(x)
+
+
+
+                # Ensure it's not empty
+
+
+
+                if label2:
+
+
+
+                    formatted.append(label2)
+
+
+
+                else:
+
+
+
+                    formatted.append(label)
+
+
+
+            else:
+
+
+
+                formatted.append(label)
+
+
+
+    return formatted
+
+
+
+
+
 def locator_to_legend_entries(locator, limits, dtype):
     """Return levels and formatted levels for brief numeric legends."""
     raw_levels = locator.tick_values(*limits).astype(dtype)
@@ -704,8 +855,7 @@ def locator_to_legend_entries(locator, limits, dtype):
     # TODO: The following two lines should be replaced
     # once pinned matplotlib>=3.1.0 with:
     # formatted_levels = formatter.format_ticks(raw_levels)
-    formatter.set_locs(raw_levels)
-    formatted_levels = [formatter(x) for x in raw_levels]
+        formatted_levels = _format_ticks_with_offset(formatter, raw_levels)
 
     return raw_levels, formatted_levels
 
diff --git a/seaborn/utils.py.backup b/seaborn/utils.py.backup
new file mode 100644
index 00000000..2407853c
--- /dev/null
+++ b/seaborn/utils.py.backup
@@ -0,0 +1,872 @@
+"""Utility functions, mostly for internal use."""
+import os
+import re
+import inspect
+import warnings
+import colorsys
+from contextlib import contextmanager
+from urllib.request import urlopen, urlretrieve
+
+import numpy as np
+import pandas as pd
+import matplotlib as mpl
+from matplotlib.colors import to_rgb
+import matplotlib.pyplot as plt
+from matplotlib.cbook import normalize_kwargs
+
+from .external.version import Version
+from .external.appdirs import user_cache_dir
+
+__all__ = ["desaturate", "saturate", "set_hls_values", "move_legend",
+           "despine", "get_dataset_names", "get_data_home", "load_dataset"]
+
+
+def ci_to_errsize(cis, heights):
+    """Convert intervals to error arguments relative to plot heights.
+
+    Parameters
+    ----------
+    cis : 2 x n sequence
+        sequence of confidence interval limits
+    heights : n sequence
+        sequence of plot heights
+
+    Returns
+    -------
+    errsize : 2 x n array
+        sequence of error size relative to height values in correct
+        format as argument for plt.bar
+
+    """
+    cis = np.atleast_2d(cis).reshape(2, -1)
+    heights = np.atleast_1d(heights)
+    errsize = []
+    for i, (low, high) in enumerate(np.transpose(cis)):
+        h = heights[i]
+        elow = h - low
+        ehigh = high - h
+        errsize.append([elow, ehigh])
+
+    errsize = np.asarray(errsize).T
+    return errsize
+
+
+def _normal_quantile_func(q):
+    """
+    Compute the quantile function of the standard normal distribution.
+
+    This wrapper exists because we are dropping scipy as a mandatory dependency
+    but statistics.NormalDist was added to the standard library in 3.8.
+
+    """
+    try:
+        from statistics import NormalDist
+        qf = np.vectorize(NormalDist().inv_cdf)
+    except ImportError:
+        try:
+            from scipy.stats import norm
+            qf = norm.ppf
+        except ImportError:
+            msg = (
+                "Standard normal quantile functions require either Python>=3.8 or scipy"
+            )
+            raise RuntimeError(msg)
+    return qf(q)
+
+
+def _draw_figure(fig):
+    """Force draw of a matplotlib figure, accounting for back-compat."""
+    # See https://github.com/matplotlib/matplotlib/issues/19197 for context
+    fig.canvas.draw()
+    if fig.stale:
+        try:
+            fig.draw(fig.canvas.get_renderer())
+        except AttributeError:
+            pass
+
+
+def _default_color(method, hue, color, kws):
+    """If needed, get a default color by using the matplotlib property cycle."""
+
+    if hue is not None:
+        # This warning is probably user-friendly, but it's currently triggered
+        # in a FacetGrid context and I don't want to mess with that logic right now
+        #  if color is not None:
+        #      msg = "`color` is ignored when `hue` is assigned."
+        #      warnings.warn(msg)
+        return None
+
+    kws = kws.copy()
+    kws.pop("label", None)
+
+    if color is not None:
+        return color
+
+    elif method.__name__ == "plot":
+
+        color = _normalize_kwargs(kws, mpl.lines.Line2D).get("color")
+        scout, = method([], [], scalex=False, scaley=False, color=color)
+        color = scout.get_color()
+        scout.remove()
+
+    elif method.__name__ == "scatter":
+
+        # Matplotlib will raise if the size of x/y don't match s/c,
+        # and the latter might be in the kws dict
+        scout_size = max(
+            np.atleast_1d(kws.get(key, [])).shape[0]
+            for key in ["s", "c", "fc", "facecolor", "facecolors"]
+        )
+        scout_x = scout_y = np.full(scout_size, np.nan)
+
+        scout = method(scout_x, scout_y, **kws)
+        facecolors = scout.get_facecolors()
+
+        if not len(facecolors):
+            # Handle bug in matplotlib <= 3.2 (I think)
+            # This will limit the ability to use non color= kwargs to specify
+            # a color in versions of matplotlib with the bug, but trying to
+            # work out what the user wanted by re-implementing the broken logic
+            # of inspecting the kwargs is probably too brittle.
+            single_color = False
+        else:
+            single_color = np.unique(facecolors, axis=0).shape[0] == 1
+
+        # Allow the user to specify an array of colors through various kwargs
+        if "c" not in kws and single_color:
+            color = to_rgb(facecolors[0])
+
+        scout.remove()
+
+    elif method.__name__ == "bar":
+
+        # bar() needs masked, not empty data, to generate a patch
+        scout, = method([np.nan], [np.nan], **kws)
+        color = to_rgb(scout.get_facecolor())
+        scout.remove()
+
+    elif method.__name__ == "fill_between":
+
+        # There is a bug on matplotlib < 3.3 where fill_between with
+        # datetime units and empty data will set incorrect autoscale limits
+        # To workaround it, we'll always return the first color in the cycle.
+        # https://github.com/matplotlib/matplotlib/issues/17586
+        ax = method.__self__
+        datetime_axis = any([
+            isinstance(ax.xaxis.converter, mpl.dates.DateConverter),
+            isinstance(ax.yaxis.converter, mpl.dates.DateConverter),
+        ])
+        if Version(mpl.__version__) < Version("3.3") and datetime_axis:
+            return "C0"
+
+        kws = _normalize_kwargs(kws, mpl.collections.PolyCollection)
+
+        scout = method([], [], **kws)
+        facecolor = scout.get_facecolor()
+        color = to_rgb(facecolor[0])
+        scout.remove()
+
+    return color
+
+
+def desaturate(color, prop):
+    """Decrease the saturation channel of a color by some percent.
+
+    Parameters
+    ----------
+    color : matplotlib color
+        hex, rgb-tuple, or html color name
+    prop : float
+        saturation channel of color will be multiplied by this value
+
+    Returns
+    -------
+    new_color : rgb tuple
+        desaturated color code in RGB tuple representation
+
+    """
+    # Check inputs
+    if not 0 <= prop <= 1:
+        raise ValueError("prop must be between 0 and 1")
+
+    # Get rgb tuple rep
+    rgb = to_rgb(color)
+
+    # Convert to hls
+    h, l, s = colorsys.rgb_to_hls(*rgb)
+
+    # Desaturate the saturation channel
+    s *= prop
+
+    # Convert back to rgb
+    new_color = colorsys.hls_to_rgb(h, l, s)
+
+    return new_color
+
+
+def saturate(color):
+    """Return a fully saturated color with the same hue.
+
+    Parameters
+    ----------
+    color : matplotlib color
+        hex, rgb-tuple, or html color name
+
+    Returns
+    -------
+    new_color : rgb tuple
+        saturated color code in RGB tuple representation
+
+    """
+    return set_hls_values(color, s=1)
+
+
+def set_hls_values(color, h=None, l=None, s=None):  # noqa
+    """Independently manipulate the h, l, or s channels of a color.
+
+    Parameters
+    ----------
+    color : matplotlib color
+        hex, rgb-tuple, or html color name
+    h, l, s : floats between 0 and 1, or None
+        new values for each channel in hls space
+
+    Returns
+    -------
+    new_color : rgb tuple
+        new color code in RGB tuple representation
+
+    """
+    # Get an RGB tuple representation
+    rgb = to_rgb(color)
+    vals = list(colorsys.rgb_to_hls(*rgb))
+    for i, val in enumerate([h, l, s]):
+        if val is not None:
+            vals[i] = val
+
+    rgb = colorsys.hls_to_rgb(*vals)
+    return rgb
+
+
+def axlabel(xlabel, ylabel, **kwargs):
+    """Grab current axis and label it.
+
+    DEPRECATED: will be removed in a future version.
+
+    """
+    msg = "This function is deprecated and will be removed in a future version"
+    warnings.warn(msg, FutureWarni
…[cut, 21412 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
