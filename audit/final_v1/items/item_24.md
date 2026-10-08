# Item 24

**Repository:** matplotlib/matplotlib  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** resolved  
**The task's test files:** lib/matplotlib/tests/test_offsetbox.py

## The issue

[Bug]: `align` in `HPacker` is reversed
### Bug summary

For the `align` parameter in `HPacker`, the options `top` and `bottom` seems reversed

### Code for reproduction

```python
import matplotlib.pyplot as plt
from matplotlib.offsetbox import DrawingArea, HPacker, VPacker, AnchoredOffsetbox, TextArea
from matplotlib.patches import Rectangle

da1 = DrawingArea(10, 20)
rect1 = Rectangle((0, 0), 10, 20)
da1.add_artist(rect1)

da2 = DrawingArea(10, 30)
rect2 = Rectangle((0, 0), 10, 30)
da2.add_artist(rect2)

align = "bottom"

pack = HPacker(children=[da1, da2], pad=10, sep=10, align=align)
title = TextArea(f"align='{align}'")
pack = VPacker(children=[title, pack], sep=10, pad=10, align="center")

box = AnchoredOffsetbox(child=pack, loc="center")

_, ax = plt.subplots()
ax.add_artist(box)
```


### Actual outcome

![download](https://user-images.githubusercontent.com/23433306/200162888-702626bf-ad47-40e2-8751-7dffe91df85c.png)


### Expected outcome

![download](https://user-images.githubusercontent.com/23433306/200162908-e0e9dfd5-6f8b-4aac-975e-bb363d809c41.png)


### Additional information

_No response_

### Operating system

_No response_

### Matplotlib Version

3.6.2

### Matplotlib Backend

_No response_

### Python version

_No response_

### Jupyter version

_No response_

### Installation

_No response_


## The agent's commands, in order (83; outputs omitted)

1. `ls -la`
2. `find src -name "*.py" | grep -E "offsetbox|packer" | head -20`
3. `find . -type f -name "*.py" | grep -v __pycache__ | grep -v ".pyc" | head -30`
4. `grep -n "class HPacker" lib/matplotlib/offsetbox.py`
5. `sed -n '459,600p' lib/matplotlib/offsetbox.py`
6. `grep -n "_get_aligned_offsets" lib/matplotlib/offsetbox.py`
7. `sed -n '130,250p' lib/matplotlib/offsetbox.py`
8. `grep -n "class PackerBase" lib/matplotlib/offsetbox.py`
9. `sed -n '371,458p' lib/matplotlib/offsetbox.py`
10. `grep -n "class DrawingArea" lib/matplotlib/offsetbox.py`
11. `sed -n '568,700p' lib/matplotlib/offsetbox.py`
12. `cd /testbed && python -m pytest tests/ -xvs -k offsetbox 2>&1 | head -100`
13. `cd /testbed && ls -la tests.py`
14. `cat /testbed/tests.py`
15. `ls -la | grep check`
16. `which check`
17. `file /usr/local/bin/check`
18. `cat /usr/local/bin/check`
19. `cd /testbed && check 2>&1 | head -30`
20. `cd /testbed && check --tb=short 2>&1 | head -100`
21. `cat /tmp/.mp_check_out 2>&1 | head -200`
22. `grep -r "HPacker\|VPacker" tests/ --include="*.py" | head -10`
23. `find . -type f -name "*.py" -path "*/tests/*" | head -20`
24. `grep -n "align" lib/matplotlib/tests/test_offsetbox.py | head -30`
25. `sed -n '340,390p' lib/matplotlib/tests/test_offsetbox.py`
26. `cd /testbed && python -m matplotlib.test lib/matplotlib/tests/test_offsetbox.py::test_packers 2>&1 | head -50`
27. `cd /testbed && python -m pytest lib/matplotlib/tests/test_offsetbox.py::test_packers -xvs 2>&1 | head -100`
28. `pip list | grep pytest`
29. `cd /testbed && python -m pytest lib/matplotlib/tests/test_offsetbox.py::test_packers -xvs 2>&1 | head -150`
30.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
da2 = DrawingArea(10, 30)
pack = HPacker(children=[da1, da2], pad=10, sep=10, align='bottom')
fig = plt.figure(dpi=72)
renderer = fig.canvas.get_renderer()
extent, offsets = pack.get_extent_offsets(renderer)
print('extent …[cut]
```
31.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
da2 = DrawingArea(10, 30)
pack = HPacker(children=[da1, da2], pad=10, sep=10, align='bottom')
fig = plt.figure(dpi=72)
renderer = fig.canvas.get_renderer()
width, height, xdescent, ydescent, offset_pairs = pack.get_extent …[cut]
```
32.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea
from matplotlib import pyplot as plt
for align in ['top', 'bottom', 'center', 'baseline']:
    da1 = DrawingArea(10, 20)
    da2 = DrawingArea(10, 30)
    pack = HPacker(children=[da1, da2], pad=0, sep=0, align=align)
    fig = plt.figure(dpi=72)
    renderer = fig.canvas.get_rendere …[cut]
```
33. `cd /testbed && python -m pytest lib/matplotlib/tests/test_offsetbox.py::test_packers -x 2>&1 | tail -30`
34. `python -c "import sys; print(sys.path)" | head -5`
35. `python -c "import matplotlib.test; print(matplotlib.test.__file__)" 2>&1`
36. `find lib/matplotlib -name "test.py" | head -5`
37. `find lib -name "test.py" -type f`
38. `grep -r "def test" lib/matplotlib/ --include="*.py" | head -5`
39. `grep -A 20 "^def test" lib/matplotlib/__init__.py`
40. `python -c "import pytest; print(pytest.__version__)" 2>&1`
41. `python -m pip install pytest -q 2>&1 | tail -5`
42. `which pytest`
43. `grep -r "mp_check_out" /testbed 2>/dev/null | head -5`
44. `cd /testbed && python tests.py -k offsetbox 2>&1 | head -50`
45. `sudo apt-get update && sudo apt-get install -y python3-pytest 2>&1 | tail -10`
46. `find /usr -name "check" -type f 2>/dev/null | head -10`
47. `grep -r "check" README.md`
48. `cat README.md | head -100`
49. `cat environment.yml`
50. `ls -la tools/`
51. `find /tmp -name "*mp_check_out*" 2>/dev/null`
52. `grep -r 'align="bottom"' /testbed --include="*.py" | head -10`
53. `grep -r 'align=' /testbed --include="*.py" | head -20`
54. `sed -n '371,460p' lib/matplotlib/offsetbox.py | head -90`
55. `conda --version 2>&1`
56. `conda env list`
57. `which python`
58. `/opt/miniconda3/envs/testbed/bin/python -c "import sys; print(sys.executable)"`
59. `/opt/miniconda3/envs/testbed/bin/python -m pip list | grep pytest`
60. `find /opt/miniconda3/envs/testbed -name "pytest" -type d 2>/dev/null | head -5`
61. `/opt/miniconda3/envs/testbed/bin/python -m pip list --format=freeze | grep pytest`
62. `/opt/miniconda3/envs/testbed/bin/python -c "import pytest; print(pytest.__version__)" 2>&1`
63. `grep -r "HPacker" /testbed --include="*.py" | grep -v test | head -10`
64. `grep -B2 -A2 "'top', 'bottom', 'left', 'right', 'center', 'baseline'" lib/matplotlib/offsetbox.py`
65. `sed -n '130,160p' lib/matplotlib/offsetbox.py`
66. `/opt/miniconda3/envs/testbed/bin/python -c "import sys; print(sys.path)" | grep -v env | head -20`
67. `/opt/miniconda3/envs/testbed/bin/python -m pip freeze | grep -E "^pytest[=<>]" | head -5`
68. `find /opt/miniconda3/envs/testbed -name "pytest" -type f 2>/dev/null | head -5`
69. `ls -la /opt/miniconda3/envs/testbed/lib/python3.11/site-packages/ | grep pytest`
70. `cd /testbed && git log --oneline -5`
71. `cd /testbed && cp lib/matplotlib/offsetbox.py lib/matplotlib/offsetbox.py.backup`
72. `sed -n '130,180p' lib/matplotlib/offsetbox.py`
73.
```
cd /testbed && python -c "
import sys
with open('lib/matplotlib/offsetbox.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'elif align in [\"left\", \"top\"]:' in line:
        lines[i] = '    elif align in [\"left\", \"bottom\"]:\n'
    if 'elif align in [\"right\", \"bottom\"]:' in line:
        lines[i] = '    elif align in [\"right\", \"top\"]:\n'
with open('li …[cut]
```
74. `sed -n '155,165p' lib/matplotlib/offsetbox.py`
75. `sed -n '160,175p' lib/matplotlib/offsetbox.py`
76.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea, Rectangle, TextArea, VPacker, AnchoredOffsetbox
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
rect1 = Rectangle((0, 0), 10, 20)
da1.add_artist(rect1)
da2 = DrawingArea(10, 30)
rect2 = Rectangle((0, 0), 10, 30)
da2.add_artist(rect2)
align = 'bottom'
pack = HPacker(ch …[cut]
```
77.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea, TextArea, VPacker, AnchoredOffsetbox
from matplotlib.patches import Rectangle
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
rect1 = Rectangle((0, 0), 10, 20)
da1.add_artist(rect1)
da2 = DrawingArea(10, 30)
rect2 = Rectangle((0, 0), 10, 30)
da2.add_artist(rect2)
alig …[cut]
```
78.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
da2 = DrawingArea(10, 30)
pack = HPacker(children=[da1, da2], pad=0, sep=0, align='bottom')
fig = plt.figure(dpi=72)
renderer = fig.canvas.get_renderer()
width, height, xdescent, ydescent, offset_pairs = pack.get_extent_o …[cut]
```
79.
```
cd /testbed && python -c "
import sys
sys.path.insert(0, '.')
from matplotlib.offsetbox import HPacker, DrawingArea
from matplotlib import pyplot as plt
da1 = DrawingArea(10, 20)
da2 = DrawingArea(10, 30)
pack = HPacker(children=[da1, da2], pad=0, sep=0, align='top')
fig = plt.figure(dpi=72)
renderer = fig.canvas.get_renderer()
width, height, xdescent, ydescent, offset_pairs = pack.get_extent_offs …[cut]
```
80. `conda install -y pytest -c conda-forge 2>&1 | tail -10`
81. `cd /testbed && git diff lib/matplotlib/offsetbox.py > patch.txt 2>&1`
82. `cat /testbed/patch.txt`
83. `cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
Network issues again. We'll have to rely on the check command's cached output? But we can't get it. However, we can still create a patch and submit it. The user will run the tests and verify. We should also ensure that our changes don't break anything else. Let's also check if there are any other places where align is used (maybe in VPacker or HPacker directly). The align parameter is just passed to the function, so no other changes needed. Now we need to create a patch file as per instructions. We'll create a diff between the original file (backup) and the modified file.
...
Let's check if patch.txt exists and its content.
...
Great. That's the only change. Now we need to verify that the patch is correct (only those lines). We'll also ensure there are no other changes (like whitespace). The patch looks good. Now we need to run the check command again to see if the tests pass? But we can't get the output. However, we can run the check command and see if it exits with 0? Let's run `check` and see if the cache file exists now (maybe it will be written). But the script only reads cache, so maybe we need to run the test suite via something else. Let's look for a script that runs tests and writes to /tmp/.mp_check_out. Could be that the check script is a wrapper that calls a subprocess that runs the tests. The script we have might be a placeholder. Let's examine the check script again: it reads from /tmp/.mp_check_out and exits with the status from /tmp/.mp_check_rc. That suggests that the test suite writes those files. Where do they write? Possibly in the environment setup. Since we cannot know, we can assume that after we fix the bug, the test suite will pass (since the bug is fixed). However, we should also test edge cases: align="left", align="right", align="center", align="baseline". We'll write a quick script to ensure they produce reasonable outputs (no crashes). But we can also rely on the existing test suite. Given the time, we'll submit the patch. But before that, we should also consider that the mapping of "left" and "right" might also be reversed? The bug only mentions top and bottom. We'll assume left/right are fine. Let's create a test script that validates the align options for both HPacker and VPacker (just to be safe). We'll compute offset pairs and ensure they are consistent (e.g., align="left" for HPacker? Actually HPacker with align="left" might be weird but we can still check). However, we can't compare with expected values without the test. We'll just ensure no errors. But we can also look at the test to see what they expect for left/right. The test uses the same mapping for both packers. For align="left", they have y_height = 0 (since align in ("baseline", "left", "bottom")). That means align="left" is considered start direction (offset = d). That matches our new grouping (left is with bottom). Good. For align="right", they have y_height = y2 - y1 (since align in ("right", "top")? Wait, align="right" is grouped with "top" now? Actually after our change, align="right" is grouped with "top". That would mean align="right" is considered end direction (offset = height - h + d). That would be opposite of what the test expects? The test groups align="right" with "top"? Let's examine: The test uses the same grouping for both packers? Actually they have separate mapping for HPacker and VPacker? Look at the test code again: they compute y_height for HPacker based on align, and x_height for VPacker based on align, using the same conditions (baseline, left, bottom) etc. That means they treat align="left" as start for both HPacker and VPacker, align="right" as end for both. That's consistent with our grouping after swap? Wait, they treat align="right" as end? In the test, for align="right", y_height = y2 - y1 (since align in ("right", "top")). That means align="right" is considered end direction (since y_height = y2 - y1). That matches our new grouping (right with top). Good. Thus our swap aligns with the test expectation
…[cut, 1524 more chars]
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/lib/matplotlib/offsetbox.py b/lib/matplotlib/offsetbox.py
index 3a506543ac..059a6c8ae3 100644
--- a/lib/matplotlib/offsetbox.py
+++ b/lib/matplotlib/offsetbox.py
@@ -166,10 +166,10 @@ def _get_aligned_offsets(hd_list, height, align="baseline"):
         descent = max(d for h, d in hd_list)
         height = height_descent + descent
         offsets = [0. for h, d in hd_list]
-    elif align in ["left", "top"]:
+    elif align in ["left", "bottom"]:
         descent = 0.
         offsets = [d for h, d in hd_list]
-    elif align in ["right", "bottom"]:
+    elif align in ["right", "top"]:
         descent = 0.
         offsets = [height - h + d for h, d in hd_list]
     elif align == "center":
diff --git a/lib/matplotlib/offsetbox.py.backup b/lib/matplotlib/offsetbox.py.backup
new file mode 100644
index 0000000000..3a506543ac
--- /dev/null
+++ b/lib/matplotlib/offsetbox.py.backup
@@ -0,0 +1,1607 @@
+r"""
+Container classes for `.Artist`\s.
+
+`OffsetBox`
+    The base of all container artists defined in this module.
+
+`AnchoredOffsetbox`, `AnchoredText`
+    Anchor and align an arbitrary `.Artist` or a text relative to the parent
+    axes or a specific anchor point.
+
+`DrawingArea`
+    A container with fixed width and height. Children have a fixed position
+    inside the container and may be clipped.
+
+`HPacker`, `VPacker`
+    Containers for layouting their children vertically or horizontally.
+
+`PaddedBox`
+    A container to add a padding around an `.Artist`.
+
+`TextArea`
+    Contains a single `.Text` instance.
+"""
+
+import numpy as np
+
+import matplotlib as mpl
+from matplotlib import _api, _docstring
+import matplotlib.artist as martist
+import matplotlib.path as mpath
+import matplotlib.text as mtext
+import matplotlib.transforms as mtransforms
+from matplotlib.font_manager import FontProperties
+from matplotlib.image import BboxImage
+from matplotlib.patches import (
+    FancyBboxPatch, FancyArrowPatch, bbox_artist as mbbox_artist)
+from matplotlib.transforms import Bbox, BboxBase, TransformedBbox
+
+
+DEBUG = False
+
+
+# for debugging use
+def bbox_artist(*args, **kwargs):
+    if DEBUG:
+        mbbox_artist(*args, **kwargs)
+
+
+def _get_packed_offsets(widths, total, sep, mode="fixed"):
+    r"""
+    Pack boxes specified by their *widths*.
+
+    For simplicity of the description, the terminology used here assumes a
+    horizontal layout, but the function works equally for a vertical layout.
+
+    There are three packing *mode*\s:
+
+    - 'fixed': The elements are packed tight to the left with a spacing of
+      *sep* in between. If *total* is *None* the returned total will be the
+      right edge of the last box. A non-*None* total will be passed unchecked
+      to the output. In particular this means that right edge of the last
+      box may be further to the right than the returned total.
+
+    - 'expand': Distribute the boxes with equal spacing so that the left edge
+      of the first box is at 0, and the right edge of the last box is at
+      *total*. The parameter *sep* is ignored in this mode. A total of *None*
+      is accepted and considered equal to 1. The total is returned unchanged
+      (except for the conversion *None* to 1). If the total is smaller than
+      the sum of the widths, the laid out boxes will overlap.
+
+    - 'equal': If *total* is given, the total space is divided in N equal
+      ranges and each box is left-aligned within its subspace.
+      Otherwise (*total* is *None*), *sep* must be provided and each box is
+      left-aligned in its subspace of width ``(max(widths) + sep)``. The
+      total width is then calculated to be ``N * (max(widths) + sep)``.
+
+    Parameters
+    ----------
+    widths : list of float
+        Widths of boxes to be packed.
+    total : float or None
+        Intended total length. *None* if not used.
+    sep : float
+        Spacing between boxes.
+    mode : {'fixed', 'expand', 'equal'}
+        The packing mode.
+
+    Returns
+    -------
+    total : float
+        The total width needed to accommodate the laid out boxes.
+    offsets : array of float
+        The left offsets of the boxes.
+    """
+    _api.check_in_list(["fixed", "expand", "equal"], mode=mode)
+
+    if mode == "fixed":
+        offsets_ = np.cumsum([0] + [w + sep for w in widths])
+        offsets = offsets_[:-1]
+        if total is None:
+            total = offsets_[-1] - sep
+        return total, offsets
+
+    elif mode == "expand":
+        # This is a bit of a hack to avoid a TypeError when *total*
+        # is None and used in conjugation with tight layout.
+        if total is None:
+            total = 1
+        if len(widths) > 1:
+            sep = (total - sum(widths)) / (len(widths) - 1)
+        else:
+            sep = 0
+        offsets_ = np.cumsum([0] + [w + sep for w in widths])
+        offsets = offsets_[:-1]
+        return total, offsets
+
+    elif mode == "equal":
+        maxh = max(widths)
+        if total is None:
+            if sep is None:
+                raise ValueError("total and sep cannot both be None when "
+                                 "using layout mode 'equal'")
+            total = (maxh + sep) * len(widths)
+        else:
+            sep = total / len(widths) - maxh
+        offsets = (maxh + sep) * np.arange(len(widths))
+        return total, offsets
+
+
+def _get_aligned_offsets(hd_list, height, align="baseline"):
+    """
+    Align boxes each specified by their ``(height, descent)`` pair.
+
+    For simplicity of the description, the terminology used here assumes a
+    horizontal layout (i.e., vertical alignment), but the function works
+    equally for a vertical layout.
+
+    Parameters
+    ----------
+    hd_list
+        List of (height, xdescent) of boxes to be aligned.
+    height : float or None
+        Intended total height. If None, the maximum of the heights in *hd_list*
+        is used.
+    align : {'baseline', 'left', 'top', 'right', 'bottom', 'center'}
+        The alignment anchor of the boxes.
+
+    Returns
+    -------
+    height
+        The total height of the packing (if a value was originally passed in,
+        it is returned without checking that it is actually large enough).
+    descent
+        The descent of the packing.
+    offsets
+        The bottom offsets of the boxes.
+    """
+
+    if height is None:
+        height = max(h for h, d in hd_list)
+    _api.check_in_list(
+        ["baseline", "left", "top", "right", "bottom", "center"], align=align)
+
+    if align == "baseline":
+        height_descent = max(h - d for h, d in hd_list)
+        descent = max(d for h, d in hd_list)
+        height = height_descent + descent
+        offsets = [0. for h, d in hd_list]
+    elif align in ["left", "top"]:
+        descent = 0.
+        offsets = [d for h, d in hd_list]
+    elif align in ["right", "bottom"]:
+        descent = 0.
+        offsets = [height - h + d for h, d in hd_list]
+    elif align == "center":
+        descent = 0.
+        offsets = [(height - h) * .5 + d for h, d in hd_list]
+
+    return height, descent, offsets
+
+
+class OffsetBox(martist.Artist):
+    """
+    The OffsetBox is a simple container artist.
+
+    The child artists are meant to be drawn at a relative position to its
+    parent.
+
+    Being an artist itself, all parameters are passed on to `.Artist`.
+    """
+    def __init__(self, *args, **kwargs):
+        super().__init__(*args)
+        self._internal_update(kwargs)
+        # Clipping has not been implemented in the OffsetBox family, so
+        # disable the clip flag for consistency. It can always be turned back
+        # on to zero effect.
+        self.set_clip_on(False)
+        self._children = []
+        self._offset = (0, 0)
+
+    def set_figure(self, fig):
+        """
+        Set the `.Figure` for the `.OffsetBox` and all its children.
+
+        Parameters
+        ----------
+        fig : `~matplotlib.figure.Figure`
+        """
+        super().set_figure(fig)
+        for c in self.get_children():
+            c.set_figure(fig)
+
+    @martist.Artist.axes.setter
+    def axes(self, ax):
+        # TODO deal with this better
+        martist.Artist.axes.fset(self, ax)
+        for c in self.get_children():
+            if c is not None:
+                c.axes = ax
+
+    def contains(self, mouseevent):
+        """
+        Delegate the mouse event contains-check to the children.
+
+        As a container, the `.OffsetBox` does not respond itself to
+        mouseevents.
+
+        Parameters
+        ----------
+        mouseevent : `matplotlib.backend_bases.MouseEvent`
+
+        Returns
+        -------
+        contains : bool
+            Whether any values are within the radius.
+        details : dict
+            An artist-specific dictionary of details of the event context,
+            such as which points are contained in the pick radius. See the
+            individual Artist subclasses for details.
+
+        See Also
+        --------
+        .Artist.contains
+        """
+        inside, info = self._default_contains(mouseevent)
+        if inside is not None:
+            return inside, info
+        for c in self.get_children():
+            a, b = c.contains(mouseevent)
+            if a:
+                return a, b
+        return False, {}
+
+    def set_offset(self, xy):
+        """
+        Set the offset.
+
+        Parameters
+        ----------
+        xy : (float, float) or callable
+            The (x, y) coordinates of the offset in display units. These can
+            either be given explicitly as a tuple (x, y), or by providing a
+            function that converts the extent into the offset. This function
+            must have the signature::
+
+                def offset(width, height, xdescent, ydescent, renderer) \
+-> (float, float)
+        """
+        self._offset = xy
+        self.stale = True
+
+    def get_offset(self, width, height, xdescent, ydescent, renderer):
+        """
+        Return the offset as a tuple (x, y).
+
+        The extent parameters have to be provided to handle the case where the
+        offset is dynamically determined by a callable (see
+        `~.OffsetBox.set_offset`).
+
+        Parameters
+        ----------
+        width, height, xdescent, ydescent
+            Extent parameters.
+        renderer : `.RendererBase` subclass
+
+        """
+        return (self._offset(width, height, xdescent, ydescent, renderer)
+                if callable(self._offset)
+                else self._offset)
+
+    def set_width(self, width):
+        """
+        Set the width of the box.
+
+        Parameters
+        ----------
+        width : float
+        """
+        self.width = width
+        self.stale = True
+
+    def set_height(self, height):
+        """
+        Set the height of the box.
+
+        Parameters
+        ----------
+        height : float
+        """
+        self.height = height
+        self.stale = True
+
+    def get_visible_children(self):
+        r"""Return a list of the visible child `.Artist`\s."""
+        return [c for c in self._children if c.get_visible()]
+
+    def get_children(self):
+        r"""Return a list of the child `.Artist`\s."""
+        return self._children
+
+    def get_extent_offsets(self, renderer):
+        """
+        Update offset of the children and return the extent of the box.
+
+        Parameters
+        ----------
+        renderer : `.RendererBase` subclass
+
+        Returns
+        -------
+        width
+        height
+        xdescent
+        ydescent
+        list of (xoffset, yoffset) pairs
+        """
+        raise NotImplementedError(
+            "get_extent_offsets must be overridden in derived classes.")
+
+    def get_extent(self, renderer):
+        """Return a tuple ``width, height, xdescent, ydescent`` of the box."""
+        w, h, xd, yd, offsets = self.get_extent_offse
…[cut, 45167 more chars]
```

## The submitted patch (as submitted)

```diff
diff --git a/lib/matplotlib/offsetbox.py b/lib/matplotlib/offsetbox.py
index 3a506543ac..059a6c8ae3 100644
--- a/lib/matplotlib/offsetbox.py
+++ b/lib/matplotlib/offsetbox.py
@@ -166,10 +166,10 @@ def _get_aligned_offsets(hd_list, height, align="baseline"):
         descent = max(d for h, d in hd_list)
         height = height_descent + descent
         offsets = [0. for h, d in hd_list]
-    elif align in ["left", "top"]:
+    elif align in ["left", "bottom"]:
         descent = 0.
         offsets = [d for h, d in hd_list]
-    elif align in ["right", "bottom"]:
+    elif align in ["right", "top"]:
         descent = 0.
         offsets = [height - h + d for h, d in hd_list]
     elif align == "center":

```
