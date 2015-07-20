# Utils

The utils library is a collection of useful but miscellaneous functions. Each function should do one thing and one thing only. Inspired by the unix commands, this ethos should allow for the removal of repetitious code without sacrificing code readability and therefore maintainability.

Here are a set of rules that should be followed when developing in the utils library:

* Each module should contain exactly one public function.
* Each module may contain multiple private funtions to make clear the intention of the public function.
* Each module should contain logging as defined in the Logging best practice.  Each module should have a test suite (unit or integration).
* Each module should do exactly one thing.
* No module should contain calls to another module in the utils library.
* Each module should be used as follows:
```python
from utils import utils_function
utils_function()
```
This is achieved by including ```from .utils_module import utils_function``` in the ```__init__.py```.
* Each module should contain a single docstring in the public function such that help(utils_function) details in pragmatic terms the behaviour of the function and precisely how it should be called. For example:
```python
def foo(bar):
    """ Here's a line explaining concisely what foo does.

    Here's a couple more lines explaining what foo does. Feel free to be a little more verbose 
    here and include details on how foo does what it does.

    :param bar: Explain concisely what bar is, including the data type if it isn't obvious.

    Usage::

    >>> from utils import foo
    >>> foo(bar)
    """
    ...
```
