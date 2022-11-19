#! /usr/bin/env python3

import argparse
from argparse import ArgumentParser
import nagiosplugin


class OptionContainer:
    pass

opts: OptionContainer = OptionContainer()

def get_argparser() -> ArgumentParser:
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="check_zpool_scrub",  # To get the right command name in the README.
    )
    return parser


@nagiosplugin.guarded(verbose=0)
def main():
    pass
    global opts
    opts = get_argparser().parse_args()

if __name__ == "__main__":
    main()
