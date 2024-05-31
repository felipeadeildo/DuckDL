import asyncio

from celery import Task


# TODO: fix async tasks wrapper (its broken)
class AsyncCeleryTask(Task):
    def __call__(self, *args, **kwargs):
        return asyncio.run(self.run(*args, **kwargs))
