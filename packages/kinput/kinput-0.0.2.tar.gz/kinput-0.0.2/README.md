# kinput

![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/kinput?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/kinput)

## Description

Simplified way for asking for user input

## Install

~~~~bash
pip install kinput
# or
pip3 install kinput
~~~~

## Demo

```python
from kinput import input

result, error = input("What's your age?", default=19, type=int)

print(result, error)
```
