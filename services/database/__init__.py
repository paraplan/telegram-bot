from typing import Any

from edgedb import create_async_client


class SingletonClient:
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            cls._client = create_async_client()
        return cls._client


class BaseRepository:
    def __init__(self) -> None:
        self._client = SingletonClient.get_instance()


def get_parameters(locals: dict[str, Any]) -> dict[str, Any]:
    locals.pop("self")
    return locals
