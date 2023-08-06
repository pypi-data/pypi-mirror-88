from typing import List, Union, cast

import pytest
from click.testing import CliRunner

from sym.cli.errors import CliError
from sym.cli.helpers.contexts import push_env
from sym.flow.cli.errors import InvalidTokenError, LoginError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.login_flow import LoginFlow
from sym.flow.cli.models import AuthToken, Organization
from sym.flow.cli.symflow import symflow as click_command


@pytest.fixture
def auth_token():
    return AuthToken(
        access_token="access",
        refresh_token="refresh",
        token_type="type",
        expires_in=86400,
        scope="scopes",
    )


def mock_login_flow(result: Union[AuthToken, CliError]):
    class MockLoginFlow(LoginFlow):
        def login(self, options: GlobalOptions, org: Organization) -> AuthToken:
            # TypedDict doesn't support isinstance
            if isinstance(result, dict):
                return result
            raise cast(CliError, result)

    return MockLoginFlow()


@pytest.fixture
def login_flow(auth_token):
    return mock_login_flow(auth_token)


@pytest.fixture
def login_flow_login_error():
    return mock_login_flow(LoginError("test"))


@pytest.fixture
def login_flow_invalid_token_error():
    return mock_login_flow(InvalidTokenError("test"))


@pytest.fixture
def login_tester(mocker, sandbox):
    def tester(
        login_flow: LoginFlow,
        email: str,
        success: bool = True,
        expected_output: List[str] = [],
    ):
        mocker.patch.object(LoginFlow, "get_login_flow", return_value=login_flow)
        with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
            runner = CliRunner()
            result = runner.invoke(click_command, ["login", "--email", email])
            print(result.output)
            for expected_str in expected_output:
                assert expected_str in result.output
            if success:
                assert result.exit_code == 0
            else:
                assert result.exit_code != 0

    return tester


def test_login_ok(login_flow, login_tester):
    expected_output = [
        "Successfully loaded org: sym (P5juMqe7UUpKo6634ZeuUgZF3QTXyIfj)",
        "Login succeeded",
        f"Credentials stored to",
    ]
    login_tester(
        login_flow=login_flow,
        email="ci@symops.io",
        success=True,
        expected_output=expected_output,
    )


def test_login_login_error(login_flow_login_error, login_tester):
    expected_output = [
        "Successfully loaded org: sym (P5juMqe7UUpKo6634ZeuUgZF3QTXyIfj)",
        "Error: Error logging in: test",
    ]
    login_tester(
        login_flow=login_flow_login_error,
        email="ci@symops.io",
        success=False,
        expected_output=expected_output,
    )


def test_login_invalid_token_error(login_flow_invalid_token_error, login_tester):
    expected_output = [
        "Successfully loaded org: sym (P5juMqe7UUpKo6634ZeuUgZF3QTXyIfj)",
        "Error: Unable to parse token: test",
    ]
    login_tester(
        login_flow=login_flow_invalid_token_error,
        email="ci@symops.io",
        success=False,
        expected_output=expected_output,
    )


def test_login_unknown_org(login_flow, login_tester):
    expected_output = [
        "Unknown email, organization could not be loaded",
        "Error: Unknown organization for email: ci@unknown.org",
    ]
    login_tester(
        login_flow=login_flow,
        email="ci@unknown.org",
        success=False,
        expected_output=expected_output,
    )
