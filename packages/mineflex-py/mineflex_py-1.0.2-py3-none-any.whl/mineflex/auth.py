from urllib.parse import urljoin
from requests import Session, codes
from .endpoint import UserEndpoint, ServerEndpoint
from .server import Server
from .exceptions import *

failed_reference = {
    "404 page not found": APIMissingException,
    "Forbidden": InsufficientPermissions
}


class MineflexSession(Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super(MineflexSession, self).__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        request_result = super(MineflexSession, self).request(method, url, *args, **kwargs)

        error_reference = failed_reference.get(request_result.text)

        if error_reference:
            raise error_reference(request_result.text)

        return request_result


class Mineflex:
    def __init__(self, email: str, password: str,
                 base_url: str = "https://mineflex.io/"):
        self.email = email
        self.password = password

        self.logged = False

        self.session = MineflexSession(base_url)

    def login(self):
        attempt = self.session.post(
            UserEndpoint.login.value,
            json={
                "email": self.email,
                "password": self.password
            }
        )
        attempt_json = attempt.json()

        if not attempt_json.get("Authorized"):
            raise InvalidCredentials(attempt_json.get("Message"))

        self.logged = True
        return True

    def get_all_server(self):
        all_server = self.session.get(ServerEndpoint.list.value).json()
        return_list = []

        for server in all_server:
            return_list.append(
                Server(self.session, id=server.get("id"), user_id=server.get("userId"), ram=server.get("ram"), protocol_version=server.get("protocolVersion"),
                       protocol_name=server.get("protocolName"),
                       domain=server.get("domain"), state=server.get("state"), host=server.get("host"), datacenter=server.get("datacenter"), max_player=server.get("maxPlayers"),
                       description=server.get("description"), server_type=server.get("serverType"))
            )
        # session, id: int, user_id: int, ram: int, protocol: Protocol, domain: str, state: str, host: int,
        # datacenter: DataCenter, description: str, server_type: ServerType, image: MineflexImage
        # {"id": 244, "userId": 191, "ram": "5G", "protocolVersion": 753, "protocolName": "1.16.3",
        #  "domain": "vibingcrusaders.us1.mineflex.io", "state": "STOPPED", "host": 1, "datacenter": "", "maxPlayers": 10,
        #  "description": "just vibing", "serverType": "PAPER", "imageId": 18}

        return return_list
