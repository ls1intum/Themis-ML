import requests
from packaging import version


class AuthRequest:
    headers = {"Content-type": "application/json"}
    cookies = {}

    def __init__(self, token, server):
        assert server[-1] != "/"
        if self.get_artemis_version(server) < version.parse("6.0.0"):
            self.headers["Authorization"] = "Bearer " + token
        else:
            self.cookies = {"jwt": token}
        self.server = server
        self.api_path = self.server + "/api"

    @staticmethod
    def get_artemis_version(server):
        response = requests.get(server)
        if not response.ok:
            raise ConnectionError(f"Connection to artemis server failed: on url {server} with reason {response.reason}, response: {response.text}")
        if "Content-Version" in response.headers:
            return version.parse(response.headers["Content-Version"])
        else:
            raise AttributeError("No Content-Version attribute in response headers")

    def get(self, path, params=None):
        if params is None:
            params = {}
        return requests.get(self.api_path + path, headers=self.headers, cookies=self.cookies, params=params)

    def post(self, path, params=None, body=None):
        if params is None:
            params = {}
        if body is None:
            body = {}
        return requests.post(self.api_path + path, headers=self.headers, cookies=self.cookies, params=params, json=body)

    def put(self, path, params=None, body=None):
        if params is None:
            params = {}
        if body is None:
            body = {}
        return requests.put(self.api_path + path, headers=self.headers, cookies=self.cookies, params=params, json=body)

    def delete(self, path, params=None):
        if params is None:
            params = {}
        return requests.delete(self.api_path + path, headers=self.headers, cookies=self.cookies, params=params)
