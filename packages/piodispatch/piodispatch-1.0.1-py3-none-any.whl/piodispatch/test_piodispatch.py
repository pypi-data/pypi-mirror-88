"""PioDispatch microlibrary unit test.
Copyright (c) Kiruse 2020. See license in LICENSE."""
from time import sleep, time
from .piodispatch import ascoroutine, dispatch
import requests
import pytest

rget = ascoroutine(requests.get)

@pytest.mark.asyncio
async def test_dispatch():
    res = await dispatch(requests.get, 'https://google.com/')
    assert type(res) is requests.Response
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_ascoroutine():
    res = await rget('https://google.com/')
    assert type(res) is requests.Response
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_true_async():
    t0 = time()
    
    coros = [dispatch(sleep, 1) for _ in range(10)]
    for coro in coros:
        await coro
    
    assert time() - t0 < 2
