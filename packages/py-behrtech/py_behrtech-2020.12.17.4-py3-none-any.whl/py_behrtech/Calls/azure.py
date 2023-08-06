import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter


class Azure:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def azureMappingGet(self, returnCount: int = '', offset: int = '', azureFunctionID: str = '') -> dict:
        """
        Gets information about the requested Azure mappings

        :param returnCount: The amount of Azure mappings to be requested. -1 is ALL
        :param offset: The Azure mapping count to start the Azure mapping data request from
        :param azureFunctionID: Unique Azure function ID
        :return: Detailed information about the requested Azure mappings
        """

        req = requests.get(url=self.server_address + f"/v2/azuremapping" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)
