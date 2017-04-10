#
#    Copyright 2017 Vitalii Kulanov
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json


class GerritClientException(Exception):
    """Base Exception for GerritClient

    All child classes must be instantiated before raising.
    """
    def __init__(self, *args, **kwargs):
        super(GerritClientException, self).__init__(*args, **kwargs)
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
        error_body = json.loads(error.response.text)['message']
    except (ValueError, TypeError, KeyError):
        error_body = error.response.text
    return error_body


def get_full_error_message(error):
    return "{} ({})".format(error, get_error_body(error))
