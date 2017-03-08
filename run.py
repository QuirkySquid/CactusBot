#!/usr/bin/env python3.5

"""Run CactusBot."""

import logging
from argparse import ArgumentParser
from asyncio import get_event_loop

from cactusbot.cactus import run
from config import SERVICE, api

if __name__ == "__main__":

    parser = ArgumentParser(description="Run CactusBot.")

    parser.add_argument(
        "--debug",
        help="set custom logger level",
        metavar="LEVEL",
        nargs='?',
        const="DEBUG",
        default="INFO"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=args.debug,
        format="{asctime} {levelname} {name} {funcName}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style='{'
    )

    loop = get_event_loop()

    try:
        # TODO: Convert this to be able to have multiple services
        loop.run_until_complete(run(api, SERVICE))
        loop.run_forever()
    finally:
        loop.close()
