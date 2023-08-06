
import os


class Defaults:

    def __init__(self):
        self.response = None
        self.data = None
        self.count = None

    def getResponse(self):
        """
        Returns the response of the class

        :return: The response of the class
        """

        return self.response

    def getData(self):
        """
        Returns the data of the class

        :return: The data of the class
        """

        return self.data

    def getCount(self):
        """
        Returns the count of the class

        :return: The count of the class
        """

        return self.count

    def writeDateToFile(self, file_name: str, file_path: os.path = 'Outputs/'):
        """
        Outputs the data of the class to a JSON file

        :param file_path: The path to write the file to
        :param file_name: The name of the file for the data of the class to be outputted to
        """

        file_path = file_path if os.path.isdir(file_path) else 'Outputs/'

        text_file = open(file_path + file_name + ".json", "w")
        text_file.write(self.data)
        text_file.close()
