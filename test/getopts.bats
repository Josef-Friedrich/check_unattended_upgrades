#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	source_exec check_unattended_upgrades
}

# -A

@test "_getopts -A" {
	_getopts -A
	[ "$OPT_ANACRON" -eq 1 ]
}

# -a

@test "_getopts -a 123" {
	_getopts -a 123
	[ "$OPT_AUTOCLEAN" -eq 123 ]
}

@test "_getopts -a" {
	run _getopts -a
	[ "$status" -eq 3 ]
}

# -c

@test "_getopts -c 123" {
	_getopts -c 123
	[ "$OPT_CRITICAL" -eq 123 ]
}

@test "_getopts -c" {
	run _getopts -c
	[ "$status" -eq 3 ]
}

# -h

@test "_getopts -h" {
	run _getopts -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

# -s

@test "_getopts -s 123" {
	_getopts -s 123
	[ "$OPT_SLEEP" -eq 123 ]
}

@test "_getopts -s" {
	run _getopts -s
	[ "$status" -eq 3 ]
}

# -u

@test "_getopts -u 123" {
	_getopts -u 123
	[ "$OPT_UNATTENDED" -eq 123 ]
}

@test "_getopts -u" {
	run _getopts -u
	[ "$status" -eq 3 ]
}

# -w

@test "_getopts -w 123" {
	_getopts -w 123
	[ "$OPT_WARNING" -eq 123 ]
}

@test "_getopts -w" {
	run _getopts -w
	[ "$status" -eq 3 ]
}
