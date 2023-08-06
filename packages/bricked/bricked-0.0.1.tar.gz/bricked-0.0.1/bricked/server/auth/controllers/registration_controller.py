from aiohttp import web

from bricked.server.auth.constants import COOKIE_KEY
from bricked.server.auth.services.auth_service import AuthService
from bricked.server.controllers.controller import Controller
from bricked.server.models.user_model import CreateUserRequest
from bricked.server.services.cookie_service import AiohttpCookieService


class RegistrationController(Controller):

    async def show(self):
        return await self.view('auth/register.html')

    async def store(
        self, request: web.Request,
        auth_service: AuthService,
        cookie_service: AiohttpCookieService,
    ):
        post_body = await request.post()
        user_request = CreateUserRequest(
            user_name=post_body['username'],
            password=post_body['password'],
            confirmed_password=post_body['password'],  # TODO
        )
        session = await auth_service.create_user(user_request)
        response = self.redirect('/home')
        await cookie_service.set(response, COOKIE_KEY, session.token, session.expires_at)
        return response
