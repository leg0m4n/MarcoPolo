# Item 31

**Repository:** sphinx-doc/sphinx  
**Task type:** ordinary  
**Run ended:** ran out of context  
**Official result of the submission:** not applicable (nothing submitted)  
**The task's test files:** tests/roots/test-ext-autodoc/target/properties.py, tests/test_domain_py.py, tests/test_ext_autodoc_autoclass.py, tests/test_ext_autodoc_autoproperty.py

## The issue

Methods decorated with @classmethod and @property do not get documented.
**EDIT:** The problem seems to be that `type(BaseClass.baseclass_property)` returns `property`, thus sphinx can just lookup `BaseClass.baseclass_property.__doc__`. However, `type(BaseClass.baseclass_class_property)` returns the type of the returned object, since essentially, a `@classmethod@property` ends up behaving like a class attribute. So Sphinx doesn't really have a chance to extract the docstring.

**EDIT 2:** Seems like this will get fixed in python 3.10, cf. https://bugs.python.org/issue43682. 

> Static methods (`@staticmethod`) and class methods (`@classmethod`) now inherit the method attributes (`__module__`, `__name__`, `__qualname__`, `__doc__`, `__annotations__`) and have a new __wrapped__ attribute. 

I will try to test this with the beta release.

-----

### Describe the bug

> Changed in version 3.9: Class methods can now wrap other descriptors such as property().

That is, since python version 3.9 we can write code like

```python
class A:
    @classmethod
    @property
    def f(cls):
        """Some class property."""
        return "property"
```

However, sphinx does not seem to document any such methods (regular `@property` decorated methods get documented just fine.)

### How to Reproduce


```bash
git clone https://github.com/randolf-scholz/sphinx_demo
cd sphinx_demo/docs
make html
# open _build/html/dummy_module.submodule.html
```

The following methods were erroneously not documented:

- `MetaClass.metaclass_class_property`
- `MetaClass.metaclass_abstract_class_property`
- `BaseClass.baseclass_class_property`
- `BaseClass.baseclass_abstract_class_property`
- `SubClass.subclass_class_property`
- `SubClass.subclass_abstract_class_property`


### Expected behavior

Methods that are decorated with both `@classmethod` and `@property` should be documented appropriately.

### Your project

https://github.com/randolf-scholz/sphinx_demo

### Screenshots

_No response_

### OS

Ubuntu 20.04.2 LTS

### Python version

3.9.6

### Sphinx version

4.0.3

### Sphinx extensions

sphinx.ext.autodoc, sphinx.ext.autosummary

### Extra tools

_No response_

### Additional context

_No response_


## The agent's commands, in order (127; outputs omitted)

1. `find / -name "sphinx_demo" -type d 2>/dev/null | head -5`
2. `pwd && ls -la`
3. `grep -r "classmethod" tests/ --include="*.py" | head -20`
4. `grep -r "classmethod.*property\|property.*classmethod" tests/ --include="*.py" -i`
5. `find sphinx -name "*.py" -exec grep -l "isclassmethod\|isproperty" {} \;`
6. `cat sphinx/util/inspect.py | head -200`
7. `grep -n "def isclassmethod\|def isproperty" sphinx/util/inspect.py`
8. `sed -n '248,300p' sphinx/util/inspect.py`
9. `sed -n '386,430p' sphinx/util/inspect.py`
10. `grep -n "isclassmethod\|isproperty" sphinx/ext/autodoc/__init__.py`
11. `sed -n '2070,2100p' sphinx/ext/autodoc/__init__.py`
12. `sed -n '2120,2150p' sphinx/ext/autodoc/__init__.py`
13. `sed -n '2650,2680p' sphinx/ext/autodoc/__init__.py`
14. `cd /testbed && check 2>&1 | head -50`
15. `grep -n "def test_pyproperty" tests/test_domain_py.py`
16. `sed -n '813,850p' tests/test_domain_py.py`
17. `grep -n "def test_properties" tests/test_ext_autodoc_autoclass.py`
18. `sed -n '204,250p' tests/test_ext_autodoc_autoclass.py`
19. `grep -n "def test_class_properties" tests/test_ext_autodoc_autoproperty.py`
20. `sed -n '32,60p' tests/test_ext_autodoc_autoproperty.py`
21. `cat tests/roots/test-ext-autodoc/target/properties.py`
22. `grep -n "classmethod" sphinx/domains/python.py | head -20`
23.
```
cd /testbed && python3 -c "
import inspect

class A:
    @classmethod
    @property
    def f(cls):
        '''Some class property.'''
        return 'property'

print('type(A.f)', type(A.f))
print('type(A.__dict__[\"f\"])', type(A.__dict__['f']))
print('inspect.isproperty(A.__dict__[\"f\"])', inspect.isproperty(A.__dict__['f']))
print('inspect.isclassmethod(A.__dict__[\"f\"])', inspect.isclassmet …[cut]
```
24.
```
cd /testbed && python3 -c "
import sys
sys.path.insert(0, '.')
from sphinx.util import inspect as inspect_module

class A:
    @classmethod
    @property
    def f(cls):
        '''Some class property.'''
        return 'property'

print('inspect_module.isproperty(A.__dict__[\"f\"])', inspect_module.isproperty(A.__dict__['f']))
print('inspect_module.isclassmethod(A.__dict__[\"f\"])', inspect_modul …[cut]
```
25. `grep -n "documenter_for_attribute\|documenter_for_member" sphinx/ext/autodoc/__init__.py | head -20`
26. `grep -n "documenter_for" sphinx/ext/autodoc/__init__.py`
27. `grep -n "documenter_for" sphinx/ext/autodoc/importer.py`
28. `grep -n "can_document_member" sphinx/ext/autodoc/__init__.py`
29. `sed -n '830,860p' sphinx/ext/autodoc/__init__.py`
30. `grep -n "class AttributeDocumenter" sphinx/ext/autodoc/__init__.py`
31. `sed -n '2477,2500p' sphinx/ext/autodoc/__init__.py`
32. `sed -n '2500,2530p' sphinx/ext/autodoc/__init__.py`
33. `grep -n "class MethodDocumenter" sphinx/ext/autodoc/__init__.py`
34. `sed -n '2060,2100p' sphinx/ext/autodoc/__init__.py`
35. `grep -n "class FunctionDocumenter" sphinx/ext/autodoc/__init__.py`
36. `sed -n '1273,1300p' sphinx/ext/autodoc/__init__.py`
37. `grep -n "priority" sphinx/ext/autodoc/__init__.py | head -30`
38. `sed -n '1395,1410p' sphinx/ext/autodoc/__init__.py`
39. `grep -n "class ModuleLevelDocumenter" sphinx/ext/autodoc/__init__.py`
40. `sed -n '1123,1150p' sphinx/ext/autodoc/__init__.py`
41.
```
cd /testbed && python3 -c "
import inspect
class A:
    @classmethod
    @property
    def f(cls):
        pass
print('inspect.isroutine(A.__dict__[\"f\"])', inspect.isroutine(A.__dict__['f']))
print('inspect.isroutine(A.f)', inspect.isroutine(A.f))
"
```
42. `grep -n "filter_members" sphinx/ext/autodoc/__init__.py`
43. `sed -n '669,730p' sphinx/ext/autodoc/__init__.py`
44. `grep -n "class PyProperty" sphinx/domains/python.py`
45. `sed -n '849,950p' sphinx/domains/python.py`
46. `grep -n "isproperty" sphinx/domains/python.py`
47. `grep -n "'property'" sphinx/domains/python.py`
48. `grep -n "class PythonDomain" sphinx/domains/python.py`
49. `sed -n '1106,1300p' sphinx/domains/python.py`
50. `find tests/roots -name "*test-domain-py*" -type d`
51. `cat tests/roots/test-domain-py/index.rst`
52. `grep -r "class Class" tests/roots/`
53. `grep -B5 -A5 "test_pyproperty" tests/test_domain_py.py`
54. `find sphinx/testing -name "*.py" -exec grep -l "domain_py" {} \;`
55. `grep -r "domain_py" . --include="*.py" 2>/dev/null | head -5`
56. `grep -r "prop1\|prop2" tests/roots/ 2>/dev/null`
57. `find tests/roots/test-domain-py -type f -name "*.py" -exec grep -l "property" {} \;`
58.
```
cd /testbed && python3 -c "
import sys
sys.path.insert(0, '.')
from sphinx.util import inspect as inspect_module

class A:
    @classmethod
    @property
    def f(cls):
        '''Some class property.'''
        return 'property'

cm = A.__dict__['f']
print('cm:', cm)
print('cm.__func__:', cm.__func__)
print('type(cm.__func__):', type(cm.__func__))
print('inspect_module.isproperty(cm.__func__):', …[cut]
```
59. `grep -r "isproperty" sphinx/ --include="*.py"`
60. `grep -n "def unwrap_all" sphinx/util/inspect.py`
61. `sed -n '126,160p' sphinx/util/inspect.py`
62. `sed -n '386,400p' sphinx/util/inspect.py`
63. `cd /testbed && python3 -m pytest tests/test_domain_py.py::test_pyproperty -xvs 2>&1 | head -100`
64. `cd /testbed && python3 -m sphinx.testing.fixtures.test_domain_py 2>&1 | head -30`
65. `python3 -c "import pytest; print(pytest.__version__)" 2>&1`
66. `cd /testbed && check --verbose 2>&1 | head -200`
67. `find . -name "domain_py.py" -type f`
68. `ls -la sphinx/testing/`
69. `grep -n "domain_py" sphinx/testing/fixtures.py`
70. `find tests/roots/test-domain-py -name "roles.rst" -exec cat {} \;`
71. `cat tests/roots/test-domain-py/module.rst`
72. `grep -r "prop2" tests/roots/test-domain-py/ 2>/dev/null`
73. `grep -n "@pytest.fixture" sphinx/testing/fixtures.py`
74. `sed -n '65,120p' sphinx/testing/fixtures.py`
75. `grep -n "def app" sphinx/testing/util.py`
76. `grep -n "^from\|^import" sphinx/testing/fixtures.py | head -10`
77. `grep -n "^def app" sphinx/testing/util.py`
78. `grep -r "@pytest.fixture.*def app" sphinx/testing/ 2>/dev/null`
79. `head -30 tests/test_domain_py.py`
80. `tail -100 sphinx/testing/util.py`
81. `grep -A5 -B5 "^def app" sphinx/testing/fixtures.py 2>/dev/null || echo "not found"`
82. `sed -n '140,200p' sphinx/testing/fixtures.py`
83. `grep -B10 "def test_pyproperty" tests/test_domain_py.py`
84. `ls -la tests/roots/root/`
85. `find tests/roots -type d -name "root" 2>/dev/null`
86. `grep -r "class Class" tests/roots/ 2>/dev/null | grep -v ".pyc" | head -5`
87. `ls -la tests/roots/test-root/`
88. `cat tests/roots/test-root/autodoc_target.py | head -100`
89. `grep -r "prop2" . --include="*.py" 2>/dev/null | grep -v ".pyc" | head -10`
90. `grep -B20 -A20 "prop2.*Class property" tests/test_domain_py.py`
91. `sed -n '813,830p' tests/test_domain_py.py`
92. `grep -n "note_object" sphinx/domains/python.py`
93. `grep -r "^class Class" . --include="*.py" 2>/dev/null | grep -v test_ext_autodoc_autoproperty | grep -v test_ext_autodoc_autoclass`
94. `find tests/roots/test-domain-py -type f -name "*.py" -exec cat {} \; 2>/dev/null | head -200`
95. `cat tests/roots/test-root/conf.py`
96. `find . -path "./sphinx/testing/fixtures/domain_py.py" 2>/dev/null`
97. `sed -n '2670,2750p' sphinx/ext/autodoc/__init__.py`
98. `grep -n "class PropertyDocumenter" sphinx/ext/autodoc/__init__.py`
99. `sed -n '2651,2700p' sphinx/ext/autodoc/__init__.py`
100.
```
cd /testbed && python3 -c "
import sys
sys.path.insert(0, '.')
from sphinx.util import inspect as inspect_module
import inspect

class Foo:
    @classmethod
    @property
    def prop2(self) -> int:
        '''docstring'''
        return 1

print('Foo.__dict__[\"prop2\"]:', Foo.__dict__['prop2'])
print('type:', type(Foo.__dict__['prop2']))
print('isproperty:', inspect_module.isproperty(Foo.__dict_ …[cut]
```
101. `grep -n "unwrap_all" sphinx/util/inspect.py | head -2`
102. `cd /testbed && cp sphinx/util/inspect.py sphinx/util/inspect.py.backup`
103. `sed -n '386,400p' sphinx/util/inspect.py`
104.
```
cd /testbed && sed -i '386,400c\
def isproperty(obj: Any) -> bool:\n    """Check if the object is property."""\n    # unwrap classmethod and staticmethod, as they can wrap property\n    obj = unwrap_all(obj)\n    if sys.version_info >= (3, 8):\n        from functools import cached_property  # cached_property is available since py3.8\n        if isinstance(obj, cached_property):\n            return …[cut]
```
105. `sed -n '386,410p' sphinx/util/inspect.py`
106. `cd /testbed && cp sphinx/util/inspect.py.backup sphinx/util/inspect.py`
107. `grep -n "def isproperty" sphinx/util/inspect.py`
108. `sed -n '386,410p' sphinx/util/inspect.py`
109.
```
cd /testbed && python3 -c "
import sys
with open('sphinx/util/inspect.py', 'r') as f:
    lines = f.readlines()
# find start and end of isproperty
start = None
for i, line in enumerate(lines):
    if line.startswith('def isproperty'):
        start = i
        break
if start is None:
    sys.exit(1)
# find end of function (next def or class with same indentation)
for i in range(start + 1, len(line …[cut]
```
110. `sed -n '386,410p' sphinx/util/inspect.py`
111.
```
cd /testbed && python3 -c "
class Foo:
    @classmethod
    @property
    def prop2(self) -> int:
        '''docstring'''
        return 1

print('prop2.__doc__:', Foo.prop2.__doc__)
print('prop2.__func__.__doc__:', Foo.prop2.__func__.__doc__)
print('prop2.__func__.fget.__doc__:', Foo.prop2.__func__.fget.__doc__)
"
```
112.
```
cd /testbed && python3 -c "
class Foo:
    @classmethod
    @property
    def prop2(self) -> int:
        '''docstring'''
        return 1

prop = Foo.__dict__['prop2']
print('prop:', prop)
print('prop.__doc__:', prop.__doc__)
print('prop.__func__:', prop.__func__)
print('prop.__func__.__doc__:', prop.__func__.__doc__)
print('prop.__func__.fget:', prop.__func__.fget)
print('prop.__func__.fget.__do …[cut]
```
113. `cd /testbed && python3 -m pytest tests/test_ext_autodoc_autoproperty.py::test_class_properties -xvs 2>&1 | head -100`
114. `pip install pytest -q 2>&1 | tail -5`
115. `grep -n "class PropertyDocumenter" sphinx/ext/autodoc/__init__.py`
116. `sed -n '2651,2720p' sphinx/ext/autodoc/__init__.py`
117. `grep -n "def add_directive_header" sphinx/ext/autodoc/__init__.py | grep -A1 -B1 "PropertyDocumenter"`
118.
```
cd /testbed && python3 -c "
import sys
with open('sphinx/ext/autodoc/__init__.py', 'r') as f:
    lines = f.readlines()
inside = False
for i, line in enumerate(lines):
    if i >= 2650 and 'def add_directive_header' in line:
        print('method start at', i+1)
        # find end of method (next def or class at same indentation)
        indent = len(line) - len(line.lstrip())
        for j in ran …[cut]
```
119. `sed -n '2673,2693p' sphinx/ext/autodoc/__init__.py`
120.
```
cd /testbed && python3 -c "
import sys
with open('sphinx/ext/autodoc/__init__.py', 'r') as f:
    lines = f.readlines()
# replace lines 2673-2693 (0-indexed 2672-2692)
new_method = '''    def add_directive_header(self, sig: str) -> None:
        super().add_directive_header(sig)
        sourcename = self.get_sourcename()

        # Determine if this property is wrapped by classmethod or staticmeth …[cut]
```
121. `sed -n '2670,2700p' sphinx/ext/autodoc/__init__.py`
122. `sed -n '710,770p' sphinx/domains/python.py`
123. `sed -n '849,950p' sphinx/domains/python.py`
124. `grep -B5 -A5 "class PyProperty" sphinx/domains/python.py`
125. `grep -n "class PyClasslike" sphinx/domains/python.py`
126. `sed -n '681,800p' sphinx/domains/python.py`
127. `cd /testbed && check 2>&1 | head -100`

## The agent's last reasoning (last 3 turns)

```
So it's a direct subclass of PyObject. That means the directive `py:property` does not support `:classmethod:`. Yet the test expects it. Something else is adding the `:classmethod:` line. Perhaps the test is using `py:method` but the test text is `py:property`? Let's examine the test's `text` variable again. It's exactly as shown. Could be that the test is wrong? But the test was written to verify the bug. The bug is that classmethod@property methods are not documented. The test expects them to be documented with `:classmethod:` line. That suggests that the directive should support `:classmethod:` option. However, the Python domain may have been updated in Sphinx version? We need to look at the version of Sphinx we're working on (likely latest). The test may have been written before a change? The issue says Sphinx doesn't document them. The test expects them to be documented with `:classmethod:` line, meaning the test is the expected behavior (i.e., what should happen after fix). So we need to make the `py:property` directive support `:classmethod:` option. That involves modifying PyProperty's option_spec and get_signature_prefix, get_index_text, etc. But also need to ensure that the domain's `note_object` stores the correct objtype? The objtype for property is 'property'. The classmethod flag is just an option. We need to decide: Should we extend PyProperty to also support `:classmethod:` and `:staticmethod:` options? That would mirror PyMethod's support. However, note that PyMethod already has `:property:` option. That means you could document a classmethod-wrapped property as `.. py:method:: prop2 :property: :classmethod:`. That might be the intended usage. But the test uses `py:property` directive. That suggests that `py:property` should also support `:classmethod:` (maybe for convenience). We can add those options to PyProperty. Let's examine PyMethod's option_spec to see how they handle `:property:` and `:classmethod:` together. They are separate flags. In PyMethod, `':property:'` flag indicates that the method is a property (i.e., a property method). That means you can have a method that is both a property and a classmethod? Actually `':property:'` is used to indicate that the method is a property (like getter). That's likely used for documenting property getters. That's different from a property descriptor. Wait, the `:property:` option in PyMethod is used to indicate that the method is a property (i.e., the method is the getter of a property). That's for documenting the property getter function itself. That's not what we need. Thus, we need to think differently. The issue is about `@classmethod @property` decorated methods. In the Python domain, how are such methods currently documented? They are likely not documented at all (the bug). The fix should make them be documented as properties with a `:classmethod:` flag. That means we need to modify the domain's detection of properties to include classmethod-wrapped properties, and also ensure that the `:classmethod:` flag is added. We have already modified `isproperty` to detect them. That will help autodoc and domain py's property detection (since domain py may also use `isproperty`? Let's search for `isproperty` in python.py again (we already did, none). So domain py likely does not use `isproperty`. It probably uses `inspect.ismethoddescriptor` or something else. We need to find where property objects are added to the domain. That's likely in `sphinx/domains/python.py` in the `get_objects` method? Actually PythonDomain doesn't have a `get_objects` method; it inherits from Domain which uses `note_object`. The objects are added by the `PyObject` class when directives are processed. That means the `py:property` directive adds objects. So the domain py's handling of classmethod-wrapped properties is only relevant for autodoc, not for domain py? But the test `test_pyproperty` is about domain py, not autodoc. That test likely uses the same module (maybe the same fixture) and
…[cut, 3208 more chars]
```

## Final state of the repository (git diff vs the starting commit, all files incl. tests)

```diff
diff --git a/sphinx/ext/autodoc/__init__.py b/sphinx/ext/autodoc/__init__.py
index 1cecb1f79..4454f2520 100644
--- a/sphinx/ext/autodoc/__init__.py
+++ b/sphinx/ext/autodoc/__init__.py
@@ -2673,24 +2673,32 @@ class PropertyDocumenter(DocstringStripSignatureMixin, ClassLevelDocumenter):  #
     def add_directive_header(self, sig: str) -> None:
         super().add_directive_header(sig)
         sourcename = self.get_sourcename()
+
+        # Determine if this property is wrapped by classmethod or staticmethod
+        prop_obj = self.object
+        if isinstance(prop_obj, classmethod):
+            self.add_line('   :classmethod:', sourcename)
+            prop_obj = prop_obj.__func__
+        elif isinstance(prop_obj, staticmethod):
+            self.add_line('   :staticmethod:', sourcename)
+            prop_obj = prop_obj.__func__
+
         if inspect.isabstractmethod(self.object):
             self.add_line('   :abstractmethod:', sourcename)
 
-        if safe_getattr(self.object, 'fget', None) and self.config.autodoc_typehints != 'none':
+        if safe_getattr(prop_obj, 'fget', None) and self.config.autodoc_typehints != 'none':
             try:
-                signature = inspect.signature(self.object.fget,
+                signature = inspect.signature(prop_obj.fget,
                                               type_aliases=self.config.autodoc_type_aliases)
                 if signature.return_annotation is not Parameter.empty:
                     objrepr = stringify_typehint(signature.return_annotation)
                     self.add_line('   :type: ' + objrepr, sourcename)
             except TypeError as exc:
-                logger.warning(__("Failed to get a function signature for %s: %s"),
+                logger.warning(__('Failed to get a function signature for %s: %s'),
                                self.fullname, exc)
                 return None
             except ValueError:
                 return None
-
-
 class NewTypeAttributeDocumenter(AttributeDocumenter):
     """
     Specialized Documenter subclass for NewTypes.
diff --git a/sphinx/util/inspect.py b/sphinx/util/inspect.py
index 23dd9e930..3210b19f2 100644
--- a/sphinx/util/inspect.py
+++ b/sphinx/util/inspect.py
@@ -385,14 +385,14 @@ def iscoroutinefunction(obj: Any) -> bool:
 
 def isproperty(obj: Any) -> bool:
     """Check if the object is property."""
+    # unwrap classmethod and staticmethod, as they can wrap property
+    obj = unwrap_all(obj)
     if sys.version_info >= (3, 8):
         from functools import cached_property  # cached_property is available since py3.8
         if isinstance(obj, cached_property):
             return True
 
     return isinstance(obj, property)
-
-
 def isgenericalias(obj: Any) -> bool:
     """Check if the object is GenericAlias."""
     if (hasattr(typing, '_GenericAlias') and  # only for py37+
diff --git a/sphinx/util/inspect.py.backup b/sphinx/util/inspect.py.backup
new file mode 100644
index 000000000..23dd9e930
--- /dev/null
+++ b/sphinx/util/inspect.py.backup
@@ -0,0 +1,865 @@
+"""
+    sphinx.util.inspect
+    ~~~~~~~~~~~~~~~~~~~
+
+    Helpers for inspecting Python modules.
+
+    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
+    :license: BSD, see LICENSE for details.
+"""
+
+import builtins
+import contextlib
+import enum
+import inspect
+import re
+import sys
+import types
+import typing
+import warnings
+from functools import partial, partialmethod
+from importlib import import_module
+from inspect import Parameter, isclass, ismethod, ismethoddescriptor, ismodule  # NOQA
+from io import StringIO
+from types import ModuleType
+from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple, Type, cast
+
+from sphinx.deprecation import RemovedInSphinx50Warning
+from sphinx.pycode.ast import ast  # for py36-37
+from sphinx.pycode.ast import unparse as ast_unparse
+from sphinx.util import logging
+from sphinx.util.typing import ForwardRef
+from sphinx.util.typing import stringify as stringify_annotation
+
+if sys.version_info > (3, 7):
+    from types import ClassMethodDescriptorType, MethodDescriptorType, WrapperDescriptorType
+else:
+    ClassMethodDescriptorType = type(object.__init__)
+    MethodDescriptorType = type(str.join)
+    WrapperDescriptorType = type(dict.__dict__['fromkeys'])
+
+if False:
+    # For type annotation
+    from typing import Type  # NOQA
+
+logger = logging.getLogger(__name__)
+
+memory_address_re = re.compile(r' at 0x[0-9a-f]{8,16}(?=>)', re.IGNORECASE)
+
+
+# Copied from the definition of inspect.getfullargspec from Python master,
+# and modified to remove the use of special flags that break decorated
+# callables and bound methods in the name of backwards compatibility. Used
+# under the terms of PSF license v2, which requires the above statement
+# and the following:
+#
+#   Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
+#   2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017 Python Software
+#   Foundation; All Rights Reserved
+def getargspec(func: Callable) -> Any:
+    """Like inspect.getfullargspec but supports bound methods, and wrapped
+    methods."""
+    warnings.warn('sphinx.ext.inspect.getargspec() is deprecated',
+                  RemovedInSphinx50Warning, stacklevel=2)
+
+    sig = inspect.signature(func)
+
+    args = []
+    varargs = None
+    varkw = None
+    kwonlyargs = []
+    defaults = ()
+    annotations = {}
+    defaults = ()
+    kwdefaults = {}
+
+    if sig.return_annotation is not sig.empty:
+        annotations['return'] = sig.return_annotation
+
+    for param in sig.parameters.values():
+        kind = param.kind
+        name = param.name
+
+        if kind is Parameter.POSITIONAL_ONLY:
+            args.append(name)
+        elif kind is Parameter.POSITIONAL_OR_KEYWORD:
+            args.append(name)
+            if param.default is not param.empty:
+                defaults += (param.default,)  # type: ignore
+        elif kind is Parameter.VAR_POSITIONAL:
+            varargs = name
+        elif kind is Parameter.KEYWORD_ONLY:
+            kwonlyargs.append(name)
+            if param.default is not param.empty:
+                kwdefaults[name] = param.default
+        elif kind is Parameter.VAR_KEYWORD:
+            varkw = name
+
+        if param.annotation is not param.empty:
+            annotations[name] = param.annotation
+
+    if not kwdefaults:
+        # compatibility with 'func.__kwdefaults__'
+        kwdefaults = None
+
+    if not defaults:
+        # compatibility with 'func.__defaults__'
+        defaults = None
+
+    return inspect.FullArgSpec(args, varargs, varkw, defaults,
+                               kwonlyargs, kwdefaults, annotations)
+
+
+def unwrap(obj: Any) -> Any:
+    """Get an original object from wrapped object (wrapped functions)."""
+    try:
+        if hasattr(obj, '__sphinx_mock__'):
+            # Skip unwrapping mock object to avoid RecursionError
+            return obj
+        else:
+            return inspect.unwrap(obj)
+    except ValueError:
+        # might be a mock object
+        return obj
+
+
+def unwrap_all(obj: Any, *, stop: Callable = None) -> Any:
+    """
+    Get an original object from wrapped object (unwrapping partials, wrapped
+    functions, and other decorators).
+    """
+    while True:
+        if stop and stop(obj):
+            return obj
+        elif ispartial(obj):
+            obj = obj.func
+        elif inspect.isroutine(obj) and hasattr(obj, '__wrapped__'):
+            obj = obj.__wrapped__
+        elif isclassmethod(obj):
+            obj = obj.__func__
+        elif isstaticmethod(obj):
+            obj = obj.__func__
+        else:
+            return obj
+
+
+def getall(obj: Any) -> Optional[Sequence[str]]:
+    """Get __all__ attribute of the module as dict.
+
+    Return None if given *obj* does not have __all__.
+    Raises ValueError if given *obj* have invalid __all__.
+    """
+    __all__ = safe_getattr(obj, '__all__', None)
+    if __all__ is None:
+        return None
+    else:
+        if (isinstance(__all__, (list, tuple)) and all(isinstance(e, str) for e in __all__)):
+            return __all__
+        else:
+            raise ValueError(__all__)
+
+
+def getannotations(obj: Any) -> Mapping[str, Any]:
+    """Get __annotations__ from given *obj* safely."""
+    __annotations__ = safe_getattr(obj, '__annotations__', None)
+    if isinstance(__annotations__, Mapping):
+        return __annotations__
+    else:
+        return {}
+
+
+def getglobals(obj: Any) -> Mapping[str, Any]:
+    """Get __globals__ from given *obj* safely."""
+    __globals__ = safe_getattr(obj, '__globals__', None)
+    if isinstance(__globals__, Mapping):
+        return __globals__
+    else:
+        return {}
+
+
+def getmro(obj: Any) -> Tuple[Type, ...]:
+    """Get __mro__ from given *obj* safely."""
+    __mro__ = safe_getattr(obj, '__mro__', None)
+    if isinstance(__mro__, tuple):
+        return __mro__
+    else:
+        return tuple()
+
+
+def getslots(obj: Any) -> Optional[Dict]:
+    """Get __slots__ attribute of the class as dict.
+
+    Return None if gienv *obj* does not have __slots__.
+    Raises TypeError if given *obj* is not a class.
+    Raises ValueError if given *obj* have invalid __slots__.
+    """
+    if not inspect.isclass(obj):
+        raise TypeError
+
+    __slots__ = safe_getattr(obj, '__slots__', None)
+    if __slots__ is None:
+        return None
+    elif isinstance(__slots__, dict):
+        return __slots__
+    elif isinstance(__slots__, str):
+        return {__slots__: None}
+    elif isinstance(__slots__, (list, tuple)):
+        return {e: None for e in __slots__}
+    else:
+        raise ValueError
+
+
+def isNewType(obj: Any) -> bool:
+    """Check the if object is a kind of NewType."""
+    __module__ = safe_getattr(obj, '__module__', None)
+    __qualname__ = safe_getattr(obj, '__qualname__', None)
+    if __module__ == 'typing' and __qualname__ == 'NewType.<locals>.new_type':
+        return True
+    else:
+        return False
+
+
+def isenumclass(x: Any) -> bool:
+    """Check if the object is subclass of enum."""
+    return inspect.isclass(x) and issubclass(x, enum.Enum)
+
+
+def isenumattribute(x: Any) -> bool:
+    """Check if the object is attribute of enum."""
+    return isinstance(x, enum.Enum)
+
+
+def unpartial(obj: Any) -> Any:
+    """Get an original object from partial object.
+
+    This returns given object itself if not partial.
+    """
+    while ispartial(obj):
+        obj = obj.func
+
+    return obj
+
+
+def ispartial(obj: Any) -> bool:
+    """Check if the object is partial."""
+    return isinstance(obj, (partial, partialmethod))
+
+
+def isclassmethod(obj: Any) -> bool:
+    """Check if the object is classmethod."""
+    if isinstance(obj, classmethod):
+        return True
+    elif inspect.ismethod(obj) and obj.__self__ is not None and isclass(obj.__self__):
+        return True
+
+    return False
+
+
+def isstaticmethod(obj: Any, cls: Any = None, name: str = None) -> bool:
+    """Check if the object is staticmethod."""
+    if isinstance(obj, staticmethod):
+        return True
+    elif cls and name:
+        # trace __mro__ if the method is defined in parent class
+        #
+        # .. note:: This only works well with new style classes.
+        for basecls in getattr(cls, '__mro__', [cls]):
+            meth = basecls.__dict__.get(name)
+            if meth:
+                if isinstance(meth, staticmethod):
+                    return True
+                else:
+                    return False
+
+    return False
+
+
+def isdescriptor(x: Any) -> bool:
+    """Check if the object is some kind of descriptor."""
+    for item in '__get__', '__set__', '__delete__':
+        if hasattr(safe_getattr(x, item, None), '__call__'):
+            return True
+    return False
+
+
+def isabstractmethod(obj: Any) -> bool:
+    """Check if the object is an abstractmet
…[cut, 22173 more chars]
```

## The submitted patch (as submitted)

```diff
(nothing submitted)
```
