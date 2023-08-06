# PioDispatch
Dispatch blocking IO calls to threads wrapped in coroutines (technically, `asyncio.Future`s). It allows easily
integrating older blocking APIs with async/await syntax.

# Installation
Install via pip:

    pip install piodispatch

# Usage
The `piodispatch` module defines two epicentral functions: `dispatch` and `ascoroutine`.

Using `dispatch` works as follows:

```python
from piodispatch import dispatch
import requests

async def myfun():
    res = await dispatch(requests.get, 'https://google.com/')
    # type(res) is requests.Response
```

`dispatch` passes any `*args` and `**kwargs` on to its first parameter, which is assumed to be a [`Callable`](https://docs.python.org/3/library/typing.html#callable).

Using `ascoroutine` works slightly differently:

```python
from piodispatch import ascoroutine
import requests

rget = ascoroutine(requests.get)

async def myfun():
    res = await rget('https://google.com/')
    # type(res) is requests.Response
```

Unlike `dispatch`, which immediately executes the method, `ascoroutine` wraps the method in a coroutine which internally
simply calls `dispatch`. While it could technically also be used as a [decorator](https://www.geeksforgeeks.org/python-decorators-a-complete-guide/),
this is effectively the same as simply writing an `async def`.

# License

MIT License

Copyright (c) 2020 Kiruse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

