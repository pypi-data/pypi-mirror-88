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
            return_list.append(Server(self.session, **server))

        return return_list
