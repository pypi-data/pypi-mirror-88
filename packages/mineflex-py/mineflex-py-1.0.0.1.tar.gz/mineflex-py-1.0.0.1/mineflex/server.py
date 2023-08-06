from enum import Enum


class Protocol:
    def __init__(self, version, name):
        self.version = version
        self.name = name


class MineflexImage:
    def __init__(self, ID:str, URL:str):
        self.ID = ID
        self.URL = URL


class DataCenter:
    BHS = "US1"


class ServerType:
    PAPER = "PAPER"


class Server:
    # id: int, user_id: int, ram: int, protocol: Protocol, domain: str, state: str, host: int,
    #                  datacenter: DataCenter, description: str, server_type: ServerType, image: MineflexImage
    def __init__(self, session, **kwargs):
        self.session = session
        for (key, value) in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

        # [{"id": 244, "userId": 191, "ram": "5G", "protocolVersion": 753, "protocolName": "1.16.3",
        #   "domain": "vibingcrusaders.us1.mineflex.io", "state": "STOPPED", "host": 1, "datacenter": "BHS",
        #   "maxPlayers": 10, "description": "just vibing", "serverType": "PAPER", "imageId": 0}]

    def