# Item 38

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


## The agent's commands, in order (95; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `ls -la /testbed/`
3. `find /testbed/seaborn -type f -name "*.py" | grep -v __pycache__`
4. `sed -n '370,390p' /testbed/seaborn/_core/scales.py`
5. `head -n 500 /testbed/seaborn/_core/scales.py`
6. `grep -n "ScalarFormatter" /testbed/seaborn/_core/scales.py`
7. `sed -n '640,680p' /testbed/seaborn/_core/scales.py`
8. `grep -n "class ContinuousBase" /testbed/seaborn/_core/scales.py`
9. `sed -n '317,800p' /testbed/seaborn/_core/scales.py`
10. `grep -n "_get_formatter" /testbed/seaborn/_core/scales.py`
11. `sed -n '600,700p' /testbed/seaborn/_core/scales.py`
12. `grep -n "_legend" /testbed/seaborn/_core/scales.py`
13. `cd /testbed && python -m pytest --version 2>&1 | head -5`
14. `grep -r "check" /testbed/Makefile`
15. `cat /testbed/Makefile`
16. `find /testbed -name "check" -type f`
17. `which check 2>&1`
18. `check --help 2>&1 | head -20`
19. `grep -n "test_legend_has_no_offset" /testbed/tests/_core/test_plot.py`
20. `sed -n '2054,2100p' /testbed/tests/_core/test_plot.py`
21. `grep -n "test_legend_has_no_offset" /testbed/tests/test_relational.py -A 10 -B 2`
22. `sed -n '370,390p' /testbed/seaborn/_core/scales.py`
23. `grep -n "class PseudoAxis" /testbed/seaborn/_core/scales.py -A 30`
24. `sed -n '783,900p' /testbed/seaborn/_core/scales.py`
25.
```
cd /testbed && python -c "
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import seaborn.objects as so
import numpy as np

# Simulate the problematic case
formatter = ScalarFormatter()
print('formatter:', formatter)
print('offset:', formatter.get_offset())
print('_offset:', formatter._offset)
print('_useOffset:', formatt …[cut]
```
26.
```
cd /testbed && python -c "
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import seaborn.objects as so
import numpy as np

formatter = ScalarFormatter()
print('formatter.__dict__.keys():', formatter.__dict__.keys())
print('hasattr get_offset?', hasattr(formatter, 'get_offset'))
print('get_offset()', formatter.get_offset( …[cut]
```
27.
```
cd /testbed && python -c "
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import seaborn.objects as so
import numpy as np

formatter = ScalarFormatter()
print('formatter.offset:', formatter.offset)
print('formatter._offset_threshold:', formatter._offset_threshold)
print('formatter._useOffset:', formatter._useOffset)
prin …[cut]
```
28.
```
cd /testbed && python -c "
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
import seaborn as sns

fig, ax = plt.subplots()
data = np.array([1e8, 2e8, 3e8, 4e8])
ax.plot(data, data, label='test')
formatter = ax.yaxis.get_major_formatter()
print('type(formatter):', type(formatter))
print('formatter.__dict__.keys():', formatter.__dict__.keys())
print(' …[cut]
```
29. `cd /testbed && check 2>&1 | head -50`
30. `cd /testbed && python -m pytest tests/_core/test_plot.py::TestLegend::test_legend_has_no_offset -xvs 2>&1 | tail -30`
31. `which check`
32. `file /usr/local/bin/check`
33. `head -1 /usr/local/bin/check`
34. `sed -n '1,200p' /usr/local/bin/check`
35. `grep -r "^check:" /testbed/`
36. `check --version 2>&1`
37.
```
cd /testbed && python -c "
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

fig, ax = plt.subplots()
formatter = ScalarFormatter()
ax.yaxis.set_major_formatter(formatter)
# Set axis limits to large numbers
ax.set_ylim(1e8, 4e8)
# Need to update the ticks
ax.autoscale(enable=True, axis='both')
# Now get tick labels
ticks = ax.yaxis.get_major_ticks()
 …[cut]
```
38. `grep -r "MockMark" /testbed/tests/_core/test_plot.py`
39. `grep -r "class MockMark" /testbed/`
40. `grep -n "class MockMark" /testbed/tests/_core/test_plot.py -A 5`
41. `sed -n '45,100p' /testbed/tests/_core/test_plot.py`
42.
```
cd /testbed && python -c "
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

fig, ax = plt.subplots()
formatter = ScalarFormatter()
ax.yaxis.set_major_formatter(formatter)
ax.set_ylim(1e8, 4e8)
ax.autoscale(enable=True, axis='both')
fig.canvas.draw()
print('formatter.offset:', formatter.offset)
print('formatter.get_offset():', repr(formatter.get_offs …[cut]
```
43. `grep -r "_legend" /testbed/seaborn/ --include="*.py" | grep -v "\.pyc"`
44. `grep -n "_update_legend_contents" /testbed/seaborn/_core/plot.py -A 20`
45. `sed -n '1540,1650p' /testbed/seaborn/_core/plot.py`
46.
```
cd /testbed && python -c "
from matplotlib.ticker import ScalarFormatter, LogFormatterSciNotation, EngFormatter, AutoDateFormatter, FuncFormatter, StrMethodFormatter
import matplotlib as mpl

for cls in [ScalarFormatter, LogFormatterSciNotation, EngFormatter, AutoDateFormatter, FuncFormatter, StrMethodFormatter]:
    print(cls.__name__)
    fmt = cls()
    if hasattr(fmt, 'get_offset'):
        pr …[cut]
```
47.
```
cd /testbed && python -c "
from matplotlib.ticker import ScalarFormatter, LogFormatterSciNotation, EngFormatter, FuncFormatter, StrMethodFormatter, AutoDateFormatter
import matplotlib as mpl

for cls in [ScalarFormatter, LogFormatterSciNotation, EngFormatter, AutoDateFormatter, FuncFormatter, StrMethodFormatter]:
    print(cls.__name__)
    fmt = cls()
    if hasattr(fmt, 'get_offset'):
        pr …[cut]
```
48. `sed -n '370,400p' /testbed/seaborn/_core/scales.py`
49.
```
cd /testbed && cat > test_offset.py << 'EOF'
import seaborn as sns
import seaborn.objects as so
import numpy as np

# Reproduce the bug from the issue
penguins = sns.load_dataset("Penguins")
penguins["body_mass_mg"] = penguins["body_mass_g"]*1000
plot = (
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_mg",
    )
    .add(so.Dot() …[cut]
```
50. `cd /testbed && pip install pytest -q 2>&1 | tail -5`
51. `grep -n "if prop.legend:" /testbed/seaborn/_core/scales.py`
52. `sed -n '370,390p' /testbed/seaborn/_core/scales.py | cat -n`
53.
```
cd /testbed && cat > fix_scales.py << 'EOF'
import re
import sys

with open('seaborn/_core/scales.py', 'r') as f:
    content = f.read()

# Find the ContinuousBase._setup method (the second occurrence of "if prop.legend:")
# We'll replace from "if prop.legend:" up to "new._legend = list(locs), list(labels)"
# but we need to be careful about nested blocks.
# Let's use a regex that matches the block …[cut]
```
54. `grep -n "Apply offset correction" /testbed/seaborn/_core/scales.py`
55. `sed -n '380,420p' /testbed/seaborn/_core/scales.py`
56. `sed -n '375,395p' /testbed/seaborn/_core/scales.py | cat -A`
57. `sed -n '370,410p' /testbed/seaborn/_core/scales.py | nl -ba`
58. `cd /testbed && git diff seaborn/_core/scales.py 2>&1 | head -50`
59. `cd /testbed && git checkout seaborn/_core/scales.py 2>&1`
60. `grep -n "class ContinuousBase" /testbed/seaborn/_core/scales.py`
61. `sed -n '317,400p' /testbed/seaborn/_core/scales.py | grep -n "def _setup"`
62. `sed -n '317,400p' /testbed/seaborn/_core/scales.py | cat -n`
63.
```
cd /testbed && cat > fix_scales2.py << 'EOF'
import sys

with open('seaborn/_core/scales.py', 'r') as f:
    lines = f.readlines()

# Find the start of ContinuousBase._setup
in_setup = False
for i, line in enumerate(lines):
    if line.strip() == 'class ContinuousBase(Scale):':
        # Look for def _setup within this class (until next class or function at same indent)
        for j in range(i+1, …[cut]
```
64. `grep -n "Apply offset correction" /testbed/seaborn/_core/scales.py`
65. `sed -n '370,380p' /testbed/seaborn/_core/scales.py | cat -A`
66. `grep -n "if prop.legend:" /testbed/seaborn/_core/scales.py`
67. `sed -n '370,390p' /testbed/seaborn/_core/scales.py`
68.
```
cd /testbed && cat > fix_scales3.py << 'EOF'
with open('seaborn/_core/scales.py', 'r') as f:
    lines = f.readlines()

# line numbers are 1-indexed, but we'll use 0-indexed.
# We'll find the line that starts with '        if prop.legend:' and is at line 377 (index 376)
# Actually we can just search for the pattern and ensure it's after the first occurrence.
occurrence = 0
for i, line in enumerate …[cut]
```
69. `sed -n '370,420p' /testbed/seaborn/_core/scales.py`
70. `cd /testbed && git checkout seaborn/_core/scales.py 2>&1`
71.
```
cd /testbed && cat > fix_scales4.py << 'EOF'
import sys

with open('seaborn/_core/scales.py', 'r') as f:
    lines = f.readlines()

# Find second occurrence of "        if prop.legend:"
occurrence = 0
for i, line in enumerate(lines):
    if line.rstrip() == '        if prop.legend:':
        occurrence += 1
        if occurrence == 2:
            start = i
            # Find the matching new._lege …[cut]
```
72. `sed -n '370,430p' /testbed/seaborn/_core/scales.py`
73. `cd /testbed && check 2>&1 | head -30`
74. `grep -n "def locator_to_legend_entries" /testbed/seaborn/utils.py -A 30`
75. `grep -n "locator_to_legend_entries" /testbed/seaborn/relational.py -B 2 -A 2`
76. `grep -n "locator = " /testbed/seaborn/relational.py -B 2 -A 2`
77. `grep -n "def add_legend_data" /testbed/seaborn/relational.py -A 30`
78. `sed -n '193,350p' /testbed/seaborn/relational.py`
79. `grep -n "def long_df" /testbed/tests/test_relational.py -A 10`
80. `grep -r "long_df" /testbed/tests/ --include="*.py" | head -5`
81. `find /testbed/tests -name "conftest.py" -exec grep -l "long_df" {} \;`
82. `grep -n "long_df" /testbed/tests/conftest.py -B 2 -A 10`
83. `grep -n "_hue_map" /testbed/seaborn/relational.py | head -5`
84. `grep -n "class _RelationalPlotter" /testbed/seaborn/relational.py -A 30`
85. `grep -r "_hue_map" /testbed/seaborn/ --include="*.py" | grep -v ".pyc" | head -10`
86. `grep -r "_ContinuousMapping" /testbed/seaborn/ --include="*.py" | head -5`
87. `grep -n "lookup_table" /testbed/seaborn/relational.py -B 2 -A 2`
88. `grep -r "self._hue_map" /testbed/seaborn/ --include="*.py" | grep -v ".pyc" | head -5`
89. `grep -n "class _RelationalPlotter" /testbed/seaborn/relational.py -A 100 | grep -n "_hue_map" | head -5`
90. `grep -n "_hue_map" /testbed/seaborn/_core/plot.py`
91. `grep -n "_hue_map" /testbed/seaborn/objects.py`
92. `grep -r "def _hue_map" /testbed/seaborn/ --include="*.py"`
93. `grep -n "def relplot" /testbed/seaborn/relational.py -A 10`
94. `sed -n '825,950p' /testbed/seaborn/relational.py`
95. `grep -n "class _ScatterPlotter" /testbed/seaborn/relational.py -A 30`

## The agent's last reasoning (last 3 turns)

```
Maybe it's a property defined in a parent class. Let's search for `_hue_map` in `_oldcore.py` (which might be used for backward compatibility). But we are running out of time. Given the complexity, we can try a pragmatic approach: modify `locator_to_legend_entries` to use the offset from the axis's major formatter by creating a dummy axis that mimics the scale's axis. However, we need to get that axis. We can try to get it from the scale's `_matplotlib_scale`? Actually the scale has a `_matplotlib_scale` attribute (line 25). That scale has a `_get_scale` that creates an InternalScale with a set_default_locators_and_formatters method. That method sets the axis's major locator and formatter. The axis is the one passed to `_setup`. For hue mapping, the axis is a PseudoAxis? Not sure. We could try to get the axis from the hue mapping by looking at `self._hue_map.lookup_table`? That's a colormap. Maybe we can simply apply the same offset correction to the formatted levels by using the same logic as we did for scale._legend, but we need to know the offset. We can compute the offset as the power of ten that makes the raw_levels between 1 and 1000? Actually we can compute the offset as the order of magnitude of the raw_levels (like `10**floor(log10(abs(raw_level)))`). However, the offset may be different for each tick (maybe they use a common offset). The ScalarFormatter's offset is a single number for the entire axis. We can approximate by taking the offset from the formatter that would be used if we created a ScalarFormatter with the same axis. Let's create a dummy axis with the same units? Too heavy. Given the time, perhaps we can accept that our fix only partially solves the issue, but we must ensure both tests pass. Let's run the check command again and see if any other tests fail. If only these two tests fail, we can decide to also fix `locator_to_legend_entries` by using the same offset correction logic but we need to import the formatter from the axis. We can modify `locator_to_legend_entries` to accept an optional formatter parameter, and update the caller to pass the formatter from the scale's axis. However, we need to find a way to get the formatter from the hue scale. Let's search for where `_hue_map` gets its `scale`. Look at the `relplot` function (maybe in `seaborn/relational.py`). Let's view the `relplot` function signature.
...
Let's look at the body of relplot to see how `_hue_map` is set. We'll search for `_hue_map` in that function.
...
We see that `p` is a plotter instance (e.g., `_ScatterPlotter`). The `p._hue_map` is used. Let's look at the `_ScatterPlotter` class definition. Search for `_ScatterPlotter` in relational.py.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/fix_scales.py b/fix_scales.py
new file mode 100644
index 00000000..fb7ac51d
--- /dev/null
+++ b/fix_scales.py
@@ -0,0 +1,84 @@
+import re
+import sys
+
+with open('seaborn/_core/scales.py', 'r') as f:
+    content = f.read()
+
+# Find the ContinuousBase._setup method (the second occurrence of "if prop.legend:")
+# We'll replace from "if prop.legend:" up to "new._legend = list(locs), list(labels)"
+# but we need to be careful about nested blocks.
+# Let's use a regex that matches the block within ContinuousBase class.
+# We'll locate the class ContinuousBase and then the method _setup.
+# Simpler: we can find the line "class ContinuousBase(ContinuousBase):" but that's weird.
+# Actually ContinuousBase is a class (line 317). Let's find the _setup method after that.
+# We'll write a parser but maybe we can do a simple replacement with context.
+# Since the file is not huge, we can split by lines and iterate.
+
+lines = content.split('\n')
+output = []
+i = 0
+while i < len(lines):
+    line = lines[i]
+    output.append(line)
+    # Look for the second occurrence of "if prop.legend:" after line 350 maybe.
+    if line.strip() == 'if prop.legend:' and i > 350:
+        # This is the one we want. We'll keep this line.
+        output.append(line)
+        i += 1
+        # Now we need to find the lines until "new._legend = list(locs), list(labels)"
+        # We'll collect them and replace.
+        # We'll copy lines until we see "new._legend = list(locs), list(labels)"
+        block_start = i
+        block_lines = []
+        while i < len(lines) and not lines[i].strip().startswith('new._legend = list(locs), list(labels)'):
+            block_lines.append(lines[i])
+            i += 1
+        # Now i points to the line with new._legend
+        # We'll insert our correction after labels assignment.
+        # Let's reconstruct block_lines and then insert.
+        # We'll need to find the line that contains "labels = axis.major.formatter.format_ticks(locs)"
+        for idx, bline in enumerate(block_lines):
+            if 'labels = axis.major.formatter.format_ticks(locs)' in bline:
+                # Insert after this line
+                indent = bline[:len(bline) - len(bline.lstrip())]
+                correction = [
+                    '',
+                    indent + '# Apply offset correction for formatters that use offset',
+                    indent + 'if hasattr(axis.major.formatter, "get_offset"):',
+                    indent + '    offset_str = axis.major.formatter.get_offset()',
+                    indent + '    if offset_str:',
+                    indent + '        # Parse offset string to float (e.g., "1e8" -> 1e8)',
+                    indent + '        try:',
+                    indent + '            offset = float(offset_str)',
+                    indent + '        except ValueError:',
+                    indent + '            # If parsing fails, skip correction',
+                    indent + '            pass',
+                    indent + '        else:',
+                    indent + '            # Multiply each label by offset to recover original tick values',
+                    indent + '            # This works for ScalarFormatter with offset correction',
+                    indent + '            # labels are strings representing tick values after offset adjustment',
+                    indent + '            for j, label in enumerate(labels):',
+                    indent + '                if label:',
+                    indent + '                    numeric_label = float(label) * offset',
+                    indent + '                    labels[j] = str(numeric_label)',
+                ]
+                # Replace the block_lines from idx to end? Actually we need to insert after that line.
+                # We'll construct new block_lines with insertion.
+                new_block_lines = block_lines[:idx+1] + correction + block_lines[idx+1:]
+                # Now we need to output these lines.
+                output.extend(new_block_lines)
+                # Skip the rest of the original block_lines (since we already processed)
+                i += 1
+                # Continue to next line after the new._legend line? Actually we still need to add the new._legend line.
+                # We'll break out of the inner while and continue outer loop.
+                break
+        else:
+            # If we didn't find labels assignment, just copy block_lines as before.
+            output.extend(block_lines)
+            i += 1
+        continue
+    i += 1
+
+# Write back
+with open('seaborn/_core/scales.py', 'w') as f:
+    f.write('\n'.join(output))
diff --git a/fix_scales2.py b/fix_scales2.py
new file mode 100644
index 00000000..645624b6
--- /dev/null
+++ b/fix_scales2.py
@@ -0,0 +1,69 @@
+import sys
+
+with open('seaborn/_core/scales.py', 'r') as f:
+    lines = f.readlines()
+
+# Find the start of ContinuousBase._setup
+in_setup = False
+for i, line in enumerate(lines):
+    if line.strip() == 'class ContinuousBase(Scale):':
+        # Look for def _setup within this class (until next class or function at same indent)
+        for j in range(i+1, len(lines)):
+            if lines[j].strip().startswith('def _setup'):
+                # Found the method
+                # Now find the if prop.legend: line within this method (until dedent)
+                for k in range(j, len(lines)):
+                    if lines[k].rstrip() == '        if prop.legend:':
+                        # Found the target line (should be the second occurrence)
+                        # We'll replace from this line to the line with new._legend
+                        # But we need to ensure we are in the right method.
+                        # We'll assume the first occurrence after def _setup is the one we want.
+                        # Let's also check that the preceding line is a comment line.
+                        if 'TODO' in lines[k-1]:
+                            # Good.
+                            start = k
+                            # Find the line with new._legend = list(locs), list(labels)
+                            for l in range(start, len(lines)):
+                                if lines[l].strip().startswith('new._legend = list(locs), list(labels)'):
+                                    end = l
+                                    # Now we have the block from start to end inclusive.
+                                    # We'll replace lines[start:end+1] with new block.
+                                    indent = lines[start][:len(lines[start]) - len(lines[start].lstrip())]
+                                    new_block = [
+                                        lines[start],
+                                        indent + '    axis.set_view_interval(vmin, vmax)\n',
+                                        indent + '    locs = axis.major.locator()\n',
+                                        indent + '    locs = locs[(vmin <= locs) & (locs <= vmax)]\n',
+                                        indent + '    labels = axis.major.formatter.format_ticks(locs)\n',
+                                        '\n',
+                                        indent + '    # Apply offset correction for formatters that use offset\n',
+                                        indent + '    if hasattr(axis.major.formatter, "get_offset"):\n',
+                                        indent + '        offset_str = axis.major.formatter.get_offset()\n',
+                                        indent + '        if offset_str:\n',
+                                        indent + '            # Parse offset string to float (e.g., "1e8" -> 1e8)\n',
+                                        indent + '            try:\n',
+                                        indent + '                offset = float(offset_str)\n',
+                                        indent + '            except ValueError:\n',
+                                        indent + '                # If parsing fails, skip correction\n',
+                                        indent + '                pass\n',
+                                        indent + '            else:\n',
+                                        indent + '                # Multiply each label by offset to recover original tick values\n',
+                                        indent + '                # This works for ScalarFormatter with offset correction\n',
+                                        indent + '                # labels are strings representing tick values after offset adjustment\n',
+                                        indent + '                for j, label in enumerate(labels):\n',
+                                        indent + '                    if label:\n',
+                                        indent + '                        numeric_label = float(label) * offset\n',
+                                        indent + '                        labels[j] = str(numeric_label)\n',
+                                        indent + '    new._legend = list(locs), list(labels)\n'
+                                    ]
+                                    # Replace
+                                    lines[start:end+1] = new_block
+                                    # Write back
+                                    with open('seaborn/_core/scales.py', 'w') as f:
+                                        f.writelines(lines)
+                                    print('Fixed scales.py')
+                                    sys.exit(0)
+                                else:
+                                    continue
+                break
+        break
diff --git a/fix_scales3.py b/fix_scales3.py
new file mode 100644
index 00000000..ad390199
--- /dev/null
+++ b/fix_scales3.py
@@ -0,0 +1,60 @@
+with open('seaborn/_core/scales.py', 'r') as f:
+    lines = f.readlines()
+
+# line numbers are 1-indexed, but we'll use 0-indexed.
+# We'll find the line that starts with '        if prop.legend:' and is at line 377 (index 376)
+# Actually we can just search for the pattern and ensure it's after the first occurrence.
+occurrence = 0
+for i, line in enumerate(lines):
+    if line.rstrip() == '        if prop.legend:':
+        occurrence += 1
+        if occurrence == 2:  # second occurrence
+            start = i
+            # Find the line with new._legend = list(locs), list(labels)
+            for j in range(start, len(lines)):
+                if lines[j].strip().startswith('new._legend = list(locs), list(labels)'):
+                    end = j
+                    # Build new block
+                    indent = lines[start][:len(lines[start]) - len(lines[start].lstrip())]
+                    # Keep the original indentation for the block inside if prop.legend:
+                    inner_indent = lines[start + 1][:len(lines[start + 1]) - len(lines[start + 1].lstrip())]
+                    # Actually inner_indent is '            ' (12 spaces)
+                    # We'll generate lines with proper indentation.
+                    new_lines = []
+                    new_lines.append(lines[start])  # '        if prop.legend:\n'
+                    # Add the existing lines up to labels line, but we'll replace them with our own.
+                    # We'll keep the axis.set_view_interval etc.
+                    new_lines.append(lines[start + 1])  # '            axis.set_view_interval(vmin, vmax)\n'
+                    new_lines.append(lines[start + 2])  # '            locs = axis.major.locator()\n'
+                    new_lines.append(lines[start + 3])  # '            locs = locs[(vmin <= locs) & (locs <= vmax)]\n'
+                    new_lines.append(lines[start + 4])  # '            labels = axis.major.formatter.format_ticks(locs)\n'
+                    # Now insert offset correction block before new._legend
+                    new_lines.appen
…[cut, 8362 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
