.. image:: http://img.shields.io/pypi/v/check-unattended-upgrades.svg
    :target: https://pypi.org/project/check-unattended-upgrades
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/check_unattended_upgrades/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/check_unattended_upgrades/actions/workflows/tests.yml
    :alt: Tests

Note: This monitoring plugin is written in Python from version 3 onwards.
Earlier versions of this plugin were written in shell script. The latest version
of the shell script can be retrieved via the `git history
<https://github.com/Josef-Friedrich/check_unattended_upgrades/tree/66d51c1c82b28f4d69c2237dac5e291b58d2df86>`__.

Command line interface
----------------------

:: 

    usage: check_unattended_upgrades [-h] [-V] [-v] [-A] [-a CONFIG_VALUE]
                                     [-w TIMESPAN] [-c TIMESPAN] [-D]
                                     [-d CONFIG_VALUE] [-e CONFIG_VALUE] [-f UNIT]
                                     [-l CONFIG_VALUE] [-m CONFIG_VALUE] [-n]
                                     [-p CUSTOM_REPOS] [-R] [-r CONFIG_VALUE] [-S]
                                     [-s CONFIG_VALUE] [-t] [-u CONFIG_VALUE]

    version 2.0.0a1
    Licensed under the MIT.
    Copyright (c) 2015-2026 Josef Friedrich <josef@friedrich.rocks>

    Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu

    options:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbose         Increase the output verbosity. Use this option up to
                            three times (-vvv):0: one line output, log.error,
                            log.warning; 1 (-v): multi-line output, log.error,
                            log.warning; 2 (-vv): multi-line output, log.error,
                            log.warning, log.info; 3 (-vvv): multi-line output,
                            log.error, log.warning, log.info, log.debug
      -A, --anacron         Check if the package 'anacron' is installed.
      -a, --autoclean CONFIG_VALUE
                            Check if the configuration
                            'APT::Periodic::AutocleanInterval' is set properly.
      -w, --warning TIMESPAN
                            Time interval since the last execution to result in a
                            warning state. See timespan format specification below
                            or specify a number without time units and use the '--
                            format' option to select the time unit.
      -c, --critical TIMESPAN
                            Time interval since the last execution to result in a
                            critical state. See timespan format specification below
                            or specify a number without time units and use the '--
                            format' option to select the time unit.
      -D, --short-description
                            Show a short description of this check plugin.
      -d, --download CONFIG_VALUE
                            Check if the configuration 'APT::Periodic:Download-
                            Upgradeable-Packages' is set properly.
      -e, --enable CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Enable' is
                            set properly
      -f, --format UNIT     Defines the unit for the numbers of '--warning' and '--
                            critical', also the output of 'last-run'. Allowed values
                            are: 'seconds', 'minutes', 'hours' and 'days', default:
                            'seconds'.
      -l, --lists CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Update-
                            Package-Lists' is set properly.
      -m, --mail CONFIG_VALUE
                            Check if the configuration 'Unattended-Upgrade::Mail' is
                            set properly.
      -n, --dry-run         Check if 'unattended-upgrades --dry-run' is working.
                            Warning: If you use this option the performance data
                            last_ago is always 0 or near to 0.
      -p, --repo, --custom-repo CUSTOM_REPOS
                            Check if 'Unattended-upgrades' is configured to include
                            the specified custom repository.
      -R, --reboot          Check if the machine needs a reboot.
      -r, --remove CONFIG_VALUE
                            Check if the configuration 'Unattended-Upgrade::Remove-
                            Unused-Dependencies' is set properly.
      -S, --security        Check if 'Unattended-upgrades' is configured to handle
                            security updates.
      -s, --sleep CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::RandomSleep'
                            is set properly.
      -t, --systemd-timers  Check if the appropriate systemd timers are enabled (
                            apt-daily-upgrade.timer, apt-daily.timer ).
      -u, --unattended CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Unattended-
                            Upgrade' is set properly.

    Performance data:
      - last_ago
           Time interval in seconds for last unattended-upgrades execution.
      - warning
           Interval of time units defined in '--format'.
      - critical
           Interval of time units defined in '--format'.

    About file system permissions:
       The user which executes this plugin must have read permissions to this
       log file:

           /var/log/unattended-upgrades/unattended-upgrades.log

       To allow every user on your system to read the mentioned log file this
       permissions are recommended:

           751 (drwxr-x--x) /var/log/unattended-upgrades
           644 (-rw-r--r--) /var/log/unattended-upgrades/unattended-upgrades.log

    Timespan format
    ---------------

    If no time unit is specified, generally seconds are assumed. The following time
    units are understood:

    - years, year, y (defined as 365.25 days)
    - months, month, M (defined as 30.44 days)
    - weeks, week, w
    - days, day, d
    - hours, hour, hr, h
    - minutes, minute, min, m
    - seconds, second, sec, s
    - milliseconds, millisecond, msec, ms
    - microseconds,  microsecond, usec, μs, μ, us

    The following are valid examples of timespan specifications:

    - 1
    - 1.23
    - 2.345s
    - 3min 45.234s
    - 34min
    - 2 months 8 days
    - 1h30m

Project pages
-------------

* https://github.com/Josef-Friedrich/check_unattended_upgrades
* https://exchange.icinga.com/joseffriedrich/check_unattended_upgrades
* https://exchange.nagios.org/directory/Plugins/Software/check_unattended_upgrades/details
