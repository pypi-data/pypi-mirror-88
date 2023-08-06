from bricked.server.auth.middleware.auth_middleware import AuthMiddleware
from bricked.server.routes.routes import Method, Route

AUTH_ROUTES = [
    # Login
    Route(Method.GET, '/login', 'LoginController@show').name("login"),
    Route(Method.POST, '/login', 'LoginController@store'),
    # Logout
    Route(Method.GET, '/logout', 'LoginController@logout').name("logout"),
    # Register
    Route(Method.GET, "/register", 'RegistrationController@show').name("register"),
    Route(Method.POST, "/register", 'RegistrationController@store'),
    # Registered user area
    Route(Method.GET, "/home", 'AuthController@show').name("home").middleware(AuthMiddleware),
    # TODO: email verification
    # TODO: password reset
]
