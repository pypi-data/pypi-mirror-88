import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter
from py_behrtech.Parsers.nodeParser import NodeParser


class Nodes:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def nodesEpEuiGet(self, epEui: str) -> NodeParser:
        """
        Gets information on a configured node with the matching epEui

        :param epEui: The unique epEui of the node to be requested
        :return: Information on the requested node
        """

        req = requests.get(url=self.server_address + f"/v2/nodes/{epEui}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return NodeParser(req=req)
        else:
            check_status_code(req=req)

    def nodesEpEuiTxDataGet(self, epEui: str) -> dict:
        """
        Gets downlink information on a configured node with the matching epEui

        :param epEui: Unique epEui of the node to be requested
        :return: Information on the requested node
        """

        req = requests.get(url=self.server_address + f"/v2/nodes/{epEui}/txdata", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def nodesEpEuiTxDataIdGet(self, epEui: str, messageId: str) -> dict:
        """
        Gets a specific requested downlink message

        :param epEui: Unique epEui of the node to request downlink message for
        :param messageId: Unique ID of the message to be requested
        :return: Message information of the requested node
        """

        req = requests.get(url=self.server_address + f"/v2/nodes/{epEui}/txdata/{messageId}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def nodesGet(self, returnCount: int = '', offset: int = '', sensor_type: str = '') -> NodeParser:
        """
        Gets information on all configured nodes

        :param returnCount: The amount of nodes to be requested. (-1 for all)
        :param offset: Node amount to start the request from
        :param sensor_type: Node type to be requested
        :return: Parser object of configured nodes
        """

        req = requests.get(url=self.server_address + f"/v2/nodes" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return NodeParser(req=req)
        else:
            check_status_code(req=req)
