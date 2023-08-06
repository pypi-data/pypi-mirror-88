import logging
from typing import Any, Dict, List, Type

import aiohttp
from aiohttp import web

from bricked.server.auth.middleware.auth_middleware import UserNotAuthenticatedException
from bricked.server.auth.middleware.exception import MiddlewareException
from bricked.server.ioc_container import IOCContainer
from bricked.server.middleware.middleware import MiddlewareInterface

LOGGER = logging.getLogger(__name__)


class RouterMiddleware:
    def __init__(
        self,
        middlewares: List[MiddlewareInterface],
        ioc_container: IOCContainer,
    ):
        self.middlewares = middlewares
        self.ioc_container = ioc_container
        self._middlewares_by_name = {type(m).__name__: m for m in self.middlewares}

    async def apply_middleware(
        self,
        request: web.Request,
        controller_middleware: List[Type[MiddlewareInterface]],
        route_middleware: List[Type[MiddlewareInterface]],
    ) -> Dict[Type, Any]:
        all_middleware = controller_middleware.copy()
        all_middleware.extend(route_middleware.copy())
        middleware_results = {}
        for middleware in route_middleware:
            middleware_name = middleware.__name__
            if middleware_name not in self._middlewares_by_name:
                raise ValueError  # TODO: better error message
            middleware_provider = self._middlewares_by_name[middleware_name]
            middleware_args = self.ioc_container.inject_dependencies(
                middleware_provider.apply,
                request,
                dict(),
            )
            try:
                result = await middleware_provider.apply(*middleware_args)
            except UserNotAuthenticatedException:
                raise aiohttp.web.HTTPFound("/login")
            except MiddlewareException as e:
                LOGGER.warning(e)
            if result is not None:
                middleware_results[type(result).__name__] = result
        return middleware_results
