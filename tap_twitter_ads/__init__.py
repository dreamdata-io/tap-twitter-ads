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
        os.path.dirname(os.path.abspath(__file__)), CREDENTIALS_FILENAME
    )
    credentials = ""
    if os.path.exists(credential_path):
        with open(credential_path, "r") as file:
            twitter_credentials = file.read()
            if twitter_credentials:
                credentials = json.loads(twitter_credentials)

    if not credentials or credentials == "":
        # Get new credentials

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
