import asyncio

import requests


class AsyncSession(requests.Session):
    """Um cliente async para requests (gambiarra)"""

    async def get(self, url, params=None, **kwargs):
        return await asyncio.to_thread(
            requests.Session.get, self, url, params=params, **kwargs
        )

    async def options(self, url, **kwargs):
        return await asyncio.to_thread(requests.Session.options, self, url, **kwargs)

    async def head(self, url, **kwargs):
        return await asyncio.to_thread(requests.Session.head, self, url, **kwargs)

    async def post(self, url, data=None, json=None, **kwargs):
        return await asyncio.to_thread(
            requests.Session.post, self, url, data=data, json=json, **kwargs
        )

    async def put(self, url, data=None, **kwargs):
        return await asyncio.to_thread(
            requests.Session.put, self, url, data=data, **kwargs
        )

    async def patch(self, url, data=None, **kwargs):
        return await asyncio.to_thread(
            requests.Session.patch, self, url, data=data, **kwargs
        )

    async def delete(self, url, **kwargs):
        return await asyncio.to_thread(requests.Session.delete, self, url, **kwargs)
