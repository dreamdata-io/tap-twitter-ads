#!/usr/bin/env python3

import asyncio
import json
import os

import singer

from singer import utils, metadata, metrics, Transformer
from requests_oauthlib import OAuth1Session

LOGGER = singer.get_logger()

CONFIG = {}
STATE = {}

REQUIRED_CONFIG_KEYS = [
    "start_date",
    "request_token_url",
    "access_token_url",
    "authorize_url",
    "consumer_key",
    "consumer_secret",
]

CREDENTIALS_FILENAME = "twitter.json"


def get_credentials():
    """ Get credentials """

    credential_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        CREDENTIALS_FILENAME,
    )
    credentials = ""
    if os.path.exists(credential_path):
        with open(credential_path, "r") as file:
            twitter_credentials = file.read()
            if twitter_credentials:
                credentials = json.loads(twitter_credentials)

    if not credentials or credentials == "":
        # Get new credentials
        credentials_file = open(credential_path, "w+")

        # Step 1: Obtain a request token which will identify you (the client) in the next step.
        # At this stage you will only need your consumer key and secret.
        oauth = OAuth1Session(
            CONFIG["consumer_key"],
            client_secret=CONFIG["consumer_secret"],
            callback_uri="http://localhost:3000/oauth/validate",
        )
        fetch_response = oauth.fetch_request_token(CONFIG["request_token_url"])
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")

        # Step 2: Obtain authorization from the user (resource owner) to access their protected resources.
        # This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter.
        # Note that not all services will give you a verifier even if they should.
        # Also the oauth_token given here will be the same as the one in the previous step.

        authorization_url = oauth.authorization_url(CONFIG["authorize_url"])
        print("Please go here and authorize,", authorization_url)
        redirect_response = input(
            "Paste the full redirect URL here (with token and verifier): "
        )
        oauth_response = oauth.parse_authorization_response(redirect_response)

        oauth_verifier = oauth_response.get("oauth_verifier")

        # Step 3: Obtain an access token from the OAuth provider. Save this token as it can be re-used later.
        # In this step we will re-use most of the credentials obtained uptil this point.
        oauth = OAuth1Session(
            CONFIG["consumer_key"],
            client_secret=CONFIG["consumer_secret"],
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=oauth_verifier,
        )
        oauth_tokens = oauth.fetch_access_token(CONFIG["access_token_url"])

        new_credentials = {
            "oauth_token": oauth_tokens.get("oauth_token"),
            "oauth_token_secret": oauth_tokens.get("oauth_token_secret"),
        }

        credentials_file.write(json.dumps(new_credentials))
        credentials_file.close()

        credentials = new_credentials

    return credentials


def do_discover():
    LOGGER.info("Testing authentication")

    credentials = get_credentials()

    print(credentials)

    LOGGER.info("Discovering core objects")
    # core_object_streams = discover_core_objects()

    LOGGER.info("Discovering reports")
    # report_streams = discover_reports()

    # json.dump({"streams": core_object_streams + report_streams}, sys.stdout, indent=2)


async def main_impl():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    CONFIG.update(args.config)
    STATE.update(args.state)

    if args.discover:
        do_discover()
        LOGGER.info("Discovery complete")
    elif args.catalog:
        # await do_sync_all_accounts(account_ids, args.catalog)
        LOGGER.info("Sync Completed")
    else:
        LOGGER.info("No catalog was provided")


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_impl())
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc
