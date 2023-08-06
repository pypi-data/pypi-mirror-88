# Introduction

The elegant-structure module contains data structures to make code more elegant.

# Install
```python
pip install elegant-structure
```
or update
```python
pip install --upgrade elegant-structure
```

# Usage
```python
from elegant_structure import Pool

class Test:
    def __init__(self, x, y):
        self.x = x
        self.y = y

test_pool = Pool(Test, verbose=True)
x = test_pool.add(1, 2)
y = test_pool.add(3, 4)

test_pool.remove(x)
test1 = test_pool[x]
if test1:
    print(test1.x, test1.y)
test2 = test_pool[y]
if test2:
    print(test2.x, test2.y)
```
```shell
the item is not exist in pool.
3 4
```

# License

elegant-io is a free software. See the file LICENSE for the full text.

# Authors

![qrcode_for_wechat_official_account](https://wx3.sinaimg.cn/mw1024/bdb7558bly1gjo23b3jrmj207607674r.jpg)

