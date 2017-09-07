[![Build Status](https://travis-ci.org/JosefFriedrich-shell/check_unattended_upgrades.svg?branch=master)](https://travis-ci.org/JosefFriedrich-shell/check_unattended_upgrades)

# check_unattended_upgrades


## Summary / Short description

> Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.

## Usage

```
check_unattended_upgrades v1.1
Copyright (c) 2015-2017 Josef Friedrich <josef@friedrich.rocks>

Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.


Usage: check_unattended_upgrades <options>

Options:
 -A, --anacron
    Check if the package 'anacron' is installed.
 -a, --autoclean
    Check if the configuration 'APT::Periodic::AutocleanInterval' is set
    properly.
 -c, --critical
    Time interval since the last execution to result in a critical state
    (seconds).
 -D, --short-description
    Show a short description of this check plugin.
 -d, --download
    Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages'
    is set properly.
 -e, --enable
    Check if the configuration 'APT::Periodic::Enable' is set properly.
 -h, --help
    Show this help message.
 -l, --lists
    Check if the configuration 'APT::Periodic::Update-Package-Lists' is set
    properly.
 -m, --mail
    Check if the configuration 'Unattended-Upgrade::Mail' is set properly.
 -R, --reboot
    Check if the machine needs a reboot.
 -r, --remove
    Check if the configuration 'Unattended-Upgrade::Remove-Unused-
    Dependencies' is set properly.
 -S, --security
    Check if 'Unattended-upgrades' is configured to handle security updates.
 -s, --sleep
    Check if the configuration 'APT::Periodic::RandomSleep' is set properly.
 -u, --unattended
    Check if the configuration 'APT::Periodic::Unattended-Upgrade' is set
    properly.
 -v, --version
    Show the version number.
 -w, --warning
    Time interval since the last execution to result in a warning state
    (seconds).

Performance data:
  - last_ago
      Time interval in seconds for last unattended-upgrades execution.
  - warning
      Interval in seconds.
  - critical
      Interval in seconds.

```

## Project pages

* https://github.com/JosefFriedrich-shell/check_unattended_upgrades
* https://exchange.icinga.com/joseffriedrich/check_unattended_upgrades
* https://exchange.nagios.org/directory/Plugins/Software/check_unattended_upgrades/details

## Testing

```
make test
```

