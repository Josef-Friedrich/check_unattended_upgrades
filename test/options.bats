#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_unattended_upgrades
}

@test "run ./check_unattended_upgrades -h" {
	run ./check_unattended_upgrades -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

@test "run ./check_unattended_upgrades -A" {
	skip
	run ./check_unattended_upgrades -A
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - Package “anacron” is not installed.' ]
}

@test "run ./check_unattended_upgrades -R" {
	skip
	run ./check_unattended_upgrades -R
	[ "$status" -eq 1 ]
	[ "${lines[0]}" = 'WARNING - Machine requires a reboot.' ]
}

@test "run ./check_unattended_upgrades" {
	_test() {
		echo lol
		case $@ in
			'-f /var/run/reboot-required')
				return 0
				;;

			'-f /var/log/unattended-upgrades/unattended-upgrades.log')
				exit 0
				;;

			'-x /usr/sbin/anacron')
				return 1
				;;
		esac
	}
	export -f _test
	fake_function test _test
	mock_path test/bin
	run ./check_unattended_upgrades
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = 'CRITICAL - You have at least to specify the two options “-c” and “-w”, e. g.: check_unattended_upgrades -c 3600 -w 7200.' ]
}
