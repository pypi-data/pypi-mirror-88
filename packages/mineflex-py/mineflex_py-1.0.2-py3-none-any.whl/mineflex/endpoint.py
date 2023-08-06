from enum import Enum

__all__ = (
    "UserEndpoint",
    "VersionEndpoint",
    "ServerEndpoint"
)


class UserEndpoint(Enum):
    login = "/user/login"


class VersionEndpoint(Enum):
    paper = "/server/versions/PAPER/list"
    bukkit = "/server/versions/BUKKIT/list"
    spigot = "/server/versions/SPIGOT/list"
    forge = "/server/versions/FORGE/list"
    fabric = "/server/version/FABRIC/list"


class ServerEndpoint(Enum):
    list = "/server/list"
    logs = "/server/actions/logs/"
    version_endpoint = VersionEndpoint
