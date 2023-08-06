import logging

from bricked.server.models.session_model import (
    CreateSessionRequest, FetchUserIdRequest,
    SessionModel,
)
from bricked.server.models.user_model import CreateUserRequest, UserModel
from bricked.server.repositories.session_repository import SessionRepositoryInterface
from bricked.server.repositories.user_repository import UserRepositoryInterface
from bricked.server.services.service import Service

DEFAULT_TOKEN_LENGTH = 30

LOG = logging.getLogger(__name__)


class AuthService(Service):
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        session_repository: SessionRepositoryInterface,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    async def create_user(self, request: CreateUserRequest) -> SessionModel:
        """
        Create a new User and Session for the user, return the session token.
        """
        LOG.info(f"Creating new user {request}")
        new_user = await self.user_repository.create(request)
        session = await self.session_repository.create(CreateSessionRequest(
            new_user.id,
            DEFAULT_TOKEN_LENGTH,
        ))
        return session

    async def user_from_session(self, request: FetchUserIdRequest) -> UserModel:
        """
        Fetch the user from the session.
        """
        user_id = await self.session_repository.fetch_user_id(request)
        return await self.user_repository.find_by_id(user_id)
