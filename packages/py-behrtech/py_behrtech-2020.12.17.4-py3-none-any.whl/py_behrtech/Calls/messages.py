import requests

from py_behrtech.Parsers.messageParser import MessageParser
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
                    sensorType: str = '', start: int = '', end: int = '') -> MessageParser:
        """
        Returns messages from the gateway.

        :param returnCount: Amount of messages to be requested. (-1 for all)
        :param offset: Message number to start the request from
        :param epEui: Unique epEui number of the node to be requested
        :param epName: Endpoint of which messages to be requested. Name is not unique
        :param bsEui: bsEui number of the messages to be requested
        :param sensorType: node type of node to be requested
        :param start: Date to start request from. Unix timestamp in seconds
        :param end: Date to end request from start date. Unix timestamp in seconds
        :return: Parser object of requested messages

        Example:
            Start: int(datetime.datetime(year=2020, month=1, day=1).timestamp())
            End: int(datetime.datetime(year=2020, month=2, day=1).timestamp())
        """

        req = requests.get(url=self.server_address + f"/v2/messages" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return MessageParser(req=req)
        else:
            check_status_code(req=req)

    def messagesPost(self):
        pass
