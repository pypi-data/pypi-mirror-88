
# c2py
Create python wrappers that call c functions, without the headaches.

In a nutshell:

```python
from c2py import dispatch
m = dispatch(
    src,  # specification of the C sources (poiting to specific C functions)
	convention,  # optional convention of wrapping rules
	**configs  # specific configuration (for wrapping rules that are not covered by convention, or need to be overwritten)
)

m.python_wrapper_to_c_func(...)  # now m is a module containing python wrappers to the desired c functions
```

Other forms:
```python
dispatch_to_file(src, target_filepath, ...)  # to get output as a persisted .py file
```

To install:	```pip install c2py```






