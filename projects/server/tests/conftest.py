import os

import pytest_asyncio
from orwynn.app import App
from orwynn.boot import Boot
from orwynn.mongo import MongoUtils
from orwynn.tst import Client
from pykit.fcode import FcodeCore
from rxcat import ServerBus


@pytest_asyncio.fixture(autouse=True)
async def autorun():
    os.environ["ORWYNN_MODE"] = "test"
    os.environ["ORWYNN_DEBUG"] = "1"
    os.environ["ORWYNN_ALLOW_CLEAN"] = "1"

    yield

    await Boot.ie().destroy()

    FcodeCore.deflock = False
    FcodeCore.clean_non_decorator_codes()
    await ServerBus.destroy()
    await MongoUtils.destroy()

    Boot.try_discard()
    ServerBus.try_discard()

@pytest_asyncio.fixture
async def app() -> App:
    app = await Boot.create_app()
    return app

@pytest_asyncio.fixture
async def client(app: App, aiohttp_client):
    return Client(await aiohttp_client(app))

@pytest_asyncio.fixture
async def server_bus(app) -> ServerBus:
    return ServerBus.ie()

