# Item 16

**Repository:** matplotlib/matplotlib  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** NOT resolved  
**The task's test files:** lib/matplotlib/tests/test_colors.py

## The issue

Confusing (broken?) colormap name handling
Consider the following example in which one creates and registers a new colormap and attempt to use it with the `pyplot` interface.

``` python
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
matplotlib.__version__
'1.4.3.'

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                             [  2.3e-03,   1.3e-03,   1.8e-02],
                             [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)
```

Everything OK so far. Note the difference in the names `some_cmap_name` and `my_cmap_name`. Now when we try to use the new colormap things start to go wrong.

``` python
plt.set_cmap('my_cmap_name')  # All OK setting the cmap
plt.imshow([[1, 1], [2, 2]])
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-c5616dc333ed> in <module>()
----> 1 plt.imshow([[1, 1], [2, 2]])

/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/pyplot.py in imshow(X, cmap, norm, aspect, interpolation, alpha, vmin, vmax, origin, extent, shape, filternorm, filterrad, imlim, resample, url, hold, **kwargs)
   2959                         vmax=vmax, origin=origin, extent=extent, shape=shape,
   2960                         filternorm=filternorm, filterrad=filterrad,
-> 2961                         imlim=imlim, resample=resample, url=url, **kwargs)
   2962         draw_if_interactive()
   2963     finally:

/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/axes/_axes.py in imshow(self, X, cmap, norm, aspect, interpolation, alpha, vmin, vmax, origin, extent, shape, filternorm, filterrad, imlim, resample, url, **kwargs)
   4640         im = mimage.AxesImage(self, cmap, norm, interpolation, origin, extent,
   4641                        filternorm=filternorm,
-> 4642                        filterrad=filterrad, resample=resample, **kwargs)
   4643 
   4644         im.set_data(X)

/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/image.py in __init__(self, ax, cmap, norm, interpolation, origin, extent, filternorm, filterrad, resample, **kwargs)
    573                                 filterrad=filterrad,
    574                                 resample=resample,
--> 575                                 **kwargs
    576                                 )
    577 

/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/image.py in __init__(self, ax, cmap, norm, interpolation, origin, filternorm, filterrad, resample, **kwargs)
     89         """
     90         martist.Artist.__init__(self)
---> 91         cm.ScalarMappable.__init__(self, norm, cmap)
     92 
     93         if origin is None:

/usr/local/continuu
…[cut, 2785 more chars]

## The agent's commands, in order (102; outputs omitted)

1. `ls -la`
2. `find src -type f -name "*.py" | grep -E "(cm|colormap)" | head -20`
3. `find src -type f -name "*.py" | head -30`
4. `ls -la src/ lib/ extern/`
5. `grep -r "register_cmap" lib/matplotlib --include="*.py" | head -10`
6. `find lib/matplotlib -name "cm.py" -type f`
7. `head -200 lib/matplotlib/cm.py`
8. `sed -n '200,400p' lib/matplotlib/cm.py`
9. `sed -n '400,600p' lib/matplotlib/cm.py`
10. `grep -n "_ensure_cmap" lib/matplotlib/cm.py`
11. `sed -n '690,750p' lib/matplotlib/cm.py`
12. `find lib/matplotlib -name "image.py" -type f`
13. `grep -n "cm.ScalarMappable.__init__" lib/matplotlib/image.py`
14. `sed -n '250,270p' lib/matplotlib/image.py`
15. `cd /testbed && python -c "import matplotlib; print(matplotlib.__version__)"`
16.
```
cd /testbed && python -c "
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
print(matplotlib.__version__)
my_cmap_data = [[1.5e-03, 4.7e-04, 1.4e-02],
                [2.3e-03, 1.3e-03, 2.8e-02],
                [3.3e-03, 2.3e-03, 2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
cm …[cut]
```
17. `grep -r "\.name" lib/matplotlib/cm.py | head -20`
18. `grep -n "get_cmap" lib/matplotlib/image.py`
19. `grep -r "\.get_cmap" lib/matplotlib --include="*.py" | grep -v "def get_cmap" | grep -v "self.get_cmap" | head -30`
20. `grep -n "from matplotlib.cm import get_cmap" lib/matplotlib/pyplot.py`
21. `grep -n "get_cmap" lib/matplotlib/pyplot.py | head -10`
22. `grep -n "set_cmap" lib/matplotlib/cm.py`
23. `grep -n "def set_cmap" lib/matplotlib/pyplot.py`
24. `sed -n '2266,2280p' lib/matplotlib/pyplot.py`
25. `sed -n '2266,2285p' lib/matplotlib/pyplot.py`
26.
```
cd /testbed && python -c "
import warnings
warnings.filterwarnings('ignore')
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
print('Matplotlib version:', matplotlib.__version__)
my_cmap_data = [[1.5e-03, 4.7e-04, 1.4e-02],
                [2.3e-03, 1.3e-03, 2.8e-02],
                [3.3e-03, 2.3e-03, 2.4e-02]]
my_cm …[cut]
```
27. `grep -n "def copy" lib/matplotlib/colors.py`
28. `sed -n '950,970p' lib/matplotlib/colors.py`
29. `grep -n "__copy__" lib/matplotlib/colors.py`
30. `sed -n '768,780p' lib/matplotlib/colors.py`
31. `cat /testbed/check 2>/dev/null || echo "not found"`
32. `cd /testbed && python -m pytest lib/matplotlib/tests/test_colors.py -xvs -k register 2>&1 | head -50`
33. `python -c "import sys; print(sys.executable)"`
34. `python -m pytest --version 2>&1 | head -5`
35. `find /testbed -name "check" -type f 2>/dev/null | head -5`
36. `ls -la /testbed/`
37. `grep -n "check" setup.py | head -10`
38. `grep -A5 -B5 "check" README.md | head -30`
39. `pip install pytest -q 2>&1 | tail -5`
40. `grep -n "test_register_cmap" lib/matplotlib/tests/test_colors.py -A 50`
41. `sed -n '770,790p' lib/matplotlib/colors.py`
42. `grep -r "rc.*cmap" lib/matplotlib --include="*.py" | head -10`
43. `grep -n "rc('image', cmap=cmap.name)" lib/matplotlib/pyplot.py`
44. `grep -n "from matplotlib.cm import" lib/matplotlib/pyplot.py | head -5`
45. `cd /testbed && python -m unittest lib.matplotlib.tests.test_colors.test_register_cmap -v 2>&1 | head -30`
46. `which apt-get`
47. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -10`
48. `whoami`
49. `find /testbed -name "pytest*.whl" -o -name "pytest*.tar.gz" 2>/dev/null | head -5`
50. `tail -50 lib/matplotlib/cm.py`
51. `sed -n '2266,2295p' lib/matplotlib/pyplot.py`
52. `cp lib/matplotlib/cm.py lib/matplotlib/cm.py.backup`
53. `grep -n "def _ensure_cmap" lib/matplotlib/cm.py`
54. `sed -n '698,800p' lib/matplotlib/cm.py`
55. `tail -n 10 lib/matplotlib/cm.py`
56. `wc -l lib/matplotlib/cm.py`
57. `sed -n '700,723p' lib/matplotlib/cm.py`
58. `tail -n 30 lib/matplotlib/cm.py | cat -n`
59. `sed -n '723,$p' lib/matplotlib/cm.py | head -5`
60. `sed -n '723,723p' lib/matplotlib/cm.py | od -c | head -5`
61. `cd /testbed && cp lib/matplotlib/cm.py lib/matplotlib/cm.py.bak2`
62.
```
cd /testbed && python -c "
import sys
with open('lib/matplotlib/cm.py', 'r') as f:
    lines = f.readlines()
# Insert after the last line (since the function ends at the end of file)
# We'll add two newlines before our function for separation.
new_lines = lines + ['\n', '\n', 'def _get_registered_name(cmap):\n', '    \"\"\"\n', '    Return the registered name for a colormap, or None if not registe …[cut]
```
63. `tail -30 lib/matplotlib/cm.py`
64. `cp lib/matplotlib/pyplot.py lib/matplotlib/pyplot.py.backup`
65. `grep -n "rc('image', cmap=cmap.name)" lib/matplotlib/pyplot.py`
66. `sed -n '2270,2295p' lib/matplotlib/pyplot.py`
67. `grep -n "from matplotlib import pyplot" lib/matplotlib/cm.py`
68.
```
cd /testbed && python -c "
import sys
with open('lib/matplotlib/pyplot.py', 'r') as f:
    lines = f.readlines()
# find line containing rc('image', cmap=cmap.name)
for i, line in enumerate(lines):
    if line.strip() == \"rc('image', cmap=cmap.name)\":
        break
else:
    print('Line not found')
    sys.exit(1)
# Replace that line with new logic
indent = line[:len(line) - len(line.lstrip())]
n …[cut]
```
69. `sed -n '2270,2300p' lib/matplotlib/pyplot.py`
70. `cp lib/matplotlib/pyplot.py.backup lib/matplotlib/pyplot.py`
71.
```
cd /testbed && python -c "
import re
with open('lib/matplotlib/pyplot.py', 'r') as f:
    content = f.read()
# Find the set_cmap function
pattern = r'(\s+def set_cmap\(cmap: Colormap \| str\) -> None:\s*\"\"\"[\s\S]*?)(\s+rc\\(\"image\", cmap=cmap\\.name\\))'
match = re.search(pattern, content)
if not match:
    print('Pattern not found')
    exit(1)
full_match = match.group(0)
indent = match.grou …[cut]
```
72. `sed -n '2275,2295p' lib/matplotlib/pyplot.py`
73. `grep -n "from matplotlib.cm import" lib/matplotlib/pyplot.py`
74. `sed -i '75s/from matplotlib.cm import _colormaps as colormaps/from matplotlib.cm import _colormaps as colormaps, _get_registered_name/' lib/matplotlib/pyplot.py`
75. `sed -n '75p' lib/matplotlib/pyplot.py`
76. `sed -n '2260,2290p' lib/matplotlib/pyplot.py | cat -n`
77.
```
cd /testbed && python -c "
with open('lib/matplotlib/pyplot.py', 'r') as f:
    lines = f.readlines()
# line numbers are 1-indexed
rc_line_idx = 2283 - 1  # convert to 0-index
assert lines[rc_line_idx].strip() == \"rc('image', cmap=cmap.name)\"
indent = lines[rc_line_idx][:len(lines[rc_line_idx]) - len(lines[rc_line_idx].lstrip())]
# Build new block
new_block = [
    indent + '    # Determine the  …[cut]
```
78. `sed -n '2260,2300p' lib/matplotlib/pyplot.py`
79. `grep -n "def set_cmap\|def imread" lib/matplotlib/pyplot.py`
80.
```
cd /testbed && python -c "
with open('lib/matplotlib/pyplot.py', 'r') as f:
    lines = f.readlines()
start = None
for i, line in enumerate(lines):
    if line.strip().startswith('def set_cmap'):
        start = i
        break
if start is None:
    print('Function not found')
    exit(1)
# Find the next function after start
end = None
for i in range(start + 1, len(lines)):
    if lines[i].strip() …[cut]
```
81. `sed -n '2266,2300p' lib/matplotlib/pyplot.py`
82. `cp lib/matplotlib/pyplot.py.backup lib/matplotlib/pyplot.py`
83. `sed -n '75p' lib/matplotlib/pyplot.py`
84. `sed -i '75s/from matplotlib.cm import _colormaps as colormaps/from matplotlib.cm import _colormaps as colormaps, _get_registered_name/' lib/matplotlib/pyplot.py`
85.
```
cd /testbed && python -c "
import sys
with open('lib/matplotlib/pyplot.py', 'r') as f:
    lines = f.readlines()
# find line with rc('image', cmap=cmap.name)
for i, line in enumerate(lines):
    if line.strip() == \"rc('image', cmap=cmap.name)\":
        rc_idx = i
        break
else:
    print('Line not found')
    sys.exit(1)
# Determine base indentation from the line before (cmap = get_cmap(cma …[cut]
```
86. `sed -n '2260,2300p' lib/matplotlib/pyplot.py`
87.
```
cd /testbed && python -c "
import warnings
warnings.filterwarnings('ignore')
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
print('Matplotlib version:', matplotlib.__version__)
my_cmap_data = [[1.5e-03, 4.7e-04, 1.4e-02],
                [2.3e-03, 1.3e-03, 2.8e-02],
                [3.3e-03, 2.3e-03, 2.4e-02]]
my_cm …[cut]
```
88. `find /testbed -name "*test*.py" -type f | grep -v __pycache__ | head -5`
89. `ls /testbed/requirements/`
90. `cat /testbed/requirements/testing`
91. `ls /testbed/requirements/testing/`
92. `grep -i pytest /testbed/requirements/testing/all.txt`
93. `python -c "import sys; print(sys.executable); import pkgutil; print(pkgutil.find_loader('pytest'))" 2>&1`
94. `find /testbed -name "pytest*.whl" -type f 2>/dev/null | head -5`
95.
```
cd /testbed && cat > test_cmap_fix.py << 'EOF'
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

print("Testing colormap name handling fix...")

# 1. Original bug: register with different name, set_cmap with registered name
cmap_data = [[0,0,1], [0,1,0], [1,0,0 …[cut]
```
96.
```
cd /testbed && cat > test_cmap_fix2.py << 'EOF'
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

print("Testing colormap name handling fix...")

# 1. Original bug: register with different name, set_cmap with registered name
cmap_data = [[0,0,1], [0,1,0], [1,0, …[cut]
```
97. `cd /testbed && python -m py_compile lib/matplotlib/cm.py 2>&1 | head -20`
98. `cd /testbed && python -m py_compile lib/matplotlib/pyplot.py 2>&1 | head -20`
99. `cd /testbed && git diff -- lib/matplotlib/cm.py lib/matplotlib/pyplot.py 2>&1 | head -100`
100. `cd /testbed && git diff -- lib/matplotlib/cm.py lib/matplotlib/pyplot.py > patch.txt`
101. `cat /testbed/patch.txt`
102. `cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
Perfect. The diff shows exactly the changes we intended. Now we need to ensure we haven't introduced any unintended changes (like extra whitespace). The diff looks clean. Now we need to create the patch file `patch.txt` with only the changes to source files (non-test files). The instructions say: "Creating/viewing the patch and submitting it MUST be separate commands (not combined with &&). If you modify patch.txt after verifying, you SHOULD verify again before submitting." We'll create the patch file now.
...
Now verify the patch file.
...
Looks good. Now we need to verify that the patch only contains changes to the specific source files we intended. It does not include any test files or configuration files. That's fine. Now we need to submit the patch using the exact command required: ```bash echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt ``` But note: we must separate the creation and submission. We already created patch.txt. Now we need to submit by running that command.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/lib/matplotlib/cm.py b/lib/matplotlib/cm.py
index 38158db956..01252a8e01 100644
--- a/lib/matplotlib/cm.py
+++ b/lib/matplotlib/cm.py
@@ -721,3 +721,24 @@ def _ensure_cmap(cmap):
     # the internal usage of this (ValueError vs KeyError)
     _api.check_in_list(sorted(_colormaps), cmap=cmap_name)
     return mpl.colormaps[cmap_name]
+
+
+def _get_registered_name(cmap):
+    """
+    Return the registered name for a colormap, or None if not registered.
+
+    Parameters
+    ----------
+    cmap : matplotlib.colors.Colormap
+        The colormap to look up.
+
+    Returns
+    -------
+    name : str or None
+        The registered name if cmap is in the registry, else None.
+    """
+    for name, registered in _colormaps._cmaps.items():
+        if registered == cmap:
+            return name
+    return None
+
diff --git a/lib/matplotlib/cm.py.backup b/lib/matplotlib/cm.py.backup
new file mode 100644
index 0000000000..38158db956
--- /dev/null
+++ b/lib/matplotlib/cm.py.backup
@@ -0,0 +1,723 @@
+"""
+Builtin colormaps, colormap handling utilities, and the `ScalarMappable` mixin.
+
+.. seealso::
+
+  :doc:`/gallery/color/colormap_reference` for a list of builtin colormaps.
+
+  :ref:`colormap-manipulation` for examples of how to make
+  colormaps.
+
+  :ref:`colormaps` an in-depth discussion of choosing
+  colormaps.
+
+  :ref:`colormapnorms` for more details about data normalization.
+"""
+
+from collections.abc import Mapping
+import functools
+
+import numpy as np
+from numpy import ma
+
+import matplotlib as mpl
+from matplotlib import _api, colors, cbook, scale
+from matplotlib._cm import datad
+from matplotlib._cm_listed import cmaps as cmaps_listed
+
+
+_LUTSIZE = mpl.rcParams['image.lut']
+
+
+def _gen_cmap_registry():
+    """
+    Generate a dict mapping standard colormap names to standard colormaps, as
+    well as the reversed colormaps.
+    """
+    cmap_d = {**cmaps_listed}
+    for name, spec in datad.items():
+        cmap_d[name] = (  # Precache the cmaps at a fixed lutsize..
+            colors.LinearSegmentedColormap(name, spec, _LUTSIZE)
+            if 'red' in spec else
+            colors.ListedColormap(spec['listed'], name)
+            if 'listed' in spec else
+            colors.LinearSegmentedColormap.from_list(name, spec, _LUTSIZE))
+    # Generate reversed cmaps.
+    for cmap in list(cmap_d.values()):
+        rmap = cmap.reversed()
+        cmap_d[rmap.name] = rmap
+    return cmap_d
+
+
+class ColormapRegistry(Mapping):
+    r"""
+    Container for colormaps that are known to Matplotlib by name.
+
+    The universal registry instance is `matplotlib.colormaps`. There should be
+    no need for users to instantiate `.ColormapRegistry` themselves.
+
+    Read access uses a dict-like interface mapping names to `.Colormap`\s::
+
+        import matplotlib as mpl
+        cmap = mpl.colormaps['viridis']
+
+    Returned `.Colormap`\s are copies, so that their modification does not
+    change the global definition of the colormap.
+
+    Additional colormaps can be added via `.ColormapRegistry.register`::
+
+        mpl.colormaps.register(my_colormap)
+    """
+    def __init__(self, cmaps):
+        self._cmaps = cmaps
+        self._builtin_cmaps = tuple(cmaps)
+        # A shim to allow register_cmap() to force an override
+        self._allow_override_builtin = False
+
+    def __getitem__(self, item):
+        try:
+            return self._cmaps[item].copy()
+        except KeyError:
+            raise KeyError(f"{item!r} is not a known colormap name") from None
+
+    def __iter__(self):
+        return iter(self._cmaps)
+
+    def __len__(self):
+        return len(self._cmaps)
+
+    def __str__(self):
+        return ('ColormapRegistry; available colormaps:\n' +
+                ', '.join(f"'{name}'" for name in self))
+
+    def __call__(self):
+        """
+        Return a list of the registered colormap names.
+
+        This exists only for backward-compatibility in `.pyplot` which had a
+        ``plt.colormaps()`` method. The recommended way to get this list is
+        now ``list(colormaps)``.
+        """
+        return list(self)
+
+    def register(self, cmap, *, name=None, force=False):
+        """
+        Register a new colormap.
+
+        The colormap name can then be used as a string argument to any ``cmap``
+        parameter in Matplotlib. It is also available in ``pyplot.get_cmap``.
+
+        The colormap registry stores a copy of the given colormap, so that
+        future changes to the original colormap instance do not affect the
+        registered colormap. Think of this as the registry taking a snapshot
+        of the colormap at registration.
+
+        Parameters
+        ----------
+        cmap : matplotlib.colors.Colormap
+            The colormap to register.
+
+        name : str, optional
+            The name for the colormap. If not given, ``cmap.name`` is used.
+
+        force : bool, default: False
+            If False, a ValueError is raised if trying to overwrite an already
+            registered name. True supports overwriting registered colormaps
+            other than the builtin colormaps.
+        """
+        _api.check_isinstance(colors.Colormap, cmap=cmap)
+
+        name = name or cmap.name
+        if name in self:
+            if not force:
+                # don't allow registering an already existing cmap
+                # unless explicitly asked to
+                raise ValueError(
+                    f'A colormap named "{name}" is already registered.')
+            elif (name in self._builtin_cmaps
+                    and not self._allow_override_builtin):
+                # We don't allow overriding a builtin unless privately
+                # coming from register_cmap()
+                raise ValueError("Re-registering the builtin cmap "
+                                 f"{name!r} is not allowed.")
+
+            # Warn that we are updating an already existing colormap
+            _api.warn_external(f"Overwriting the cmap {name!r} "
+                               "that was already in the registry.")
+
+        self._cmaps[name] = cmap.copy()
+
+    def unregister(self, name):
+        """
+        Remove a colormap from the registry.
+
+        You cannot remove built-in colormaps.
+
+        If the named colormap is not registered, returns with no error, raises
+        if you try to de-register a default colormap.
+
+        .. warning::
+
+            Colormap names are currently a shared namespace that may be used
+            by multiple packages. Use `unregister` only if you know you
+            have registered that name before. In particular, do not
+            unregister just in case to clean the name before registering a
+            new colormap.
+
+        Parameters
+        ----------
+        name : str
+            The name of the colormap to be removed.
+
+        Raises
+        ------
+        ValueError
+            If you try to remove a default built-in colormap.
+        """
+        if name in self._builtin_cmaps:
+            raise ValueError(f"cannot unregister {name!r} which is a builtin "
+                             "colormap.")
+        self._cmaps.pop(name, None)
+
+    def get_cmap(self, cmap):
+        """
+        Return a color map specified through *cmap*.
+
+        Parameters
+        ----------
+        cmap : str or `~matplotlib.colors.Colormap` or None
+
+            - if a `.Colormap`, return it
+            - if a string, look it up in ``mpl.colormaps``
+            - if None, return the Colormap defined in :rc:`image.cmap`
+
+        Returns
+        -------
+        Colormap
+        """
+        # get the default color map
+        if cmap is None:
+            return self[mpl.rcParams["image.cmap"]]
+
+        # if the user passed in a Colormap, simply return it
+        if isinstance(cmap, colors.Colormap):
+            return cmap
+        if isinstance(cmap, str):
+            _api.check_in_list(sorted(_colormaps), cmap=cmap)
+            # otherwise, it must be a string so look it up
+            return self[cmap]
+        raise TypeError(
+            'get_cmap expects None or an instance of a str or Colormap . ' +
+            f'you passed {cmap!r} of type {type(cmap)}'
+        )
+
+
+# public access to the colormaps should be via `matplotlib.colormaps`. For now,
+# we still create the registry here, but that should stay an implementation
+# detail.
+_colormaps = ColormapRegistry(_gen_cmap_registry())
+globals().update(_colormaps)
+
+
+@_api.deprecated("3.7", alternative="``matplotlib.colormaps.register(name)``")
+def register_cmap(name=None, cmap=None, *, override_builtin=False):
+    """
+    Add a colormap to the set recognized by :func:`get_cmap`.
+
+    Register a new colormap to be accessed by name ::
+
+        LinearSegmentedColormap('swirly', data, lut)
+        register_cmap(cmap=swirly_cmap)
+
+    Parameters
+    ----------
+    name : str, optional
+       The name that can be used in :func:`get_cmap` or :rc:`image.cmap`
+
+       If absent, the name will be the :attr:`~matplotlib.colors.Colormap.name`
+       attribute of the *cmap*.
+
+    cmap : matplotlib.colors.Colormap
+       Despite being the second argument and having a default value, this
+       is a required argument.
+
+    override_builtin : bool
+
+        Allow built-in colormaps to be overridden by a user-supplied
+        colormap.
+
+        Please do not use this unless you are sure you need it.
+    """
+    _api.check_isinstance((str, None), name=name)
+    if name is None:
+        try:
+            name = cmap.name
+        except AttributeError as err:
+            raise ValueError("Arguments must include a name or a "
+                             "Colormap") from err
+    # override_builtin is allowed here for backward compatibility
+    # this is just a shim to enable that to work privately in
+    # the global ColormapRegistry
+    _colormaps._allow_override_builtin = override_builtin
+    _colormaps.register(cmap, name=name, force=override_builtin)
+    _colormaps._allow_override_builtin = False
+
+
+def _get_cmap(name=None, lut=None):
+    """
+    Get a colormap instance, defaulting to rc values if *name* is None.
+
+    Parameters
+    ----------
+    name : `matplotlib.colors.Colormap` or str or None, default: None
+        If a `.Colormap` instance, it will be returned. Otherwise, the name of
+        a colormap known to Matplotlib, which will be resampled by *lut*. The
+        default, None, means :rc:`image.cmap`.
+    lut : int or None, default: None
+        If *name* is not already a Colormap instance and *lut* is not None, the
+        colormap will be resampled to have *lut* entries in the lookup table.
+
+    Returns
+    -------
+    Colormap
+    """
+    if name is None:
+        name = mpl.rcParams['image.cmap']
+    if isinstance(name, colors.Colormap):
+        return name
+    _api.check_in_list(sorted(_colormaps), name=name)
+    if lut is None:
+        return _colormaps[name]
+    else:
+        return _colormaps[name].resampled(lut)
+
+# do it in two steps like this so we can have an un-deprecated version in
+# pyplot.
+get_cmap = _api.deprecated(
+    '3.7',
+    name='get_cmap',
+    alternative=(
+        "``matplotlib.colormaps[name]`` " +
+        "or ``matplotlib.colormaps.get_cmap(obj)``"
+    )
+)(_get_cmap)
+
+
+@_api.deprecated("3.7",
+                 alternative="``matplotlib.colormaps.unregister(name)``")
+def unregister_cmap(name):
+    """
+    Remove a colormap recognized by :func:`get_cmap`.
+
+    You may not remove built-in colormaps.
+
+    If the named colormap is not registered, returns with no error, raises
+    if you try to de-register a default colormap.
+
+    .. warning::
+
+      Colormap names are currently a shared namespace that may be used
+      by multiple packages. Use `unregister_cmap` only if you know you
+      have registered that name bef
…[cut, 188403 more chars]
```

## The submitted patch (as submitted)

```diff
diff --git a/lib/matplotlib/cm.py b/lib/matplotlib/cm.py
index 38158db956..01252a8e01 100644
--- a/lib/matplotlib/cm.py
+++ b/lib/matplotlib/cm.py
@@ -721,3 +721,24 @@ def _ensure_cmap(cmap):
     # the internal usage of this (ValueError vs KeyError)
     _api.check_in_list(sorted(_colormaps), cmap=cmap_name)
     return mpl.colormaps[cmap_name]
+
+
+def _get_registered_name(cmap):
+    """
+    Return the registered name for a colormap, or None if not registered.
+
+    Parameters
+    ----------
+    cmap : matplotlib.colors.Colormap
+        The colormap to look up.
+
+    Returns
+    -------
+    name : str or None
+        The registered name if cmap is in the registry, else None.
+    """
+    for name, registered in _colormaps._cmaps.items():
+        if registered == cmap:
+            return name
+    return None
+
diff --git a/lib/matplotlib/pyplot.py b/lib/matplotlib/pyplot.py
index 58ce4c03fa..bb90f7cee2 100644
--- a/lib/matplotlib/pyplot.py
+++ b/lib/matplotlib/pyplot.py
@@ -72,7 +72,7 @@ from matplotlib import mlab  # for detrend_none, window_hanning
 from matplotlib.scale import get_scale_names
 
 from matplotlib import cm
-from matplotlib.cm import _colormaps as colormaps
+from matplotlib.cm import _colormaps as colormaps, _get_registered_name
 from matplotlib.cm import register_cmap  # type: ignore
 from matplotlib.colors import _color_sequences as color_sequences
 
@@ -2280,7 +2280,12 @@ def set_cmap(cmap: Colormap | str) -> None:
     """
     cmap = get_cmap(cmap)
 
-    rc('image', cmap=cmap.name)
+    # Determine the registered name if any
+    registered_name = _get_registered_name(cmap)
+    if registered_name is not None:
+        rc("image", cmap=registered_name)
+    else:
+        rc("image", cmap=cmap.name)
     im = gci()
 
     if im is not None:

```
