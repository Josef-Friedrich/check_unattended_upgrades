import unittest

from tests.helper import execute_main


class TestConfigAutoClean(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--autoclean", "7"])
        result.assert_exitcode(0)
        result.assert_first_line("LAST-RUN OK")

    def test_critical(self) -> None:
        result = execute_main(["--autoclean", "42"])
        result.assert_exitcode(2)
        result.assert_first_line(
            "LAST-RUN CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


if __name__ == "__main__":
    unittest.main()
