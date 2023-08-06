from typing import Any


class Repository:
    pass


class MemoryRepository(Repository):
    def __init__(self):
        self._store = {}

    async def store(self, key: str, value: Any):
        self._store[key] = value

    async def fetch(self, key: str) -> Any:
        return self._store[key]


from bricked.server.repositories.user_repository import MemoryUserRepository

REPOSITORIES = [
    MemoryRepository(),
    MemoryUserRepository(),
]
