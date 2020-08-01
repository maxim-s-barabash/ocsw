class Error(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        super(Error, self).__init__()
        self.message = message


class InvalidResource(Error):
    """If resource is invalid."""


class APIError(Error):
    """If the server returns an error."""

    def __init__(self, message, response=None):
        super(APIError, self).__init__(message)
        self.message = message
        self.response = response

    def __str__(self):
        message = super(APIError, self).__str__()
        reason = self.response.reason
        if self.is_client_error():
            message = f"{self.status_code} Client Error: {reason}"
        elif self.is_server_error():
            message = f"{self.status_code} Server Error: {reason}"
        return message

    @property
    def status_code(self):
        if self.response is not None:
            return self.response.status
        return None

    def is_error(self):
        return self.is_client_error() or self.is_server_error()

    def is_client_error(self):
        if self.status_code is None:
            return False
        return 400 <= self.status_code < 500

    def is_server_error(self):
        if self.status_code is None:
            return False
        return 500 <= self.status_code < 600


class BadRequest(APIError):
    """Request is invalid."""


class Forbidden(APIError):
    """Do not have access to the object/namespace."""


class NotFound(APIError):
    """The specified resource could not be found."""


class InternalServerError(APIError):
    """The problem with server."""


# MAP_API_ERROR = {
#     400: BadRequest,
#     403: Forbidden,
#     404: NotFound,
#     500: InternalServerError,
# }


# def create_api_error_from_http_exception(exception):
#     """
#     Create a suitable APIError based on response status code
#     """
#     cls = APIError
#     if response is not None:
#         cls = MAP_API_ERROR.get(response.status, APIError)

#     return cls(message='\n'.join(errors), response=response)
