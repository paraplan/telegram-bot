from typing import Any

from edgedb import create_async_client


def read_query_file(filename: str) -> str:
    with open(f"database/queries/{filename}", "r") as file:
        return file.read()


class SingletonClient:
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            cls._client = create_async_client()
        return cls._client


def get_parameters(locals: dict[str, Any]) -> dict[str, Any]:
    locals.pop("self")
    return locals
