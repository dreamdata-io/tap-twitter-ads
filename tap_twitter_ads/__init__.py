#!/usr/bin/env python3

import asyncio

import singer

from singer import utils, metadata, metrics, Transformer

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


def do_discover():
    LOGGER.info("Testing authentication")
    # test_credentials(account_ids)

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
