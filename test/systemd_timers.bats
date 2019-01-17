#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	patch check_unattended_upgrades 's/ test / test_patched /g'
}

@test "Systemd timer 1" {
	mock_path test/bin/systemd_timers_1
	run ./check_unattended_upgrades_patched --systemd-timers
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - Systemd timer apt-daily.timer is not enabled.' ]
}

@test "Systemd timer 2" {
	mock_path test/bin/systemd_timers_2
	run ./check_unattended_upgrades_patched --systemd-timers
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - Systemd timer apt-daily-upgrade.timer is not enabled.' ]
}

