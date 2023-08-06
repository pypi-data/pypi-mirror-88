from typing import TypedDict

from sym.cli.helpers.config.base import ConfigBase
from sym.flow.cli.models import AuthToken, Organization


class ConfigSchema(TypedDict, total=False):
    org: Organization
    email: str
    auth_token: AuthToken


class Config(ConfigBase[ConfigSchema]):
    @classmethod
    def get_org(cls) -> Organization:
        return cls.instance()["org"]

    @classmethod
    def get_auth_token(cls) -> AuthToken:
        return cls.instance()["auth_token"]


def store_login_config(email: str, org: Organization, auth_token: AuthToken) -> str:
    cfg = Config.instance()
    cfg["email"] = email
    cfg["org"] = org
    cfg["auth_token"] = auth_token
    return str(cfg.file)
