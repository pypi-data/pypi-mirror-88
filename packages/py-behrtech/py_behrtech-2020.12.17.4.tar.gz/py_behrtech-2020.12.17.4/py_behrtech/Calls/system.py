import requests

from py_behrtech.exceptions import check_status_code


class System:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def authTicketGet(self) -> str:
        """
        Get ticket information from which you can request an upgrade to a websocket connection at /ws

        :return: Parser object of ticket information
        """

        req = requests.get(url=self.server_address + f"/v2/auth/ticket", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json().get("ticket")
        else:
            check_status_code(req=req)

    def systemEulaGet(self) -> str:
        """
        Gets the end user license agreement

        :return: The end user license agreement
        """

        req = requests.get(url=self.server_address + f"/v2/system/eula", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json().get("EULA")
        else:
            check_status_code(req=req)

    def systemGet(self) -> dict:
        """
        Gets system status information

        :return: Parser object of system status information
        """

        req = requests.get(url=self.server_address + f"/v2/system", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def wsGet(self, access_token: str = None) -> dict:
        """
        Request an upgrade to a websocket connection (Handshake is handled by goland http upgrader)

        :param access_token: Unique token to authenticate to for requesting an upgrade to a websocket connection
        :return: Parser object of a websocket connection upgrade
        """
        if not access_token:
            access_token = self.authTicketGet()

        req = requests.get(url=self.server_address + f"/v2/ws?accessToken={access_token}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)
