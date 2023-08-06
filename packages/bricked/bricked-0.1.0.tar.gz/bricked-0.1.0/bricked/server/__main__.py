import asyncio
import logging

from bricked.server.application import Application, IOCContainer
from bricked.server.auth.auth_routes import AUTH_ROUTES
from bricked.server.auth.controllers import AUTH_CONTROLLERS
from bricked.server.auth.middleware.auth_middleware import AuthMiddleware
from bricked.server.auth.services.auth_service import AuthService
from bricked.server.controllers.controller import TestController
from bricked.server.middleware.middleware import NullMiddleware
from bricked.server.repositories.repository import MemoryRepository
from bricked.server.repositories.session_repository import MemorySessionRepository
from bricked.server.repositories.user_repository import MemoryUserRepository
from bricked.server.routes.router import Router
from bricked.server.routes.router_middleware import RouterMiddleware
from bricked.server.routes.routes import Method, Route
from bricked.server.services.cookie_service import AiohttpCookieService
from bricked.server.services.service import NullService


def create_app(
    use_auth: bool,
):
    ioc_container = IOCContainer()
    session_repository = MemorySessionRepository()
    user_repository = MemoryUserRepository()
    auth_service = AuthService(
        user_repository,
        session_repository,
    )
    repositories = [
        MemoryRepository(),
        user_repository,
        session_repository,
    ]
    services = [
        NullService(),
        AiohttpCookieService(),
    ]
    if use_auth:
        services.append(auth_service)
    middlewares = [
        NullMiddleware(),
    ]
    if use_auth:
        middlewares.extend(
            [
                AuthMiddleware(),
            ]
        )
    routes = [
        Route(Method.GET, "/", "TestController@index"),
        Route(Method.GET, "/test", "TestController@show"),
        Route(Method.GET, "/middleware", "TestController@apply_middleware").middleware(
            NullMiddleware
        ),
        Route(Method.GET, "/repository", "TestController@repository_incr"),
        Route(Method.GET, "/template", "TestController@render_test"),
    ]
    if use_auth:
        routes.extend(AUTH_ROUTES)
    controllers = [
        TestController(),
    ]
    if use_auth:
        controllers.extend(AUTH_CONTROLLERS)

    return Application(
        ioc_container,
        Router(
            routes,
            RouterMiddleware(middlewares, ioc_container),
            controllers,
            ioc_container,
        ),
        services,
        repositories,
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    app = create_app(use_auth=True)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(app.start("localhost", 8080))
        loop.run_forever()
    finally:
        loop.run_until_complete(app.shutdown())
