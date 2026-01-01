"""Tests for gerritclient.settings module."""

import os
from unittest import mock

import pytest
from pydantic import ValidationError

from gerritclient.settings import GerritSettings, get_settings


class TestGerritSettings:
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

        assert settings.url == "https://review.example.com"
        assert settings.auth_type == "basic"
        assert settings.username == "admin"
        assert settings.password == "secret"

    def test_url_validation_requires_scheme(self):
        """URL must start with http:// or https://."""
        env = {"GERRIT_URL": "review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()

    def test_url_http_scheme_accepted(self):
        """HTTP URLs should be accepted."""
        env = {"GERRIT_URL": "http://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        assert settings.url == "http://review.example.com"

    def test_url_https_scheme_accepted(self):
        """HTTPS URLs should be accepted."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        assert settings.url == "https://review.example.com"

    def test_url_trailing_slash_stripped(self):
        """Trailing slashes should be removed from URL."""
        env = {"GERRIT_URL": "https://review.example.com/"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()
        assert settings.url == "https://review.example.com"

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
        assert settings.auth_type == "basic"

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
        assert settings.auth_type == "digest"

    def test_invalid_auth_type_rejected(self):
        """Only 'basic' and 'digest' auth types are valid."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "invalid",
            "GERRIT_USERNAME": "user",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()

    def test_auth_type_requires_username(self):
        """auth_type requires username."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_PASSWORD": "pass",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()

    def test_auth_type_requires_password(self):
        """auth_type requires password."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
            "GERRIT_USERNAME": "user",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()

    def test_auth_type_requires_both_credentials(self):
        """auth_type requires both username and password."""
        env = {
            "GERRIT_URL": "https://review.example.com",
            "GERRIT_AUTH_TYPE": "basic",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()

    def test_anonymous_access_no_auth(self):
        """Anonymous access requires no credentials."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            settings = GerritSettings()

        assert settings.auth_type is None
        assert settings.username is None
        assert settings.password is None

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
        assert result == expected

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
        assert result == expected

    def test_missing_url_raises_validation_error(self):
        """Missing URL should raise ValidationError."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValidationError):
                GerritSettings()


class TestGetSettings:
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

        assert isinstance(result, dict)
        assert result["url"] == "https://review.example.com"
        assert result["auth_type"] == "basic"
        assert result["username"] == "admin"
        assert result["password"] == "secret"

    def test_get_settings_anonymous(self):
        """get_settings() should work for anonymous access."""
        env = {"GERRIT_URL": "https://review.example.com"}
        with mock.patch.dict(os.environ, env, clear=True):
            result = get_settings()

        assert result["url"] == "https://review.example.com"
        assert result["auth_type"] is None

    def test_get_settings_missing_config_raises(self):
        """get_settings() should raise when no config available."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValidationError):
                get_settings()
