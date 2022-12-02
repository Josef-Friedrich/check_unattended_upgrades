import io
import os
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock
from unittest.mock import Mock

import check_unattended_upgrades


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
    __print: Mock
    __stdout: str | None
    __stderr: str | None

    def __init__(
        self, sys_exit_mock: Mock, print_mock: Mock, stdout: str, stderr: str
    ) -> None:
        self.__sys_exit = sys_exit_mock
        self.__print = print_mock
        self.__stdout = stdout
        self.__stderr = stderr

    @property
    def exitcode(self) -> int:
        """The captured exit code"""
        return self.__sys_exit.call_args[0][0]

    @property
    def print_calls(self) -> list[str]:
        """The captured print calls as a list for each line."""
        output: list[str] = []
        for call in self.__print.call_args_list:
            output.append(str(call[0][0]))
        return output

    @property
    def stdout(self) -> str | None:
        """The function ``redirect_stdout()`` is used to capture the ``stdout``
        output."""
        if self.__stdout:
            return self.__stdout

    @property
    def stderr(self) -> str | None:
        """The function ``redirect_stderr()`` is used to capture the ``stderr``
        output."""
        if self.__stderr:
            return self.__stderr

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
        if self.print_calls:
            out += "\n".join(self.print_calls)

        return out

    @property
    def first_line(self) -> str | None:
        """The first line of the output without a newline break at the
        end as a string.
        """
        if self.output:
            return self.output.split("\n", 1)[0]

    def assert_exitcode(self, exitcode: int) -> None:
        assert self.exitcode == exitcode, "exitcode {} != {}".format(
            self.exitcode, exitcode
        )

    def assert_ok(self) -> None:
        self.assert_exitcode(0)

    def assert_warn(self) -> None:
        self.assert_exitcode(1)

    def assert_critical(self) -> None:
        self.assert_exitcode(2)

    def assert_unknown(self) -> None:
        self.assert_exitcode(3)

    def assert_first_line(self, first_line: str) -> None:
        assert self.first_line == first_line, "first_line “{}” != “{}”".format(
            self.first_line, first_line
        )


class CompletedProcess:
    returncode: int = 0
    stdout: str


def perform_subprocess_run_side_effect(args: list[str], **kwargs):
    process = CompletedProcess()
    process.returncode = 0
    process.stdout = read_text_file("apt-config.txt")
    return process


def execute_main(
    argv: list[str] = ["check_unattended_upgrades.py"],
    main_log_file: str = "info.log",
) -> MockResult:
    if not argv or argv[0] != "check_unattended_upgrades.py":
        argv.insert(0, "check_unattended_upgrades.py")
    with mock.patch("sys.exit") as sys_exit, mock.patch(
        "subprocess.run", side_effect=perform_subprocess_run_side_effect
    ), mock.patch("sys.argv", argv), mock.patch(
        "builtins.print"
    ) as mocked_print, mock.patch(
        "check_unattended_upgrades.open",
        mock.mock_open(
            read_data=read_text_file(os.path.join("main-log", main_log_file))
        ),
    ):

        file_stdout: io.StringIO = io.StringIO()
        file_stderr: io.StringIO = io.StringIO()
        with redirect_stdout(file_stdout), redirect_stderr(file_stderr):
            check_unattended_upgrades.main()

    return MockResult(
        sys_exit_mock=sys_exit,
        print_mock=mocked_print,
        stdout=file_stdout.getvalue(),
        stderr=file_stderr.getvalue(),
    )
