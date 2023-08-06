"""Supplies utilities to assist in developing software using the FastAPI
REST Framework.
"""
import argparse
import time

import ioc

TEN_YEARS = (time.time() + (86400 * 365 * 10))
parser = argparse.ArgumentParser()
commands = parser.add_subparsers()


@ioc.inject('encoder', 'BearerTokenDecoder')
def create_token(args, encoder):
    print(encoder.encode(args.aud, args.sub, time.time() + TEN_YEARS,
        {'scopes': ['*']}, signing_key=args.sign_with))
create_token.parser = commands.add_parser("create-token",
    help=(
        "Generates a Bearer token with full audience and permission, for "
        "use in local development scenarios."
    )
)
create_token.parser.add_argument('--aud',
    help="specify the `aud` claim on the bearer token.")
create_token.parser.add_argument('--sub',
    help="specify the `sub` claim on the bearer token.")
create_token.parser.add_argument('--sign-with',
    help="the secret to sign the claims with.")
create_token.parser.set_defaults(func=create_token)


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
