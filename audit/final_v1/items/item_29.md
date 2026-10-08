# Item 29

**Repository:** matplotlib/matplotlib  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** resolved  
**The task's test files:** lib/matplotlib/tests/test_axes.py

## The issue

[Bug]: offsetText is colored based on tick.color instead of tick.labelcolor
### Bug summary

In version 3.6.3, when setting ytick.labelcolor / xtick.labelcolor in styles / rcParams, it does not change the color of the exponent label as well. It will be colored based on xtick.color / ytick.color.

### Code for reproduction

```python
import matplotlib.pyplot as plt

plt.rcParams.update({'ytick.labelcolor': 'red'})
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot([1.01e9,1.02e9,1.03e9])
```


### Actual outcome

![wrong_color](https://user-images.githubusercontent.com/50588526/217083612-dddf85ba-ebfa-4bf0-8ae0-3dce36c17198.png)


### Expected outcome

![correct_color](https://user-images.githubusercontent.com/50588526/217083512-34b3b32f-5d3a-4242-8742-2269bb09c20c.png)


### Additional information

The following patch seems to fix it for my simple usecases:

```
diff --git a/axis.py b/axis.py
--- a/axis.py	
+++ b/axis.py	(date 1675716341305)
@@ -2203,7 +2203,7 @@
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['xtick.labelsize'],
-            color=mpl.rcParams['xtick.color'],
+            color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],
         )
         self.offset_text_position = 'bottom'
 
@@ -2456,7 +2456,7 @@
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['ytick.labelsize'],
-            color=mpl.rcParams['ytick.color'],
+            color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor'],
         )
         self.offset_text_position = 'left'
 
```

### Operating system

_No response_

### Matplotlib Version

3.6.3

### Matplotlib Backend

_No response_

### Python version

_No response_

### Jupyter version

_No response_

### Installation

None


## The agent's commands, in order (92; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed`
3. `ls -la /testbed/lib/matplotlib/`
4. `sed -n '2190,2210p' /testbed/lib/matplotlib/axis.py`
5. `grep -n "color=mpl.rcParams\['xtick.color'\]" /testbed/lib/matplotlib/axis.py`
6. `sed -n '2240,2270p' /testbed/lib/matplotlib/axis.py`
7. `grep -n "color=mpl.rcParams\['ytick.color'\]" /testbed/lib/matplotlib/axis.py`
8. `sed -n '2500,2535p' /testbed/lib/matplotlib/axis.py`
9. `grep -n "labelcolor" /testbed/lib/matplotlib/axis.py`
10. `sed -n '940,1100p' /testbed/lib/matplotlib/axis.py`
11. `grep -n "offsetText.set" /testbed/lib/matplotlib/axis.py`
12. `grep -n "class Axis" /testbed/lib/matplotlib/axis.py`
13. `sed -n '604,800p' /testbed/lib/matplotlib/axis.py | grep -n "__init__" -A 2`
14. `sed -n '604,1000p' /testbed/lib/matplotlib/axis.py`
15. `grep -n "def _init" /testbed/lib/matplotlib/axis.py`
16. `sed -n '2237,2270p' /testbed/lib/matplotlib/axis.py`
17. `sed -n '2496,2525p' /testbed/lib/matplotlib/axis.py`
18. `grep -n "labelcolor" /testbed/lib/matplotlib/tick.py`
19. `find /testbed/lib/matplotlib -name "tick.py" -type f`
20. `grep -n "class Tick" /testbed/lib/matplotlib/axis.py`
21. `sed -n '36,500p' /testbed/lib/matplotlib/axis.py | grep -n "_apply_params" -A 30`
22. `sed -n '316,360p' /testbed/lib/matplotlib/axis.py`
23. `sed -n '316,400p' /testbed/lib/matplotlib/axis.py`
24. `sed -n '36,200p' /testbed/lib/matplotlib/axis.py`
25. `grep -n "offsetText.set_color" /testbed/lib/matplotlib/axis.py`
26.
```
cd /testbed && python -c "
import matplotlib.pyplot as plt
plt.rcParams.update({'ytick.labelcolor': 'red'})
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot([1.01e9,1.02e9,1.03e9])
print('offsetText color:', ax.yaxis.offsetText.get_color())
print('expected red')
" 2>&1
```
27. `grep -n "labelcolor" /testbed/lib/matplotlib/rcsetup.py | head -20`
28. `grep -B2 -A2 "xtick.labelcolor" /testbed/lib/matplotlib/rcsetup.py | head -30`
29. `grep -n "rcParams.default" /testbed/lib/matplotlib/rcsetup.py | head -5`
30. `find /testbed/lib/matplotlib -name "*.template" -type f`
31. `grep -r "xtick.labelcolor" /testbed/lib/matplotlib/ | head -5`
32. `grep -B1 -A1 "xtick.labelcolor" /testbed/lib/matplotlib/mpl-data/matplotlibrc`
33. `head -50 /testbed/lib/matplotlib/axis.py | grep -n "import"`
34. `cd /testbed && python -m pytest --version 2>&1 | head -5`
35. `cd /testbed && cat README.md | head -30`
36. `ls -la /testbed/Makefile 2>/dev/null || echo "No Makefile"`
37. `cat /testbed/tox.ini`
38. `ls -la /testbed/tools/`
39. `which check 2>/dev/null || echo "not found"`
40. `head -30 /usr/local/bin/check`
41. `python -c "import sys; print(sys.executable)"`
42. `pip install pytest -q 2>&1 | tail -5`
43. `ls -la /tmp/.mp_check* 2>/dev/null || echo "no check files"`
44. `conda --version 2>&1 | head -1`
45. `conda install -y pytest 2>&1 | tail -10`
46. `cd /testbed && check 2>&1 | head -30`
47. `cd /testbed && check 2>&1 | tail -30`
48. `python -c "import pytest; print(pytest.__version__)" 2>&1`
49. `cat /usr/local/bin/check`
50. `grep -r "offsetText" /testbed/lib/matplotlib/tests/ 2>/dev/null | head -10`
51. `grep -B5 -A10 "def test_xaxis_offsetText_color" /testbed/lib/matplotlib/tests/test_axes.py`
52. `which python`
53. `ls /opt/miniconda3/envs/testbed/lib/python3.*/site-packages/ | grep pytest`
54. `cd /testbed && python -m pytest lib/matplotlib/tests/test_axes.py::test_xaxis_offsetText_color -xvs 2>&1 | head -50`
55. `python -c "import sys; print('\n'.join(sys.path))" | head -5`
56. `python -c "import site; print(site.getsitepackages())"`
57. `ls /opt/miniconda3/envs/testbed/lib/python3.11/site-packages/ | grep pytest`
58. `python -c "import sys; sys.path.insert(0, '/opt/miniconda3/envs/testbed/lib/python3.11/site-packages'); import pytest; print('ok')" 2>&1`
59. `ls -la /opt/miniconda3/envs/testbed/lib/python3.11/site-packages/ | grep pytest`
60. `find /opt/miniconda3/envs/testbed -name pytest -type f 2>/dev/null | head -5`
61. `grep -r "mp_check" /testbed 2>/dev/null | head -5`
62. `head -50 /testbed/.circleci/config.yml`
63. `grep -A10 -B10 "check:" /testbed/.circleci/config.yml | head -80`
64. `cat /testbed/setup.py | head -50`
65. `find /testbed -name "*pytest*.whl" -type f 2>/dev/null | head -5`
66. `python -m pip --version 2>&1 | head -1`
67. `python -m pip list 2>&1 | grep -i pytest`
68. `cat /testbed/setup.cfg`
69. `grep -A5 -B5 "test" /testbed/mplsetup.cfg.template | head -30`
70. `ls /opt/miniconda3/envs/testbed/bin/ | grep pytest`
71. `find /testbed -name "pytest*.whl" -type f 2>/dev/null | head -5`
72. `head -30 /testbed/lib/matplotlib/tests/test_axes.py`
73. `grep -r "mp_check_out" /testbed 2>/dev/null`
74. `grep -r "check" /testbed/tools/ 2>/dev/null | head -5`
75. `sed -n '2250,2270p' /testbed/lib/matplotlib/axis.py`
76.
```
cd /testbed && cat > fix_axis.py << 'EOF'
import sys
import re

with open('lib/matplotlib/axis.py', 'r') as f:
    content = f.read()

# Replace xtick offsetText color
pattern1 = r"(color=mpl\.rcParams\['xtick\.color'\],)"
replacement1 = r"color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],"
new_content = re.sub(pattern1, replacem …[cut]
```
77. `sed -n '2255,2265p' /testbed/lib/matplotlib/axis.py`
78. `sed -n '2515,2525p' /testbed/lib/matplotlib/axis.py`
79.
```
cd /testbed && cat > test_offset_color_fix.py << 'EOF'
import matplotlib.pyplot as plt
import matplotlib as mpl

print("Testing xtick.labelcolor and ytick.labelcolor")

# Test 1: default (labelcolor = inherit)
plt.rcParams.update({'xtick.labelcolor': 'inherit', 'ytick.labelcolor': 'inherit'})
plt.rcParams.update({'xtick.color': 'black', 'ytick.color': 'black'})
fig = plt.figure()
ax = fig.add_subp …[cut]
```
80. `grep -A20 "def test_xaxis_offsetText_color" /testbed/lib/matplotlib/tests/test_axes.py`
81. `apt-get update && apt-get install -y python3-pytest 2>&1 | tail -10`
82.
```
cd /testbed && cat > run_specific_tests.py << 'EOF'
import sys
import importlib.util
import matplotlib
import matplotlib.pyplot as plt

# Import the test module
spec = importlib.util.spec_from_file_location('test_axes', 'lib/matplotlib/tests/test_axes.py')
test_module = importlib.util.module_from_spec(spec)
sys.modules['test_axes'] = test_module
spec.loader.exec_module(test_module)

# Reset rcPara …[cut]
```
83. `find /usr/local/lib -name "pytest" -type f 2>/dev/null | head -5`
84. `grep -n "offsetText" /testbed/lib/matplotlib/axis.py | grep -i color`
85. `grep -n "class XAxis\|class YAxis" /testbed/lib/matplotlib/axis.py`
86. `grep -B2 -A2 "offsetText\.set" /testbed/lib/matplotlib/axis.py | grep -i color`
87. `cd /testbed && git diff lib/matplotlib/axis.py > /tmp/patch.txt 2>&1 && head -50 /tmp/patch.txt`
88. `cd /testbed && git diff lib/matplotlib/axis.py > patch.txt 2>&1 && echo "Patch created:" && head -20 patch.txt`
89.
```
cd /testbed && cat > run_exact_tests.py << 'EOF'
import matplotlib.pyplot as plt
import matplotlib as mpl

# Reset rcParams to defaults
mpl.rcParams.update({
    'xtick.labelcolor': 'inherit',
    'ytick.labelcolor': 'inherit',
    'xtick.color': 'black',
    'ytick.color': 'black',
})

print("Running test_xaxis_offsetText_color...")
plt.rcParams['xtick.labelcolor'] = 'blue'
ax = plt.axes()
assert …[cut]
```
90. `cd /testbed && wc -l patch.txt`
91. `cat /testbed/patch.txt`
92. `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
Excellent! Our fix passes the exact existing tests. That means the bug is fixed and the existing test suite (at least those two tests) will pass. Now we need to ensure that our changes don't break any other tests. Since we cannot run the full suite, we have to rely on the fact that the changes are minimal and follow the same pattern as Tick.__init__. Also we should check if there are any other references to xtick.color or ytick.color that might need similar updates? For example, maybe label color? But label color is axes.labelcolor, not tick.labelcolor. That's fine. We should also consider that there might be a similar bug for minor ticks? The offsetText is only used for major ticks (I think). The tick.labelcolor is used for both major and minor tick labels. The offsetText is only for major tick labels (when there is an offset). The fix we applied applies to XAxis and YAxis, which are the axes objects. That should cover all ticks (major/minor) because the offsetText is shared. Now we need to create the final submission. According to instructions, we must: 1. Create the patch file (already done) 2. Verify the patch (we already viewed) 3. Submit using the exact command: `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt` But we must ensure that the patch.txt is in the current directory and contains only the changes we made. Let's verify the patch.txt content length.
...
It's only 22 lines, which seems correct. Let's view the entire patch to ensure there are no extra changes.
...
Perfect. Now we need to submit. Let's run the required command.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/fix_axis.py b/fix_axis.py
new file mode 100644
index 0000000000..85700b9d7d
--- /dev/null
+++ b/fix_axis.py
@@ -0,0 +1,34 @@
+import sys
+import re
+
+with open('lib/matplotlib/axis.py', 'r') as f:
+    content = f.read()
+
+# Replace xtick offsetText color
+pattern1 = r"(color=mpl\.rcParams\['xtick\.color'\],)"
+replacement1 = r"color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],"
+new_content = re.sub(pattern1, replacement1, content, count=1)
+if new_content == content:
+    # try alternative pattern (maybe there is extra whitespace)
+    pattern1 = r"color=mpl\.rcParams\['xtick\.color'\]"
+    replacement1 = r"color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor']"
+    new_content = re.sub(pattern1, replacement1, content, count=1)
+    if new_content == content:
+        print("Failed to replace xtick offsetText color")
+        sys.exit(1)
+
+# Replace ytick offsetText color
+pattern2 = r"(color=mpl\.rcParams\['ytick\.color'\],)"
+replacement2 = r"color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor'],"
+new_content = re.sub(pattern2, replacement2, new_content, count=1)
+if new_content == content:
+    pattern2 = r"color=mpl\.rcParams\['ytick\.color'\]"
+    replacement2 = r"color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor']"
+    new_content = re.sub(pattern2, replacement2, content, count=1)
+    if new_content == content:
+        print("Failed to replace ytick offsetText color")
+        sys.exit(1)
+
+with open('lib/matplotlib/axis.py', 'w') as f:
+    f.write(new_content)
+print("Fixed axis.py")
diff --git a/lib/matplotlib/axis.py b/lib/matplotlib/axis.py
index c0e706e2b3..0920063693 100644
--- a/lib/matplotlib/axis.py
+++ b/lib/matplotlib/axis.py
@@ -2255,7 +2255,7 @@ class XAxis(Axis):
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['xtick.labelsize'],
-            color=mpl.rcParams['xtick.color'],
+            color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],
         )
         self.offset_text_position = 'bottom'
 
@@ -2515,7 +2515,7 @@ class YAxis(Axis):
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['ytick.labelsize'],
-            color=mpl.rcParams['ytick.color'],
+            color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor'],
         )
         self.offset_text_position = 'left'
 
diff --git a/patch.txt b/patch.txt
new file mode 100644
index 0000000000..ffa8d4a3ed
--- /dev/null
+++ b/patch.txt
@@ -0,0 +1,22 @@
+diff --git a/lib/matplotlib/axis.py b/lib/matplotlib/axis.py
+index c0e706e2b3..0920063693 100644
+--- a/lib/matplotlib/axis.py
++++ b/lib/matplotlib/axis.py
+@@ -2255,7 +2255,7 @@ class XAxis(Axis):
+             transform=mtransforms.blended_transform_factory(
+                 self.axes.transAxes, mtransforms.IdentityTransform()),
+             fontsize=mpl.rcParams['xtick.labelsize'],
+-            color=mpl.rcParams['xtick.color'],
++            color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],
+         )
+         self.offset_text_position = 'bottom'
+ 
+@@ -2515,7 +2515,7 @@ class YAxis(Axis):
+             transform=mtransforms.blended_transform_factory(
+                 self.axes.transAxes, mtransforms.IdentityTransform()),
+             fontsize=mpl.rcParams['ytick.labelsize'],
+-            color=mpl.rcParams['ytick.color'],
++            color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor'],
+         )
+         self.offset_text_position = 'left'
+ 
diff --git a/run_exact_tests.py b/run_exact_tests.py
new file mode 100644
index 0000000000..4f72a7d7cc
--- /dev/null
+++ b/run_exact_tests.py
@@ -0,0 +1,38 @@
+import matplotlib.pyplot as plt
+import matplotlib as mpl
+
+# Reset rcParams to defaults
+mpl.rcParams.update({
+    'xtick.labelcolor': 'inherit',
+    'ytick.labelcolor': 'inherit',
+    'xtick.color': 'black',
+    'ytick.color': 'black',
+})
+
+print("Running test_xaxis_offsetText_color...")
+plt.rcParams['xtick.labelcolor'] = 'blue'
+ax = plt.axes()
+assert ax.xaxis.offsetText.get_color() == 'blue', f'Expected blue, got {ax.xaxis.offsetText.get_color()}'
+print('  PASS')
+
+plt.rcParams['xtick.color'] = 'yellow'
+plt.rcParams['xtick.labelcolor'] = 'inherit'
+ax = plt.axes()
+assert ax.xaxis.offsetText.get_color() == 'yellow', f'Expected yellow, got {ax.xaxis.offsetText.get_color()}'
+print('  PASS')
+plt.close('all')
+
+print("Running test_yaxis_offsetText_color...")
+plt.rcParams['ytick.labelcolor'] = 'green'
+ax = plt.axes()
+assert ax.yaxis.offsetText.get_color() == 'green', f'Expected green, got {ax.yaxis.offsetText.get_color()}'
+print('  PASS')
+
+plt.rcParams['ytick.color'] = 'red'
+plt.rcParams['ytick.labelcolor'] = 'inherit'
+ax = plt.axes()
+assert ax.yaxis.offsetText.get_color() == 'red', f'Expected red, got {ax.yaxis.offsetText.get_color()}'
+print('  PASS')
+plt.close('all')
+
+print("All exact tests passed!")
diff --git a/run_specific_tests.py b/run_specific_tests.py
new file mode 100644
index 0000000000..401a99ebe8
--- /dev/null
+++ b/run_specific_tests.py
@@ -0,0 +1,37 @@
+import sys
+import importlib.util
+import matplotlib
+import matplotlib.pyplot as plt
+
+# Import the test module
+spec = importlib.util.spec_from_file_location('test_axes', 'lib/matplotlib/tests/test_axes.py')
+test_module = importlib.util.module_from_spec(spec)
+sys.modules['test_axes'] = test_module
+spec.loader.exec_module(test_module)
+
+# Reset rcParams before each test
+def reset_rcparams():
+    # Reset to defaults (but we just need to clear any changes)
+    # We'll just reset the specific params that the tests use
+    plt.rcParams['xtick.labelcolor'] = 'inherit'
+    plt.rcParams['ytick.labelcolor'] = 'inherit'
+    plt.rcParams['xtick.color'] = 'black'
+    plt.rcParams['ytick.color'] = 'black'
+
+print("Running test_xaxis_offsetText_color...")
+try:
+    test_module.test_xaxis_offsetText_color()
+    print("PASS")
+except AssertionError as e:
+    print(f"FAIL: {e}")
+    sys.exit(1)
+
+print("Running test_yaxis_offsetText_color...")
+try:
+    test_module.test_yaxis_offsetText_color()
+    print("PASS")
+except AssertionError as e:
+    print(f"FAIL: {e}")
+    sys.exit(1)
+
+print("All specific tests passed!")
diff --git a/test_offset_color_fix.py b/test_offset_color_fix.py
new file mode 100644
index 0000000000..ffcc5348b3
--- /dev/null
+++ b/test_offset_color_fix.py
@@ -0,0 +1,54 @@
+import matplotlib.pyplot as plt
+import matplotlib as mpl
+
+print("Testing xtick.labelcolor and ytick.labelcolor")
+
+# Test 1: default (labelcolor = inherit)
+plt.rcParams.update({'xtick.labelcolor': 'inherit', 'ytick.labelcolor': 'inherit'})
+plt.rcParams.update({'xtick.color': 'black', 'ytick.color': 'black'})
+fig = plt.figure()
+ax = fig.add_subplot(1,1,1)
+ax.plot([1e9, 2e9])
+print('X offsetText color (default inherit):', ax.xaxis.offsetText.get_color())
+assert ax.xaxis.offsetText.get_color() == 'black', f'Expected black, got {ax.xaxis.offsetText.get_color()}'
+print('Y offsetText color (default inherit):', ax.yaxis.offsetText.get_color())
+assert ax.yaxis.offsetText.get_color() == 'black', f'Expected black, got {ax.yaxis.offsetText.get_color()}'
+plt.close(fig)
+
+# Test 2: labelcolor set to 'red'
+plt.rcParams.update({'xtick.labelcolor': 'red', 'ytick.labelcolor': 'red'})
+plt.rcParams.update({'xtick.color': 'black', 'ytick.color': 'black'})
+fig = plt.figure()
+ax = fig.add_subplot(1,1,1)
+ax.plot([1e9, 2e9])
+print('X offsetText color (labelcolor red):', ax.xaxis.offsetText.get_color())
+assert ax.xaxis.offsetText.get_color() == 'red', f'Expected red, got {ax.xaxis.offsetText.get_color()}'
+print('Y offsetText color (labelcolor red):', ax.yaxis.offsetText.get_color())
+assert ax.yaxis.offsetText.get_color() == 'red', f'Expected red, got {ax.yaxis.offsetText.get_color()}'
+plt.close(fig)
+
+# Test 3: labelcolor = 'inherit' but tick.color changed (should follow tick.color)
+plt.rcParams.update({'xtick.labelcolor': 'inherit', 'ytick.labelcolor': 'inherit'})
+plt.rcParams.update({'xtick.color': 'blue', 'ytick.color': 'blue'})
+fig = plt.figure()
+ax = fig.add_subplot(1,1,1)
+ax.plot([1e9, 2e9])
+print('X offsetText color (inherit with blue tick):', ax.xaxis.offsetText.get_color())
+assert ax.xaxis.offsetText.get_color() == 'blue', f'Expected blue, got {ax.xaxis.offsetText.get_color()}'
+print('Y offsetText color (inherit with blue tick):', ax.yaxis.offsetText.get_color())
+assert ax.yaxis.offsetText.get_color() == 'blue', f'Expected blue, got {ax.yaxis.offsetText.get_color()}'
+plt.close(fig)
+
+# Test 4: xaxis labelcolor red, yaxis labelcolor green, different tick colors
+plt.rcParams.update({'xtick.labelcolor': 'red', 'ytick.labelcolor': 'green'})
+plt.rcParams.update({'xtick.color': 'black', 'ytick.color': 'black'})
+fig = plt.figure()
+ax = fig.add_subplot(1,1,1)
+ax.plot([1e9, 2e9])
+print('X offsetText color (red):', ax.xaxis.offsetText.get_color())
+assert ax.xaxis.offsetText.get_color() == 'red', f'Expected red, got {ax.xaxis.offsetText.get_color()}'
+print('Y offsetText color (green):', ax.yaxis.offsetText.get_color())
+assert ax.yaxis.offsetText.get_color() == 'green', f'Expected green, got {ax.yaxis.offsetText.get_color()}'
+plt.close(fig)
+
+print("All tests passed!")

```

## The submitted patch (as submitted)

```diff
diff --git a/lib/matplotlib/axis.py b/lib/matplotlib/axis.py
index c0e706e2b3..0920063693 100644
--- a/lib/matplotlib/axis.py
+++ b/lib/matplotlib/axis.py
@@ -2255,7 +2255,7 @@ class XAxis(Axis):
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['xtick.labelsize'],
-            color=mpl.rcParams['xtick.color'],
+            color=mpl.rcParams['xtick.color'] if mpl.rcParams['xtick.labelcolor']=='inherit' else mpl.rcParams['xtick.labelcolor'],
         )
         self.offset_text_position = 'bottom'
 
@@ -2515,7 +2515,7 @@ class YAxis(Axis):
             transform=mtransforms.blended_transform_factory(
                 self.axes.transAxes, mtransforms.IdentityTransform()),
             fontsize=mpl.rcParams['ytick.labelsize'],
-            color=mpl.rcParams['ytick.color'],
+            color=mpl.rcParams['ytick.color'] if mpl.rcParams['ytick.labelcolor']=='inherit' else mpl.rcParams['ytick.labelcolor'],
         )
         self.offset_text_position = 'left'
 

```
