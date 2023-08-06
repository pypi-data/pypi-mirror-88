from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateUserRequest:
    user_name: str
    password: str
    confirmed_password: str

    def __repr__(self):
        return f"CreateUserRequest(user_name={self.user_name})"


@dataclass
class UserModel:
    id: int
    user_name: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
