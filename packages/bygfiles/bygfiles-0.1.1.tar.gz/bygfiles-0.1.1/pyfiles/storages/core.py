import asyncio
import aiohttp
from contextlib import contextmanager
import urllib.request
import sys

if sys.version_info >= (3, 7):
    from contextlib import asynccontextmanager
else:
    asynccontextmanager = lambda x: x


class Storage:  # TODO necessary ?
    async def search(self, namespace, filename, version):
        raise NotImplementedError()

    async def versions(self, namespace, filename):
        raise NotImplementedError()

    async def store(self, stream, namespace, filename, version):
        raise NotImplementedError()

    async def delete(self, stream, namespace, filename):
        raise NotImplementedError()

    @asynccontextmanager
    async def open(self, namespace, filename, version="latest"):
        result = self.search_sync(namespace, filename, version)
        url = result["url"]

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                yield resp.context

    @contextmanager
    def open_sync(self, namespace, filename, version="latest"):
        result = self.search_sync(namespace, filename, version)
        url = result["url"]

        with urllib.request.urlopen(url) as resp:
            yield resp

    # Synced version of previous methods
    def search_sync(self, namespace, filename, version="latest"):
        return asyncio.get_event_loop().run_until_complete(
            self.search(namespace, filename, version)
        )

    def versions_sync(self, namespace, filename):
        return asyncio.get_event_loop().run_until_complete(
            self.versions(namespace, filename)
        )

    def store_sync(self, stream, namespace, filename, version):
        return asyncio.get_event_loop().run_until_complete(
            self.store(stream, namespace, filename, version)
        )

    def delete_sync(self, namespace, filename, version):
        return asyncio.get_event_loop().run_until_complete(
            self.delete(namespace, filename, version)
        )
