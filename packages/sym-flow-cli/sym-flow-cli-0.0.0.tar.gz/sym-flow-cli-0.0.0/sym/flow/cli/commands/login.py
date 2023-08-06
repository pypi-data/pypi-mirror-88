import click
import validators

from sym.flow.cli.helpers.config import store_login_config
from sym.flow.cli.helpers.login.login_flow import LoginFlow

from ..helpers.global_options import GlobalOptions
from ..helpers.login.org import lookup_org
from .symflow import symflow


def validate_email(ctx, param, value):
    if value and not validators.email(value):
        raise click.BadParameter("must enter a valid email address")
    return value


@symflow.command(short_help="login")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--browser/--no-browser",
    default=True,
    is_flag=True,
)
@click.option(
    "--port",
    default=11001,
)
@click.option(
    "--email",
    callback=validate_email,
    prompt=True,
)
def login(options: GlobalOptions, browser: bool, port: int, email: str) -> None:
    org = lookup_org(email)
    click.echo("Successfully loaded org: {slug} ({client_id})".format(**org))
    auth_token = LoginFlow.get_login_flow(email, browser, port).login(options, org)
    options.dprint(auth_token=auth_token)
    click.echo("Login succeeded")
    file = store_login_config(email, org, auth_token)
    click.echo(f"Credentials stored to {file}")
