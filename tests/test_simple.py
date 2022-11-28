import unittest

from tests.helper import execute_main


class TestOk(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--sleep", "1"])
        self.assertEqual(0, result.exitcode)
        self.assertEqual("SYSTEMD OK - all", result.first_line)


if __name__ == "__main__":
    unittest.main()
