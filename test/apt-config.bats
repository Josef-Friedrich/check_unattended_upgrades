#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	patch check_unattended_upgrades 's/ test / test_patched /g'
}

##
# -a
##

@test "run ./check_unattended_upgrades_patched -a 7" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -a 7
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -a 1" {
	run ./check_unattended_upgrades_patched -a 1
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::AutocleanInterval' is not \
configured properly. It has the value '7', \
but it should have the value '1'." ]
}

##
# -d
##

@test "run ./check_unattended_upgrades_patched -d 1" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -d 1
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -d 7" {
	run ./check_unattended_upgrades_patched -d 7
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::Download-Upgradeable-Packages' is not \
configured properly. It has the value '1', \
but it should have the value '7'." ]
}

##
# -e
##

@test "run ./check_unattended_upgrades_patched -e 1" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -e 1
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -e 7" {
	run ./check_unattended_upgrades_patched -e 7
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::Enable' is not \
configured properly. It has the value '1', \
but it should have the value '7'." ]
}

##
# -l
##

@test "run ./check_unattended_upgrades_patched -l 1" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -l 1
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -l 7" {
	run ./check_unattended_upgrades_patched -l 7
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::Update-Package-Lists' is not \
configured properly. It has the value '1', \
but it should have the value '7'." ]
}

##
# -m
##

@test "run ./check_unattended_upgrades_patched -m you@example.com" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -m you@example.com
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -m i@example.com" {
	run ./check_unattended_upgrades_patched -m i@example.com
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'Unattended-Upgrade::Mail' is not \
configured properly. It has the value 'you@example.com', \
but it should have the value 'i@example.com'." ]
}

##
# -r
##

@test "run ./check_unattended_upgrades_patched -r true" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -r true
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -r false" {
	run ./check_unattended_upgrades_patched -r false
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'Unattended-Upgrade::Remove-Unused-Dependencies' is not \
configured properly. It has the value 'true', \
but it should have the value 'false'." ]
}

##
# -s
##

@test "run ./check_unattended_upgrades_patched -s 0" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -s 0
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -s 1" {
	run ./check_unattended_upgrades_patched -s 1
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::RandomSleep' is not \
configured properly. It has the value '0', \
but it should have the value '1'." ]
}

##
# -u
##

@test "run ./check_unattended_upgrades_patched -u 1" {
	mock_path test/bin/ok_first
	run ./check_unattended_upgrades_patched -u 1
	[ "$status" -eq 0 ]
}

@test "run ./check_unattended_upgrades_patched -u 7" {
	run ./check_unattended_upgrades_patched -u 7
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "CRITICAL - The configuration \
'APT::Periodic::Unattended-Upgrade' is not \
configured properly. It has the value '1', \
but it should have the value '7'." ]
}
