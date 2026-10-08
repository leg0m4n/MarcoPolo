# Item 64

**Repository:** astropy/astropy  
**Task type:** ordinary  
**Run ended:** submitted a patch  
**Official result of the submission:** NOT resolved  
**The task's test files:** astropy/units/tests/test_quantity.py, astropy/units/tests/test_quantity_ufuncs.py

## The issue

Should `Quantity.__array_ufunc__()` return `NotImplemented` instead of raising `ValueError` if the inputs are incompatible?
### Description
I'm trying to implement a duck type of `astropy.units.Quantity`. If you are interested, the project is available [here](https://github.com/Kankelborg-Group/named_arrays). I'm running into trouble trying to coerce my duck type to use the reflected versions of the arithmetic operators if the left operand is not an instance of the duck type _and_ they have equivalent but different units. Consider the following minimal working example of my duck type.

```python3
import dataclasses
import numpy as np
import astropy.units as u


@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    ndarray: u.Quantity

    @property
    def unit(self) -> u.UnitBase:
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):

        inputs = [inp.ndarray if isinstance(inp, DuckArray) else inp for inp in inputs]

        for inp in inputs:
            if isinstance(inp, np.ndarray):
                result = inp.__array_ufunc__(function, method, *inputs, **kwargs)
                if result is not NotImplemented:
                    return DuckArray(result)

        return NotImplemented
```
If I do an operation like
```python3
DuckArray(1 * u.mm) + (1 * u.m)
```
It works as expected. Or I can do
```python3
(1 * u.mm) + DuckArray(1 * u.mm)
```
and it still works properly. But if the left operand has different units
```python3
(1 * u.m) + DuckArray(1 * u.mm)
```
I get the following error:
```python3
..\..\..\AppData\Local\Programs\Python\Python310\lib\site-packages\astropy\units\quantity.py:617: in __array_ufunc__
    arrays.append(converter(input_) if converter else input_)
..\..\..\AppData\Local\Programs\Python\Python310\lib\site-packages\astropy\units\core.py:1042: in <lambda>
    return lambda val: scale * _condition_arg(val)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

value = DuckArray(ndarray=<Quantity 1. mm>)

    def _condition_arg(value):
        """
        Validate value is acceptable for conversion purposes.
    
        Will convert into an array if not a scalar, and can be converted
        into an array
    
        Parameters
        ----------
        value : int or float value, or sequence of such values
    
        Returns
        -------
        Scalar value or numpy array
    
        Raises
        ------
        ValueError
            If value is not as expected
        """
        if isinstance(value, (np.ndarray, float, int, complex, np.void)):
            return value
    
        avalue = np.array(value)
        if avalue.dtype.kind not in ['i', 'f', 'c']:
>           raise ValueError("Value not scalar compatible or convertible to "
                             "an int, float, or complex array")
E           ValueError: Value 
…[cut, 762 more chars]

## The agent's commands, in order (82; outputs omitted)

1. `find /testbed -type f -name "*.py" | head -20`
2. `grep -r "__array_ufunc__" /testbed --include="*.py" | head -30`
3. `grep -n "def __array_ufunc__" /testbed/astropy/units/quantity.py`
4. `sed -n '620,800p' /testbed/astropy/units/quantity.py`
5. `grep -n "_condition_arg" /testbed/astropy/units/core.py`
6. `sed -n '1060,1080p' /testbed/astropy/units/core.py`
7. `grep -n "def converters_and_unit" /testbed/astropy/units/quantity.py`
8. `grep -r "converters_and_unit" /testbed --include="*.py" | head -5`
9. `find /testbed -name "converters.py" -path "*/units/*"`
10. `sed -n '1,200p' /testbed/astropy/units/quantity_helper/converters.py`
11. `sed -n '200,400p' /testbed/astropy/units/quantity_helper/converters.py`
12. `find /testbed -name "helpers.py" -path "*/units/*"`
13. `sed -n '1,200p' /testbed/astropy/units/quantity_helper/helpers.py`
14. `sed -n '2600,2700p' /testbed/astropy/units/core.py`
15. `grep -n "helper_twoarg_invariant" /testbed/astropy/units/quantity_helper/helpers.py`
16. `sed -n '260,300p' /testbed/astropy/units/quantity_helper/helpers.py`
17. `grep -n "def get_converters_and_unit" /testbed/astropy/units/quantity_helper/helpers.py -A 30`
18. `sed -n '69,100p' /testbed/astropy/units/quantity_helper/helpers.py`
19. `cd /testbed && python -m pytest --version 2>&1 | head -5`
20. `cd /testbed && ls -la`
21. `find /testbed -name "check" -type f -executable`
22. `grep -A 10 -B 10 "check" /testbed/tox.ini`
23. `grep -r "def check" /testbed --include="*.py" | head -5`
24. `cat /testbed/conftest.py | head -100`
25. `ls -la /testbed | grep -E "check|test"`
26. `grep -A 5 -B 5 "test" /testbed/setup.py | head -30`
27. `find /testbed -type f -name "check" -o -name "check.py" -o -name "check.sh" 2>/dev/null`
28. `grep -i check /testbed/README.rst | head -5`
29. `ls -la /testbed/.github/`
30. `grep -r "check" /testbed/.github/workflows/ 2>/dev/null | head -10`
31. `find /testbed/.github/workflows -name "*.yml" -o -name "*.yaml" | head -10`
32. `cat /testbed/.github/workflows/ci_workflows.yml | head -100`
33. `grep -n "^check" /testbed/tox.ini`
34. `grep -i check /testbed/setup.cfg`
35. `find /testbed -name "*test*.py" -path "*/units/*" | head -20`
36. `grep -n "NotImplemented" /testbed/astropy/units/tests/test_quantity_ufuncs.py | head -10`
37. `sed -n '1350,1400p' /testbed/astropy/units/tests/test_quantity_ufuncs.py`
38. `grep -n "class DuckQuantity" /testbed/astropy/units/tests/test_quantity_ufuncs.py -A 20`
39. `sed -n '1310,1400p' /testbed/astropy/units/tests/test_quantity_ufuncs.py`
40. `grep -n "class Quantity" /testbed/astropy/units/quantity.py | head -2`
41. `grep -n "^class Quantity" /testbed/astropy/units/quantity.py`
42.
```
cd /testbed && python -c "
import dataclasses
import numpy as np
import astropy.units as u

@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    ndarray: u.Quantity

    @property
    def unit(self) -> u.UnitBase:
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):

        inputs = [inp.ndarray if isinstance(inp, DuckAr …[cut]
```
43. `sed -n '700,750p' /testbed/astropy/units/quantity.py`
44. `grep -n "arrays.append" /testbed/astropy/units/quantity.py`
45. `sed -n '660,680p' /testbed/astropy/units/quantity.py`
46. `cp /testbed/astropy/units/quantity.py /testbed/astropy/units/quantity.py.backup`
47. `sed -n '650,680p' /testbed/astropy/units/quantity.py`
48.
```
cd /testbed && python -c "
import sys
with open('astropy/units/quantity.py', 'r') as f:
    lines = f.readlines()

# Find the line with 'arrays.append(converter(input_) if converter else input_)'
for i, line in enumerate(lines):
    if 'arrays.append(converter(input_) if converter else input_)' in line:
        target = i
        break
else:
    print('Line not found')
    sys.exit(1)

# We need t …[cut]
```
49. `sed -n '650,690p' /testbed/astropy/units/quantity.py`
50. `sed -n '680,690p' /testbed/astropy/units/quantity.py | cat -A`
51. `sed -n '670,710p' /testbed/astropy/units/quantity.py | cat -n`
52. `sed -n '660,710p' /testbed/astropy/units/quantity.py`
53. `sed -n '670,680p' /testbed/astropy/units/quantity.py.backup`
54.
```
cd /testbed && python -c "
import sys
with open('astropy/units/quantity.py', 'r') as f:
    lines = f.readlines()

# Find the line with 'for input_, converter in zip(inputs, converters):'
for i, line in enumerate(lines):
    if 'for input_, converter in zip(inputs, converters):' in line:
        loop_start = i
        break

# Find the line after the loop (where indentation decreases)
for j in ran …[cut]
```
55.
```
cd /testbed && python -c "
import dataclasses
import numpy as np
import astropy.units as u

@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    ndarray: u.Quantity

    @property
    def unit(self) -> u.UnitBase:
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):

        inputs = [inp.ndarray if isinstance(inp, DuckAr …[cut]
```
56. `sed -n '667,690p' /testbed/astropy/units/quantity.py | cat -A`
57. `cd /testbed && pip install pytest -q 2>&1 | tail -5`
58. `cd /testbed && python -m pytest --version 2>&1`
59. `find /testbed -name "*.py" -exec grep -l "def check" {} \; 2>/dev/null | head -5`
60. `cd /testbed && python -c "import sys; sys.path.insert(0, '.'); import astropy; print(astropy.__version__)" 2>&1`
61. `ls -la /testbed/ | grep -E "^.*check$" 2>/dev/null`
62. `python -c "import numpy; print(numpy.__version__)" 2>&1`
63. `conda list | grep pytest 2>&1 | head -5`
64. `python -c "import pytest; print(pytest.__version__)" 2>&1`
65. `which pytest 2>&1`
66. `find /testbed -type f -executable -name "check" 2>/dev/null`
67. `which tox 2>&1`
68. `conda install -y tox 2>&1 | tail -5`
69. `find /testbed -name "*run*test*" -type f 2>/dev/null | head -10`
70. `head -30 /testbed/.pyinstaller/run_astropy_tests.py`
71. `grep -n "_get_converter" /testbed/astropy/units/core.py | head -5`
72.
```
cd /testbed && python -c "
import dataclasses
import numpy as np
import astropy.units as u

@dataclasses.dataclass
class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
    ndarray: u.Quantity

    @property
    def unit(self) -> u.UnitBase:
        return self.ndarray.unit

    def __array_ufunc__(self, function, method, *inputs, **kwargs):

        inputs = [inp.ndarray if isinstance(inp, DuckAr …[cut]
```
73. `cd /testbed && git diff HEAD -- astropy/units/quantity.py 2>&1 | head -100`
74. `cd /testbed && git diff HEAD -- astropy/units/quantity.py > patch.txt 2>&1`
75. `ls -l /testbed/patch.txt`
76. `cat /testbed/patch.txt`
77. `conda info --base 2>&1 | head -1`
78. `echo $PATH | tr ':' '\n' | grep -E "opt.*miniconda" | head -5`
79. `find /opt/miniconda3/envs/testbed -name "pytest" -type f 2>/dev/null`
80. `python -c "import sys; print(sys.path)" 2>&1 | head -5`
81. `ls /opt/miniconda3/envs/testbed/lib/python3.9/site-packages | grep pytest`
82. `cd /testbed && echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`

## The agent's last reasoning (last 3 turns)

```
Not found. So pytest is not installed as a standalone script. However, the pytest-* packages are installed, which likely depend on pytest itself. That means pytest is installed as a Python package but not in the PATH? Actually pip installs packages into the same environment, so pytest should be importable. But earlier we got ModuleNotFoundError. That suggests pytest is not installed at all, but the pytest-* packages are installed because they are dependencies of something else? That's weird. Let's check if there is a `pytest` module in site-packages.
...
Let's look in lib/python3.9/site-packages for pytest.
...
There is no pytest package, only pytest_*. That means pytest itself is not installed. The test suite must be using something else (maybe nose). However, the user said pytest is not installed; `check` is the way to run the tests. That suggests `check` is a script that installs pytest and runs tests. Since we cannot install packages, we need to assume that the existing tests will be run later by the user (maybe in CI). Our responsibility is to make the fix and provide the patch. Given the instructions, we should submit the patch now. However, we should also ensure that our change doesn't break anything else by at least running the specific test file that is mentioned in the issue (maybe there is a test file for the user's duck type). Since we cannot run pytest, we can't be sure. But we can still try to run the test file using the unittest module directly if we can import it without pytest dependencies. The test file uses pytest fixtures and decorators, which will fail. That's not good. We need to think differently: maybe the "check" command is a tox environment that uses the existing environment (which already has pytest installed as a system package). However, we have evidence that pytest is not installed. Could be that pytest is installed via `pip install .[test]` but not installed globally. Since we cannot run that, we must rely on the user's assurance. Given the situation, I think we should proceed to submit the patch. However, we should also consider adding a more robust fix: maybe we should also check if input_ is numeric before applying converter (i.e., check if it's an instance of np.ndarray, float, int, complex, np.void). That would avoid the try-except. But the try-except is fine. Now we need to ensure that the change is consistent with the numpy documentation: returning NotImplemented when the operation is not implemented. That's exactly what we want. Thus I'll finalize. Let's create the patch file again (just in case) and then submit.
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/astropy/units/quantity.py b/astropy/units/quantity.py
index b98abfafb..1ebed12c9 100644
--- a/astropy/units/quantity.py
+++ b/astropy/units/quantity.py
@@ -667,7 +667,14 @@ class Quantity(np.ndarray):
         arrays = []
         for input_, converter in zip(inputs, converters):
             input_ = getattr(input_, "value", input_)
-            arrays.append(converter(input_) if converter else input_)
+            if converter is not None:
+                try:
+                    input_ = converter(input_)
+                except ValueError:
+                    # Input is not numeric (e.g., a duck type that has a unit but no .value).
+                    # Return NotImplemented to allow other operands to handle the operation.
+                    return NotImplemented
+            arrays.append(input_)
 
         # Call our superclass's __array_ufunc__
         result = super().__array_ufunc__(function, method, *arrays, **kwargs)
diff --git a/astropy/units/quantity.py.backup b/astropy/units/quantity.py.backup
new file mode 100644
index 000000000..b98abfafb
--- /dev/null
+++ b/astropy/units/quantity.py.backup
@@ -0,0 +1,2229 @@
+# Licensed under a 3-clause BSD style license - see LICENSE.rst
+"""
+This module defines the `Quantity` object, which represents a number with some
+associated units. `Quantity` objects support operations like ordinary numbers,
+but will deal with unit conversions internally.
+"""
+
+# STDLIB
+import numbers
+import operator
+import re
+import warnings
+from fractions import Fraction
+
+# THIRD PARTY
+import numpy as np
+
+# LOCAL
+from astropy import config as _config
+from astropy.utils.compat import NUMPY_LT_1_22
+from astropy.utils.data_info import ParentDtypeInfo
+from astropy.utils.exceptions import AstropyDeprecationWarning, AstropyWarning
+from astropy.utils.misc import isiterable
+
+from .core import (
+    Unit,
+    UnitBase,
+    UnitConversionError,
+    UnitsError,
+    UnitTypeError,
+    dimensionless_unscaled,
+    get_current_unit_registry,
+)
+from .format import Base, Latex
+from .quantity_helper import can_have_arbitrary_unit, check_output, converters_and_unit
+from .quantity_helper.function_helpers import (
+    DISPATCHED_FUNCTIONS,
+    FUNCTION_HELPERS,
+    SUBCLASS_SAFE_FUNCTIONS,
+    UNSUPPORTED_FUNCTIONS,
+)
+from .structured import StructuredUnit, _structured_unit_like_dtype
+from .utils import is_effectively_unity
+
+__all__ = [
+    "Quantity",
+    "SpecificTypeQuantity",
+    "QuantityInfoBase",
+    "QuantityInfo",
+    "allclose",
+    "isclose",
+]
+
+
+# We don't want to run doctests in the docstrings we inherit from Numpy
+__doctest_skip__ = ["Quantity.*"]
+
+_UNIT_NOT_INITIALISED = "(Unit not initialised)"
+_UFUNCS_FILTER_WARNINGS = {np.arcsin, np.arccos, np.arccosh, np.arctanh}
+
+
+class Conf(_config.ConfigNamespace):
+    """
+    Configuration parameters for Quantity
+    """
+
+    latex_array_threshold = _config.ConfigItem(
+        100,
+        "The maximum size an array Quantity can be before its LaTeX "
+        'representation for IPython gets "summarized" (meaning only the first '
+        'and last few elements are shown with "..." between). Setting this to a '
+        "negative number means that the value will instead be whatever numpy "
+        "gets from get_printoptions.",
+    )
+
+
+conf = Conf()
+
+
+class QuantityIterator:
+    """
+    Flat iterator object to iterate over Quantities
+
+    A `QuantityIterator` iterator is returned by ``q.flat`` for any Quantity
+    ``q``.  It allows iterating over the array as if it were a 1-D array,
+    either in a for-loop or by calling its `next` method.
+
+    Iteration is done in C-contiguous style, with the last index varying the
+    fastest. The iterator can also be indexed using basic slicing or
+    advanced indexing.
+
+    See Also
+    --------
+    Quantity.flatten : Returns a flattened copy of an array.
+
+    Notes
+    -----
+    `QuantityIterator` is inspired by `~numpy.ma.core.MaskedIterator`.  It
+    is not exported by the `~astropy.units` module.  Instead of
+    instantiating a `QuantityIterator` directly, use `Quantity.flat`.
+    """
+
+    def __init__(self, q):
+        self._quantity = q
+        self._dataiter = q.view(np.ndarray).flat
+
+    def __iter__(self):
+        return self
+
+    def __getitem__(self, indx):
+        out = self._dataiter.__getitem__(indx)
+        # For single elements, ndarray.flat.__getitem__ returns scalars; these
+        # need a new view as a Quantity.
+        if isinstance(out, type(self._quantity)):
+            return out
+        else:
+            return self._quantity._new_view(out)
+
+    def __setitem__(self, index, value):
+        self._dataiter[index] = self._quantity._to_own_unit(value)
+
+    def __next__(self):
+        """
+        Return the next value, or raise StopIteration.
+        """
+        out = next(self._dataiter)
+        # ndarray.flat._dataiter returns scalars, so need a view as a Quantity.
+        return self._quantity._new_view(out)
+
+    next = __next__
+
+    def __len__(self):
+        return len(self._dataiter)
+
+    #### properties and methods to match `numpy.ndarray.flatiter` ####
+
+    @property
+    def base(self):
+        """A reference to the array that is iterated over."""
+        return self._quantity
+
+    @property
+    def coords(self):
+        """An N-dimensional tuple of current coordinates."""
+        return self._dataiter.coords
+
+    @property
+    def index(self):
+        """Current flat index into the array."""
+        return self._dataiter.index
+
+    def copy(self):
+        """Get a copy of the iterator as a 1-D array."""
+        return self._quantity.flatten()
+
+
+class QuantityInfoBase(ParentDtypeInfo):
+    # This is on a base class rather than QuantityInfo directly, so that
+    # it can be used for EarthLocationInfo yet make clear that that class
+    # should not be considered a typical Quantity subclass by Table.
+    attrs_from_parent = {"dtype", "unit"}  # dtype and unit taken from parent
+    _supports_indexing = True
+
+    @staticmethod
+    def default_format(val):
+        return f"{val.value}"
+
+    @staticmethod
+    def possible_string_format_functions(format_):
+        """Iterate through possible string-derived format functions.
+
+        A string can either be a format specifier for the format built-in,
+        a new-style format string, or an old-style format string.
+
+        This method is overridden in order to suppress printing the unit
+        in each row since it is already at the top in the column header.
+        """
+        yield lambda format_, val: format(val.value, format_)
+        yield lambda format_, val: format_.format(val.value)
+        yield lambda format_, val: format_ % val.value
+
+
+class QuantityInfo(QuantityInfoBase):
+    """
+    Container for meta information like name, description, format.  This is
+    required when the object is used as a mixin column within a table, but can
+    be used as a general way to store meta information.
+    """
+
+    _represent_as_dict_attrs = ("value", "unit")
+    _construct_from_dict_args = ["value"]
+    _represent_as_dict_primary_data = "value"
+
+    def new_like(self, cols, length, metadata_conflicts="warn", name=None):
+        """
+        Return a new Quantity instance which is consistent with the
+        input ``cols`` and has ``length`` rows.
+
+        This is intended for creating an empty column object whose elements can
+        be set in-place for table operations like join or vstack.
+
+        Parameters
+        ----------
+        cols : list
+            List of input columns
+        length : int
+            Length of the output column object
+        metadata_conflicts : str ('warn'|'error'|'silent')
+            How to handle metadata conflicts
+        name : str
+            Output column name
+
+        Returns
+        -------
+        col : `~astropy.units.Quantity` (or subclass)
+            Empty instance of this class consistent with ``cols``
+
+        """
+
+        # Get merged info attributes like shape, dtype, format, description, etc.
+        attrs = self.merge_cols_attributes(
+            cols, metadata_conflicts, name, ("meta", "format", "description")
+        )
+
+        # Make an empty quantity using the unit of the last one.
+        shape = (length,) + attrs.pop("shape")
+        dtype = attrs.pop("dtype")
+        # Use zeros so we do not get problems for Quantity subclasses such
+        # as Longitude and Latitude, which cannot take arbitrary values.
+        data = np.zeros(shape=shape, dtype=dtype)
+        # Get arguments needed to reconstruct class
+        map = {
+            key: (data if key == "value" else getattr(cols[-1], key))
+            for key in self._represent_as_dict_attrs
+        }
+        map["copy"] = False
+        out = self._construct_from_dict(map)
+
+        # Set remaining info attributes
+        for attr, value in attrs.items():
+            setattr(out.info, attr, value)
+
+        return out
+
+    def get_sortable_arrays(self):
+        """
+        Return a list of arrays which can be lexically sorted to represent
+        the order of the parent column.
+
+        For Quantity this is just the quantity itself.
+
+
+        Returns
+        -------
+        arrays : list of ndarray
+        """
+        return [self._parent]
+
+
+class Quantity(np.ndarray):
+    """A `~astropy.units.Quantity` represents a number with some associated unit.
+
+    See also: https://docs.astropy.org/en/stable/units/quantity.html
+
+    Parameters
+    ----------
+    value : number, `~numpy.ndarray`, `~astropy.units.Quantity` (sequence), or str
+        The numerical value of this quantity in the units given by unit.  If a
+        `Quantity` or sequence of them (or any other valid object with a
+        ``unit`` attribute), creates a new `Quantity` object, converting to
+        `unit` units as needed.  If a string, it is converted to a number or
+        `Quantity`, depending on whether a unit is present.
+
+    unit : unit-like
+        An object that represents the unit associated with the input value.
+        Must be an `~astropy.units.UnitBase` object or a string parseable by
+        the :mod:`~astropy.units` package.
+
+    dtype : ~numpy.dtype, optional
+        The dtype of the resulting Numpy array or scalar that will
+        hold the value.  If not provided, it is determined from the input,
+        except that any integer and (non-Quantity) object inputs are converted
+        to float by default.
+        If `None`, the normal `numpy.dtype` introspection is used, e.g.
+        preventing upcasting of integers.
+
+    copy : bool, optional
+        If `True` (default), then the value is copied.  Otherwise, a copy will
+        only be made if ``__array__`` returns a copy, if value is a nested
+        sequence, or if a copy is needed to satisfy an explicitly given
+        ``dtype``.  (The `False` option is intended mostly for internal use,
+        to speed up initialization where a copy is known to have been made.
+        Use with care.)
+
+    order : {'C', 'F', 'A'}, optional
+        Specify the order of the array.  As in `~numpy.array`.  This parameter
+        is ignored if the input is a `Quantity` and ``copy=False``.
+
+    subok : bool, optional
+        If `False` (default), the returned array will be forced to be a
+        `Quantity`.  Otherwise, `Quantity` subclasses will be passed through,
+        or a subclass appropriate for the unit will be used (such as
+        `~astropy.units.Dex` for ``u.dex(u.AA)``).
+
+    ndmin : int, optional
+        Specifies the minimum number of dimensions that the resulting array
+        should have.  Ones will be pre-pended to the shape as needed to meet
+        this requirement.  This parameter is ignored if the input is a
+        `Quantity` and ``copy=False``.
+
+    Rai
…[cut, 76769 more chars]
```

## The submitted patch (as submitted)

```diff
diff --git a/astropy/units/quantity.py b/astropy/units/quantity.py
index b98abfafb..1ebed12c9 100644
--- a/astropy/units/quantity.py
+++ b/astropy/units/quantity.py
@@ -667,7 +667,14 @@ class Quantity(np.ndarray):
         arrays = []
         for input_, converter in zip(inputs, converters):
             input_ = getattr(input_, "value", input_)
-            arrays.append(converter(input_) if converter else input_)
+            if converter is not None:
+                try:
+                    input_ = converter(input_)
+                except ValueError:
+                    # Input is not numeric (e.g., a duck type that has a unit but no .value).
+                    # Return NotImplemented to allow other operands to handle the operation.
+                    return NotImplemented
+            arrays.append(input_)
 
         # Call our superclass's __array_ufunc__
         result = super().__array_ufunc__(function, method, *arrays, **kwargs)

```
