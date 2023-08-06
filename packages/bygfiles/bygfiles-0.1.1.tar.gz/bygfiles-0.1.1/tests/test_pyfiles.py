#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyfiles` package."""

import shutil
import io
import pytest
import tempfile
import asyncio


from pyfiles.storages import get_storage


def run(fun):
    return asyncio.get_event_loop().run_until_complete(fun)


DATA1 = b"The answer is 42"
DATA2 = b"The answer is 43"
DATA3 = b"The answer is 44"
DATA4 = b"The answer is 45"


@pytest.fixture
def disk_storage():
    """Disk storage"""
    backend = "pyfiles.storages.diskstorage.DiskStorage"

    storage_path = tempfile.mkdtemp()

    options = {"basepath": storage_path, "base_url": "file://"}

    yield get_storage(backend, options)

    shutil.rmtree(storage_path)


def test_disk_storage(disk_storage):
    """Test disk storage"""

    result = disk_storage.search_sync("test.name", "data.csv", "10.3")
    assert result is None

    data1 = io.BytesIO(DATA1)
    data2 = io.BytesIO(DATA2)
    data3 = io.BytesIO(DATA3)
    data4 = io.BytesIO(DATA4)

    disk_storage.store_sync(data1, "test.name", "data.csv", "10.3.2")
    disk_storage.store_sync(data2, "test.name", "data.csv", "10.3.1")
    disk_storage.store_sync(data3, "test.name", "data.csv", "10.4.4")
    disk_storage.store_sync(data4, "test.name", "data.csv", "11.4.2")

    result = disk_storage.search_sync("test.name", "data.csv", "10.3")

    assert result["version"] == "10.3.2"
    print(result)

    with disk_storage.open_sync("test.name", "data.csv", "10.3") as f:
        content = f.read()

    assert content == DATA1

    with disk_storage.open_sync("test.name", "data.csv", "10.4") as f:
        content = f.read()

    assert content == DATA3

    # Test latest
    with disk_storage.open_sync("test.name", "data.csv") as f:
        content = f.read()

    assert content == DATA4

    disk_storage.delete_sync("test.name", "data.csv", "11.4.2")

    result = disk_storage.search_sync("test.name", "data.csv")

    assert result["version"] == "10.4.4"

    result = disk_storage.versions_sync("test.name", "data.csv")

    assert result == ["10.3.1", "10.3.2", "10.4.4"]
