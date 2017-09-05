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

@test "_getopts --anacron" {
	_getopts --anacron
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

@test "_getopts --autoclean=123" {
	_getopts --autoclean=123
	[ "$OPT_AUTOCLEAN" -eq 123 ]
}

@test "_getopts --autoclean" {
	run _getopts --autoclean
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

@test "_getopts --critical=123" {
	_getopts --critical=123
	[ "$OPT_CRITICAL" -eq 123 ]
}

@test "_getopts --critical" {
	run _getopts --critical
	[ "$status" -eq 3 ]
}

# -d

@test "_getopts -d 123" {
	_getopts -d 123
	[ "$OPT_DOWNLOAD" -eq 123 ]
}

@test "_getopts -d" {
	run _getopts -d
	[ "$status" -eq 3 ]
}

@test "_getopts --download=123" {
	_getopts --download=123
	[ "$OPT_DOWNLOAD" -eq 123 ]
}

@test "_getopts --download" {
	run _getopts --download
	[ "$status" -eq 3 ]
}

# -e

@test "_getopts -e 123" {
	_getopts -e 123
	[ "$OPT_ENABLE" -eq 123 ]
}

@test "_getopts -e" {
	run _getopts -e
	[ "$status" -eq 3 ]
}

@test "_getopts --enable=123" {
	_getopts --enable=123
	[ "$OPT_ENABLE" -eq 123 ]
}

@test "_getopts --enable" {
	run _getopts --enable
	[ "$status" -eq 3 ]
}

# -h

@test "_getopts -h" {
	run _getopts -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

# -l

@test "_getopts -l 123" {
	_getopts -l 123
	[ "$OPT_LISTS" -eq 123 ]
}

@test "_getopts -l" {
	run _getopts -l
	[ "$status" -eq 3 ]
}

# -m

@test "_getopts -m 123" {
	_getopts -m 123
	[ "$OPT_MAIL" -eq 123 ]
}

@test "_getopts -m" {
	run _getopts -m
	[ "$status" -eq 3 ]
}

# -R

@test "_getopts -R" {
	_getopts -R
	[ "$OPT_REBOOT" -eq 1 ]
}


# -r

@test "_getopts -r 123" {
	_getopts -r 123
	[ "$OPT_REMOVE" -eq 123 ]
}

@test "_getopts -r" {
	run _getopts -r
	[ "$status" -eq 3 ]
}

# -S

@test "_getopts -S" {
	_getopts -S
	[ "$OPT_SECURITY" -eq 1 ]
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
