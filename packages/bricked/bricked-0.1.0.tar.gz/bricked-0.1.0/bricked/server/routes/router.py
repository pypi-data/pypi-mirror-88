import logging
from typing import Any, Awaitable, Callable, List, Tuple, Type

from aiohttp import web

from bricked.server.controllers.controller import Controller
from bricked.server.ioc_container import IOCContainer
from bricked.server.middleware.middleware import MiddlewareInterface
from bricked.server.routes.router_middleware import RouterMiddleware
from bricked.server.routes.routes import Method, Route

CONTROLLER_METHOD_TYPE = Callable[[List[Any]], Awaitable[web.Response]]

LOG = logging.getLogger(__name__)


class Router:
    def __init__(
        self,
        routes: List[Route],
        router_middleware: RouterMiddleware,
        controllers: List[Controller],
        ioc_container: IOCContainer,
    ):
        self.routes = routes
        self.router_middleware = router_middleware
        self.controllers = controllers
        self.ioc_container = ioc_container
        self._controllers_by_name = {type(c).__name__: c for c in self.controllers}

    def _convert_route(self, route: Route) -> Any:
        http_method_by_route_method = {
            Method.GET: web.get,
            Method.POST: web.post,
            Method.DELETE: web.delete,
            Method.HEAD: web.head,
            Method.PATCH: web.patch,
        }
        method = http_method_by_route_method.get(route.method)
        if method is None:
            raise NotImplementedError(route.method)
        return method(
            route.path,
            lambda request: self._handle_routing_decorator(
                route.controller_method_name,
                route.applied_middlewares,
                request,
            ),
        )

    async def _resolve_controller_method(
        self,
        controller_method_name: str,
    ) -> Tuple[Controller, CONTROLLER_METHOD_TYPE]:
        split_controller_method_name = controller_method_name.split("@")
        if len(split_controller_method_name) != 2:
            raise ValueError  # TODO: better error message
        controller_name, method_name = split_controller_method_name
        if controller_name not in self._controllers_by_name:
            raise ValueError  # TODO: better error message
        controller = self._controllers_by_name[controller_name]
        if not hasattr(controller, method_name):
            raise ValueError  # TODO: better error message
        return controller, getattr(controller, method_name)

    async def _handle_routing_decorator(
        self,
        controller_method_name: str,
        route_middleware: List[Type[MiddlewareInterface]],
        request: web.Request,
    ) -> web.Response:
        controller, method = await self._resolve_controller_method(controller_method_name)
        middleware_results = await self.router_middleware.apply_middleware(
            request, controller.middlewares, route_middleware
        )
        controller_method_args: List[Any] = self.ioc_container.inject_dependencies(
            method,
            request,
            middleware_results,
        )
        return await method(*controller_method_args)

    def bind_routes(self, app: web.Application):
        LOG.debug(f"Binding {len(self.routes)} routers")
        app.add_routes([self._convert_route(route) for route in self.routes])
