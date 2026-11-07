#! /usr/bin/env python3


"""
Monitoring scopes
=================

* ``anacron``: Check if the package 'anacron' is installed.
* ``config``: Check some configuration values using “apt-config dump”.
* ``custom_repo``: Check if 'unattended-upgrades' is configured to include the
                   specified custom repository.
* ``dry_run``: Check if “unattended-upgrades --dry-run” is working.
* ``errors_in_log``: Check if there are any errors in the log files concerning
                     the last run.
* ``last_run``: Check when the program was last run.
* ``reboot``: Check if the machine needs a reboot.
* ``security``: Check if 'unattended-upgrades' is configured to handle
                security updates.
* ``systemd_timers``: Check if the appropriate systemd timers are enabled.
"""

from __future__ import annotations

import argparse
import datetime
import gzip
import os
import pathlib
import re
import shutil
import subprocess
import typing
from importlib import metadata

import mplugin
from mplugin.cli import setup_argparser
from mplugin.timespan import TIMESPAN_FORMAT_HELP, convert_timespan_to_sec

__version__: str = metadata.version("check_unattended_upgrades")


class OptionContainer:
    anacron: bool
    autoclean: str | None
    critical: int
    custom_repos: list[str] | None
    download: str | None
    dry_run: bool
    enable: str | None
    format: str | None
    lists: str | None
    mail: str | None
    reboot: bool
    remove: str | None
    security: bool
    sleep: str | None
    systemd_timers: bool
    unattended: str | None
    verbose: int
    warning: int


opts: OptionContainer = OptionContainer()

LOG_FILE = "/var/log/unattended-upgrades/unattended-upgrades.log"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, encoding="utf-8", capture_output=True)


def get_argparser() -> argparse.ArgumentParser:
    parser = setup_argparser(
        name="unattended_upgrades",
        version=__version__,
        license="MIT",
        copyright="Copyright (c) 2015-2026 Josef Friedrich <josef@friedrich.rocks>",
        description="Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu",
        epilog="Performance data:\n"
        "  - last_ago\n"
        "       Time interval in seconds for last unattended-upgrades execution.\n"
        "  - warning\n"
        "       Interval of time units defined in '--format'.\n"
        "  - critical\n"
        "       Interval of time units defined in '--format'.\n"
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
        "       644 (-rw-r--r--) "
        "/var/log/unattended-upgrades/unattended-upgrades.log\n" + TIMESPAN_FORMAT_HELP,
        verbose=True,
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
        help="Check if the configuration 'APT::Periodic::AutocleanInterval' "
        "is set properly.",
    )

    parser.add_argument(
        "-w",
        "--warning",
        default=93600,  # 26h = 1d + 2h
        type=convert_timespan_to_sec,
        metavar="TIMESPAN",
        help="Time interval since the last execution to result in a "
        "warning state. See timespan format specification below "
        "or specify a number without time units and use the '--format' option "
        "to select the time unit.",
    )

    parser.add_argument(
        "-c",
        "--critical",
        default=187200,  # 52h = 2d + 4h
        type=convert_timespan_to_sec,
        metavar="TIMESPAN",
        help="Time interval since the last execution to result in a critical "
        "state. See timespan format specification below "
        "or specify a number without time units and use the '--format' option "
        "to select the time unit.",
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
        help="Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages' "
        "is set properly.",
    )

    parser.add_argument(
        "-e",
        "--enable",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Enable' is set properly",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["seconds", "minutes", "hours", "days"],
        default="seconds",
        metavar="UNIT",
        help="Defines the unit for the numbers of '--warning' and '--critical', "
        "also the output of 'last-run'. Allowed values are: "
        "'seconds', 'minutes', 'hours' and 'days', default: 'seconds'.",
    )

    parser.add_argument(
        "-l",
        "--lists",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Update-Package-Lists' "
        "is set properly.",
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
        help="Check if 'unattended-upgrades --dry-run' is working. Warning: "
        "If you use this option the performance data last_ago is "
        "always 0 or near to 0.",
    )

    parser.add_argument(
        "-p",
        "--repo",
        "--custom-repo",
        dest="custom_repos",
        action="append",
        help="Check if 'Unattended-upgrades' is configured to include the "
        "specified custom repository.",
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
        help="Check if the configuration "
        "'Unattended-Upgrade::Remove-Unused-Dependencies' is set properly.",
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
        help="Check if the appropriate systemd timers are enabled "
        "( apt-daily-upgrade.timer, apt-daily.timer ).",
    )

    parser.add_argument(
        "-u",
        "--unattended",
        metavar="CONFIG_VALUE",
        help="Check if the configuration 'APT::Periodic::Unattended-Upgrade' "
        "is set properly.",
    )

    return parser


# auxiliary classes ###########################################################

# apt config ##################################################################


class AptConfig:
    __cache: dict[str, str] | None = None

    @staticmethod
    def __read_all_config_values() -> dict[str, str]:
        process: subprocess.CompletedProcess[str] = subprocess.run(
            ("apt-config", "dump"),
            check=False,
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )

        cache: dict[str, str] = {}

        for line in process.stdout.splitlines():
            match: re.Match[str] | None = re.match(r'(.*) "(.*)";', line)

            if match:
                key: str = match[1]
                value: str = match[2]
                # Handle multiline config values like:
                # Unattended-Upgrade::Origins-Pattern "";
                # Unattended-Upgrade::Origins-Pattern:: "origin=*";
                # Unattended-Upgrade::Origins-Pattern:: "o=Canonical";
                if re.match(r".+::$", key):
                    key = key[:-2]
                    cache[key] += value
                else:
                    cache[key] = value

        return cache

    @staticmethod
    def get(key: str) -> str | None:
        if not AptConfig.__cache:
            AptConfig.__cache = AptConfig.__read_all_config_values()

        if key in AptConfig.__cache:
            return AptConfig.__cache[key]
        return None

    @staticmethod
    def reset() -> None:
        AptConfig.__cache = None

    @staticmethod
    def get_repos() -> str | None:
        output: str = ""

        allowed_origins = AptConfig.get("Unattended-Upgrade::Allowed-Origins")

        if allowed_origins:
            output += allowed_origins

        origins_pattern = AptConfig.get("Unattended-Upgrade::Origins-Pattern")

        if origins_pattern:
            output += origins_pattern

        if output != "":
            return output
        return None


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

    @property
    def level(self) -> LogLevel:
        return self.__level

    @property
    def message(self) -> str:
        return self.__message


class Run:
    """Collection of all log messages of an execution of the
    unattended-upgrades script."""

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
    runs: typing.ClassVar[list[Run]] = []

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
            r"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d),\d\d\d "
            r"(DEBUG|INFO|WARNING|ERROR|EXCEPTION) (.*)\n?$",
            line,
        )
        if match:
            message: LogMessage = LogMessage(
                time=datetime.datetime.strptime(match[1], "%Y-%m-%d %H:%M:%S"),
                level=typing.cast(LogLevel, match[2]),
                message=match[3],
            )
            return message
        return None

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
    def reset() -> None:
        LogParser.runs = []

    @staticmethod
    def parse() -> list[Run]:
        if len(LogParser.runs) > 0:
            return LogParser.runs
        main_log_file: pathlib.Path = pathlib.Path(LOG_FILE)
        zipped_log_file: pathlib.Path = pathlib.Path(LOG_FILE + ".1.gz")

        messages: list[LogMessage] = []

        if main_log_file.exists():
            messages = LogParser.__parsed_main(main_log_file)

        if len(messages) == 0 and zipped_log_file.exists():
            messages = LogParser.__parse_zipped(zipped_log_file)

        runs: list[Run] = []
        if len(messages) > 0:
            run: Run = Run()
            for message in messages:
                if message.time - run.end_time > 500:
                    run = Run()
                    runs.append(run)
                run.add_message(message)
        LogParser.runs = runs
        return runs


# scope: anacron ##############################################################


class AnacronResource(mplugin.Resource):
    def probe(self) -> mplugin.Metric:
        return mplugin.Metric("anacron", shutil.which("anacron"))


class AnacronContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("anacron")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        if metric.value is not None:
            return self.ok(
                metric=metric,
                hint="Package 'anacron' is installed in: " + metric.value,
            )
        else:
            return self.critical(
                metric=metric,
                hint="Package 'anacron' is not installed.",
            )


# scope: config ###############################################################


class ConfigResource(mplugin.Resource):
    key: str

    expected: str

    def __init__(self, key: str, expected: str) -> None:
        self.key = key
        self.expected = expected

    def probe(self) -> mplugin.Metric:
        value = AptConfig.get(self.key)
        return mplugin.Metric(name=self.key, value=value, context="config")


class ConfigContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("config")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        r: ConfigResource = typing.cast(ConfigResource, resource)

        if metric.value == r.expected:
            return self.ok(
                metric=metric,
                hint=f"Configuration value for “{r.key}”: {metric.value}",
            )
        else:
            return self.critical(
                metric=metric,
                hint=f"Configuration value for “{r.key}” unexpected! "
                f"actual: {metric.value} expected: {r.expected}",
            )


# scope: custom_repo ##########################################################


class CustomRepoResource(mplugin.Resource):
    repo: str

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    def probe(self) -> mplugin.Metric:
        return mplugin.Metric(self.repo, AptConfig.get_repos())


class CustomRepoContext(mplugin.Context):
    def __init__(self, repo: str) -> None:
        super().__init__(repo)

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        if self.name in metric.value:
            return self.ok(
                metric=metric,
                hint=f"Handling updates for custom repository '{self.name}'.",
            )

        else:
            return self.critical(
                metric=metric,
                hint="Unattended-upgrades is not configured to handle updates "
                f"for custom repository '{self.name}'.",
            )


# scope: dry_run ##############################################################


class DryRunResource(mplugin.Resource):
    def probe(self) -> mplugin.Metric:
        process: subprocess.CompletedProcess[bytes] = subprocess.run(
            ("unattended-upgrades", "--dry-run"), check=False
        )
        return mplugin.Metric("dry_run", process.returncode)


class DryRunContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("dry_run")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        if metric.value == 0:
            return self.ok(
                metric=metric,
                hint="unattended-upgrades --dry-run exits with a zero status (OK).",
            )
        else:
            return self.critical(
                metric=metric,
                hint="unattended-upgrades --dry-run exits with a non-zero status.",
            )


# scope: errors_in_log ########################################################


class WarningsInLogResource(mplugin.Resource):
    def probe(self) -> typing.Generator[mplugin.Metric, None, None]:
        runs = LogParser.parse()
        if len(runs) > 0:
            last_run = runs[-1]
            for message in last_run.log_messages:
                if (
                    message.level == "WARNING"
                    or message.level == "ERROR"
                    or message.level == "EXCEPTION"
                ):
                    yield mplugin.Metric("errors_in_log", message)


class WarningsInLogContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("errors_in_log")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        message: LogMessage = metric.value

        state: mplugin.ServiceState = mplugin.ok

        if message.level == "ERROR" or message.level == "EXCEPTION":
            state = mplugin.critical
        elif message.level == "WARNING":
            state = mplugin.warning

        return self.result(state, metric=metric, hint=message.message)


# scope: last_run #############################################################


class LastRunResource(mplugin.Resource):
    def probe(self) -> mplugin.Metric:
        runs = LogParser.parse()
        if len(runs) == 0:
            return mplugin.Metric("last_run", 0)
        return mplugin.Metric("last_run", runs[-1].end_time)


class LastRunContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("last_run")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        interval: int = 0
        total_seconds: int = int(datetime.datetime.now().timestamp() - metric.value)
        total_minutes: int = total_seconds // 60
        total_hours: int = total_minutes // 60
        total_days: int = total_hours // 24

        if opts.format == "days":
            interval = total_days
            hint = f"last-run was {total_days} days, {total_hours % 24} hours and {total_minutes % 60} minutes ago"
        elif opts.format == "hours":
            interval = total_hours
            hint = f"last-run was {total_hours} hours, {total_minutes % 60} minutes and {total_seconds % 60} seconds ago"
        elif opts.format == "minutes":
            interval = total_minutes
            hint = f"last-run was {total_minutes} minutes and {total_seconds % 60} seconds ago"
        else:
            interval = total_seconds
            hint = f"last-run was {total_seconds} seconds ago"

        if interval > opts.critical:
            return self.critical(metric=metric, hint=hint)
        elif interval > opts.warning:
            return self.warning(metric=metric, hint=hint)
        else:
            return self.ok(metric=metric, hint=hint)


# scope: reboot ###############################################################


class RebootResource(mplugin.Resource):
    def probe(self) -> mplugin.Metric:
        # os.path.exists instead of pathlib.Path for better testing and mocking
        return mplugin.Metric("reboot", os.path.exists("/var/run/reboot-required"))


class RebootContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("reboot")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        if not metric.value:
            return self.ok(
                metric=metric,
                hint="No reboot required yet.",
            )
        else:
            return self.warning(
                metric=metric,
                hint="The machine requires a reboot.",
            )


# scope: security #############################################################


class SecurityResource(mplugin.Resource):
    def probe(self) -> mplugin.Metric:
        repos = AptConfig.get_repos()
        return mplugin.Metric("security", repos and "security" in repos)


class SecurityContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("security")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        if metric.value:
            return self.ok(
                metric=metric,
                hint="unattended-upgrades is handling security updates.",
            )
        else:
            return self.critical(
                metric=metric,
                hint="unattended-upgrades is not configured to handle "
                "security updates.",
            )


# scope: systemd_timers #######################################################


class SystemdTimersResource(mplugin.Resource):
    def __is_enabled(self, timer_name: str) -> bool:
        process: subprocess.CompletedProcess[str] = run(
            "systemctl", "is-enabled", timer_name
        )
        return process.returncode == 0

    def probe(self) -> typing.Generator[mplugin.Metric, None, None]:
        for timer_name in ("apt-daily.timer", "apt-daily-upgrade.timer"):
            is_enabled: bool = self.__is_enabled(timer_name)
            yield mplugin.Metric("systemd_timers", [timer_name, is_enabled])


class SystemdTimersContext(mplugin.Context):
    def __init__(self) -> None:
        super().__init__("systemd_timers")

    def evaluate(
        self, metric: mplugin.Metric, resource: mplugin.Resource
    ) -> mplugin.Result:
        state: mplugin.ServiceState = mplugin.ok
        not_string = ""
        if not metric.value[1]:
            state = mplugin.critical
            not_string = "not "
        return self.result(
            state,
            metric=metric,
            hint=f"The systemd timer “{metric.value[0]}” is {not_string}enabled.",
        )


###############################################################################
# Summary
###############################################################################


class UnattendedUpgradesSummary(mplugin.Summary):
    def ok(self, results: mplugin.Results) -> str:
        return "all"

    def problem(self, results: mplugin.Results) -> str:
        return ", ".join(f"{result}" for result in results.most_significant)

    def verbose(self, results: mplugin.Results) -> list[str]:
        summary: list[str] = []
        for result in results.results:
            summary.append(f"{str(result.state).upper()}: {result}")
        return summary


class ChecksCollection:
    checks: list[mplugin.Resource | mplugin.Context | mplugin.Summary]

    def __init__(self, opts: OptionContainer) -> None:
        self.checks = [
            LastRunResource(),
            LastRunContext(),
            WarningsInLogResource(),
            WarningsInLogContext(),
            UnattendedUpgradesSummary(),
        ]

        if opts.anacron:
            self.checks += [AnacronResource(), AnacronContext()]

        if opts.dry_run:
            self.checks += [DryRunResource(), DryRunContext()]

        if opts.reboot:
            self.checks += [RebootResource(), RebootContext()]

        if opts.security:
            self.checks += [SecurityResource(), SecurityContext()]

        if opts.systemd_timers:
            self.checks += [SystemdTimersResource(), SystemdTimersContext()]

        self.check_config("APT::Periodic::AutocleanInterval", opts.autoclean)
        self.check_config("APT::Periodic::Download-Upgradeable-Packages", opts.download)
        self.check_config("APT::Periodic::Enable", opts.enable)
        self.check_config("APT::Periodic::RandomSleep", opts.sleep)
        self.check_config("APT::Periodic::Unattended-Upgrade", opts.unattended)
        self.check_config("APT::Periodic::Update-Package-Lists", opts.lists)
        self.check_config("Unattended-Upgrade::Mail", opts.mail)
        self.check_config("Unattended-Upgrade::Remove-Unused-Dependencies", opts.remove)

        if opts.custom_repos:
            for repo in opts.custom_repos:
                self.checks += [CustomRepoResource(repo), CustomRepoContext(repo)]

    def check_config(self, key: str, expected: str | None) -> None:
        if expected:
            self.checks.append(ConfigResource(key, expected))
            self.checks.append(ConfigContext())


# @guarded(verbose=0)
def main() -> None:
    global opts

    opts = typing.cast(OptionContainer, get_argparser().parse_args())

    LogParser.reset()
    AptConfig.reset()

    checks: ChecksCollection = ChecksCollection(opts)
    check: mplugin.Check = mplugin.Check(*checks.checks)
    check.name = "unattended_upgrades"
    check.main(opts.verbose)


if __name__ == "__main__":
    main()
