#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	patch check_unattended_upgrades 's/ test / test_patched /g'
}

@test "CRITICAL caused by non-zero status of unattended-upgrades --dry-run" {
	mock_path test/bin/errors
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - unattended-upgrades --dry-run exits with a non-zero status.' ]
}
