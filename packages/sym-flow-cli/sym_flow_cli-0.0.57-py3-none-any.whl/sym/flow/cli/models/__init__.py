from dataclasses import dataclass
from typing import TypedDict

from sym.flow.cli.errors import InvalidTokenError


class Organization(TypedDict):
    slug: str
    client_id: str

    def __init__(self, slug: str, client_id: str):
        # This is necessary instead of @dataclass due to an
        # incompatibility between dataclass + TypedDict in python3.9
        self.slug = slug
        self.client_id = client_id


SymOrganization = Organization(slug="sym", client_id="P5juMqe7UUpKo6634ZeuUgZF3QTXyIfj")
HealthyHealthOrganization = Organization(
    slug="healthy-health", client_id="Y4dnvjDlRibbKqSXA57hFnvZKyINHyJW"
)


@dataclass
class UserCredentials:
    username: str
    password: str


class AuthToken(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        token_type: str,
        expires_in: int,
        scope: str,
    ):
        # This is necessary instead of @dataclass due to an
        # incompatibility between dataclass + TypedDict in python3.9
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope


def parse_auth_token(json_response: dict) -> AuthToken:
    try:
        return AuthToken(
            access_token=json_response["access_token"],
            refresh_token=json_response["refresh_token"],
            token_type=json_response["token_type"],
            expires_in=json_response["expires_in"],
            scope=json_response["scope"],
        )
    except KeyError:
        raise InvalidTokenError(str(json_response))
