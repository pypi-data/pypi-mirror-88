import logging
from typing import Any, Optional

from aiohttp import web

LOG = logging.getLogger(__name__)


class MiddlewareInterface:

    async def apply(self, *args, **kwargs) -> Optional[Any]:
        raise NotImplementedError


class NullMiddleware(MiddlewareInterface):

    async def apply(self, request: web.Request) -> str:
        return "Hello from NullMiddleware"
