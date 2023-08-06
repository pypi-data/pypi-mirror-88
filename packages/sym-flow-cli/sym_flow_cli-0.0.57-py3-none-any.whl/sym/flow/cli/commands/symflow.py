import click

from ..helpers.constants import DEFAULT_API_URL, DEFAULT_AUTH_URL
from ..helpers.global_options import GlobalOptions


@click.group(name="symflow", context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--debug", is_flag=True, help="enable verbose debugging", envvar="SYM_DEBUG"
)
@click.option(
    "--api-url",
    default=DEFAULT_API_URL,
    help="set the Sym API URL",
    envvar="SYM_API_URL",
)
@click.option(
    "--auth-url",
    default=DEFAULT_AUTH_URL,
    help="set the Sym auth url",
    envvar="SYM_AUTH_URL",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def symflow(options: GlobalOptions, auth_url: str, api_url: str, debug: bool) -> None:
    """Sym Flow CLI"""
    options.debug = debug
    options.api_url = api_url
    options.auth_url = auth_url
    options.dprint(auth_url=auth_url, api_url=api_url)
