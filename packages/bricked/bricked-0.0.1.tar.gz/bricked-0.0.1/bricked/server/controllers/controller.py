import json
import os
from typing import List, Optional, Type

from aiohttp import web
from jinja2 import Environment, FileSystemLoader, select_autoescape

from bricked.server.middleware.middleware import MiddlewareInterface
from bricked.server.repositories.repository import MemoryRepository
from bricked.server.services.service import NullService


class Controller:

    def __init__(
        self,
        middlewares: Optional[List[MiddlewareInterface]] = None,
    ):
        self.middlewares: List[Type[MiddlewareInterface]] = middlewares or list()
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'views',
            'templates',
        )
        self._template_env = Environment(
            loader=FileSystemLoader(searchpath=template_path),
            autoescape=select_autoescape(['html'])
        )

    def text(
        self,
        body: str,
        status_code: int = 200,
    ) -> web.Response:
        return web.Response(
            body=body.encode(),
            status=status_code,
            content_type='text/plain',
        )

    def json(
        self,
        body: dict,
        status_code: int = 200,
    ) -> web.Response:
        return web.Response(
            body=json.dumps(body).encode(),
            status=status_code,
            content_type='application/json',
        )

    async def view(
        self,
        template_path: str,
        status_code: int = 200,
        **kwargs,
    ) -> web.Response:
        # TODO: this should be async
        template = self._template_env.get_template(template_path)
        rendered_template = template.render(kwargs)
        return web.Response(
            body=rendered_template.encode(),
            status=status_code,
            content_type='text/html',
        )

    def redirect(self, path: str):
        return web.HTTPSeeOther(path)


class TestController(Controller):

    async def index(self, request: web.Request):
        return self.json(dict(request.headers))

    async def show(self, null_service: NullService):
        return self.text(null_service.do_something())

    async def apply_middleware(self, injected_middleware_text: str):
        return self.text(injected_middleware_text)

    async def repository_incr(self, memory_repository: MemoryRepository):
        key = 'counter'
        try:
            value = await memory_repository.fetch(key)
            value += 1
            await memory_repository.store(key, value)
        except KeyError:
            value = 1
            await memory_repository.store(key, value)
        return self.json({key: value})

    async def render_test(self):
        return await self.view('index.html', test='this is a test message')
