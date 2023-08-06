# ReturnType

Generic type ReturnType and mypy checker plugin

# Install

```shell
pip install return_type
```
add plugin to `mypy.ini`
```ini
[mypy]
plugins = return_type/mypy-plugin.py
```

# Usage
```python3
import typing as t
from return_type import ReturnType

C = t.Callable[..., int]
RC = ReturnType[C]

assert RC = int
v1: RC = 1  # correct
v2: RC = 1.  # error
```
