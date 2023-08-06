from pydantic import BaseSettings, Field
from functools import lru_cache
from urllib.parse import urlparse
from threedi_api_client.threedi_api_client import ThreediApiClient
from openapi_client.api_client import ApiClient
from dataclasses import dataclass, field


class EnvSettings(BaseSettings):
    api_host: str = Field(..., env='API_HOST')


class WsSettings(BaseSettings):
    api_host: str
    host_name: str
    api_version: str
    proto: str
    client: ApiClient
    token: str


@lru_cache()
def get_settings(env_file):
    env_settings = EnvSettings(_env_file=env_file)
    parsed_url = urlparse(env_settings.api_host)
    host_name = parsed_url.netloc
    api_version = parsed_url.path.lstrip('/')
    proto = "wss" if parsed_url.scheme == "https" else "ws"
    client = ThreediApiClient(env_file)
    return WsSettings(
        api_host=env_settings.api_host,
        proto=proto,
        host_name=host_name,
        api_version=api_version,
        client=client,
        token=client.configuration.get_api_key_with_prefix("Authorization")
    )
