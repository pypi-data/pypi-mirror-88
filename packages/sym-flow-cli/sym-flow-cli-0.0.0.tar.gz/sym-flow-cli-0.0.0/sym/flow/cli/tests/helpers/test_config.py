import os
from pathlib import Path

import immutables
import pytest

from sym.cli.helpers.contexts import push_env
from sym.cli.tests.helpers.sandbox import Sandbox

from ...helpers.config import Config, store_login_config
from ...models import AuthToken, Organization


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def org() -> Organization:
    return Organization(slug="slug", client_id="client-id")


@pytest.fixture
def email() -> str:
    return "ci@symops.io"


@pytest.fixture
def auth_token() -> AuthToken:
    return AuthToken(
        access_token="access-token",
        refresh_token="refresh-token",
        token_type="token-type",
        expires_in=86400,
        scope="scopes",
    )


__config_yaml = """
auth_token:
  access_token: access-token
  expires_in: 86400
  refresh_token: refresh-token
  scope: scopes
  token_type: token-type
email: ci@symops.io
org:
  client_id: client-id
  slug: slug
"""


def test_write_login_config(sandbox, org, email, auth_token):
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        path = store_login_config(email=email, org=org, auth_token=auth_token)
        with open(path) as fd:
            data = fd.read()
            assert data.strip() == __config_yaml.strip()


def test_read_login_config(sandbox, org, email, auth_token):
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        config_dir = sandbox.path / ".config" / "symflow" / "default"
        os.makedirs(config_dir)
        with open(str(config_dir / "config.yml"), "w") as fd:
            fd.write(__config_yaml)
            fd.flush()
            assert Config.get_email() == email
            assert Config.get_org() == immutables.Map(org)
            assert Config.get_auth_token() == immutables.Map(auth_token)
