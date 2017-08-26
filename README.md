[![Build Status](https://travis-ci.org/JosefFriedrich-shell/check_unattended_upgrades.svg?branch=master)](https://travis-ci.org/JosefFriedrich-shell/check_unattended_upgrades)

# check_unattended_upgrades


## Summary / Short description

> Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.

## Usage

```
check_unattended_upgrades v1.0
Copyright (c) 2015 Josef Friedrich <jf@josef-friedrich.de>

Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.


Usage: check_unattended_upgrades <options>

Options:
 -a
    Check if the configuration 'APT::Periodic::AutocleanInterval' is set
    properly.
 -A
    Check if the package 'anacron' is installed.
 -c
    Time interval since the last execution to result in a critical state
    (seconds).
 -d
    Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages'
    is set properly.
 -e
    Check if the configuration 'APT::Periodic::Enable' is set properly.
 -h
    Show this help message.
 -l
    Check if the configuration 'APT::Periodic::Update-Package-Lists' is set
    properly.
 -m
    Check if the configuration 'Unattended-Upgrade::Mail' is set properly.
 -r
    Check if the configuration 'Unattended-Upgrade::Remove-Unused-
    Dependencies' is set properly.
 -R
    Check if the machine needs a reboot.
 -s
    Check if the configuration 'APT::Periodic::RandomSleep' is set properly.
 -S
    Check if 'Unattended-upgrades' is configured to handle security updates.
 -u
    Check if the configuration 'APT::Periodic::Unattended-Upgrade' is set
    properly.
 -w
    Time interval since the last execution to result in a warning state
    (seconds).

```

## Testing

```
make test
```

