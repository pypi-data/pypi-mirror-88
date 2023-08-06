from enum import Enum
from .endpoint import ServerEndpoint


class MineflexImage:
    def __init__(self, URL: str):
        self.URL = URL


class DataCenter(Enum):
    BHS = "US1"


class ServerState(Enum):
    stopped = "STOPPED"
    stopping = "STOPPING"
    running = "RUNNING"


class ServerType(Enum):
    paper = "PAPER"


class Protocol:
    def __init__(self, name: str, version: int, title: str, image: MineflexImage,
                 server_type: ServerType, build: int):
        self.name = name
        self.version = version
        self.title = title
        self.image = image
        self.server_type = server_type
        self.build = build


class Server:
    # id: int, user_id: int, ram: int, protocol: Protocol, domain: str, state: str, host: int,
    #                  datacenter: DataCenter, description: str, server_type: ServerType, image: MineflexImage
    def __init__(self, session, **kwargs):
        self.session = session

        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def get_logs(self):
        return self.session.get(ServerEndpoint.logs.value + str(self.id)).json()

    def get_protocol(self):
        all_ver = self.session.get(
            ServerEndpoint.version_endpoint[self.server_type.name].value
        ).json()

        for ver in all_ver:
            if ver['protocolName'] == self.protocol.name:
                return Protocol(
                    ver['protocolName'], ver['protocolVersions'], ver['title'], MineflexImage(ver['imageUrl']),
                    ServerType[ver['server_type'].lower()], build=ver['build']
                )
