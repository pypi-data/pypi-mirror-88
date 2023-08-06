import requests

from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError, ConnectTimeoutError
from py_behrtech.exceptions import JWTError, check_status_code


class User:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def login(self) -> str:
        """
        Gets the JWT token of the login endpoint

        :return: The JWT token of the login endpoint
        """

        try:
            req = requests.post(url=self.server_address + "/v2/login", verify=False,
                                json={'user': self.username, 'password': self.password}, timeout=3)

            if req.status_code == 200:
                # Successfully logged in
                return req.json().get("JWT")
            else:
                check_status_code(req=req)

        except (TimeoutError, ConnectTimeoutError, MaxRetryError, RequestException):
            raise JWTError(status_code=401, message="The wrong server IP address or login credentials were provided")

    def userGet(self) -> dict:
        """
        Gets information on all registered users, only accessible for admin users

        :return: All registered users
        """

        req = requests.get(url=self.server_address + f"/v2/user", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def userPost(self, name: str, email: str, admin: bool, getMethodsOnly: bool) -> dict:
        """
        Adds a new user, only accessible for admin users

        :param name: Name of the user account
        :param email: Email for the user account
        :param admin: If user account is a admin
        :param getMethodsOnly:
        :return: Newly create user account information
        """

        req = requests.post(url=self.server_address + f"/v2/user", verify=False,
                            headers={"Authorization": f"Bearer {self.jwt_token}"},
                            json={'name': name, 'email': email, 'admin': admin, 'getMethodsOnly': getMethodsOnly},
                            timeout=3)

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def userUUIDDelete(self, uuid: str) -> bool:
        """
        Deletes the specified user, only accessible for admin users

        :param uuid: Unique user ID
        :return: Bool if user has been successfully deleted or not
        """

        req = requests.delete(url=self.server_address + f"/v2/user/{uuid}", verify=False,
                              headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def userUUIDGet(self, uuid: str) -> dict:
        """
        Gets user information for the specified user, only accessible for admin users

        :param uuid: Unique user ID
        :return: User profile information
        """

        req = requests.get(url=self.server_address + f"/v2/user/{uuid}", verify=False,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return req.json()
        else:
            check_status_code(req=req)

    def userUUIDProfilePost(self, uuid: str, **kwargs) -> bool:
        """
        Updates user profile information

        :param uuid: Unique user ID
        :keyword name: Name of user account
        :keyword email: Email of user account
        :keyword oldPassword: Old password of user account
        :keyword newPassword: New password of user account
        :keyword acceptedEULA: If EULA has been accepted
        :return: Bool if user profile information has been updated or not
        """

        allowed = ['name', 'email', 'oldPassword', 'newPassword', 'acceptedEULA']
        body = {x: kwargs[x] for x in kwargs if x in allowed and kwargs[x] is not None}

        req = requests.post(url=self.server_address + f"/v2/user/{uuid}/profile", verify=False,
                            headers={"Authorization": f"Bearer {self.jwt_token}"}, json=body, timeout=3)

        if req.status_code == 200:
            return True
        else:
            check_status_code(req=req)

    def userUUIDResetPasswordPost(self, uuid: str) -> str:
        """
        Resets a users password to a randomly generated one, only accessible for admin users

        :param uuid: Unique user ID
        :return: New reset password for user
        """

        req = requests.post(url=self.server_address + f"/v2/user/{uuid}/resetpassword", verify=False,
                            headers={"Authorization": f"Bearer {self.jwt_token}"}, timeout=3)

        if req.status_code == 200:
            return req.json().get("password")
        else:
            check_status_code(req=req)
