import os
import asyncio
from functools import partial

from bygfiles.storages.core import Storage
from concurrent.futures import ThreadPoolExecutor


class DiskStorage(Storage):
    def __init__(self, basepath, base_url, loop=None):
        self.base = os.path.realpath(basepath)
        self.base_url = base_url
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.loop = loop or asyncio.get_event_loop()

    async def listdir(self, path):
        fun = partial(os.listdir, path)
        return await self.loop.run_in_executor(self.executor, fun)

    async def remove(self, path):
        fun = partial(os.remove, path)
        return await self.loop.run_in_executor(self.executor, fun)

    async def search(self, namespace, filename, version="latest"):
        basename = os.path.join(self.base, *namespace.split("."))

        try:
            all_files = sorted(await self.listdir(basename))
        except FileNotFoundError:
            return None

        # TODO add regex match for YYYY.MM.DD__<filename>
        filelist = [f for f in all_files if f.endswith(filename)]

        if version != "latest":
            filelist = [f for f in filelist if f.startswith(version)]

        if not filelist:
            return None

        selected_file = filelist[-1]

        # TODO Add url prefix here
        filepath = os.path.join(basename, selected_file)

        return {
            "version": selected_file.split("__")[0],
            "url": f"{self.base_url}{filepath}",
        }

    async def versions(self, namespace, filename):
        basename = os.path.join(self.base, *namespace.split("."))

        all_files = sorted(await self.listdir(basename))

        versionlist = [f.split("__")[0] for f in all_files if f.endswith(filename)]

        return versionlist

    async def store(self, stream, namespace, filename, version):
        basename = os.path.join(self.base, *namespace.split("."))

        try:
            os.makedirs(basename)
        except OSError:
            pass

        filepath = os.path.join(basename, f"{version}__{filename}")

        def write_file():
            with open(filepath, "wb") as fout:
                fout.write(stream.read())

        return await self.loop.run_in_executor(self.executor, write_file)

    async def delete(self, namespace, filename, version):
        basename = os.path.join(self.base, *namespace.split("."))
        filepath = os.path.join(basename, f"{version}__{filename}")

        await self.remove(filepath)
