import logging
from typing import List, Optional

from aiohttp import web

from bricked.server.ioc_container import IOCContainer
from bricked.server.repositories.repository import Repository
from bricked.server.routes.router import Router
from bricked.server.services.service import Service

LOG = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        ioc_container: IOCContainer,
        router: Router,
        services: List[Service],
        repositories: List[Repository],
    ):
        self.ioc_container = ioc_container
        self.router = router
        self.services = services
        self.app: Optional[web.Application] = None
        self.repositories = repositories

        self.runner: Optional[web.AppRunner] = None

        # Update the IoC Container
        self.ioc_container.update_ioc_container({type(s).__name__: s for s in self.services})
        self.ioc_container.update_ioc_container({type(r).__name__: r for r in self.repositories})

    def create_app(self) -> web.Application:
        self.app = web.Application()
        self.router.bind_routes(self.app)
        return self.app

    async def start(
        self,
        bind_interface: str,
        bind_port: int,
    ):
        _ = self.create_app()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        LOG.info(f"Starting server on http://{bind_interface}:{bind_port}")
        site = web.TCPSite(self.runner, bind_interface, bind_port)
        await site.start()

    async def shutdown(self):
        await self.runner.cleanup()
