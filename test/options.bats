#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_unattended_upgrades
	./test/patch.sh
}

@test "run ./check_unattended_upgrades_patched -h" {
	run ./check_unattended_upgrades_patched -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

@test "run ./check_unattended_upgrades_patched -A" {
	run ./check_unattended_upgrades_patched -A
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - Package “anacron” is not installed.' ]
}

@test "run ./check_unattended_upgrades_patched -R" {
	run ./check_unattended_upgrades_patched -R
	[ "$status" -eq 1 ]
	[ "${lines[0]}" = 'WARNING - Machine requires a reboot.' ]
}

@test "run ./check_unattended_upgrades_patched" {
	run ./check_unattended_upgrades_patched
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - You have at least to specify the two options “-c” and “-w”, e. g.: check_unattended_upgrades -c 3600 -w 7200.' ]
}
