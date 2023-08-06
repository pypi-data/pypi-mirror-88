import pytest

from sym.flow.cli.helpers.global_options import GlobalOptions

from ....models import AuthToken


@pytest.fixture
def global_options(mocker):
    options = GlobalOptions()
    options.debug = False
    options.api_url = "https://api.com"
    options.auth_url = "https://auth.com"
    return options


@pytest.fixture
def auth_token(mocker):
    return AuthToken(
        access_token="access",
        refresh_token="refresh",
        token_type="type",
        expires_in=86400,
        scope="scopes",
    )
