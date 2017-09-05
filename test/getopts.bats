#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	source_exec check_unattended_upgrades
}

@test "_getopts -h" {
	run _getopts -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}
