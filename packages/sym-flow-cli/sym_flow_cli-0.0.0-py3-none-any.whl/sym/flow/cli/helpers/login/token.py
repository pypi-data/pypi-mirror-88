from sym.flow.cli.errors import NotAuthorizedError

from ..config import Config


def get_auth_header() -> str:
    try:
        token = Config.get_auth_token()
        token_type = token["token_type"]
        access_token = token["access_token"]
        return f"{token_type} {access_token}"
    except KeyError:
        raise NotAuthorizedError()
