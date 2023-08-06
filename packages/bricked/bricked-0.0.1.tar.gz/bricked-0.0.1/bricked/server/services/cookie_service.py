import logging
from datetime import datetime

from aiohttp import web

LOG = logging.getLogger(__name__)


class AiohttpCookieService:
    COOKIE_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

    async def get(
        self,
        request: web.Request,
        key: str,
    ) -> str:
        return request.cookies[key]

    async def set(
        self,
        response: web.Response,
        key: str,
        value: str,
        expiry: datetime,
    ):
        response.set_cookie(
            key,
            value,
            expires=expiry.strftime(self.COOKIE_DATE_FORMAT),
        )
