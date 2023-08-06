
from .Calls import Azure, BaseStation, Messages, Models, Mqtt, Nodes, Plugins, System, User


class Calls(Azure, BaseStation, Messages, Models, Mqtt, Nodes, Plugins, System, User):
    """
    Class for handling API requests to BehrTech's industrial gateways
    """

    def __init__(self, username: str, password: str, server_address: str):
        Azure.__init__(self)
        BaseStation.__init__(self)
        Messages.__init__(self)
        Models.__init__(self)
        Mqtt.__init__(self)
        Nodes.__init__(self)
        Plugins.__init__(self)
        System.__init__(self)
        User.__init__(self)
        self.username = username
        self.password = password
        self.server_address = f"https://{server_address}:443"
        self.jwt_token = self.login()

    def __repr__(self):
        return f"Connection to {self.server_address} for user {self.username}"

    def set_username(self, username: str):
        """
        Sets the login username for the given gateway

        :param username: username credential
        """

        self.username = username

    def get_username(self) -> str:
        """
        Returns the username credential for the given gateway

        :return: The username credential for the given gateway
        """

        return self.username

    def set_password(self, password: str):
        """
        Sets the login password for the given gateway

        :param password: password credential
        """

        self.password = password

    def get_password(self) -> str:
        """
        Returns the password credential for the given gateway

        :return: The password credential for the given gateway
        """

        return self.password

    def set_server_address(self, server_address):
        """
        Sets the IP address for the given gateway

        :param server_address: The IP address of the given gateway
        """

        self.server_address = server_address

    def get_server_address(self) -> str:
        """
        Returns the set IP address of the gateway

        :return: The set IP address of the gateway
        """

        return self.server_address

    def test_connection(self) -> bool:
        if self.jwt_token:
            return True
        else:
            return False
