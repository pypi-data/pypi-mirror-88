from aiohttp import web

from bricked.server.controllers.controller import Controller


class LoginController(Controller):
    async def show(self):
        return self.text("create login")

    async def store(self, request: web.Request):
        # if model and bcrypt.checkpw(bytes(password, "utf-8"), password_as_bytes):
        return self.text("creating user")
