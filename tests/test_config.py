from tests.helper import execute_main


class TestConfigAutoclean:
    def test_ok(self) -> None:
        result = execute_main(["--autoclean", "7"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--autoclean", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::AutocleanInterval” "
            "unexpected! actual: 7 expected: 42"
        )


class TestConfigDownload:
    def test_ok(self) -> None:
        result = execute_main(["--download", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--download", "0"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Download-Upgradeable-Packages” "
            "unexpected! actual: 1 expected: 0"
        )


class TestConfigEnable:
    def test_ok(self) -> None:
        result = execute_main(["--enable", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--enable", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Enable” "
            "unexpected! actual: 1 expected: 42"
        )


class TestConfigSleep:
    def test_ok(self) -> None:
        result = execute_main(["--sleep", "0"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--sleep", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::RandomSleep” unexpected! "
            "actual: 0 expected: 42"
        )


class TestConfigUnattended:
    def test_ok(self) -> None:
        result = execute_main(["--unattended", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--unattended", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Unattended-Upgrade” unexpected! "
            "actual: 1 expected: 42"
        )


class TestConfigLists:
    def test_ok(self) -> None:
        result = execute_main(["--lists", "1"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--lists", "42"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Update-Package-Lists” unexpected! "
            "actual: 1 expected: 42"
        )


class TestConfigMail:
    def test_ok(self) -> None:
        result = execute_main(["--mail", "logs@example.com"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--mail", "logs@xxx.xx"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “Unattended-Upgrade::Mail” unexpected! "
            "actual: logs@example.com expected: logs@xxx.xx"
        )


class TestConfigRemove:
    def test_ok(self) -> None:
        result = execute_main(["--remove", "true"])
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--remove", "false"])
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for "
            "“Unattended-Upgrade::Remove-Unused-Dependencies” unexpected! "
            "actual: true expected: false"
        )
