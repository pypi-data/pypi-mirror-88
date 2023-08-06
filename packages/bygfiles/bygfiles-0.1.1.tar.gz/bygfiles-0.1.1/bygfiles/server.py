import os

from sanic import Sanic

from sanic.response import json
from sanic.response import stream
from sanic import response
from sanic.exceptions import NotFound
from bygfiles.storages import DiskStorage


def get_app(storage):

    app = Sanic()

    @app.get('/')
    async def home(request):
        return response.html("<h1>Web api started and working. Good luck!</h1>")


    @app.get('/search/<namespace>/<filename>')
    async def search(request, namespace, filename):

        version = request.args.get('version') or 'latest'

        fileinfo = await storage.search(namespace, filename, version)

        return response.json(fileinfo)


    @app.get('/versions/<namespace>/<filename>')
    async def show_versions(request, namespace, filename):

        versions = await storage.versions(namespace, filename)

        return response.json(versions)

    return app

