=======
pyfiles
=======


.. image:: https://img.shields.io/pypi/v/pyfiles.svg
        :target: https://pypi.python.org/pypi/pyfiles

.. image:: https://img.shields.io/travis/jrmi/pyfiles.svg
        :target: https://travis-ci.org/jrmi/pyfiles

.. image:: https://readthedocs.org/projects/pyfiles/badge/?version=latest
        :target: https://pyfiles.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/jrmi/pyfiles/shield.svg
     :target: https://pyup.io/repos/github/jrmi/pyfiles/
     :alt: Updates



A Big file collection manager.

Install
-------

In a virtual env:


.. code-block:: sh

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip wheel
    pip install git+git://github.com/jrmi/pyfiles@master # Or any last commit
    # Then create your setup.py file before using CLI

CLI
---

Create a `settings.py` files where you want to execute the cli with
this configuration for file storage:

.. code-block:: python

    BACKEND = "pyfiles.storages.diskstorage.DiskStorage"

    BACKEND_OPTIONS = {
        "basepath": "/tmp/tmpdir",
        "base_url": "http://localhost:8000"
    }

And for S3:

.. code-block:: python

    BACKEND = "pyfiles.storages.s3storage.S3Storage"

    BACKEND_OPTIONS = {
        "access_key":"<you-S3-access-key>",
        "secret_key":"<you-S3-secret-key>",
        "endpoint_url":"<S3-api-endpoint>",
        "region_name":"<region>",
        "bucket_name":"<bucket name>",

    }

Then to store a file:

.. code-block:: sh

    $ pyfiles store <file path> <file.namespace> <file.name> <version>

`version` should respect the format: YYYY.MM.DD-Rev
or any `semver <https://semver.org/>`_ like X.Y.Z

To list all version of a file:

.. code-block:: sh

    $ pyfiles versions <file.namespace> <file.name>

To search for a file:

.. code-block:: sh

    $ pyfiles search <file.namespace> <file.name> [<version-prefix>]

`version-prefix` can be YYYY or X or YYYY.MM or X.Y or YYYY.MM.DD or X.Y.Z or Latest. Latest by default if missing.

Finnaly to delete a file:

.. code-block:: sh

    $ pyfiles delete <file.namespace> <file.name> <version>

To start the web api server:

.. code-block:: sh

    $ pyfiles serve


Web API
-------

    **GET** on `/search/<namespace>/<filename>[?version=<version>]`

To get file version download link. `Namespace` is a namespace to organise data and `filename` is the file name.
You can optionnaly add a version like `latest` or `<year>` or `<year.month>` or `<major>` or `<major>.<minor>`, ...
You get the latest for the specified version.

    **GET** on `/versions/<namespace>/<filename>`

To show all avaible file versions.

Python API
----------

See pyfiles.storage classes for more informations.

You can use `pyfiles.storage.get_storage(<backend path>, <options>)` to initialize
your storage.

Features
--------

* An API to download files with rich version selection
* List all version of a file
* Can be used for CSV or Geojson files
* File can have version like 2018.01.10-01
* Find file by a part of the version. `2018` or `2018.01`

Roadmap
-------

* Allow authentification with private data
* Handle file diff between versions
* Get the update date of a file to ease caching
* Add a client library and CLI

License
-------

* Free software: MIT license
* Documentation: https://pyfiles.readthedocs.io.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
