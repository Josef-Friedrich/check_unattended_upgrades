import unittest

from tests.helper import execute_main


class TestAnacron(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(
            ["--anacron"],
        )
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--anacron"], anacron=None)
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - Package 'anacron' is not installed."
        )


class TestDryRun(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(
            ["--dry-run"],
        )
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(["--dry-run"], dry_run=1)
        result.assert_critical()
        result.assert_first_line(
            "UNATTENDED_UPGRADES CRITICAL - unattended-upgrades --dry-run "
            "exits with a non-zero status."
        )


class TestErrorsInLog(unittest.TestCase):
    def test_warn(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="warning.log", time="2022-12-02 02:51:17"
        )
        result.assert_warn()
        result.assert_first_line(
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
        result.assert_critical()
        result.assert_first_line(
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


class TestLastRun(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main()
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()


class TestReboot(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--reboot"], reboot=False)
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()

    def test_warn(self) -> None:
        result = execute_main(["--reboot"], reboot=True)
        result.assert_first_line(
            "UNATTENDED_UPGRADES WARNING - The machine requires a reboot."
        )
        result.assert_warn()


class TestSystemdTimers(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--systemd-timers", "--verbose"])
        result.assert_ok()
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
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
        result.assert_critical()
        result.assert_first_line(
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


if __name__ == "__main__":
    unittest.main()
