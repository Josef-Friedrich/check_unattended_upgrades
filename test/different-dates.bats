#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	./test/patch.sh
}

@test "Date: OK_FIRST" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = \
'OK - The last execution of “unattended-upgrades” was at 2017-09-04 13:17:10.' ]
}

@test "Date: OK_LAST" {
	mock_path test/bin/ok_last
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = \
'OK - The last execution of “unattended-upgrades” was at 2017-09-03 11:17:11.' ]
}

@test "Date: WARNING_FIRST" {
	mock_path test/bin/warning_first
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 1 ]
	[ "${lines[0]}" = \
'WARNING - The last execution of “unattended-upgrades” was at 2017-09-03 11:17:10.' ]
}

@test "Date: WARNING_LAST" {
	mock_path test/bin/warning_last
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 1 ]
	[ "${lines[0]}" = \
'WARNING - The last execution of “unattended-upgrades” was at 2017-09-02 09:17:11.' ]
}

@test "Date: CRITICAL_FIRST" {
	skip
	mock_path test/bin/critical_first
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = \
'CRITICAL - The last execution of “unattended-upgrades” was at 2017-09-02 09:17:10.' ]
}
