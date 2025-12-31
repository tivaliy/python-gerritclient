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

"""Pydantic-based settings management for gerritclient.

Configuration is loaded from environment variables with the GERRIT_ prefix.
A .env file in the current directory is also supported.

Environment variables:
    GERRIT_URL: Gerrit server URL (required)
    GERRIT_AUTH_TYPE: Authentication type - 'basic' or 'digest' (optional)
    GERRIT_USERNAME: Username for authentication (required if auth_type set)
    GERRIT_PASSWORD: HTTP password for authentication (required if auth_type set)

Example .env file:
    GERRIT_URL=https://review.example.com
    GERRIT_AUTH_TYPE=basic
    GERRIT_USERNAME=admin
    GERRIT_PASSWORD=secret
"""

from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GerritSettings(BaseSettings):
    """Gerrit client configuration with validation.

    Configuration sources (highest to lowest priority):
    1. Explicit keyword arguments
    2. Environment variables (GERRIT_URL, GERRIT_AUTH_TYPE, etc.)
    3. .env file in current directory
    """

    model_config = SettingsConfigDict(
        env_prefix="GERRIT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str = Field(
        ..., description="Gerrit server URL (e.g., https://review.example.com)"
    )
    auth_type: Literal["basic", "digest"] | None = Field(
        default=None,
        description="HTTP authentication scheme. Omit for anonymous access.",
    )
    username: str | None = Field(default=None, description="Gerrit username")
    password: str | None = Field(default=None, description="Gerrit HTTP password")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate and normalize the Gerrit server URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v.rstrip("/")

    @model_validator(mode="after")
    def validate_auth_credentials(self) -> "GerritSettings":
        """Ensure username and password are provided when auth_type is set."""
        if self.auth_type and not all([self.username, self.password]):
            raise ValueError("username and password are required when auth_type is set")
        return self

    def to_dict(self) -> dict:
        """Convert settings to dict compatible with client.connect()."""
        return {
            "url": self.url,
            "auth_type": self.auth_type,
            "username": self.username,
            "password": self.password,
        }


def get_settings() -> dict:
    """Load gerritclient configuration.

    Configuration sources (highest to lowest priority):
    1. Environment variables (GERRIT_URL, GERRIT_AUTH_TYPE, etc.)
    2. .env file in current directory

    Returns:
        Configuration dictionary compatible with connect()

    Raises:
        pydantic.ValidationError: If configuration is invalid or missing
    """
    settings = GerritSettings()
    return settings.to_dict()
