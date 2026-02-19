import pytest

from tests.helper import execute_main


class TestAnacron:
    def test_ok(self) -> None:
        result = execute_main(
            ["--anacron"],
        )
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--anacron"], anacron=None)
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - Package 'anacron' is not installed."
        )


class TestDryRun:
    def test_ok(self) -> None:
        result = execute_main(
            ["--dry-run"],
        )
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--dry-run"], dry_run=1)
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - unattended-upgrades --dry-run "
            "exits with a non-zero status."
        )


class TestErrorsInLog:
    def test_warn(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="warning.log", time="2022-12-02 02:51:17"
        )
        assert result.exitcode == 1
        assert result.first_line == (
            "UNATTENDED_UPGRADES WARNING - Found /var/run/reboot-required, rebooting, "
            "Shutdown msg: "
            'b"Shutdown scheduled for Fri 2022-12-02 04:00:00 CET, '
            "use 'shutdown -c' to cancel.\""
        )
        # TODO Fix test
        # result.assert_output(
        #     "UNATTENDED_UPGRADES WARNING - "
        #     "Found /var/run/reboot-required, rebooting, "
        #     "Shutdown msg: "
        #     'b"Shutdown scheduled for Fri 2022-12-02 04:00:00 CET, '
        #     "use 'shutdown -c' to cancel.\"\n"
        #     # "CRITICAL: Sperrung konnte nicht erreicht werden "
        #     # "(läuft eine weitere Paketverwaltung?)\n"
        #     "OK: last-run was 3600.0 seconds ago\n"
        #     "WARNING: Found /var/run/reboot-required, rebooting\n"
        #     'WARNING: Shutdown msg: b"Shutdown scheduled for '
        #     "Fri 2022-12-02 04:00:00 CET, use 'shutdown -c' to cancel.\"\n"
        # )

    def test_critical(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="error_lock.log", time="2017-06-01 18:17:25"
        )
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - Sperrung konnte nicht erreicht werden "
            "(läuft eine weitere Paketverwaltung?)"
        )
        # TODO Fix test
        # result.assert_output(
        #     "UNATTENDED_UPGRADES CRITICAL - Sperrung konnte nicht erreicht werden "
        #     "(läuft eine weitere Paketverwaltung?)\n"
        #     "OK: last-run was 3600.0 seconds ago\n"
        #     "CRITICAL: Sperrung konnte nicht erreicht werden "
        #     "(läuft eine weitere Paketverwaltung?)\n"
        # )


class TestLastRun:
    def test_ok(self) -> None:
        result = execute_main()
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0


class TestReboot:
    def test_ok(self) -> None:
        result = execute_main(["--reboot"], reboot=False)
        assert result.first_line == "UNATTENDED_UPGRADES OK - all"
        assert result.exitcode == 0

    def test_warn(self) -> None:
        result = execute_main(["--reboot"], reboot=True)
        assert result.first_line == (
            "UNATTENDED_UPGRADES WARNING - The machine requires a reboot."
        )
        assert result.exitcode == 1


class TestSecurity:
    @pytest.mark.skip
    def test_ok(self) -> None:
        result = execute_main(["--security"], apt_config="allowed-origins.txt")
        assert result.exitcode == 0

    def test_critical(self) -> None:
        result = execute_main(["--security"])
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "unattended-upgrades is not configured to handle security updates."
        )


class TestSystemdTimers:
    def test_ok(self) -> None:
        result = execute_main(["--systemd-timers", "--verbose"])
        assert result.exitcode == 0
        assert result.first_line == ("UNATTENDED_UPGRADES OK - all")
        # TODO Fix test
        # result.assert_output(
        #     "UNATTENDED_UPGRADES OK - all\n"
        #     "OK: last-run was 3600.0 seconds ago\n"
        #     "OK: The systemd timer “apt-daily.timer” is enabled.\n"
        #     "OK: The systemd timer “apt-daily-upgrade.timer” is enabled.\n"
        # )

    def test_critical(self) -> None:
        result = execute_main(
            ["--systemd-timers", "--verbose"],
            systemd_apt_daily_timer=False,
            systemd_apt_daily_upgrade_timer=False,
        )
        assert result.exitcode == 2
        assert result.first_line == (
            "UNATTENDED_UPGRADES CRITICAL - "
            "The systemd timer “apt-daily.timer” is not enabled., "
            "The systemd timer “apt-daily-upgrade.timer” is not enabled."
        )
        # TODO Fix test
        # result.assert_output(
        #     "UNATTENDED_UPGRADES CRITICAL - "
        #     "The systemd timer “apt-daily.timer” is not enabled., "
        #     "The systemd timer “apt-daily-upgrade.timer” is not enabled.\n"
        #     "OK: last-run was 3600.0 seconds ago\n"
        #     "CRITICAL: The systemd timer “apt-daily.timer” is not enabled.\n"
        #     "CRITICAL: The systemd timer “apt-daily-upgrade.timer” is not enabled.\n"
        # )
