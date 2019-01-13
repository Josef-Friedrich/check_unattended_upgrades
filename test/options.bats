#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_unattended_upgrades
	patch check_unattended_upgrades 's/ test / test_patched /g'
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

@test "run ./check_unattended_upgrades_patched -S" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -S
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -p LP-PPA-webupd8team-atom" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -p LP-PPA-webupd8team-atom
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -p some-obscure-repo" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -p some-obscure-repo
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - Unattended-upgrades is not \
configured to handle updates for custom repository “some-obscure-repo”." ]
}
