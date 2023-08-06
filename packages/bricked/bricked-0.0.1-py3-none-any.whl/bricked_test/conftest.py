import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from bricked.server.__main__ import create_app


@pytest.fixture
def web_application(
    loop,
    aiohttp_client,
) -> TestClient:
    server = create_app(True)
    app: web.Application = server.create_app()
    return loop.run_until_complete(aiohttp_client(app))
