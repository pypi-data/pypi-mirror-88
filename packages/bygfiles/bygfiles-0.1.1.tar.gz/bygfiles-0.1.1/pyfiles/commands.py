import os
import sys
import pyfiles
import importlib

from pyfiles.conf import settings
from pyfiles.storages import get_storage

# TODO: remove below if statement asap. This is a workaround for a bug in begins
# TODO: which provokes an exception when calling pypeman without parameters.
# TODO: more info at https://github.com/aliles/begins/issues/48

if len(sys.argv) == 1:
    sys.argv.append("-h")

CURRENT_DIR = os.getcwd()

# Keep this import
sys.path.insert(0, CURRENT_DIR)

import asyncio  # noqa
import begin


@begin.subcommand  # noqa: F722
def search(namespace: "file namespace", filename: "filename", revision="latest"):
    """ Search for an entry """

    loop = asyncio.get_event_loop()
    settings.init_settings()

    storage = get_storage(settings.BACKEND, settings.BACKEND_OPTIONS)

    result = loop.run_until_complete(
        storage.search(namespace=namespace, filename=filename, version=revision)
    )

    print(
        f"""url: {result['url']}
version: {result['version']}"""
    )


@begin.subcommand  # noqa: F722
def versions(namespace: "file namespace", filename: "filename"):
    """ Show available versions for a specific file """

    loop = asyncio.get_event_loop()
    settings.init_settings()

    storage = get_storage(settings.BACKEND, settings.BACKEND_OPTIONS)

    result = loop.run_until_complete(
        storage.versions(namespace=namespace, filename=filename)
    )

    print("Avaible version(s) for this file:")
    [print(v) for v in result]


@begin.subcommand  # noqa: F722
def store(
    path: "file path to upload",
    namespace: "Namespace to store",
    filename: "File name to store",
    revision: "File version",
):
    """ Store or update file in storage """

    loop = asyncio.get_event_loop()
    settings.init_settings()

    storage = get_storage(settings.BACKEND, settings.BACKEND_OPTIONS)

    with open(path, "rb") as fin:
        print("Storage in progress...")
        loop.run_until_complete(
            storage.store(
                stream=fin, namespace=namespace, filename=filename, version=revision
            )
        )

    print("Stored!")


@begin.subcommand  # noqa: F722
def delete(
    namespace: "Namespace to store",
    filename: "File name to delete",
    revision: "File version",
):
    """ Delete file from storage """

    loop = asyncio.get_event_loop()
    settings.init_settings()

    storage = get_storage(settings.BACKEND, settings.BACKEND_OPTIONS)

    print("Delete in progress...")
    loop.run_until_complete(
        storage.delete(namespace=namespace, filename=filename, version=revision)
    )

    print("Deleted!")


@begin.subcommand  # noqa: F722
def serve(host: "Web api host" = "localhost", port: "Listen port" = 8080):
    from pyfiles.server import get_app

    loop = asyncio.get_event_loop()
    settings.init_settings()

    storage = get_storage(settings.BACKEND, settings.BACKEND_OPTIONS)

    app = get_app(storage)
    import webbrowser

    webbrowser.open(f"http://{host}:{port}")
    app.run(host=host, port=port)


@begin.start  # noqa: F722
def run(version=False):
    """ Pyfiles allow you to easilly store and share data files """

    if version:
        print(pyfiles.__version__)
        sys.exit(0)
