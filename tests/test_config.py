import unittest

from tests.helper import execute_main


class TestConfigAutoclean(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--autoclean", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--autoclean", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigDownload(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--download", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--download", "0"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::Download-Upgradeable-Packages” unexpected! actual: 1 expected: 0"
        )


class TestConfigEnable(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--enable", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--enable", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigSleep(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--sleep", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--sleep", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigUnattended(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--unattended", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--unattended", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigLists(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--lists", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--lists", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigMail(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--mail", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--mail", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::AutocleanInterval” unexpected! actual: 7 expected: 42"
        )


class TestConfigRemove(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--remove", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--remove", "0"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Configuration value for “APT::Periodic::Download-Upgradeable-Packages” unexpected! actual: 1 expected: 0"
        )


if __name__ == "__main__":
    unittest.main()
