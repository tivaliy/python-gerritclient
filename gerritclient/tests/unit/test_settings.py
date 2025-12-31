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

import os
from unittest import mock

from oslotest import base as oslo_base
from pydantic import ValidationError

from gerritclient.settings import GerritSettings, get_settings


class TestGerritSettings(oslo_base.BaseTestCase):
    """Test suite for Pydantic settings configuration."""

    def test_load_from_env_vars(self):
        """Settings should load from environment variables."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_USERNAME": "admin",
            "GERRIT_PASSWORD": "secret",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()

        self.assertEqual(settings.url, "https://review.example.com")
        self.assertEqual(settings.auth_type, "basic")
        self.assertEqual(settings.username, "admin")
        self.assertEqual(settings.password, "secret")

    def test_url_validation_requires_scheme(self):
        """URL must start with http:// or https://."""
        env = {"GERRIT_URL": "review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertRaises(ValidationError, GerritSettings)

    def test_url_http_scheme_accepted(self):
        """HTTP URLs should be accepted."""
        env = {"GERRIT_URL": "http://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        self.assertEqual(settings.url, "http://review.example.com")

    def test_url_https_scheme_accepted(self):
        """HTTPS URLs should be accepted."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        self.assertEqual(settings.url, "https://review.example.com")

    def test_url_trailing_slash_stripped(self):
        """Trailing slashes should be removed from URL."""
        env = {"GERRIT_URL": "https://review.example.com/"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        self.assertEqual(settings.url, "https://review.example.com")

    def test_auth_type_basic_accepted(self):
        """Basic auth type should be accepted."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_USERNAME": "user",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        self.assertEqual(settings.auth_type, "basic")

    def test_auth_type_digest_accepted(self):
        """Digest auth type should be accepted."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "digest",
            "GERRIT_USERNAME": "user",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        self.assertEqual(settings.auth_type, "digest")

    def test_invalid_auth_type_rejected(self):
        """Only 'basic' and 'digest' auth types are valid."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "invalid",
            "GERRIT_USERNAME": "user",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertRaises(ValidationError, GerritSettings)

    def test_auth_type_requires_username(self):
        """auth_type requires username."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertRaises(ValidationError, GerritSettings)

    def test_auth_type_requires_password(self):
        """auth_type requires password."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_USERNAME": "user",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertRaises(ValidationError, GerritSettings)

    def test_auth_type_requires_both_credentials(self):
        """auth_type requires both username and password."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertRaises(ValidationError, GerritSettings)

    def test_anonymous_access_no_auth(self):
        """Anonymous access requires no credentials."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()

        self.assertIsNone(settings.auth_type)
        self.assertIsNone(settings.username)
        self.assertIsNone(settings.password)

    def test_to_dict_returns_connect_compatible_dict(self):
        """to_dict() should return dict compatible with client.connect()."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "digest",
            "GERRIT_USERNAME": "user",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
            result = settings.to_dict()

        expected = {
            "url": "https://review.example.com",
            "auth_type": "digest",
            "username": "user",
            "password": "pass",
        }
        self.assertEqual(result, expected)

    def test_to_dict_anonymous_access(self):
        """to_dict() should work for anonymous access."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
            result = settings.to_dict()

        expected = {
            "url": "https://review.example.com",
            "auth_type": None,
            "username": None,
            "password": None,
        }
        self.assertEqual(result, expected)

    def test_missing_url_raises_validation_error(self):
        """Missing URL should raise ValidationError."""
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertRaises(ValidationError, GerritSettings)


class TestGetSettings(oslo_base.BaseTestCase):
    """Test suite for get_settings() function."""

    def test_get_settings_returns_dict(self):
        """get_settings() should return a dictionary."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_USERNAME": "admin",
            "GERRIT_PASSWORD": "secret",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            result = get_settings()

        self.assertIsInstance(result, dict)
        self.assertEqual(result["url"], "https://review.example.com")
        self.assertEqual(result["auth_type"], "basic")
        self.assertEqual(result["username"], "admin")
        self.assertEqual(result["password"], "secret")

    def test_get_settings_anonymous(self):
        """get_settings() should work for anonymous access."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            result = get_settings()

        self.assertEqual(result["url"], "https://review.example.com")
        self.assertIsNone(result["auth_type"])

    def test_get_settings_missing_config_raises(self):
        """get_settings() should raise when no config available."""
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertRaises(ValidationError, get_settings)
