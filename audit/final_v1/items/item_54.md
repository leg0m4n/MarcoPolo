# Item 54

**Repository:** matplotlib/matplotlib  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** NOT resolved  
**The task's test files:** lib/matplotlib/tests/test_colorbar.py

## The issue

[Bug]: Colorbar with drawedges=True and extend='both' does not draw edges at extremities
### Bug summary

When creating a matplotlib colorbar, it is possible to set drawedges to True which separates the colors of the colorbar with black lines. However, when the colorbar is extended using extend='both', the black lines at the extremities do not show up.

### Code for reproduction

```python
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
ax = plt.subplot(111)
cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)
plt.subplots_adjust(left=0.05, bottom=0.4, right=0.95, top=0.9)
plt.show()
```


### Actual outcome

![image](https://user-images.githubusercontent.com/34058459/164254401-7516988d-1efb-4887-a631-de9a68357685.png)


### Expected outcome

![image](https://user-images.githubusercontent.com/34058459/164254881-92c167b7-aa13-4972-9955-48221b38b866.png)


### Additional information

_No response_

### Operating system

_No response_

### Matplotlib Version

3.5.1

### Matplotlib Backend

_No response_

### Python version

_No response_

### Jupyter version

_No response_

### Installation

_No response_


## The agent's commands, in order (96; outputs omitted)

1. `find /testbed -type f -name "*.py" | grep -E "(colorbar|color)" | head -20`
2. `ls -la /testbed/`
3. `find /testbed -type f -path "*/lib/matplotlib/*.py" | grep -v test | head -30`
4. `ls -la /testbed/lib/matplotlib/`
5.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
a …[cut]
```
6. `cd /testbed && python -m pytest lib/matplotlib/tests/test_colorbar.py -xvs 2>&1 | head -100`
7. `cd /testbed && cat tests.py | head -30`
8. `cd /testbed && which check`
9. `head -50 /usr/local/bin/check`
10. `find /testbed -name "check" -type f 2>/dev/null | head -10`
11. `grep -r "check" /testbed/setup.py 2>/dev/null | head -5`
12. `grep -n "drawedges" /testbed/lib/matplotlib/colorbar.py | head -20`
13. `sed -n '650,670p' /testbed/lib/matplotlib/colorbar.py`
14. `grep -n "_make_edges\|_edges\|_X\|_Y" /testbed/lib/matplotlib/colorbar.py | head -30`
15. `grep -B5 -A5 "self.drawedges" /testbed/lib/matplotlib/colorbar.py`
16. `grep -n "def _make" /testbed/lib/matplotlib/colorbar.py`
17. `grep -n "^    def " /testbed/lib/matplotlib/colorbar.py | head -30`
18. `sed -n '634,660p' /testbed/lib/matplotlib/colorbar.py`
19. `grep -n "self._add_solids" /testbed/lib/matplotlib/colorbar.py`
20. `sed -n '620,640p' /testbed/lib/matplotlib/colorbar.py`
21. `sed -n '580,630p' /testbed/lib/matplotlib/colorbar.py`
22. `grep -n "_mesh" /testbed/lib/matplotlib/colorbar.py`
23. `sed -n '1176,1250p' /testbed/lib/matplotlib/colorbar.py`
24. `grep -n "_extend_lower\|_extend_upper\|_extend" /testbed/lib/matplotlib/colorbar.py | head -30`
25. `sed -n '1352,1360p' /testbed/lib/matplotlib/colorbar.py`
26. `sed -n '620,635p' /testbed/lib/matplotlib/colorbar.py`
27. `grep -n "_process_values" /testbed/lib/matplotlib/colorbar.py`
28. `sed -n '1123,1220p' /testbed/lib/matplotlib/colorbar.py`
29. `find /testbed -name "*test*colorbar*.py" -type f | grep -v __pycache__`
30. `grep -n "drawedges" /testbed/lib/matplotlib/tests/test_colorbar.py | head -20`
31. `sed -n '932,960p' /testbed/lib/matplotlib/tests/test_colorbar.py`
32. `grep -B20 "def test_colorbar_extend_drawedges" /testbed/lib/matplotlib/tests/test_colorbar.py`
33.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
a …[cut]
```
34. `grep -n "class ColorbarBase" /testbed/lib/matplotlib/colorbar.py`
35. `grep -n "class.*Colorbar" /testbed/lib/matplotlib/colorbar.py`
36. `grep -n "ColorbarBase" /testbed/lib/matplotlib/colorbar.py`
37. `cd /testbed && python -m pytest lib/matplotlib/tests/test_colorbar.py::test_colorbar_extend_drawedges -xvs 2>&1 | head -80`
38. `cd /testbed && ls -la | grep -i test`
39. `cd /testbed && python tests.py --help 2>&1 | head -30`
40. `pip install pytest -q 2>&1 | tail -5`
41. `cat /usr/local/bin/check`
42. `python -c "import sys; print(sys.executable)"`
43. `conda list | grep pytest 2>&1 | head -5`
44. `cd /testbed && python -m pytest lib/matplotlib/tests/test_colorbar.py::test_colorbar_extend_drawedges -xvs 2>&1 | tail -30`
45. `which python`
46. `cd /testbed && /opt/miniconda3/envs/testbed/bin/python -m pytest lib/matplotlib/tests/test_colorbar.py::test_colorbar_extend_drawedges -xvs 2>&1 | tail -50`
47. `conda env list`
48. `cd /testbed && /opt/miniconda3/envs/testbed/bin/pip install pytest --no-index --find-links=/opt/miniconda3/envs/testbed/lib/python3.11/site-packages 2>&1 | tail -10`
49.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
a …[cut]
```
50.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
a …[cut]
```
51.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as colorbar

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, exten …[cut]
```
52. `grep -n "_proportional_y" /testbed/lib/matplotlib/colorbar.py`
53. `sed -n '1289,1340p' /testbed/lib/matplotlib/colorbar.py`
54. `grep -n "_inside" /testbed/lib/matplotlib/colorbar.py`
55. `sed -n '405,420p' /testbed/lib/matplotlib/colorbar.py`
56.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

cmap = plt.get_cmap('viridis')
bounds = np.arange(3)
nb_colors = len(bounds) + 1  # =4
colors = cmap(np.linspace(100, 255, nb_colors).astype(int))
cmap, norm = from_levels_and_colors(bounds, colors, extend='both')

print('bounds:', bounds)
p …[cut]
```
57.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as colorbar

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, exten …[cut]
```
58. `grep -B10 -A10 "np.dstack" /testbed/lib/matplotlib/colorbar.py`
59. `cp /testbed/lib/matplotlib/colorbar.py /testbed/lib/matplotlib/colorbar.py.backup`
60. `sed -n '651,656p' /testbed/lib/matplotlib/colorbar.py`
61. `grep -n "self.dividers.set_segments" /testbed/lib/matplotlib/colorbar.py`
62. `sed -n '645,660p' /testbed/lib/matplotlib/colorbar.py`
63. `cd /testbed && git log --oneline -10 lib/matplotlib/colorbar.py 2>&1 | head -20`
64. `cd /testbed && sed -i '654s/np.dstack(\[X, Y\])\[1:-1\]/np.dstack([X, Y])/' lib/matplotlib/colorbar.py`
65. `sed -n '654,654p' /testbed/lib/matplotlib/colorbar.py`
66. `sed -n '654,655p' /testbed/lib/matplotlib/colorbar.py`
67.
```
cd /testbed && python -c "
import re
with open('lib/matplotlib/colorbar.py', 'r') as f:
    content = f.read()
# find the pattern
pattern = r'(\s+self\.dividers\.set_segments\(\s*)np\.dstack\(\[X, Y\]\)\[1:-1\]'
replacement = r'\1np.dstack([X, Y])'
new_content = re.sub(pattern, replacement, content)
with open('lib/matplotlib/colorbar.py', 'w') as f:
    f.write(new_content)
print('Patched')
"
```
68. `sed -n '654,655p' /testbed/lib/matplotlib/colorbar.py`
69.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

plt.figure(figsize=(5, 1))
a …[cut]
```
70.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as mcolorbar

def test_extend(extend, coloroffset):
    cmap = plt.get_cmap('viridis')
    bounds = np.arange(3)
    nb_colors = len(bounds) + coloroffset
    colors = cmap(np.linspace(100, 255, nb_colors).astype(int) …[cut]
```
71.
```
cd /testbed && python -c "
import re
with open('lib/matplotlib/colorbar.py', 'r') as f:
    content = f.read()
# replace the line with new logic
pattern = r'(\s+self\.dividers\.set_segments\(\s*)np\.dstack\(\[X, Y\]\) if self\.drawedges else \[\]\)'
replacement = r'''\1if self.drawedges:
                segments = np.dstack([X, Y])
                if not self._extend_lower():
                    s …[cut]
```
72. `sed -n '650,680p' /testbed/lib/matplotlib/colorbar.py`
73. `cp /testbed/lib/matplotlib/colorbar.py.backup /testbed/lib/matplotlib/colorbar.py`
74. `grep -n "self.dividers.set_segments" /testbed/lib/matplotlib/colorbar.py`
75. `sed -n '654,660p' /testbed/lib/matplotlib/colorbar.py`
76.
```
cd /testbed && python -c "
import sys
with open('lib/matplotlib/colorbar.py', 'r') as f:
    lines = f.readlines()
# find the line with self.dividers.set_segments(
for i, line in enumerate(lines):
    if 'self.dividers.set_segments(' in line and i+2 < len(lines) and 'np.dstack([X, Y])[1:-1] if self.drawedges else []' in lines[i+1]:
        # replace lines i to i+2
        indent = line[:len(line)  …[cut]
```
77. `sed -n '654,670p' /testbed/lib/matplotlib/colorbar.py`
78.
```
cd /testbed && python -c "
import re
with open('lib/matplotlib/colorbar.py', 'r') as f:
    content = f.read()
# pattern from line 654 to line 656
pattern = r'(\s+)self\.dividers\.set_segments\(\s*\n\s*\)\n\s*\n\s*\n'
# Actually we need to match across multiple lines.
# Let's do a simpler approach: replace the three lines.
lines = content.splitlines(keepends=True)
for i in range(len(lines)-2):
    …[cut]
```
79. `sed -n '650,680p' /testbed/lib/matplotlib/colorbar.py`
80. `cp /testbed/lib/matplotlib/colorbar.py.backup /testbed/lib/matplotlib/colorbar.py`
81.
```
cd /testbed && python -c "
with open('lib/matplotlib/colorbar.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'self.dividers.set_segments(' in line:
        print(i+1, line.rstrip())
        print('next line:', lines[i+1].rstrip())
        print('next+1:', lines[i+2].rstrip())
        break
"
```
82.
```
cd /testbed && python -c "
with open('lib/matplotlib/colorbar.py', 'r') as f:
    lines = f.readlines()
# replace lines 654-656 (0-indexed 653-655)
indent = lines[653][:len(lines[653]) - len(lines[653].lstrip())]
new_lines = [
    indent + 'if self.drawedges:\n',
    indent + '    segments = np.dstack([X, Y])\n',
    indent + '    if not self._extend_lower():\n',
    indent + '        segments = s …[cut]
```
83. `sed -n '650,680p' /testbed/lib/matplotlib/colorbar.py`
84.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as mcolorbar

print('=== Bug reproduction (extend=\"both\") ===')
my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_ …[cut]
```
85. `find /testbed -name "Makefile" -o -name "tox.ini" -o -name "pytest.ini" | head -5`
86. `cat /testbed/pytest.ini`
87. `which python`
88. `/opt/miniconda3/envs/testbed/bin/python -c "import pytest; print(pytest.__version__)" 2>&1`
89. `cd /testbed && diff -u lib/matplotlib/colorbar.py.backup lib/matplotlib/colorbar.py > patch.txt 2>&1`
90. `ls -la /testbed/patch.txt 2>&1`
91. `head -30 /testbed/patch.txt`
92. `find /testbed/lib -name "check" -type f 2>/dev/null`
93.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as mcolorbar

# replicates test_colorbar_extend_drawedges
def test_one(extend, coloroffset, res):
    cmap = plt.get_cmap('viridis')
    bounds = np.arange(3)
    nb_colors = len(bounds) + coloroffset
    colors = cma …[cut]
```
94.
```
cd /testbed && python -c "
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import matplotlib.colorbar as mcolorbar

# vertical orientation
my_cmap = mpl.cm.viridis
bounds = np.arange(10)
nb_colors = len(bounds) + 1
colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
my_cmap, my_norm = from_levels_and_colors …[cut]
```
95. `cd /testbed && python -m py_compile lib/matplotlib/colorbar.py 2>&1`
96. `cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
Excellent! All four test cases pass. That means our fix matches the expected behavior for the existing test suite (at least those four parametrized cases). That's a strong indicator that our fix is correct and does not break existing functionality. Now we should also test edge cases: orientation='vertical', spacing='uniform' vs 'proportional', etc. But the bug is about drawedges and extend='both'. Our fix is based on _extend_lower and _extend_upper, which should work for any orientation. We should also test vertical orientation with extend='both' to ensure edges are drawn correctly (should be horizontal lines). Let's write a quick test.
...
Looks good. The segments are horizontal lines (y varying). We have 10 segments (should be 10 inner boundaries). That's correct. Now we need to ensure that the fix also works for extend='both' with spacing='uniform' and 'proportional'. The test already includes both spacings? Actually the test earlier (the other one) includes both spacings but we didn't examine. However, the test we just passed does not specify spacing, so it defaults to 'uniform'. That's fine. Now we should also test with hatch? Not needed. Now we have a fix that passes the existing test and resolves the bug. We should also verify that the fix doesn't break when drawedges=False. That's trivial. Now we need to create the final patch file and submit it. However, we must ensure we haven't introduced any syntax errors. Let's run a quick syntax check on the modified file.
...
No output means success. Good. Now we should also run a quick lint (flake8) maybe but we can skip. Now we need to create the patch file as required. The instructions say to create a patch file with `git diff -- path/to/file1 path/to/file2 > patch.txt`. However, we already have a patch.txt from diff. Let's ensure it only contains changes to the specific source files we modified (i.e., colorbar.py). The diff we have includes only colorbar.py. That's good. Now we need to verify that the patch only contains changes to source files (no test files). It does. Now we should also verify that the patch does not include any other modifications (like whitespace). The diff looks clean. Now we can submit the patch using the exact command: `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt` But we must ensure we are in the correct directory and that patch.txt is present. It is. Let's run the submission command.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/lib/matplotlib/colorbar.py b/lib/matplotlib/colorbar.py
index c59b0ac815..3af64c3c32 100644
--- a/lib/matplotlib/colorbar.py
+++ b/lib/matplotlib/colorbar.py
@@ -651,9 +651,15 @@ class Colorbar:
             if not self.drawedges:
                 if len(self._y) >= self.n_rasterize:
                     self.solids.set_rasterized(True)
-        self.dividers.set_segments(
-            np.dstack([X, Y])[1:-1] if self.drawedges else [])
-
+        if self.drawedges:
+            segments = np.dstack([X, Y])
+            if not self._extend_lower():
+                segments = segments[1:]
+            if not self._extend_upper():
+                segments = segments[:-1]
+            self.dividers.set_segments(segments)
+        else:
+            self.dividers.set_segments([])
     def _add_solids_patches(self, X, Y, C, mappable):
         hatches = mappable.hatches * len(C)  # Have enough hatches.
         patches = []
diff --git a/lib/matplotlib/colorbar.py.backup b/lib/matplotlib/colorbar.py.backup
new file mode 100644
index 0000000000..c59b0ac815
--- /dev/null
+++ b/lib/matplotlib/colorbar.py.backup
@@ -0,0 +1,1637 @@
+"""
+Colorbars are a visualization of the mapping from scalar values to colors.
+In Matplotlib they are drawn into a dedicated `~.axes.Axes`.
+
+.. note::
+   Colorbars are typically created through `.Figure.colorbar` or its pyplot
+   wrapper `.pyplot.colorbar`, which internally use `.Colorbar` together with
+   `.make_axes_gridspec` (for `.GridSpec`-positioned axes) or `.make_axes` (for
+   non-`.GridSpec`-positioned axes).
+
+   End-users most likely won't need to directly use this module's API.
+"""
+
+import logging
+import textwrap
+
+import numpy as np
+
+import matplotlib as mpl
+from matplotlib import _api, cbook, collections, cm, colors, contour, ticker
+import matplotlib.artist as martist
+import matplotlib.patches as mpatches
+import matplotlib.path as mpath
+import matplotlib.scale as mscale
+import matplotlib.spines as mspines
+import matplotlib.transforms as mtransforms
+from matplotlib import _docstring
+
+_log = logging.getLogger(__name__)
+
+_make_axes_kw_doc = """
+location : None or {'left', 'right', 'top', 'bottom'}
+    The location, relative to the parent axes, where the colorbar axes
+    is created.  It also determines the *orientation* of the colorbar
+    (colorbars on the left and right are vertical, colorbars at the top
+    and bottom are horizontal).  If None, the location will come from the
+    *orientation* if it is set (vertical colorbars on the right, horizontal
+    ones at the bottom), or default to 'right' if *orientation* is unset.
+
+orientation : None or {'vertical', 'horizontal'}
+    The orientation of the colorbar.  It is preferable to set the *location*
+    of the colorbar, as that also determines the *orientation*; passing
+    incompatible values for *location* and *orientation* raises an exception.
+
+fraction : float, default: 0.15
+    Fraction of original axes to use for colorbar.
+
+shrink : float, default: 1.0
+    Fraction by which to multiply the size of the colorbar.
+
+aspect : float, default: 20
+    Ratio of long to short dimensions.
+
+pad : float, default: 0.05 if vertical, 0.15 if horizontal
+    Fraction of original axes between colorbar and new image axes.
+
+anchor : (float, float), optional
+    The anchor point of the colorbar axes.
+    Defaults to (0.0, 0.5) if vertical; (0.5, 1.0) if horizontal.
+
+panchor : (float, float), or *False*, optional
+    The anchor point of the colorbar parent axes. If *False*, the parent
+    axes' anchor will be unchanged.
+    Defaults to (1.0, 0.5) if vertical; (0.5, 0.0) if horizontal.
+"""
+
+_colormap_kw_doc = """
+extend : {'neither', 'both', 'min', 'max'}
+    Make pointed end(s) for out-of-range values (unless 'neither').  These are
+    set for a given colormap using the colormap set_under and set_over methods.
+
+extendfrac : {*None*, 'auto', length, lengths}
+    If set to *None*, both the minimum and maximum triangular colorbar
+    extensions will have a length of 5% of the interior colorbar length (this
+    is the default setting).
+
+    If set to 'auto', makes the triangular colorbar extensions the same lengths
+    as the interior boxes (when *spacing* is set to 'uniform') or the same
+    lengths as the respective adjacent interior boxes (when *spacing* is set to
+    'proportional').
+
+    If a scalar, indicates the length of both the minimum and maximum
+    triangular colorbar extensions as a fraction of the interior colorbar
+    length.  A two-element sequence of fractions may also be given, indicating
+    the lengths of the minimum and maximum colorbar extensions respectively as
+    a fraction of the interior colorbar length.
+
+extendrect : bool
+    If *False* the minimum and maximum colorbar extensions will be triangular
+    (the default).  If *True* the extensions will be rectangular.
+
+spacing : {'uniform', 'proportional'}
+    For discrete colorbars (`.BoundaryNorm` or contours), 'uniform' gives each
+    color the same space; 'proportional' makes the space proportional to the
+    data interval.
+
+ticks : None or list of ticks or Locator
+    If None, ticks are determined automatically from the input.
+
+format : None or str or Formatter
+    If None, `~.ticker.ScalarFormatter` is used.
+    Format strings, e.g., ``"%4.2e"`` or ``"{x:.2e}"``, are supported.
+    An alternative `~.ticker.Formatter` may be given instead.
+
+drawedges : bool
+    Whether to draw lines at color boundaries.
+
+label : str
+    The label on the colorbar's long axis.
+
+boundaries, values : None or a sequence
+    If unset, the colormap will be displayed on a 0-1 scale.
+    If sequences, *values* must have a length 1 less than *boundaries*.  For
+    each region delimited by adjacent entries in *boundaries*, the color mapped
+    to the corresponding value in values will be used.
+    Normally only useful for indexed colors (i.e. ``norm=NoNorm()``) or other
+    unusual circumstances.
+"""
+
+_docstring.interpd.update(colorbar_doc="""
+Add a colorbar to a plot.
+
+Parameters
+----------
+mappable
+    The `matplotlib.cm.ScalarMappable` (i.e., `~matplotlib.image.AxesImage`,
+    `~matplotlib.contour.ContourSet`, etc.) described by this colorbar.
+    This argument is mandatory for the `.Figure.colorbar` method but optional
+    for the `.pyplot.colorbar` function, which sets the default to the current
+    image.
+
+    Note that one can create a `.ScalarMappable` "on-the-fly" to generate
+    colorbars not attached to a previously drawn artist, e.g. ::
+
+        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
+
+cax : `~matplotlib.axes.Axes`, optional
+    Axes into which the colorbar will be drawn.
+
+ax : `~matplotlib.axes.Axes`, list of Axes, optional
+    One or more parent axes from which space for a new colorbar axes will be
+    stolen, if *cax* is None.  This has no effect if *cax* is set.
+
+use_gridspec : bool, optional
+    If *cax* is ``None``, a new *cax* is created as an instance of Axes.  If
+    *ax* is an instance of Subplot and *use_gridspec* is ``True``, *cax* is
+    created as an instance of Subplot using the :mod:`.gridspec` module.
+
+Returns
+-------
+colorbar : `~matplotlib.colorbar.Colorbar`
+
+Notes
+-----
+Additional keyword arguments are of two kinds:
+
+  axes properties:
+%s
+  colorbar properties:
+%s
+
+If *mappable* is a `~.contour.ContourSet`, its *extend* kwarg is included
+automatically.
+
+The *shrink* kwarg provides a simple way to scale the colorbar with respect
+to the axes. Note that if *cax* is specified, it determines the size of the
+colorbar and *shrink* and *aspect* kwargs are ignored.
+
+For more precise control, you can manually specify the positions of
+the axes objects in which the mappable and the colorbar are drawn.  In
+this case, do not use any of the axes properties kwargs.
+
+It is known that some vector graphics viewers (svg and pdf) renders white gaps
+between segments of the colorbar.  This is due to bugs in the viewers, not
+Matplotlib.  As a workaround, the colorbar can be rendered with overlapping
+segments::
+
+    cbar = colorbar()
+    cbar.solids.set_edgecolor("face")
+    draw()
+
+However this has negative consequences in other circumstances, e.g. with
+semi-transparent images (alpha < 1) and colorbar extensions; therefore, this
+workaround is not used by default (see issue #1188).
+""" % (textwrap.indent(_make_axes_kw_doc, "    "),
+       textwrap.indent(_colormap_kw_doc, "    ")))
+
+
+def _set_ticks_on_axis_warn(*args, **kwargs):
+    # a top level function which gets put in at the axes'
+    # set_xticks and set_yticks by Colorbar.__init__.
+    _api.warn_external("Use the colorbar set_ticks() method instead.")
+
+
+class _ColorbarSpine(mspines.Spine):
+    def __init__(self, axes):
+        self._ax = axes
+        super().__init__(axes, 'colorbar',
+                         mpath.Path(np.empty((0, 2)), closed=True))
+        mpatches.Patch.set_transform(self, axes.transAxes)
+
+    def get_window_extent(self, renderer=None):
+        # This Spine has no Axis associated with it, and doesn't need to adjust
+        # its location, so we can directly get the window extent from the
+        # super-super-class.
+        return mpatches.Patch.get_window_extent(self, renderer=renderer)
+
+    def set_xy(self, xy):
+        self._path = mpath.Path(xy, closed=True)
+        self._xy = xy
+        self.stale = True
+
+    def draw(self, renderer):
+        ret = mpatches.Patch.draw(self, renderer)
+        self.stale = False
+        return ret
+
+
+class _ColorbarAxesLocator:
+    """
+    Shrink the axes if there are triangular or rectangular extends.
+    """
+    def __init__(self, cbar):
+        self._cbar = cbar
+        self._orig_locator = cbar.ax._axes_locator
+
+    def __call__(self, ax, renderer):
+        if self._orig_locator is not None:
+            pos = self._orig_locator(ax, renderer)
+        else:
+            pos = ax.get_position(original=True)
+        if self._cbar.extend == 'neither':
+            return pos
+
+        y, extendlen = self._cbar._proportional_y()
+        if not self._cbar._extend_lower():
+            extendlen[0] = 0
+        if not self._cbar._extend_upper():
+            extendlen[1] = 0
+        len = sum(extendlen) + 1
+        shrink = 1 / len
+        offset = extendlen[0] / len
+        # we need to reset the aspect ratio of the axes to account
+        # of the extends...
+        if hasattr(ax, '_colorbar_info'):
+            aspect = ax._colorbar_info['aspect']
+        else:
+            aspect = False
+        # now shrink and/or offset to take into account the
+        # extend tri/rectangles.
+        if self._cbar.orientation == 'vertical':
+            if aspect:
+                self._cbar.ax.set_box_aspect(aspect*shrink)
+            pos = pos.shrunk(1, shrink).translated(0, offset * pos.height)
+        else:
+            if aspect:
+                self._cbar.ax.set_box_aspect(1/(aspect * shrink))
+            pos = pos.shrunk(shrink, 1).translated(offset * pos.width, 0)
+        return pos
+
+    def get_subplotspec(self):
+        # make tight_layout happy..
+        ss = getattr(self._cbar.ax, 'get_subplotspec', None)
+        if ss is None:
+            if not hasattr(self._orig_locator, "get_subplotspec"):
+                return None
+            ss = self._orig_locator.get_subplotspec
+        return ss()
+
+
+@_docstring.Substitution(_colormap_kw_doc)
+class Colorbar:
+    r"""
+    Draw a colorbar in an existing axes.
+
+    Typically, colorbars are created using `.Figure.colorbar` or
+    `.pyplot.colorbar` and associated with `.ScalarMappable`\s (such as an
+    `.AxesImage` generated via `~.axes.Axes.imshow`).
+
+    In order to draw a colorbar not associated with other elements in the
+    figure, e.g. when showing a colormap by itself, one can create an empty
+    `
…[cut, 54217 more chars]
```

## The submitted patch (as submitted)

```diff
--- lib/matplotlib/colorbar.py.backup	2026-09-30 10:57:12.502871276 +0000
+++ lib/matplotlib/colorbar.py	2026-09-30 10:59:27.451130020 +0000
@@ -651,9 +651,15 @@
             if not self.drawedges:
                 if len(self._y) >= self.n_rasterize:
                     self.solids.set_rasterized(True)
-        self.dividers.set_segments(
-            np.dstack([X, Y])[1:-1] if self.drawedges else [])
-
+        if self.drawedges:
+            segments = np.dstack([X, Y])
+            if not self._extend_lower():
+                segments = segments[1:]
+            if not self._extend_upper():
+                segments = segments[:-1]
+            self.dividers.set_segments(segments)
+        else:
+            self.dividers.set_segments([])
     def _add_solids_patches(self, X, Y, C, mappable):
         hatches = mappable.hatches * len(C)  # Have enough hatches.
         patches = []

```
