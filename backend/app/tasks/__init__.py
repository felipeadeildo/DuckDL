import asyncio
import functools
import threading

import gevent.monkey
from app.config import settings
from huey import SqliteHuey

gevent.monkey.patch_all()

huey_app = SqliteHuey(filename=settings.huey_filename)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def get_running_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        t = threading.Thread(target=start_loop, args=(loop,), daemon=True)
        t.start()
    return loop


def run_async_task(async_func):
    @functools.wraps(async_func)
    def wrapper(*args, **kwargs):
        loop = get_running_loop()
        coroutine = async_func(*args, **kwargs)
        future = asyncio.run_coroutine_threadsafe(coroutine, loop)
        return future.result()

    return wrapper
