
import os
import json

from typing import Union
from requests import Response
from py_behrtech.Parsers.defaults import Defaults


class ModelParser(Defaults):

    def __init__(self, req: Response):

        def getCount():
            count = json.loads(self.data).get('count')
            return count if count is not None else 1

        Defaults.__init__(self)
        self.response: Response = req
        self.data: str = req.text
        self.count = getCount()
        self.models = json.loads(self.data).get('models')

    def getTypes(self) -> Union[list, dict]:
        """
        Gets type of sensor model

        :return: Type of sensor model
        """

        if self.models:
            return [{'name': x.get('name'), 'type': x.get('type')} for x in self.models]
        else:
            return {'name': json.loads(self.data).get('name'), 'type': json.loads(self.data).get('type')}

    def getComponents(self) -> Union[list, dict]:
        """
        Gets measured components for a specified sensor model

        :return: Measure components
        """

        if self.models:
            return [{'name': x.get('name'), 'components': x.get('components')} for x in self.models]
        else:
            return json.loads(self.data).get('components')

    def getComponentsNames(self) -> list:
        """
        Gets a list of measured components names for the specified sensor model

        :return: Measured components names
        """

        if self.models:
            return [{'name': x.get('name'), 'components': [y for y in x.get('components')]} for x in self.models]
        else:
            return [x for x in json.loads(self.data).get('components')]

    def getUnits(self) -> Union[list, dict]:
        """
        Gets units for measured components for the specified sensor model

        :return: Units for measured components
        """

        if self.models:
            return [{
                'name': x.get('name'),
                'units': {
                    y: x.get('components').get(y)['unit'] for y in x.get('components')
                }
            } for x in self.models]
        else:
            components = json.loads(self.data).get('components')
            return {x: components.get(x)['unit'] for x in components}
