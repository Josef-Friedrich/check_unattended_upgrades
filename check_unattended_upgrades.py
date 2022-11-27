#! /usr/bin/env python3

import argparse
import datetime
import gzip
import nagiosplugin
import re
import shutil
import subprocess
import typing
import pathlib

__version__: str = "1.4"


class OptionContainer:
    anacron: bool
    autoclean: str | None
    critical: int
    download: str | None
    enable: str | None
    lists: str | None
    mail: str | None
    dry_run: bool
    repo: str
    reboot: bool
    remove: str | None
    security: bool
    sleep: str | None
    systemd_timers: bool
    unattended: str | None
    warning: int


opts: OptionContainer = OptionContainer()

LOG_FILE = "/var/log/unattended-upgrades/unattended-upgrades.log"


def get_argparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
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


# reboot ######################################################################


class RebootResource(nagiosplugin.Resource):
    name: typing.Literal["reboot"] = "reboot"

    def probe(self) -> nagiosplugin.Metric:
        path = pathlib.Path("/var/run/reboot-required")
        return nagiosplugin.Metric("reboot", path.exists())


class RebootContext(nagiosplugin.Context):
    def __init__(self) -> None:
        super(RebootContext, self).__init__("reboot")

    def evaluate(
        self, metric: nagiosplugin.Metric, resource: nagiosplugin.Resource
    ) -> nagiosplugin.Result:
        if metric.value:
            return self.result_cls(
                nagiosplugin.Ok,
                metric=metric,
            )
        else:
            return self.result_cls(
                nagiosplugin.Critical,
                metric=metric,
                hint="The machine requires a reboot.",
            )


# anacron #####################################################################


class AnacronResource(nagiosplugin.Resource):
    name: typing.Literal["anacron"] = "anacron"

    def probe(self) -> nagiosplugin.Metric:
        return nagiosplugin.Metric("anacron", shutil.which("anacron"))


class AnacronContext(nagiosplugin.Context):
    def __init__(self) -> None:
        super(AnacronContext, self).__init__("anacron")

    def evaluate(
        self, metric: nagiosplugin.Metric, resource: nagiosplugin.Resource
    ) -> nagiosplugin.Result:
        if metric.value is not None:
            return self.result_cls(
                nagiosplugin.Ok,
                metric=metric,
                hint="Package 'anacron' is installed in: " + metric.value,
            )
        else:
            return self.result_cls(
                nagiosplugin.Critical,
                metric=metric,
                hint="Package 'anacron' is not installed.",
            )


# dry-run #####################################################################


class DryRunResource(nagiosplugin.Resource):
    name: typing.Literal["dry-run"] = "dry-run"

    def probe(self) -> nagiosplugin.Metric:
        process: subprocess.CompletedProcess[bytes] = subprocess.run(
            ("unattended-upgrades", "--dry-run")
        )
        return nagiosplugin.Metric("dry-run", process.returncode)


class DryRunContext(nagiosplugin.Context):
    def __init__(self) -> None:
        super(DryRunContext, self).__init__("dry-run")

    def evaluate(
        self, metric: nagiosplugin.Metric, resource: nagiosplugin.Resource
    ) -> nagiosplugin.Result:
        if metric.value == 0:
            return self.result_cls(nagiosplugin.Ok, metric=metric)
        else:
            return self.result_cls(
                nagiosplugin.Critical,
                metric=metric,
                hint="unattended-upgrades --dry-run exits with a non-zero status.",
            )


# config ######################################################################


class AptConfig:

    __cache: dict[str, str] | None = None

    @staticmethod
    def __read_all_config_values() -> dict[str, str]:
        process: subprocess.CompletedProcess[str] = subprocess.run(
            ("apt-config", "dump"), encoding="utf-8", stdout=subprocess.PIPE
        )

        cache: dict[str, str] = {}

        for line in process.stdout.splitlines():
            match: re.Match[str] | None = re.match(r'(.*) "(.*)";', line)
            if match:
                cache[match[1]] = match[2]

        return cache

    @staticmethod
    def get(key: str) -> str:
        if not AptConfig.__cache:
            AptConfig.__cache = AptConfig.__read_all_config_values()
        return AptConfig.__cache[key]


class ConfigResource(nagiosplugin.Resource):

    key: str

    name: typing.Literal["config"] = "config"

    def __init__(self, key: str) -> None:
        self.key = key

    def probe(self) -> nagiosplugin.Metric:
        value = AptConfig.get(self.key)
        return nagiosplugin.Metric("config", value)


class ConfigContext(nagiosplugin.Context):

    expected: str

    def __init__(self, expected: str) -> None:
        super(ConfigContext, self).__init__("config")
        self.expected = expected

    def evaluate(
        self, metric: nagiosplugin.Metric, resource: nagiosplugin.Resource
    ) -> nagiosplugin.Result:
        r: ConfigResource = typing.cast(ConfigResource, resource)
        if metric.value == self.expected:
            return self.result_cls(nagiosplugin.Ok, metric=metric)
        else:
            return self.result_cls(
                nagiosplugin.Critical,
                metric=metric,
                hint="{} actual: {} expected: {}".format(
                    r.key, metric.value, self.expected
                ),
            )


# log #########################################################################

LogLevel = typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "EXCEPTION"]


class LogMessage:

    __time: datetime.datetime
    __level: LogLevel
    __message: str

    def __init__(self, time: datetime.datetime, level: LogLevel, message: str) -> None:
        self.__time = time
        self.__level = level
        self.__message = message

    @property
    def time(self) -> float:
        return self.__time.timestamp()


class Execution:

    log_messages: list[LogMessage]

    def __init__(self) -> None:
        self.log_messages = []

    @property
    def start_time(self) -> float:
        if len(self.log_messages) > 0:
            return self.log_messages[0].time
        return 0

    @property
    def end_time(self) -> float:
        if len(self.log_messages) > 0:
            return self.log_messages[-1].time

        return 0

    def add_message(self, message: LogMessage) -> None:
        self.log_messages.append(message)


class LogParser:
    @staticmethod
    def __read_lines(content: str) -> list[LogMessage]:
        messages: list[LogMessage] = []
        for line in content.splitlines():
            message = LogParser.__read_log_line(line)
            if message:
                messages.append(message)
        return messages

    @staticmethod
    def __read_log_line(line: str) -> LogMessage | None:
        match = re.match(
            r"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d),\d\d\d (DEBUG|INFO|WARNING|ERROR|EXCEPTION) (.*)\n?$",
            line,
        )
        if match:
            message: LogMessage = LogMessage(
                time=datetime.datetime.strptime(match[1], "%Y-%m-%d %H:%M:%S"),
                level=typing.cast(LogLevel, match[2]),
                message=match[3],
            )
            return message

    @staticmethod
    def __parse_zipped(path: pathlib.Path) -> list[LogMessage]:
        with gzip.open(path, "r") as f:
            file_content: bytes = f.read()
            return LogParser.__read_lines(file_content.decode("utf-8"))

    @staticmethod
    def __parsed_main(path: pathlib.Path) -> list[LogMessage]:
        with open(path, "r") as log_file:
            return LogParser.__read_lines(log_file.read())

    @staticmethod
    def parse() -> list[Execution]:
        main_log_file: pathlib.Path = pathlib.Path(LOG_FILE)
        zipped_log_file: pathlib.Path = pathlib.Path(LOG_FILE + ".1.gz")

        messages: list[LogMessage] = []

        if main_log_file.exists():
            messages = LogParser.__parsed_main(main_log_file)

        if len(messages) == 0:
            if zipped_log_file.exists():
                messages = LogParser.__parse_zipped(zipped_log_file)

        executions: list[Execution] = []
        if len(messages) > 0:
            execution: Execution = Execution()
            for message in messages:
                if message.time - execution.end_time > 500:
                    execution = Execution()
                    executions.append(execution)
                execution.add_message(message)

        return executions


class LogResource(nagiosplugin.Resource):
    def probe(self) -> nagiosplugin.Metric:
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

                    print(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S"))
        return nagiosplugin.Metric("log", 0)


class ChecksCollection:

    checks: list[nagiosplugin.Resource | nagiosplugin.Context] = []

    def __init__(self, opts: OptionContainer) -> None:
        if opts.reboot:
            self.checks += [RebootResource(), RebootContext()]
        if opts.dry_run:
            self.checks += [DryRunResource(), DryRunContext()]
        if opts.anacron:
            self.checks += [AnacronResource(), AnacronContext()]

        self.check_config("APT::Periodic::AutocleanInterval", opts.autoclean)
        self.check_config("APT::Periodic::Download-Upgradeable-Packages", opts.download)
        self.check_config("APT::Periodic::Enable", opts.enable)
        self.check_config("APT::Periodic::RandomSleep", opts.sleep)
        self.check_config("APT::Periodic::Unattended-Upgrade", opts.unattended)
        self.check_config("APT::Periodic::Update-Package-Lists", opts.lists)
        self.check_config("Unattended-Upgrade::Mail", opts.mail)
        self.check_config("Unattended-Upgrade::Remove-Unused-Dependencies", opts.remove)

    def check_config(self, key: str, expected: str | None) -> None:
        if expected:
            self.checks.append(ConfigResource(key))
            self.checks.append(ConfigContext(expected))


# @guarded(verbose=0)
def main() -> None:
    global opts

    opts = typing.cast(OptionContainer, get_argparser().parse_args())

    LogParser.parse()

    checks: ChecksCollection = ChecksCollection(opts)
    check: nagiosplugin.Check = nagiosplugin.Check(*checks.checks)
    check.main()


if __name__ == "__main__":
    main()
