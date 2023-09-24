# check_unattended_upgrades

Note: The monitoring plugin is currently being rewritten from
Shell
([check_unattended_upgrades](https://github.com/Josef-Friedrich/check_unattended_upgrades/blob/master/check_unattended_upgrades)) to
Python
([check_unattended_upgrades.py](https://github.com/Josef-Friedrich/check_unattended_upgrades/blob/master/check_unattended_upgrades.py)). Use the Shell version until further notice.

## Summary / Short description

> Monitoring plugin to check automatic updates ([unattended-upgrades](https://github.com/mvo5/unattended-upgrades)) on Debian / Ubuntu.

## Usage

```
check_unattended_upgrades v1.4
Copyright (c) 2015-2019 Josef Friedrich <josef@friedrich.rocks>

Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.


Usage: check_unattended_upgrades <options>

Options:
 -A, --anacron
	Check if the package 'anacron' is installed.
 -a, --autoclean
	Check if the configuration 'APT::Periodic::AutocleanInterval' is set
	properly.
 -c, --critical
        Time interval since the last execution to result in a
        critical state (time units depending on '--format').
 -D, --short-description
	Show a short description of this check plugin.
 -d, --download
	Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages'
	is set properly.
 -e, --enable
	Check if the configuration 'APT::Periodic::Enable' is set properly.
 -f UNIT, --format UNIT
        Defines the unit for the numbers of '--warning' and '--
        critical', also the output of 'last-run'. Allowed values
        are: 'seconds', 'minutes', 'hours' and 'days', default:
        'seconds'.
 -h, --help
	Show this help message.
 -l, --lists
	Check if the configuration 'APT::Periodic::Update-Package-Lists' is set
	properly.
 -m, --mail
	Check if the configuration 'Unattended-Upgrade::Mail' is set properly.
 -n, --dry-run
	Check if 'unattended-upgrades --dry-run' is working. Warning: If you use
	this option the performance data last_ago is always 0 or near to 0.
 -p, --repo
	Check if 'Unattended-upgrades' is configured to include the specified
	custom repository.
 -R, --reboot
	Check if the machine needs a reboot.
 -r, --remove
	Check if the configuration 'Unattended-Upgrade::Remove-Unused-
	Dependencies' is set properly.
 -S, --security
	Check if 'Unattended-upgrades' is configured to handle security updates.
 -s, --sleep
	Check if the configuration 'APT::Periodic::RandomSleep' is set properly.
 -t, --systemd-timers
	Check if the appropriate Systemd timers are enabled ( apt-daily-upgrade.timer, apt-daily.timer ).
 -u, --unattended
	Check if the configuration 'APT::Periodic::Unattended-Upgrade' is set
	properly.
 -v, --version
	Show the version number.
 -w, --warning
        Time interval since the last execution to result in a
        warning state (time units depending on '--format').

Performance data:
  - last_ago
	  Time interval in seconds for last unattended-upgrades execution.
  - warning
	  Interval in seconds.
  - critical
	  Interval in seconds.

About file system permissions:
	The user which executes this plugin must have read permissions to this
	log file:

		/var/log/unattended-upgrades/unattended-upgrades.log

	To allow every user on your system to read the mentioned log file this
	permissions are recommended:

		751 (drwxr-x--x) /var/log/unattended-upgrades
		644 (-rw-r--r--) /var/log/unattended-upgrades/unattended-upgrades.log

```

## Project pages

* https://github.com/Josef-Friedrich/check_unattended_upgrades
* https://exchange.icinga.com/joseffriedrich/check_unattended_upgrades
* https://exchange.nagios.org/directory/Plugins/Software/check_unattended_upgrades/details

## Testing

```
make test
```
