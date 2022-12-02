import unittest

from tests.helper import execute_main


class TestOk(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main()
        result.assert_ok()
        result.assert_first_line("UNATTENDED_UPGRADES OK")


class TestVersion(unittest.TestCase):
    def test_short_argument(self) -> None:
        result = execute_main(["-V"])
        result.assert_ok()

        if result.first_line == None:
            self.fail()

        self.assertTrue("check_unattended_upgrades " in result.first_line)

    def test_long_argument(self) -> None:
        result = execute_main(["--version"])
        result.assert_ok()

        if result.first_line == None:
            self.fail()

        self.assertTrue("check_unattended_upgrades " in result.first_line)


if __name__ == "__main__":
    unittest.main()
