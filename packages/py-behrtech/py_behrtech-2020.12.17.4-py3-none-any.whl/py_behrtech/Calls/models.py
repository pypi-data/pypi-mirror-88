import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter
from py_behrtech.Parsers.modelParser import ModelParser


class Models:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def sensorModelsDelete(self):
        pass

    def sensorModelsGet(self, returnCount: int = '', offset: int = '') -> ModelParser:
        """
        Gets information on all registered node models

        :param returnCount: The amount of node models to be requested. (-1 for all)
        :param offset: Node model amount to start the request from
        :return: Parser object of configured node models
        """

        req = requests.get(url=self.server_address + f"/v2/sensormodels" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return ModelParser(req=req)
        else:
            check_status_code(req=req)

    def sensorModelsPost(self):
        pass

    def sensorModelsSensorTypeDelete(self):
        pass

    def sensorModelsSensorTypeGet(self, sensorType: str) -> ModelParser:
        """
        Gets information on a registered node model

        :param sensorType: Unique identifier of the node model to be requested
        :return: Parser object of configured node model
        """

        req = requests.get(url=self.server_address + f"/v2/sensormodels/{sensorType}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return ModelParser(req=req)
        else:
            check_status_code(req=req)

    def sensorModelsSensorTypePost(self):
        pass
