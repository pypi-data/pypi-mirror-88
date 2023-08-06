import logging
import sys

import click

from ._aws import update_aws_creds
from ._client import (browser_authenticate, decrypt_msg,
                      poll_opaque_token_service)
from ._crypto import generate_keys
from ._pgpass import update_pgpass

logger = logging.getLogger("gimme_db_token")
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - - %(funcName)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)


@click.command(name="gimme_db_token")
@click.argument("db", type=click.Choice(["pg", "s3"], case_sensitive=False), nargs=-1)
@click.option(
    "--tenant",
    required=True,
    envvar="CYRAL_TENANT",
    show_envvar=True,
    help="Tenant Name.",
)
@click.option(
    "--profile",
    help="(Required only for S3) Name of AWS profile to store S3 access credentials in. NOTE: any existing credentials in this profile will be overwritten. If no AWS profile with the provided name exists, it will be created.",
)
@click.option(
    "--timeout",
    default=5 * 60,
    envvar="CYRAL_DB_TOKEN_TIMEOUT",
    type=click.INT,
    show_envvar=True,
    help="Number of seconds to wait for Cyral server to respond before timeout",
)
@click.option("-v", "--verbose", is_flag=True)
@click.version_option(version="0.2.0")
def update_token(tenant, db, profile, timeout, verbose):
    """Fetch a fresh database access token from Cyral and store it locally.
    Currently, gimme_db_token supports Postgresql and S3 (with more coming!).
    If a database type is not specified, Postgresql database type is used.

    Example usage:

        This command will fetch a database access token for Postgresql and store it in your system.

        > gimme_db_token pg --tenant mycompany

        You can also specify multiple database types:

        > gimme_db_token pg s3 --tenant mycompany
    """
    if db == ():
        # for backwards compatibility, if DB type is not set, use Postgresql
        db = ("pg",)
    if "s3" in db and not profile:
        print("Please provide an AWS profile name to use via --profile")
        return

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("/* IN DEBUG MODE */")
    try:
        private_key, public_key = generate_keys()
        browser_authenticate(tenant, public_key)
        msg = poll_opaque_token_service(tenant, public_key, timeout)
        decrypt_msg(msg, private_key)
        # note: despite the field name, this access token is not encrypted anymore.
        # it was decrypted by the above line
        access_token = msg["EncryptedAccessToken"]
        print("")
        if "pg" in db:
            update_pgpass(access_token, msg.get("SidecarEndpoints"))
            print("")
        if "s3" in db:
            update_aws_creds(access_token, msg.get("UserEmail"), profile)

    except Exception as e:
        print(
            "There was an error fetching your token. If this persists, please run the tool with the -v flag and contact support@cyral.com with the output. We’d be happy to help!"
        )
        if verbose:
            raise e


def run():
    update_token(prog_name="gimme_db_token")


if __name__ == "__main__":
    run()
