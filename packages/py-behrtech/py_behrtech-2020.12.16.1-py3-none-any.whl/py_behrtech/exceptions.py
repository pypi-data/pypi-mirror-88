
from requests import Response


def check_status_code(req: Response):
    """
    Check status code of requests response to raise the correct exception

    :param req: The requests Response of your requests call
    """

    if req.status_code == 400:
        raise QueryError(status_code=400, url=req.url, message="Endpoint is invalid or was built incorrectly")
    elif req.status_code == 401:
        raise JWTError(status_code=401, message="JWT Access token is missing or invalid credentials were provided")
    elif req.status_code == 403:
        raise PermissionsError(status_code=403, message="User doesn't have the correct permissions to access this data")
    elif req.status_code == 404:
        raise QueryError(status_code=404, url=req.url, message="Endpoint is invalid or was built incorrectly")


class PyBehrtechException(Exception):
    """Base exception used by this module."""
    pass


class JWTError(PyBehrtechException):
    """A request for the JWT failed"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)


class PermissionsError(PyBehrtechException):
    """User of request doesn't have permissions"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)


class QueryError(PyBehrtechException):
    """Request to endpoint is invalid or was built incorrectly"""

    def __init__(self, status_code, url, message):
        self.status_code = status_code
        self.url = url
        PyBehrtechException.__init__(self, status_code, url, message)
