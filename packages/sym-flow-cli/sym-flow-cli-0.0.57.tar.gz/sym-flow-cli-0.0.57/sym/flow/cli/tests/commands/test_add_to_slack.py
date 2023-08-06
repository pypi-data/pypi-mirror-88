from unittest.mock import patch

import pytest
from requests import Response

from sym.cli.errors import CliError
from sym.cli.helpers.contexts import push_env
from sym.flow.cli.commands.add_to_slack import initialize_slack_install
from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.symflow import symflow as click_command


def get_mock_response(status_code: int):
    response = Response()
    response.status_code = status_code
    return response


class TestAddToSlack:
    """Suite for testing Slack installation."""

    @patch("sym.flow.cli.commands.add_to_slack.initialize_slack_install")
    def test_click_calls_install_method(self, mock_initialize_slack_install, click_setup):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["add-to-slack"])
            assert result.exit_code == 0
            mock_initialize_slack_install.assert_called_once()

    def test_initialize_slack_install_not_authorized_fails(self, sandbox):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
                initialize_slack_install("http://afakeurl.symops.io/")

    @patch("sym.flow.cli.commands.add_to_slack.get_auth_header", return_value="")
    @patch("sym.flow.cli.commands.add_to_slack.requests.get", return_value=0)
    def test_initialize_slack_install_unknown_error_caught(
        self, mock_requests_get, mock_get_auth_header, sandbox
    ):
        with pytest.raises(CliError, match="Unexpected error occurred during Slack"):
            with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
                initialize_slack_install("http://afakeurl.symops.io/")

    @patch("sym.flow.cli.commands.add_to_slack.webbrowser.open")
    @patch("sym.flow.cli.commands.add_to_slack.get_auth_header", return_value="")
    @patch(
        "sym.flow.cli.commands.add_to_slack.requests.get",
        return_value=get_mock_response(500),
    )
    def test_bad_response_doesnt_open_browser(
        self, mock_requests_get, mock_get_auth_header, mock_webbrowser_open, sandbox
    ):
        with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
            with pytest.raises(CliError, match="responded with a status code of 500"):
                initialize_slack_install("http://afakeurl.symops.io/")

        mock_requests_get.assert_called_once()
        mock_get_auth_header.assert_called_once()
        mock_webbrowser_open.assert_not_called()

    @patch("sym.flow.cli.commands.add_to_slack.webbrowser.open")
    @patch("sym.flow.cli.commands.add_to_slack.get_auth_header", return_value="")
    @patch(
        "sym.flow.cli.commands.add_to_slack.requests.get",
        return_value=get_mock_response(302),
    )
    def test_good_response_opens_browser(
        self, mock_requests_get, mock_get_auth_header, mock_webbrowser_open, sandbox
    ):
        with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
            initialize_slack_install("http://afakeurl.symops.io/")

        mock_requests_get.assert_called_once()
        mock_get_auth_header.assert_called_once()
        mock_webbrowser_open.assert_called_once()
