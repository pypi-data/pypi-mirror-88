from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateSessionRequest:
    user_id: int
    token_length: int


@dataclass
class SessionModel:
    id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime


@dataclass
class FetchUserIdRequest:
    session_token: str
