import json


class GerritClientException(Exception):
    """Base Exception for GerritClient

    All child classes must be instantiated before raising.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = args[0]


class BadDataException(GerritClientException):
    """Should be raised when passed incorrect data."""


class InvalidFileException(GerritClientException):
    """Should be raised when some problems while working with file occurred."""


class ConfigNotFoundException(GerritClientException):
    """Should be raised if configuration for gerritclient was not specified."""


class HTTPError(GerritClientException):
    pass


def get_error_body(error):
    try:
        error_body = json.loads(error.response.text)["message"]
    except (ValueError, TypeError, KeyError):
        error_body = error.response.text
    return error_body


def get_full_error_message(error):
    return f"{error} ({get_error_body(error)})"
