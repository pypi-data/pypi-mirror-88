
import os
import json

from typing import Union
from requests import Response
from py_behrtech.Parsers.defaults import Defaults


class NodeParser(Defaults):
    # TODO: setup for downlink messages from nodesEpEuiTxDataGet and nodesEpEuiTxDataIdGet when bi-directional is setup

    def __init__(self, req: Response):

        def getCount():
            count = json.loads(self.data).get('count')
            return count if count is not None else 1

        Defaults.__init__(self)
        self.response: Response = req
        self.data: str = req.text
        self.count = getCount()
        self.nodes = json.loads(self.data).get('nodes')

    def getEpEui(self) -> Union[list, dict]:
        """
        Gets the epEui of nodes

        :return: The epEui of nodes
        """

        if self.nodes:
            return [{'name': x.get('name'), 'epEui': x.get('epEui')} for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'epEui': data.get('epEui')}

    def getType(self) -> Union[list, dict]:
        """
        Gets the type of nodes

        :return: The type of nodes
        """

        if self.nodes:
            return [{'name': x.get('name'), 'type': x.get('type')} for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'type': data.get('type')}

    def getMapping(self) -> Union[list, dict]:
        """
        Gets the mapping of nodes

        :return: The mapping of nodes
        """

        if self.nodes:
            return [{'name': x.get('name'), 'mapping': x.get('mapping')} for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'mapping': data.get('mapping')}

    def getAzureMapping(self) -> Union[list, dict]:
        """
        Gets the Azure mapping of nodes

        :return: The Azure mapping of nodes
        """

        if self.nodes:
            return [{'name': x.get('name'), 'Azure Mapping': x.get('mapping').get('azureMapping')} for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'Azure Mapping': data.get('mapping').get('azureMapping')}

    def getMqttMapping(self) -> Union[list, dict]:
        """
        Gets the MQTT mapping of nodes

        :return: The MQTT mapping of nodes
        """

        if self.nodes:
            return [{'name': x.get('name'), 'MQTT Mapping': x.get('mapping').get('mqttMapping')} for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'MQTT Mapping': data.get('mapping').get('mqttMapping')}

    def getPluginMapping(self) -> Union[list, dict]:
        """
        Gets the plugin mapping of nodes

        :return: The plugin mapping of nodes
        """

        if self.nodes:
            return [{
                'name': x.get('name'),
                'Plugin Mapping': x.get('mapping').get('pluginMapping')
            } for x in self.nodes]
        else:
            data = json.loads(self.data)
            return {'name': data.get('name'), 'Plugin Mapping': data.get('mapping').get('pluginMapping')}
