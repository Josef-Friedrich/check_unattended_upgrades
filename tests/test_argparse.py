import unittest

import check_unattended_upgrades
from tests.helper import run


class TestWithSubprocess:
    def test_help(self) -> None:
        process = run(["--help"])
        assert process.returncode == 0
        assert "usage: check_unattended_upgrades" in process.stdout

    def test_version(self) -> None:
        process = run(
            ["--version"],
        )
        assert process.returncode == 0
        assert (
            "check_unattended_upgrades " + check_unattended_upgrades.__version__
            in process.stdout
        )


if __name__ == "__main__":
    unittest.main()
