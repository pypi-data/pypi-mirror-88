from enum import Enum
from typing import List, Optional, Type

from bricked.server.middleware.middleware import MiddlewareInterface


class Method(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"


class Route:

    def __init__(
        self,
        method: Method,
        path: str,
        controller_method_name: str,
    ):
        self.method = method
        self.path = path
        self.controller_method_name = controller_method_name
        self.route_name: Optional[str] = None
        self.applied_middlewares: List[Type[MiddlewareInterface]] = list()

    def name(self, route_name: str):
        if self.route_name is not None:
            raise RuntimeError(f"Route already has name, {self.route_name}")
        self.route_name = route_name
        return self  # chain calls

    def middleware(self, *middlewares):
        for middleware in middlewares:
            if not issubclass(middleware, MiddlewareInterface):
                raise ValueError  # TODO: better error message
            if middleware not in self.applied_middlewares:
                self.applied_middlewares.append(middleware)
        return self  # chain calls
