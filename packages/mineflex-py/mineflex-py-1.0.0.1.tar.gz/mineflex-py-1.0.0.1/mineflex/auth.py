from urllib.parse import urljoin
from requests import Session, codes
from .endpoint import User
from .exceptions import *


class MineflexSession(Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super(MineflexSession, self).__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        request_result = super(MineflexSession, self).request(method, url, *args, **kwargs)

        if request_result.text == "404 page not found":
            raise APIMissingException(request_result.text)

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
            User.login.value,
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
