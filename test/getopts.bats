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

@test "_getopts --anacron=123" {
	run _getopts --anacron=123
	[ "$status" -eq 4 ]
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

# -D

@test "_getopts -D" {
	run _getopts -D
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "Monitoring plugin to check automatic updates \
(unattended-upgrades) on Debian / Ubuntu." ]
}

@test "_getopts --short-description" {
	run _getopts --short-description
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "Monitoring plugin to check automatic updates \
(unattended-upgrades) on Debian / Ubuntu." ]
}

@test "_getopts --short-description=123" {
	run _getopts --short-description=123
	[ "$status" -eq 4 ]
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

@test "_getopts --help" {
	run _getopts --help
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_unattended_upgrades v$VERSION" ]
}

@test "_getopts --help=123" {
	run _getopts --help=123
	[ "$status" -eq 4 ]
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

@test "_getopts --lists=123" {
	_getopts --lists=123
	[ "$OPT_LISTS" -eq 123 ]
}

@test "_getopts --lists" {
	run _getopts --lists
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

@test "_getopts --mail=123" {
	_getopts --mail=123
	[ "$OPT_MAIL" -eq 123 ]
}

@test "_getopts --mail" {
	run _getopts --mail
	[ "$status" -eq 3 ]
}

# -R

@test "_getopts -R" {
	_getopts -R
	[ "$OPT_REBOOT" -eq 1 ]
}

@test "_getopts --reboot" {
	_getopts --reboot
	[ "$OPT_REBOOT" -eq 1 ]
}

@test "_getopts --reboot=123" {
	run _getopts --reboot=123
	[ "$status" -eq 4 ]
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

@test "_getopts --remove=123" {
	_getopts --remove=123
	[ "$OPT_REMOVE" -eq 123 ]
}

@test "_getopts --remove" {
	run _getopts --remove
	[ "$status" -eq 3 ]
}

# -S

@test "_getopts -S" {
	_getopts -S
	[ "$OPT_SECURITY" -eq 1 ]
}

@test "_getopts --security" {
	_getopts --security
	[ "$OPT_SECURITY" -eq 1 ]
}

@test "_getopts --security=123" {
	run _getopts --security=123
	[ "$status" -eq 4 ]
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

@test "_getopts --sleep=123" {
	_getopts --sleep=123
	[ "$OPT_SLEEP" -eq 123 ]
}

@test "_getopts --sleep" {
	run _getopts --sleep
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

@test "_getopts --unattended=123" {
	_getopts --unattended=123
	[ "$OPT_UNATTENDED" -eq 123 ]
}

@test "_getopts --unattended" {
	run _getopts --unattended
	[ "$status" -eq 3 ]
}

# -v

@test "_getopts -v" {
	run _getopts -v
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "$VERSION" ]
}

@test "_getopts --version" {
	run _getopts --version
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "$VERSION" ]
}

@test "_getopts --version=123" {
	run _getopts --version=123
	[ "$status" -eq 4 ]
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

@test "_getopts --warning=123" {
	_getopts --warning=123
	[ "$OPT_WARNING" -eq 123 ]
}

@test "_getopts --warning" {
	run _getopts --warning
	[ "$status" -eq 3 ]
}
