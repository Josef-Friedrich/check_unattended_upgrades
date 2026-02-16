from __future__ import annotations

import io
import os
import subprocess
import typing
from contextlib import redirect_stderr, redirect_stdout
from unittest import TestCase, mock
from unittest.mock import Mock

from freezegun import freeze_time

import check_unattended_upgrades

test: TestCase = TestCase()
test.maxDiff = None


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["./src/check_unattended_upgrades/__init__.py"] + args,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def read_text_file(file_name: str) -> str:
    file: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "files", file_name
    )
    with open(file, "r") as f:
        return f.read()


class MockResult:
    """A class to collect all results of a mocked execution of the main
    function."""

    __sys_exit: Mock
    __stdout: str | None
    __stderr: str | None

    def __init__(self, sys_exit_mock: Mock, stdout: str, stderr: str) -> None:
        self.__sys_exit = sys_exit_mock
        self.__stdout = stdout
        self.__stderr = stderr

    @property
    def exitcode(self) -> int:
        """The captured exit code"""
        return int(self.__sys_exit.call_args[0][0])

    @property
    def stdout(self) -> str | None:
        """The function ``redirect_stdout()`` is used to capture the ``stdout``
        output."""
        if self.__stdout:
            return self.__stdout
        return None

    @property
    def stderr(self) -> str | None:
        """The function ``redirect_stderr()`` is used to capture the ``stderr``
        output."""
        if self.__stderr:
            return self.__stderr
        return None

    @property
    def output(self) -> str:
        """A combined string of the captured stderr, stdout  and the print
        calls. Somehow the whole stdout couldn’t be read. The help text could
        be read, but not the plugin output using the function
        ``redirect_stdout()``."""
        out: str = ""

        if self.__stderr:
            out += self.__stderr

        if self.__stdout:
            out += self.__stdout

        return out

    def assert_exitcode(self, exitcode: int) -> None:
        assert self.exitcode == exitcode

    def assert_ok(self) -> None:
        self.assert_exitcode(0)

    def assert_warn(self) -> None:
        self.assert_exitcode(1)

    def assert_critical(self) -> None:
        self.assert_exitcode(2)

    def assert_unknown(self) -> None:
        self.assert_exitcode(3)

    @property
    def first_line(self) -> str | None:
        """The first line of the output without a newline break at the
        end as a string.
        """
        if self.output:
            return self.output.split("\n", 1)[0]
        return None

    def assert_first_line(self, first_line: str) -> None:
        assert self.first_line == first_line, self.first_line

    def assert_output(self, output: str) -> None:
        assert self.output == output, self.output


class CompletedProcess:
    returncode: int = 0
    stdout: str


def execute_main(
    argv: list[str] = ["check_unattended_upgrades.py"],
    main_log_file: str = "info.log",
    time: str = "2017-09-01 10:55:34",
    systemd_apt_daily_timer: bool = True,
    systemd_apt_daily_upgrade_timer: bool = True,
    anacron: str | None = "/usr/sbin/anacron",
    dry_run: int = 0,
    reboot: bool = False,
    apt_config: typing.Literal["default.txt", "allowed-origins.txt"] = "default.txt",
) -> MockResult:
    def perform_subprocess_run_side_effect(
        args: list[str], **kwargs: typing.Any
    ) -> CompletedProcess:
        command: str = " ".join(args)
        process: CompletedProcess = CompletedProcess()

        if command == "apt-config dump":
            process.returncode = 0
            process.stdout = read_text_file("apt-config/" + apt_config)

        elif command == "systemctl is-enabled apt-daily.timer":
            process.returncode = 0 if systemd_apt_daily_timer else 1
            process.stdout = "enabled\n" if systemd_apt_daily_timer else "disabled\n"

        elif command == "systemctl is-enabled apt-daily-upgrade.timer":
            process.returncode = 0 if systemd_apt_daily_upgrade_timer else 1
            process.stdout = (
                "enabled\n" if systemd_apt_daily_upgrade_timer else "disabled\n"
            )
        elif command == "unattended-upgrades --dry-run":
            process.returncode = dry_run
        return process

    if not argv or argv[0] != "check_unattended_upgrades":
        argv.insert(0, "check_unattended_upgrades")

    with (
        mock.patch("sys.exit") as sys_exit,
        mock.patch("subprocess.run", side_effect=perform_subprocess_run_side_effect),
        mock.patch("os.path.exists", return_value=reboot),
        mock.patch("shutil.which", return_value=anacron),
        mock.patch("sys.argv", argv),
        mock.patch(
            "check_unattended_upgrades.open",
            mock.mock_open(
                read_data=read_text_file(os.path.join("main-log", main_log_file))
            ),
        ),
        freeze_time(time),
    ):
        file_stdout: io.StringIO = io.StringIO()
        file_stderr: io.StringIO = io.StringIO()
        with redirect_stdout(file_stdout), redirect_stderr(file_stderr):
            check_unattended_upgrades.main()

    return MockResult(
        sys_exit_mock=sys_exit,
        stdout=file_stdout.getvalue(),
        stderr=file_stderr.getvalue(),
    )
