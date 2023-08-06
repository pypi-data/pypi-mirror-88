import click

from sym.flow.cli.errors import UnknownOrgError

from ...models import HealthyHealthOrganization, Organization, SymOrganization


def lookup_org(email: str) -> Organization:
    """
    Given an email address, loads the org slug and ID and any other data needed for login.
    """
    if email.endswith("symops.io"):
        return SymOrganization

    if email.endswith("healthy-health.co"):
        return HealthyHealthOrganization

    click.secho("Unknown email, organization could not be loaded", fg="red")
    raise UnknownOrgError(email)
