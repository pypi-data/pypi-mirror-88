import asyncio
from datetime import datetime

import bcrypt

from bricked.server.models.user_model import CreateUserRequest, UserModel
from bricked.server.repositories.repository import Repository


class UserRepositoryInterface(Repository):
    async def create(self, request: CreateUserRequest) -> UserModel:
        raise NotImplementedError

    async def find_by_id(self, user_id: int) -> UserModel:
        raise NotImplementedError


class MemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self._store = {}
        self._next_user_id = 0
        self._resource_lock = asyncio.Lock()

    async def create(self, request: CreateUserRequest) -> UserModel:
        if request.password != request.confirmed_password:
            raise ValueError  # TODO: better error message
        async with self._resource_lock:
            now = datetime.now()
            new_model = UserModel(
                id=self._next_user_id,
                user_name=request.user_name,
                hashed_password=bytes(
                    bcrypt.hashpw(bytes(request.password, "utf-8"), bcrypt.gensalt())
                ).decode("utf-8"),
                created_at=now,
                updated_at=now,
            )
            self._next_user_id += 1
            self._store[new_model.id] = new_model
        return new_model

    async def find_by_id(self, user_id: int) -> UserModel:
        if user_id not in self._store:
            raise ValueError  # TODO: better error message
        return self._store[user_id]
