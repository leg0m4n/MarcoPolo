# Item 25

**Repository:** matplotlib/matplotlib  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
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

## The agent's commands, in order (113; outputs omitted)

1. `find /testbed -type f -name "*.py" | grep -E "(cm|colormap)" | head -20`
2. `ls -la /testbed/`
3. `cat /testbed/lib/matplotlib/cm.py | head -200`
4. `cat /testbed/lib/matplotlib/cm.py | tail -200`
5. `grep -n "_colormaps\|def get_cmap" /testbed/lib/matplotlib/cm.py`
6. `cat /testbed/lib/matplotlib/cm.py | sed -n '220,310p'`
7. `cat /testbed/lib/matplotlib/cm.py | sed -n '720,740p'`
8. `grep -n "class ScalarMappable" /testbed/lib/matplotlib/cm.py`
9. `cat /testbed/lib/matplotlib/cm.py | sed -n '373,450p'`
10. `grep -n "def get_cmap" /testbed/lib/matplotlib/cm.py`
11. `cat /testbed/lib/matplotlib/cm.py | sed -n '180,210p'`
12. `grep -n "^get_cmap = " /testbed/lib/matplotlib/cm.py`
13. `cat /testbed/lib/matplotlib/cm.py | sed -n '250,310p'`
14. `find /testbed -name "pyplot.py" -type f | head -5`
15. `grep -n "def set_cmap" /testbed/lib/matplotlib/pyplot.py`
16. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2280p'`
17. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2290p'`
18. `cat /testbed/lib/matplotlib/cm.py | sed -n '700,730p'`
19. `cat /testbed/lib/matplotlib/pyplot.py | grep -B5 -A5 "def set_cmap"`
20.
```
cd /testbed && python3 -c "
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
print('Version:', matplotlib.__version__)

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list( …[cut]
```
21. `grep -n "colormaps" /testbed/lib/matplotlib/__init__.py`
22.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
print('Version:', matplotlib.__version__)

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list( …[cut]
```
23. `cd /testbed && python3 -c "import matplotlib.cm as cm; print(dir(cm))"`
24.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
print('Version:', matplotlib.__version__)

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list …[cut]
```
25. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2280p'`
26. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2285p'`
27. `cat /testbed/lib/matplotlib/cm.py | sed -n '220,240p'`
28. `grep -n "^get_cmap = " /testbed/lib/matplotlib/pyplot.py`
29. `grep -n "get_cmap" /testbed/lib/matplotlib/pyplot.py | head -20`
30. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2258,2265p'`
31. `cat /testbed/lib/matplotlib/cm.py | sed -n '250,310p'`
32.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

# Test 1: Register with different names
print('Test 1: Register with different names')
my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', [[0,0,1], [1,0,0]])
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)

plt.set_cmap('my_c …[cut]
```
33. `grep -n "def set_cmap" /testbed/lib/matplotlib/axes/_axes.py`
34. `grep -n "def set_cmap" /testbed/lib/matplotlib/image.py`
35. `cat /testbed/lib/matplotlib/image.py | sed -n '1204,1220p'`
36. `grep -n "def set_cmap" /testbed/lib/matplotlib/cm.py`
37. `cat /testbed/lib/matplotlib/cm.py | sed -n '574,600p'`
38. `grep -r "rc('image', cmap=" /testbed/lib/matplotlib/ --include="*.py" | head -10`
39. `grep -r "rcParams\['image\.cmap'\]" /testbed/lib/matplotlib/ --include="*.py" | head -20`
40. `grep -n "name = mpl.rcParams\['image.cmap'\]" /testbed/lib/matplotlib/cm.py`
41. `cat /testbed/lib/matplotlib/cm.py | sed -n '280,300p'`
42. `find /testbed -name "*.py" -type f -exec grep -l "set_cmap" {} \; | grep -i test | head -10`
43. `grep -n "set_cmap" /testbed/lib/matplotlib/tests/test_colors.py | head -20`
44. `cat /testbed/lib/matplotlib/tests/test_colors.py | sed -n '1646,1680p'`
45. `cat /testbed/lib/matplotlib/tests/test_colors.py | sed -n '1654,1680p'`
46. `grep -n "def register" /testbed/lib/matplotlib/cm.py`
47. `cat /testbed/lib/matplotlib/cm.py | sed -n '103,140p'`
48.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
print('my …[cut]
```
49. `cd /testbed && python3 -m pytest lib/matplotlib/tests/test_colors.py::test_set_cmap_mismatched_name -xvs`
50. `cd /testbed && cat pyproject.toml | grep -A5 -B5 "test"`
51. `cd /testbed && ls -la`
52. `cd /testbed && cat README.md | head -50`
53. `cd /testbed && ls -la | grep check`
54. `find /testbed -name "check" -type f`
55. `cd /testbed && python3 setup.py --help-commands | grep test`
56.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
print('my …[cut]
```
57. `cat /testbed/lib/matplotlib/cm.py | sed -n '220,265p'`
58. `cat /testbed/lib/matplotlib/cm.py | sed -n '103,180p'`
59.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

# Create a colormap with one name
cmap1 = LinearSegmentedColormap.from_list('test-cmap', [[0,0,1], [1,0,0]])
print('cmap1.name:', cmap1.name)

# Register it with a different name (simulating the test)
# Actually, we need to check what matpl …[cut]
```
60. `cat /testbed/lib/matplotlib/tests/test_colors.py | sed -n '1654,1680p'`
61.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps

cmap1 = colormaps['viridis']
print('viridis.name:', cmap1.name)
cmap2 = cmap1.with_extremes(over='r')
print('cmap2.name:', cmap2.name)
"
```
62.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps
import matplotlib.pyplot as plt

cmap = colormaps['viridis'].with_extremes(over='r')
print('cmap.name before:', cmap.name)
cmap.name = 'test-cmap'
print('cmap.name after:', cmap.name)

# Register using new API
colormaps.register(name='wrong-cmap', cmap=cmap)
print('registered')

# Get it back using pyplot
plt.set_cmap(' …[cut]
```
63. `grep -B5 -A5 "test_set_cmap_mismatched_name" /testbed/lib/matplotlib/tests/test_colors.py`
64.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps
import matplotlib.pyplot as plt

cmap = colormaps['viridis'].with_extremes(over='r')
print('cmap.name before:', cmap.name)
cmap.name = 'test-cmap'
print('cmap.name after:', cmap.name)

# Register using new API
colormaps.register(name='wrong-cmap', cmap=cmap)
print('registered')

# Check what's in the registry
print('col …[cut]
```
65. `cd /testbed && python3 -m pytest lib/matplotlib/tests/test_colors.py::test_set_cmap_mismatched_name -xvs 2>&1 | tail -50`
66. `cd /testbed && python3 -c "import sys; print(sys.executable); import pytest; print(pytest.__version__)" 2>&1`
67. `cd /testbed && cat requirements/default.txt | head -20`
68. `cd /testbed && ls -la requirements/`
69. `cd /testbed && grep -i test pyproject.toml`
70. `cd /testbed && find . -name "check" -type f 2>/dev/null`
71. `cd /testbed && find . -name "*.py" -type f -exec grep -l "def check" {} \; 2>/dev/null | head -10`
72. `cd /testbed && ls -la | grep -i check`
73. `cd /testbed && ls -la tools/`
74. `cd /testbed && cat tools/README.txt`
75. `cd /testbed && pip install pytest 2>&1 | tail -20`
76. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2285p'`
77. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2290p'`
78. `cat /testbed/lib/matplotlib/pyplot.py | sed -n '2266,2300p'`
79. `cd /testbed && cp lib/matplotlib/pyplot.py lib/matplotlib/pyplot.py.backup`
80. `cd /testbed && sed -i '2266,2290p' lib/matplotlib/pyplot.py`
81.
```
cd /testbed && python3 -c "
import re

# Read the file
with open('lib/matplotlib/pyplot.py', 'r') as f:
    content = f.read()

# Find the set_cmap function
pattern = r'def set_cmap\(cmap: Colormap \| str\) -> None:\n.*?\n\n'
match = re.search(pattern, content, re.DOTALL)

if match:
    print('Found set_cmap function')
    # Print a sample
    print(match.group(0)[:200])
else:
    print('Function  …[cut]
```
82. `cd /testbed && head -2300 lib/matplotlib/pyplot.py | tail -50`
83. `cd /testbed && cp lib/matplotlib/pyplot.py.backup lib/matplotlib/pyplot.py`
84. `cd /testbed && grep -n "def set_cmap" lib/matplotlib/pyplot.py`
85. `cd /testbed && sed -n '2266,2290p' lib/matplotlib/pyplot.py`
86.
```
cd /testbed && cat > fix_set_cmap.py << 'EOF'
import re

# Read the file
with open('lib/matplotlib/pyplot.py', 'r') as f:
    lines = f.readlines()

# Find the set_cmap function
start_line = None
for i, line in enumerate(lines):
    if line.strip() == 'def set_cmap(cmap: Colormap | str) -> None:':
        start_line = i
        break

if start_line is None:
    print("Could not find set_cmap funct …[cut]
```
87.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

print('Testing the fix...')

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_cmap_n …[cut]
```
88.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps
import matplotlib.pyplot as plt

# Create a colormap
cmap1 = colormaps['viridis'].with_extremes(over='r')
print('cmap1.name:', cmap1.name)

# Pass it directly to set_cmap
plt.set_cmap(cmap1)
print('After set_cmap(cmap1), rc(\"image.cmap\"):', plt.rcParams['image.cmap'])

# Get it back
cm2 = plt.get_cmap('viridis')  # Us …[cut]
```
89. `cat /testbed/lib/matplotlib/cm.py | sed -n '710,730p'`
90.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.pyplot as plt

cmap = matplotlib.colormaps['viridis'].with_extremes(over='r')
print('cmap.name:', cmap.name)
cmap.name = 'test-cmap'
print('after rename:', cmap.name)

matplotlib.colormaps.register(name='wrong-cmap', cmap=cmap)
print('registered')

plt.set_cmap('wrong-cmap')
print('after set_cmap')

cmap_returned = plt.get_cmap('wrong …[cut]
```
91. `cd /testbed && git log --oneline -n 5 lib/matplotlib/tests/test_colors.py 2>&1 | head -20`
92. `cd /testbed && git diff 164974f228 lib/matplotlib/tests/test_colors.py 2>&1 | head -100`
93. `cd /testbed && grep -A20 "def test_set_cmap_mismatched_name" lib/matplotlib/tests/test_colors.py`
94.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps

cmap = colormaps['viridis'].with_extremes(over='r')
print('cmap.name:', cmap.name)
cmap.name = 'test-cmap'
print('after rename:', cmap.name)

colormaps.register(name='wrong-cmap', cmap=cmap)
print('registered')

# Get it via colormaps
retrieved = colormaps['wrong-cmap']
print('retrieved.name:', retrieved.name)
print('r …[cut]
```
95. `cd /testbed && git log --oneline -p --follow lib/matplotlib/tests/test_colors.py | grep -A50 -B5 "test_set_cmap_mismatched_name" | head -100`
96. `cd /testbed && git show 0205b4a20e:lib/matplotlib/tests/test_colors.py | grep -A20 "test_set_cmap_mismatched_name"`
97. `cd /testbed && git show 164974f228:lib/matplotlib/tests/test_colors.py | grep -A20 "test_set_cmap_mismatched_name"`
98. `cat /testbed/lib/matplotlib/cm.py | sed -n '103,180p'`
99.
```
cd /testbed && python3 -c "
from matplotlib import colormaps
import matplotlib.colors as colors

cmap = colormaps['viridis']
print('cmap.name:', cmap.name)
print('hasattr(cmap, \"name\"):', hasattr(cmap, 'name'))

# Can we change it?
cmap.name = 'newname'
print('after change:', cmap.name)

# Create a new colormap
new_cmap = colors.LinearSegmentedColormap('newname', {'red': [(0,0,1)], 'green': [(0, …[cut]
```
100. `cd /testbed && python3 -m pytest lib/matplotlib/tests/test_colors.py -xvs 2>&1 | tail -100`
101. `cd /testbed && find . -name ".pre-commit-config.yaml" -type f | xargs cat`
102. `cd /testbed && ls -la | grep -E "Makefile|setup.py"`
103. `cd /testbed && pip install pytest -q 2>&1 | tail -20`
104.
```
cd /testbed && cat > fix_register.py << 'EOF'
import re

# Read the file
with open('lib/matplotlib/cm.py', 'r') as f:
    content = f.read()

# Find the register method in ColormapRegistry
# We need to find the line "self._cmaps[name] = cmap.copy()" and modify it
# Actually, we should change the name of the copy after copying

# The issue is that we need to import the copy function
# But actually, …[cut]
```
105.
```
cd /testbed && python3 -c "
import matplotlib
from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

print('Testing the fix...')

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                 [  2.3e-03,   1.3e-03,   1.8e-02],
                 [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = LinearSegmentedColormap.from_list('some_ …[cut]
```
106. `grep -n "def register_cmap" /testbed/lib/matplotlib/cm.py`
107. `cat /testbed/lib/matplotlib/cm.py | sed -n '224,265p'`
108. `grep -n "def unregister_cmap" /testbed/lib/matplotlib/cm.py`
109. `cat /testbed/lib/matplotlib/cm.py | sed -n '309,320p'`
110.
```
cd /testbed && python3 -c "
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

print('Testing basic colormap functionality...')

# Test 1: Built-in colormap
cmap1 = plt.get_cmap('viridis')
print(f'viridis.name: {cmap1.name}')

# Test 2: Register and get back
cmap2 = mcolors.LinearSegmentedColormap.from_list('mycmap', [[0,0,1], [1,0,0]])
from matplotlib import co …[cut]
```
111.
```
cd /testbed && cat > test_issue_fix.py << 'EOF'
"""
Test for the fix of the colormap name handling issue described in the issue.

The issue was:
- When you register a colormap with name 'my_cmap_name' but the colormap
  object has name 'some_cmap_name', calling plt.set_cmap('my_cmap_name')
  would set rc('image.cmap') to 'some_cmap_name' instead of 'my_cmap_name'.
- This caused errors when later t …[cut]
```
112. `cat /testbed/lib/matplotlib/cm.py | sed -n '250,310p'`
113.
```
cd /testbed && python3 -c "
import matplotlib.pyplot as plt

# Test what rc('image', cmap=...) expects
print('Testing rc(\"image\", cmap=\"test\")')
plt.rc('image', cmap='test')
print(f'rcParams[\"image.cmap\"]: {plt.rcParams[\"image.cmap\"]}')

print()
print('Testing rc(\"image\", cmap=None)')
plt.rc('image', cmap=None)
print(f'rcParams[\"image.cmap\"]: {plt.rcParams[\"image.cmap\"]}')
"
```

## The agent's last reasoning (last 3 turns)

```
Great! The basic functionality works. Now I should create a comprehensive test to verify the fix for the original issue.
...
There's an issue with Test 3. When we pass a colormap object directly to `set_cmap`, it sets `rc('image.cmap')` to the colormap's name ('mycolormap'). But then when we call `plt.get_cmap()` (without arguments), it tries to look up 'mycolormap' in the registry, but it's not registered! This is actually expected behavior. If you pass a colormap object directly to `set_cmap`, you're setting that colormap as the default. The name stored in `rc('image.cmap')` is the colormap's internal name. But `plt.get_cmap()` (without arguments) tries to look up that name in the registry, which fails because unregistered colormaps can't be looked up via name. Actually, looking at the error message, `plt.get_cmap()` calls `_get_cmap(name=None)`, which then sets `name = mpl.rcParams['image.cmap']` (which is 'mycolormap'). Then it checks if 'mycolormap' is in the registry. But it's not registered! This is actually a pre-existing issue, not something I introduced. If you set the default colormap to an unregistered colormap via `set_cmap(cmap_object)`, then `plt.get_cmap()` will fail because it can't find the colormap by name. But wait, `plt.get_cmap()` without arguments should return the colormap from `rc('image.cmap')`. It should use that name to look up the colormap. But unregistered colormaps can't be looked up by name. Actually, I think the issue is that `plt.get_cmap()` should work even if the colormap wasn't registered. It should return the colormap that's stored as the default (from `rc('image.cmap')`), not look it up by name. Let me check the implementation of `_get_cmap`.
...
So `_get_cmap` has a problem: if `name` is None, it gets the name from `rcParams['image.cmap']`. Then if that name is not in the registry (because it was set via `set_cmap(cmap_object)`), it fails. But actually, I think this is a pre-existing bug, not something I introduced. Let me test this with the original code (before my fixes). Actually, wait - I already modified the file. Let me check if this issue exists in the original code by looking at the test that was failing before. Actually, the test `test_set_cmap_mismatched_name` expects `cmap_returned.name == "wrong-cmap"`. So with the original code, if you call `plt.set_cmap("wrong-cmap")` (which looks up the registered colormap), then `plt.get_cmap()` (without arguments) should return that colormap. That should work because "wrong-cmap" is in the registry. So the issue I'm seeing in Test 3 might be a real bug in matplotlib: you can't set an unregistered colormap as the default via `set_cmap(cmap_object)`. But actually, that seems like a reasonable expectation. If you pass a colormap object to `set_cmap`, you're setting that specific colormap object as the default. `plt.get_cmap()` should return that same object, not try to look it up by name. The problem is that `_get_cmap` assumes that the name in `rcParams['image.cmap']` is a registered name. But it could be a colormap's internal name. Actually, I think the fix should be: if `_get_cmap` receives a name that's not in the registry, and that name is not None, maybe it should still return the colormap? But how would it know which colormap? Actually, I think the issue is that `rcParams['image.cmap']` should store the colormap object itself, not its name. But that's a bigger change. Given that this is a pre-existing issue and not something I introduced with my fix, I should probably not try to fix it now. My fix addresses the specific issue described in the problem statement. But wait, let me check if my `set_cmap` implementation has this issue. In my implementation, when `cmap` is a Colormap object, I set `rc('image', cmap=cmap_obj.name)`. So `rc('image.cmap')` is set to the colormap's name. Then when `plt.get_cmap()` is called (without arguments), it tries to look up that name in the registry, which fails. Actually, I think I should fix this in m
…[cut, 223 more chars]
```

## Final state of the repository (git diff vs the starting commit)

### Test files (shown in full)

```diff
diff --git a/test_issue_fix.py b/test_issue_fix.py
new file mode 100644
index 0000000000..cee1ff99ba
--- /dev/null
+++ b/test_issue_fix.py
@@ -0,0 +1,144 @@
+"""
+Test for the fix of the colormap name handling issue described in the issue.
+
+The issue was:
+- When you register a colormap with name 'my_cmap_name' but the colormap
+  object has name 'some_cmap_name', calling plt.set_cmap('my_cmap_name')
+  would set rc('image.cmap') to 'some_cmap_name' instead of 'my_cmap_name'.
+- This caused errors when later trying to use the colormap.
+
+The fix:
+1. Modified the register method to store a copy with the registered name,
+   not the original colormap name.
+2. Modified set_cmap to use the registered name for rc('image.cmap') when
+   a string is passed (the registered name), not the colormap's internal name.
+"""
+
+import matplotlib
+import matplotlib.pyplot as plt
+from matplotlib.colors import LinearSegmentedColormap
+from matplotlib import colormaps
+
+def test_original_issue():
+    """Test the exact scenario from the issue description."""
+    print("Test 1: Original issue scenario")
+    print("-" * 40)
+    
+    my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
+                     [  2.3e-03,   1.3e-03,   1.8e-02],
+                     [  3.3e-03,   2.3e-03,   2.4e-02]]
+    my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
+    print(f"my_cmap.name: {my_cmap.name}")
+    
+    # Register with different name
+    colormaps.register(name='my_cmap_name', cmap=my_cmap)
+    
+    # Verify the registered colormap has the registered name
+    registered_cmap = colormaps['my_cmap_name']
+    print(f"colormaps['my_cmap_name'].name: {registered_cmap.name}")
+    assert registered_cmap.name == 'my_cmap_name', \
+        f"Expected 'my_cmap_name', got {registered_cmap.name}"
+    
+    # This should not raise an error
+    plt.set_cmap('my_cmap_name')
+    print(f"After set_cmap('my_cmap_name'), rc['image.cmap']: {plt.rcParams['image.cmap']}")
+    assert plt.rcParams['image.cmap'] == 'my_cmap_name', \
+        f"Expected rc['image.cmap'] to be 'my_cmap_name', got {plt.rcParams['image.cmap']}"
+    
+    # This should work without error
+    fig, ax = plt.subplots()
+    im = ax.imshow([[1, 1], [2, 2]])
+    print("plt.imshow([[1, 1], [2, 2]]) succeeded")
+    
+    plt.close(fig)
+    print("Test 1 passed!\n")
+    
+
+def test_mismatched_name_registration():
+    """Test registering a colormap with a different name than its internal name."""
+    print("Test 2: Mismatched name registration")
+    print("-" * 40)
+    
+    # Create a colormap with one name
+    cmap1 = LinearSegmentedColormap.from_list('test-cmap', [[0, 0, 1], [1, 0, 0]])
+    print(f"cmap1.name: {cmap1.name}")
+    
+    # Register it with a different name
+    colormaps.register(name='wrong-cmap', cmap=cmap1)
+    
+    # The registered colormap should have the registered name
+    retrieved = colormaps['wrong-cmap']
+    print(f"colormaps['wrong-cmap'].name: {retrieved.name}")
+    assert retrieved.name == 'wrong-cmap', \
+        f"Expected 'wrong-cmap', got {retrieved.name}"
+    
+    # set_cmap should use the registered name
+    plt.set_cmap('wrong-cmap')
+    assert plt.rcParams['image.cmap'] == 'wrong-cmap', \
+        f"Expected rc['image.cmap'] to be 'wrong-cmap', got {plt.rcParams['image.cmap']}"
+    
+    # get_cmap should return a colormap with the registered name
+    cmap2 = plt.get_cmap('wrong-cmap')
+    print(f"plt.get_cmap('wrong-cmap').name: {cmap2.name}")
+    assert cmap2.name == 'wrong-cmap', \
+        f"Expected 'wrong-cmap', got {cmap2.name}"
+    
+    plt.close('all')
+    print("Test 2 passed!\n")
+    
+
+def test_set_cmap_with_colormap_object():
+    """Test that set_cmap with a colormap object uses its name."""
+    print("Test 3: set_cmap with colormap object")
+    print("-" * 40)
+    
+    # Create a colormap
+    cmap1 = LinearSegmentedColormap.from_list('mycolormap', [[0, 1, 0], [1, 0, 0]])
+    print(f"cmap1.name: {cmap1.name}")
+    
+    # Pass it directly to set_cmap
+    plt.set_cmap(cmap1)
+    
+    # rc('image.cmap') should be set to the colormap's name
+    assert plt.rcParams['image.cmap'] == 'mycolormap', \
+        f"Expected rc['image.cmap'] to be 'mycolormap', got {plt.rcParams['image.cmap']}"
+    
+    # get_cmap() (no arguments) should return the same colormap
+    cmap2 = plt.get_cmap()
+    assert cmap2.name == 'mycolormap', \
+        f"Expected 'mycolormap', got {cmap2.name}"
+    
+    plt.close('all')
+    print("Test 3 passed!\n")
+    
+
+def test_backward_compatibility():
+    """Test that the fix doesn't break existing functionality."""
+    print("Test 4: Backward compatibility")
+    print("-" * 40)
+    
+    # Test with built-in colormaps
+    cmap1 = plt.get_cmap('viridis')
+    assert cmap1.name == 'viridis'
+    
+    # Register and unregister
+    cmap2 = LinearSegmentedColormap.from_list('tempcmap', [[0, 0, 1], [1, 0, 0]])
+    colormaps.register(name='tempcmap', cmap=cmap2)
+    assert 'tempcmap' in colormaps
+    
+    colormaps.unregister('tempcmap')
+    assert 'tempcmap' not in colormaps
+    
+    print("Test 4 passed!\n")
+
+if __name__ == '__main__':
+    print("Running tests for colormap name handling fix\n")
+    print("=" * 60)
+    
+    test_original_issue()
+    test_mismatched_name_registration()
+    test_set_cmap_with_colormap_object()
+    test_backward_compatibility()
+    
+    print("=" * 60)
+    print("All tests passed!")

```

### All other files

```diff
diff --git a/fix_register.py b/fix_register.py
new file mode 100644
index 0000000000..4477580e5f
--- /dev/null
+++ b/fix_register.py
@@ -0,0 +1,71 @@
+import re
+
+# Read the file
+with open('lib/matplotlib/cm.py', 'r') as f:
+    content = f.read()
+
+# Find the register method in ColormapRegistry
+# We need to find the line "self._cmaps[name] = cmap.copy()" and modify it
+# Actually, we should change the name of the copy after copying
+
+# The issue is that we need to import the copy function
+# But actually, we can just set cmap_copy.name = name after copying
+
+# Let me rewrite the register method more cleanly
+
+# Find the register method
+pattern = r'(\s+)self\._cmaps\[name\] = cmap\.copy\(\)'
+match = re.search(pattern, content)
+
+if match:
+    print(f"Found at: {match.start()}")
+    print(f"Indentation: {match.group(1)}")
+    
+    # We need to modify this line to set the name of the copy
+    # But we need to be careful not to break anything
+    
+    # Actually, let me check what happens after this line
+    # There's nothing else in the method
+    
+    # We could change it to:
+    # self._cmaps[name] = cmap.copy()
+    # self._cmaps[name].name = name
+    
+    # But actually, we should do this for all register methods, not just ColormapRegistry.register
+    # Because there's also register_cmap which calls _colormaps.register
+    
+    # Let me check if there are other register methods
+else:
+    print("Pattern not found")
+    
+# Let me try a different approach - rewrite the entire register method
+lines = content.split('\n')
+
+# Find the start of the register method
+for i, line in enumerate(lines):
+    if 'def register(self, cmap, *, name=None, force=False):' in line:
+        print(f"Found register method at line {i+1}")
+        
+        # Find the end of the method
+        for j in range(i, len(lines)):
+            if lines[j].strip() == '' and j > i + 50:
+                print(f"Method ends around line {j+1}")
+                
+                # Replace the line with cmap.copy()
+                for k in range(i, j):
+                    if 'self._cmaps[name] = cmap.copy()' in lines[k]:
+                        print(f"Found copy line at {k+1}: {lines[k]}")
+                        # Modify it
+                        indent = len(lines[k]) - len(lines[k].lstrip())
+                        spaces = ' ' * indent
+                        lines[k] = f'{spaces}self._cmaps[name] = cmap.copy()\n{spaces}self._cmaps[name].name = name'
+                        print(f"Modified line {k+1}")
+                        break
+                break
+        break
+
+# Write back
+with open('lib/matplotlib/cm.py', 'w') as f:
+    f.write('\n'.join(lines))
+    
+print("Fixed register method")
diff --git a/fix_set_cmap.py b/fix_set_cmap.py
new file mode 100644
index 0000000000..f6282a8560
--- /dev/null
+++ b/fix_set_cmap.py
@@ -0,0 +1,82 @@
+import re
+
+# Read the file
+with open('lib/matplotlib/pyplot.py', 'r') as f:
+    lines = f.readlines()
+
+# Find the set_cmap function
+start_line = None
+for i, line in enumerate(lines):
+    if line.strip() == 'def set_cmap(cmap: Colormap | str) -> None:':
+        start_line = i
+        break
+
+if start_line is None:
+    print("Could not find set_cmap function")
+    exit(1)
+
+# Find the end of the function (next empty line after the body)
+end_line = start_line
+for i in range(start_line + 1, len(lines)):
+    if lines[i].strip() == '' and i > start_line + 20:  # Skip the docstring
+        end_line = i
+        break
+    elif i == len(lines) - 1:
+        end_line = len(lines) - 1
+        break
+
+# Extract the function
+func_lines = lines[start_line:end_line+1]
+
+# Find the line with 'cmap = get_cmap(cmap)'
+for i, line in enumerate(func_lines):
+    if 'cmap = get_cmap(cmap)' in line:
+        get_cmap_line = i
+        break
+
+# We need to modify the function. The issue is that after get_cmap(cmap),
+# we lose the information about whether cmap was originally a string or object.
+# So we need to check before calling get_cmap.
+
+# Let's rewrite the function
+new_func = []
+new_func.append('def set_cmap(cmap: Colormap | str) -> None:\n')
+new_func.append('    """\n')
+new_func.append('    Set the default colormap, and applies it to the current image if any.\n')
+new_func.append('\n')
+new_func.append('    Parameters\n')
+new_func.append('    ----------\n')
+new_func.append('    cmap : `~matplotlib.colors.Colormap` or str\n')
+new_func.append('        A colormap instance or the name of a registered colormap.\n')
+new_func.append('\n')
+new_func.append('    See Also\n')
+new_func.append('    --------\n')
+new_func.append('    colormaps\n')
+new_func.append('    matplotlib.cm.register_cmap\n')
+new_func.append('    matplotlib.cm.get_cmap\n')
+new_func.append('    """\n')
+new_func.append('    # Store the original input to use for rc("image.cmap") later\n')
+new_func.append('    if isinstance(cmap, str):\n')
+new_func.append('        # cmap is a registered name, use it for rc("image.cmap")\n')
+new_func.append('        cmap_obj = get_cmap(cmap)\n')
+new_func.append('        rc_name = cmap  # Use the registered name\n')
+new_func.append('        rc(\'image\', cmap=rc_name)\n')
+new_func.append('        im = gci()\n')
+new_func.append('        if im is not None:\n')
+new_func.append('            im.set_cmap(cmap_obj)\n')
+new_func.append('    else:\n')
+new_func.append('        # cmap is a Colormap object, use its name for rc("image.cmap")\n')
+new_func.append('        cmap_obj = get_cmap(cmap)  # This just returns cmap\n')
+new_func.append('        rc(\'image\', cmap=cmap_obj.name)\n')
+new_func.append('        im = gci()\n')
+new_func.append('        if im is not None:\n')
+new_func.append('            im.set_cmap(cmap_obj)\n')
+
+# Replace the original function
+lines[start_line:end_line+1] = new_func
+
+# Write back
+with open('lib/matplotlib/pyplot.py', 'w') as f:
+    f.writelines(lines)
+
+print("Fixed set_cmap function")
diff --git a/lib/matplotlib/cm.py b/lib/matplotlib/cm.py
index 38158db956..abbf58bc6f 100644
--- a/lib/matplotlib/cm.py
+++ b/lib/matplotlib/cm.py
@@ -146,6 +146,7 @@ class ColormapRegistry(Mapping):
                                "that was already in the registry.")
 
         self._cmaps[name] = cmap.copy()
+        self._cmaps[name].name = name
 
     def unregister(self, name):
         """
diff --git a/lib/matplotlib/pyplot.py b/lib/matplotlib/pyplot.py
index 58ce4c03fa..7ac0a253a4 100644
--- a/lib/matplotlib/pyplot.py
+++ b/lib/matplotlib/pyplot.py
@@ -2278,14 +2278,22 @@ def set_cmap(cmap: Colormap | str) -> None:
     matplotlib.cm.register_cmap
     matplotlib.cm.get_cmap
     """
-    cmap = get_cmap(cmap)
-
-    rc('image', cmap=cmap.name)
-    im = gci()
-
-    if im is not None:
-        im.set_cmap(cmap)
-
+    # Store the original input to use for rc("image.cmap") later
+    if isinstance(cmap, str):
+        # cmap is a registered name, use it for rc("image.cmap")
+        cmap_obj = get_cmap(cmap)
+        rc_name = cmap  # Use the registered name
+        rc('image', cmap=rc_name)
+        im = gci()
+        if im is not None:
+            im.set_cmap(cmap_obj)
+    else:
+        # cmap is a Colormap object, use its name for rc("image.cmap")
+        cmap_obj = get_cmap(cmap)  # This just returns cmap
+        rc('image', cmap=cmap_obj.name)
+        im = gci()
+        if im is not None:
+            im.set_cmap(cmap_obj)
 
 @_copy_docstring_and_deprecators(matplotlib.image.imread)
 def imread(
diff --git a/lib/matplotlib/pyplot.py.backup b/lib/matplotlib/pyplot.py.backup
new file mode 100644
index 0000000000..58ce4c03fa
--- /dev/null
+++ b/lib/matplotlib/pyplot.py.backup
@@ -0,0 +1,4281 @@
+# Note: The first part of this file can be modified in place, but the latter
+# part is autogenerated by the boilerplate.py script.
+
+"""
+`matplotlib.pyplot` is a state-based interface to matplotlib. It provides
+an implicit,  MATLAB-like, way of plotting.  It also opens figures on your
+screen, and acts as the figure GUI manager.
+
+pyplot is mainly intended for interactive plots and simple cases of
+programmatic plot generation::
+
+    import numpy as np
+    import matplotlib.pyplot as plt
+
+    x = np.arange(0, 5, 0.1)
+    y = np.sin(x)
+    plt.plot(x, y)
+
+The explicit object-oriented API is recommended for complex plots, though
+pyplot is still usually used to create the figure and often the axes in the
+figure. See `.pyplot.figure`, `.pyplot.subplots`, and
+`.pyplot.subplot_mosaic` to create figures, and
+:doc:`Axes API </api/axes_api>` for the plotting methods on an Axes::
+
+    import numpy as np
+    import matplotlib.pyplot as plt
+
+    x = np.arange(0, 5, 0.1)
+    y = np.sin(x)
+    fig, ax = plt.subplots()
+    ax.plot(x, y)
+
+
+See :ref:`api_interfaces` for an explanation of the tradeoffs between the
+implicit and explicit interfaces.
+"""
+
+# fmt: off
+
+from __future__ import annotations
+
+from contextlib import ExitStack
+from enum import Enum
+import functools
+import importlib
+import inspect
+import logging
+import re
+import sys
+import threading
+import time
+
+from cycler import cycler
+import matplotlib
+import matplotlib.colorbar
+import matplotlib.image
+from matplotlib import _api
+from matplotlib import rcsetup, style
+from matplotlib import _pylab_helpers, interactive
+from matplotlib import cbook
+from matplotlib import _docstring
+from matplotlib.backend_bases import (
+    FigureCanvasBase, FigureManagerBase, MouseButton)
+from matplotlib.figure import Figure, FigureBase, figaspect
+from matplotlib.gridspec import GridSpec, SubplotSpec
+from matplotlib import rcParams, rcParamsDefault, get_backend, rcParamsOrig
+from matplotlib.rcsetup import interactive_bk as _interactive_bk
+from matplotlib.artist import Artist
+from matplotlib.axes import Axes, Subplot  # type: ignore
+from matplotlib.projections import PolarAxes  # type: ignore
+from matplotlib import mlab  # for detrend_none, window_hanning
+from matplotlib.scale import get_scale_names
+
+from matplotlib import cm
+from matplotlib.cm import _colormaps as colormaps
+from matplotlib.cm import register_cmap  # type: ignore
+from matplotlib.colors import _color_sequences as color_sequences
+
+import numpy as np
+
+from typing import TYPE_CHECKING
+
+if TYPE_CHECKING:
+    import datetime
+    import pathlib
+    import os
+
+    import PIL
+
+    from numpy.typing import ArrayLike
+    from typing import (
+        Any, BinaryIO, Callable, Hashable, Literal, Sequence, Iterable, Type
+    )
+
+    from matplotlib.axis import Tick
+    from matplotlib.axes._base import _AxesBase
+    from matplotlib.backend_bases import RendererBase, Event
+    from matplotlib.cm import ScalarMappable
+    from matplotlib.contour import ContourSet, QuadContourSet
+    from matplotlib.collections import (
+        Collection,
+        LineCollection,
+        BrokenBarHCollection,
+        PolyCollection,
+        PathCollection,
+        EventCollection,
+        QuadMesh,
+    )
+    from matplotlib.colorbar import Colorbar
+    from matplotlib.colors import Colormap
+    from matplotlib.container import (
+        BarContainer,
+        ErrorbarContainer,
+        StemContainer,
+    )
+    from matplotlib.figure import SubFigure
+    from matplotlib.legend import Legend
+    from matplotlib.mlab import GaussianKDE
+    from matplotlib.image import AxesImage
+    from matplotlib.patches import FancyArrow, StepPatch
+    from matplotlib.quiver import Barbs, Quiver, QuiverKey
+    from matplotlib.scale import ScaleBase
+    from matplotlib.transforms import Transform, Bbox
+    from matplotlib.typing import ColorType, LineStyleType, MarkerType, HashableList
+    from matplotlib.widgets import SubplotTool
+
+# We may not need the following imports here:
+from matplotlib.colors import Normalize
+from matplotlib.lines import Line2D
+from matplotlib.text import Text, Annotation
+from matplotlib.
…[cut, 134717 more chars]
```

## The submitted patch (as submitted)

### Test files (shown in full)

```diff
(none)
```

### All other files

```diff
(nothing submitted)
```
