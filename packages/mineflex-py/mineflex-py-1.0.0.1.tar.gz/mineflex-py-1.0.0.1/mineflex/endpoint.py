from enum import Enum

__all__ = (
    "User",
)


class User(Enum):
    login = "/user/login"


class Server(Enum):
    server_list = "/server/list"
