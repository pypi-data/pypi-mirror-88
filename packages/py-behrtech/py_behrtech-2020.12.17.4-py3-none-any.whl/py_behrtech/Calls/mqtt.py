import requests

from py_behrtech.exceptions import check_status_code
from py_behrtech.Calls.functions import buildParameter


class Mqtt:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def brokerBrokerIDGet(self, brokerID: str) -> dict:
        """
        Gets information about the requested MQTT broker

        :param brokerID: Unique broker ID
        :return: Detailed information about the requested MQTT broker
        """

        req = requests.get(url=self.server_address + f"/v2/broker/{brokerID}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def brokerGet(self, returnCount: int = '', offset: int = '') -> dict:
        """
        Gets information about the requested MQTT brokers

        :param returnCount: The amount of MQTT Brokers to be requested. -1 is ALL
        :param offset: The MQTT broker count to start the MQTT Broker data request from
        :return: Detailed information about the requested MQTT brokers
        """

        req = requests.get(url=self.server_address + f"/v2/broker" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def mqttMappingGet(self, returnCount: int = '', offset: int = '') -> dict:
        """
        Gets information about the requested MQTT mappings

        :param returnCount: The amount of MQTT mappings to be requested. -1 is ALL
        :param offset: The MQTT mappings count to start the MQTT mappings data request from
        :return: Detailed information about the requested MQTT mappings
        """

        req = requests.get(url=self.server_address + f"/v2/mqttmapping" + buildParameter(params=vars()), verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def mqttMappingMappingIDGet(self, mappingID: str) -> dict:
        """
        Gets information about the requested MQTT mapping

        :param mappingID: Unique mapping ID
        :return: Detailed information about the requested MQTT mapping
        """

        req = requests.get(url=self.server_address + f"/v2/mqttmapping/{mappingID}",
                           verify=False, headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)
