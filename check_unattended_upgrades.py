#! /usr/bin/env python3

import argparse
from argparse import ArgumentParser
import nagiosplugin
from typing import cast
import re
from datetime import datetime
import gzip

__version__: str = "1.4"


class OptionContainer:
    pass


opts: OptionContainer = OptionContainer()

LOG_FILE = "/var/log/unattended-upgrades/unattended-upgrades.log"


def get_argparser() -> ArgumentParser:
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="check_unattended_upgrades",  # To get the right command name in the README.
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog, width=80
        ),  # noqa: E501
        description="Copyright (c) 2015-22 Josef Friedrich <josef@friedrich.rocks>\n"
        "\n"
        "Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.\n",  # noqa: E501
        epilog="Performance data:\n"
        "  - last_ago\n"
        "       Time interval in seconds for last unattended-upgrades execution.\n"
        "  - warning\n"
        "       Interval in seconds.\n"
        "  - critical\n"
        "       Interval in seconds.\n"
        "\n"
        "About file system permissions:\n"
        "   The user which executes this plugin must have read permissions to this\n"
        "   log file:\n"
        "\n"
        "       /var/log/unattended-upgrades/unattended-upgrades.log\n"
        "\n"
        "   To allow every user on your system to read the mentioned log file this\n"
        "   permissions are recommended:\n"
        "\n"
        "       751 (drwxr-x--x) /var/log/unattended-upgrades\n"
        "       644 (-rw-r--r--) /var/log/unattended-upgrades/unattended-upgrades.log\n",
    )

    parser.add_argument(
        "-A",
        "--anacron",
        action="store_true",
        help="Check if the package 'anacron' is installed.",
    )

    parser.add_argument(
        "-a",
        "--autoclean",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::AutocleanInterval' is set properly.",
    )

    parser.add_argument(
        "-c",
        "--critical",
        help="Time interval since the last execution to result in a critical state (seconds).",
    )

    parser.add_argument(
        "-D",
        "--short-description",
        action="store_true",
        help="Show a short description of this check plugin.",
    )

    parser.add_argument(
        "-d",
        "--download",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages' is set properly.",
    )

    parser.add_argument(
        "-e",
        "--enable",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Enable' is set properly",
    )

    parser.add_argument(
        "-l",
        "--lists",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Update-Package-Lists' is set properly.",
    )

    parser.add_argument(
        "-m",
        "--mail",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'Unattended-Upgrade::Mail' is set properly.",
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Check if 'unattended-upgrades --dry-run' is working. Warning: If you use this option the performance data last_ago is always 0 or near to 0.",
    )

    parser.add_argument(
        "-p",
        "--repo",
        help="Check if 'Unattended-upgrades' is configured to include the specified custom repository.",
    )

    parser.add_argument(
        "-R",
        "--reboot",
        action="store_true",
        help="Check if the machine needs a reboot.",
    )

    parser.add_argument(
        "-r",
        "--remove",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'Unattended-Upgrade::Remove-Unused- Dependencies' is set properly.",
    )

    parser.add_argument(
        "-S",
        "--security",
        action="store_true",
        help="Check if 'Unattended-upgrades' is configured to handle security updates.",
    )

    parser.add_argument(
        "-s",
        "--sleep",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::RandomSleep' is set properly.",
    )

    parser.add_argument(
        "-t",
        "--systemd-timers",
        action="store_true",
        help="Check if the appropriate Systemd timers are enabled ( apt-daily-upgrade.timer, apt-daily.timer ).",
    )

    parser.add_argument(
        "-u",
        "--unattended",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Unattended-Upgrade' is set properly.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
    )

    parser.add_argument(
        "-w",
        "--warning",
        help="Time interval since the last execution to result in a warning state (seconds).",
    )

    return parser


def read_zipped_log_file():
    # with ZipFile(LOG_FILE + ".1.gz") as zip_file:
    #     with zip_file.open('unattended-upgrades.log.1') as file:
    #         for line in file.readlines():
    #             print(line)

    with gzip.open(LOG_FILE + ".1.gz", "r") as f:
        file_content = f.read()
        print(file_content.decode("utf-8"))


class LogFile(nagiosplugin.Resource):
    def probe(self):
        with open(LOG_FILE, "r") as log_file:
            for line in log_file.readlines():
                line.find(" ")
                match = re.match(
                    r"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d),\d\d\d (DEBUG|INFO|WARNING|ERROR|EXCEPTION) (.*)\n$",
                    line,
                )
                if match:
                    time = match[1]
                    log_level = match[2]
                    message = match[3]

                    print(time, log_level, message)

                    print(datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        return nagiosplugin.Metric("log", 0)


# @guarded(verbose=0)
def main():
    global opts

    read_zipped_log_file()

    opts = cast(OptionContainer, get_argparser().parse_args())

    check = nagiosplugin.Check(LogFile(), nagiosplugin.Context("log"))
    check.main()


if __name__ == "__main__":
    main()
