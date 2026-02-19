from tests.helper import execute_main


class TestConfigAutoclean:
    def test_ok(self) -> None:
        result = execute_main(["--autoclean", "7"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--autoclean", "42"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            + "Configuration value for “APT::Periodic::AutocleanInterval” "
            + "unexpected! actual: 7 expected: 42"
        )


class TestConfigDownload:
    def test_ok(self) -> None:
        result = execute_main(["--download", "1"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--download", "0"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Download-Upgradeable-Packages” "
            "unexpected! actual: 1 expected: 0"
        )


class TestConfigEnable:
    def test_ok(self) -> None:
        result = execute_main(["--enable", "1"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--enable", "42"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Enable” "
            "unexpected! actual: 1 expected: 42"
        )


class TestConfigSleep:
    def test_ok(self) -> None:
        result = execute_main(["--sleep", "0"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--sleep", "42"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::RandomSleep” unexpected! "
            "actual: 0 expected: 42"
        )


class TestConfigUnattended:
    def test_ok(self) -> None:
        result = execute_main(["--unattended", "1"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--unattended", "42"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Unattended-Upgrade” unexpected! "
            "actual: 1 expected: 42"
        )


class TestConfigLists:
    def test_ok(self) -> None:
        result = execute_main(["--lists", "1"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--lists", "42"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “APT::Periodic::Update-Package-Lists” unexpected! "
            "actual: 1 expected: 42"
        )


class TestConfigMail:
    def test_ok(self) -> None:
        result = execute_main(["--mail", "logs@example.com"])
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--mail", "logs@xxx.xx"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for “Unattended-Upgrade::Mail” unexpected! "
            "actual: logs@example.com expected: logs@xxx.xx"
        )


class TestConfigRemove:
    def test_ok(self) -> None:
        result = execute_main(["--remove", "true"])
        assert result.first_line == ("UNATTENDED_UPGRADES OK - all")
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--remove", "false"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "Configuration value for "
            "“Unattended-Upgrade::Remove-Unused-Dependencies” unexpected! "
            "actual: true expected: false"
        )
