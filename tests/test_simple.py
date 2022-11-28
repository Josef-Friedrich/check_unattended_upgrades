import unittest

from tests.helper import execute_main


class TestOk(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main()
        result.assert_exitcode(0)
        result.assert_first_line("LAST-RUN OK")


if __name__ == "__main__":
    unittest.main()