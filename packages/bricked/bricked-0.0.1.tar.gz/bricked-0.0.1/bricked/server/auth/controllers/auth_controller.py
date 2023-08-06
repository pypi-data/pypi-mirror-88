from bricked.server.controllers.controller import Controller
from bricked.server.models.user_model import UserModel


class AuthController(Controller):

    async def show(self, user: UserModel):
        print("AuthController@show: user: '{}'".format(user))  # DEBUG
        return self.text('home page')
