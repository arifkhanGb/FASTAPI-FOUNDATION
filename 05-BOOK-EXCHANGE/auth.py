"""API-key authentication shared by protected endpoints."""

import secrets
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


API_KEY_ENV_VAR = "API_KEY"
API_KEY_HEADER = "X-API-Key"

# ``auto_error=False`` lets us return the same 401 response for absent and
# invalid credentials, without exposing which case occurred.
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


class SecuritySettings(BaseSettings):
    """Security configuration loaded from environment variables or a local .env."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).with_name(".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    api_key: SecretStr = Field(min_length=32, validation_alias=API_KEY_ENV_VAR)


@lru_cache
def get_security_settings() -> SecuritySettings:
    """Load configuration once; environment variables override values in .env."""
    try:
        return SecuritySettings()
    except ValidationError as exc:
        raise RuntimeError(
            f"{API_KEY_ENV_VAR} must be configured with a value of at least 32 characters."
        ) from exc


def get_configured_api_key() -> str:
    """Return the deployment-provided API key or fail safely if it is absent."""
    return get_security_settings().api_key.get_secret_value()


def validate_api_key_configuration() -> None:
    """Validate required security configuration during application startup."""
    get_configured_api_key()


def verify_api_key(
    provided_api_key: Annotated[str | None, Security(api_key_header)],
) -> str:
    """Require a valid ``X-API-Key`` request header on protected endpoints."""
    configured_api_key = get_configured_api_key()

    if not provided_api_key or not secrets.compare_digest(provided_api_key, configured_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return provided_api_key
