from aiohttp import ClientResponse
from aiohttp.test_utils import TestClient


async def test_index_route(web_application: TestClient):
    response: ClientResponse = await web_application.get('/')
    assert response.status == 200
    response_json = await response.json()
    assert "Host" in response_json


async def test_null_service(web_application: TestClient):
    response: ClientResponse = await web_application.get('/test')
    assert response.status == 200
    content = (await response.read()).decode()
    assert "nothing" in content


async def test_null_middleware(web_application: TestClient):
    response: ClientResponse = await web_application.get('/middleware')
    assert response.status == 200
    content = (await response.read()).decode()
    assert "Hello from NullMiddleware" in content


async def test_repository_injection(web_application: TestClient):
    for count in range(1, 10):
        response: ClientResponse = await web_application.get('/repository')
        assert response.status == 200
        counter = (await response.json())['counter']
        assert counter == count


async def test_render_content(web_application: TestClient):
    response: ClientResponse = await web_application.get('/template')
    assert response.status == 200
    content = (await response.read()).decode()
    assert "<h1>" in content
    assert "</h1>" in content
