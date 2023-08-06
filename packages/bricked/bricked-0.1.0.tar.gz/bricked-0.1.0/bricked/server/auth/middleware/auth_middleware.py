import logging
from typing import Optional

from aiohttp import web

from bricked.server.auth.constants import COOKIE_KEY
from bricked.server.auth.middleware.exception import MiddlewareException
from bricked.server.auth.services.auth_service import AuthService
from bricked.server.middleware.middleware import MiddlewareInterface
from bricked.server.models.session_model import FetchUserIdRequest
from bricked.server.models.user_model import UserModel
from bricked.server.services.cookie_service import AiohttpCookieService

LOGGER = logging.getLogger(__name__)


class UserNotAuthenticatedException(MiddlewareException):
    pass


class AuthMiddleware(MiddlewareInterface):
    async def apply(
        self,
        request: web.Request,
        auth_service: AuthService,
        aiohttp_cookie_service: AiohttpCookieService,
    ) -> Optional[UserModel]:
        session_id = await aiohttp_cookie_service.get(request, COOKIE_KEY)
        if session_id is None:
            LOGGER.info(f"No user found in request for {request.path}")
            raise UserNotAuthenticatedException
        try:
            return await auth_service.user_from_session(FetchUserIdRequest(session_id))
        except Exception as e:
            raise UserNotAuthenticatedException
