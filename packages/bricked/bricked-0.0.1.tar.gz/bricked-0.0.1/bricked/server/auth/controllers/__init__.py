from bricked.server.auth.controllers.auth_controller import AuthController
from bricked.server.auth.controllers.login_controller import LoginController
from bricked.server.auth.controllers.registration_controller import RegistrationController

AUTH_CONTROLLERS = [
    AuthController(),
    LoginController(),
    RegistrationController(),
]
