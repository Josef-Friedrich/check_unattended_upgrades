#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	#mock_path test/bin
	source_exec check_unattended_upgrades
}

@test "run ./check_unattended_upgrades -h" {
	run ./check_unattended_upgrades -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

@test "run ./check_unattended_upgrades -A" {
	run ./check_unattended_upgrades -A
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - Package “anacron” is not installed.' ]
}
