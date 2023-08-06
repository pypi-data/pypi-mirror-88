import requests

from py_behrtech.parsers import Parser
from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter


class Messages:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def messagesDelete(self, deleteAll: bool = False) -> dict:
        """
        Deletes all messages from the gateways

        :param deleteAll: Verifies deletion was on purpose
        :return: Deletion status information
        """

        req = requests.delete(url=self.server_address + f"/v2/messages?deleteAll={deleteAll}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def messagesGet(self, returnCount: int = '', offset: int = '', epEui: str = '', epName: str = '', bsEui: str = '',
                    sensorType: str = '') -> Parser:
        """
        Returns messages from the gateway.

        :param returnCount: The amount of messages to be requested. (-1 for all)
        :param offset: Message number to start the request from
        :param epEui: The unique epEui number of the node to be requested
        :param epName: Endpoint of which messages to be requested. Name is not unique
        :param bsEui: The bsEui number of the messages to be requested
        :param sensorType: The node type of a node to be requested
        :return: Parser object of requested messages
        """

        req = requests.get(url=self.server_address + f"/v2/messages" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        else:
            check_status_code(req=req)

    def messagesPost(self):
        pass
