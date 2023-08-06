import webbrowser

import click
import requests

from sym.cli.errors import CliError
from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.helpers.login.token import get_auth_header

from ..helpers.global_options import GlobalOptions
from .symflow import symflow


@symflow.command(short_help="add Sym bot to Slack")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def add_to_slack(options: GlobalOptions) -> None:
    """Install the Sym Slack bot into your Slack workspace. Will open a
    browser window to confirm the installation.
    """

    initialize_slack_install(api_url=options.api_url)


def initialize_slack_install(api_url: str):
    try:
        url = f"{api_url}install/slack/"
        response = requests.get(url, headers={"Authorization": get_auth_header()})
        if response.ok:
            webbrowser.open(response.url)
        else:
            raise CliError(
                f"Sym API responded with a status code of {response.status_code}"
            )
    except NotAuthorizedError:
        raise
    except Exception as e:
        raise CliError(f"Unexpected error occurred during Slack installation: {e}")
