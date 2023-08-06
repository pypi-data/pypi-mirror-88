import asyncio
import binascii
import os
from datetime import datetime, timedelta
from typing import Dict

from bricked.server.models.session_model import (
    CreateSessionRequest,
    FetchUserIdRequest,
    SessionModel,
)


class SessionRepositoryInterface(object):
    async def create(self, request: CreateSessionRequest) -> SessionModel:
        raise NotImplementedError

    async def fetch_user_id(self, request: FetchUserIdRequest) -> int:
        raise NotImplementedError


class MemorySessionRepository(SessionRepositoryInterface):
    def __init__(self):
        self._session_store_by_token: Dict[str, SessionModel] = dict()
        self._resource_lock = asyncio.Lock()
        self._next_id = 0

    async def create(self, request: CreateSessionRequest) -> SessionModel:
        async with self._resource_lock:
            now = datetime.now()
            token = bytes(binascii.b2a_hex(os.urandom(request.token_length // 2))).decode("utf-8")
            new_session = SessionModel(
                id=self._next_id,
                user_id=request.user_id,
                token=token,
                created_at=now,
                expires_at=now + timedelta(days=14),
            )
            self._session_store_by_token[new_session.token] = new_session
            self._next_id += 1
        return new_session

    async def fetch_user_id(self, request: FetchUserIdRequest) -> int:
        if request.session_token not in self._session_store_by_token:
            raise ValueError  # TODO: better error message
        now = datetime.now()
        session = self._session_store_by_token[request.session_token]
        if session.expires_at < now:
            raise RuntimeError  # TODO: better error message
        return session.user_id
