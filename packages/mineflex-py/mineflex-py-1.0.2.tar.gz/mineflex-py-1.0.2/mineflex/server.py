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
    def __init__(self, session,
                 id: int,
                 user_id: int,
                 ram: int,
                 protocol_version: int,
                 protocol_name: str,
                 domain: str,
                 state: str,
                 host: int,
                 datacenter: DataCenter or str,
                 description: str,
                 server_type: ServerType or str,
                 max_player: int):

        for (key, value) in locals().items():
            setattr(self, key, value)

        self.session = session

        if not isinstance(self.datacenter, DataCenter):
            self.datacenter = DataCenter[self.datacenter]
        if not isinstance(self.server_type, ServerType):
            self.server_type = ServerType[self.server_type.lower()]

        self.protocol = self.get_protocol()

    def get_logs(self):
        return self.session.get(ServerEndpoint.logs.value + str(self.id)).json()

    def get_protocol(self):
        all_ver = self.session.get(
            ServerEndpoint.version_endpoint.value[self.server_type.name].value
        ).json()

        for ver in all_ver:
            if ver['protocolName'] == self.protocol_name:
                return Protocol(
                    ver['protocolName'], ver['protocolVersions'], ver['title'], MineflexImage(ver['imageUrl']),
                    ServerType[ver['serverType'].lower()], build=ver['build']
                )

