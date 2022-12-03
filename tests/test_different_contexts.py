import unittest

from tests.helper import execute_main


class TestLastRun(unittest.TestCase):
    def test_ok(self) -> None:
        result = execute_main()
        result.assert_output("UNATTENDED_UPGRADES OK - all")
        result.assert_ok()


class TestWarningsInLog(unittest.TestCase):
    def test_error(self) -> None:
        result = execute_main(
            ["-v"], main_log_file="error_lock.log", time="2017-06-01 18:17:25"
        )
        result.assert_output(
            "UNATTENDED_UPGRADES CRITICAL - Sperrung konnte nicht erreicht werden "
            "(läuft eine weitere Paketverwaltung?)"
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
            "use 'shutdown -c' to cancel.\""
        )
        result.assert_warn()


if __name__ == "__main__":
    unittest.main()
