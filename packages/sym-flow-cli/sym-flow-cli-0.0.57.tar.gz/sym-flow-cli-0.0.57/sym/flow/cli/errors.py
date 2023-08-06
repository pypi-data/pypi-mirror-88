from sym.cli.errors import CliError


class LoginError(CliError):
    def __init__(self, response_body) -> None:
        super().__init__(f"Error logging in: {response_body}")


class UnknownOrgError(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Unknown organization for email: {email}")


class InvalidTokenError(CliError):
    def __init__(self, raw_token) -> None:
        super().__init__(f"Unable to parse token: {raw_token}")


class NotAuthorizedError(CliError):
    def __init__(self) -> None:
        super().__init__(f"Please run `symflow login`")
