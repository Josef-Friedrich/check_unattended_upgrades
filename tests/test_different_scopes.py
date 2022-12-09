import unittest

from tests.helper import execute_main


class TestLastRun(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main()
        result.assert_first_line("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()


class TestErrorsInLog(unittest.TestCase):
    def test_error(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="error_lock.log", time="2017-06-01 18:17:25"
        )
        result.assert_output(
            "UNATTENDED_UPGRADES CRITICAL - Sperrung konnte nicht erreicht werden "
            "(läuft eine weitere Paketverwaltung?)\n"
            "OK: last-run was 3600.0 seconds ago\n"
            "CRITICAL: Sperrung konnte nicht erreicht werden "
            "(läuft eine weitere Paketverwaltung?)\n"
        )
        result.assert_critical()

    def test_warning(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="warning.log", time="2022-12-02 02:51:17"
        )
        result.assert_output(
            "UNATTENDED_UPGRADES WARNING - Found /var/run/reboot-required, rebooting, "
            "Shutdown msg: "
            'b"Shutdown scheduled for Fri 2022-12-02 04:00:00 CET, '
            "use 'shutdown -c' to cancel.\"\n"
            # "CRITICAL: Sperrung konnte nicht erreicht werden "
            # "(läuft eine weitere Paketverwaltung?)\n"
            "OK: last-run was 3600.0 seconds ago\n"
            "WARNING: Found /var/run/reboot-required, rebooting\n"
            'WARNING: Shutdown msg: b"Shutdown scheduled for '
            "Fri 2022-12-02 04:00:00 CET, use 'shutdown -c' to cancel.\"\n"
        )
        result.assert_warn()


class TestSystemdTimers(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main(["--systemd-timers", "--verbose"])
        result.assert_output(
            "UNATTENDED_UPGRADES OK - all\n"
            "OK: last-run was 3600.0 seconds ago\n"
            "OK: The systemd timer “apt-daily.timer” is enabled.\n"
            "OK: The systemd timer “apt-daily-upgrade.timer” is enabled.\n"
        )
        result.assert_ok()

    def test_critical(self) -> None:
        result = execute_main(
            ["--systemd-timers", "--verbose"],
            systemd_apt_daily_timer=False,
            systemd_apt_daily_upgrade_timer=False,
        )
        result.assert_output(
            "UNATTENDED_UPGRADES CRITICAL - "
            "The systemd timer “apt-daily.timer” is not enabled., "
            "The systemd timer “apt-daily-upgrade.timer” is not enabled.\n"
            "OK: last-run was 3600.0 seconds ago\n"
            "CRITICAL: The systemd timer “apt-daily.timer” is not enabled.\n"
            "CRITICAL: The systemd timer “apt-daily-upgrade.timer” is not enabled.\n"
        )
        result.assert_critical()


if __name__ == "__main__":
    unittest.main()
