.. image:: http://img.shields.io/pypi/v/check-unattended-upgrades.svg
    :target: https://pypi.org/project/check-unattended-upgrades
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/check_unattended_upgrades/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/check_unattended_upgrades/actions/workflows/tests.yml
    :alt: Tests

Command line interface
----------------------

:: 

    usage: check_unattended_upgrades [-h] [-A] [-a CONFIG_VALUE] [-c SECONDS] [-D]
                                     [-d CONFIG_VALUE] [-e CONFIG_VALUE]
                                     [-l CONFIG_VALUE] [-m CONFIG_VALUE] [-n]
                                     [-p CUSTOM_REPO] [-R] [-r CONFIG_VALUE] [-S]
                                     [-s CONFIG_VALUE] [-t] [-u CONFIG_VALUE] [-v]
                                     [-V] [-w SECONDS]

    Copyright (c) 2015-22 Josef Friedrich <josef@friedrich.rocks>

    Monitoring plugin to check automatic updates (unattended-upgrades) on Debian / Ubuntu.

    options:
      -h, --help            show this help message and exit
      -A, --anacron         Check if the package 'anacron' is installed.
      -a CONFIG_VALUE, --autoclean CONFIG_VALUE
                            Check if the configuration
                            'APT::Periodic::AutocleanInterval' is set properly.
      -c SECONDS, --critical SECONDS
                            Time interval since the last execution to result in a
                            critical state (seconds).
      -D, --short-description
                            Show a short description of this check plugin.
      -d CONFIG_VALUE, --download CONFIG_VALUE
                            Check if the configuration 'APT::Periodic:Download-
                            Upgradeable-Packages' is set properly.
      -e CONFIG_VALUE, --enable CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Enable' is
                            set properly
      -l CONFIG_VALUE, --lists CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Update-
                            Package-Lists' is set properly.
      -m CONFIG_VALUE, --mail CONFIG_VALUE
                            Check if the configuration 'Unattended-Upgrade::Mail' is
                            set properly.
      -n, --dry-run         Check if 'unattended-upgrades --dry-run' is working.
                            Warning: If you use this option the performance data
                            last_ago is always 0 or near to 0.
      -p CUSTOM_REPO, --repo CUSTOM_REPO, --custom-repo CUSTOM_REPO
                            Check if 'Unattended-upgrades' is configured to include
                            the specified custom repository.
      -R, --reboot          Check if the machine needs a reboot.
      -r CONFIG_VALUE, --remove CONFIG_VALUE
                            Check if the configuration 'Unattended-Upgrade::Remove-
                            Unused-Dependencies' is set properly.
      -S, --security        Check if 'Unattended-upgrades' is configured to handle
                            security updates.
      -s CONFIG_VALUE, --sleep CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::RandomSleep'
                            is set properly.
      -t, --systemd-timers  Check if the appropriate systemd timers are enabled (
                            apt-daily-upgrade.timer, apt-daily.timer ).
      -u CONFIG_VALUE, --unattended CONFIG_VALUE
                            Check if the configuration 'APT::Periodic::Unattended-
                            Upgrade' is set properly.
      -v, --verbose
      -V, --version         show program's version number and exit
      -w SECONDS, --warning SECONDS
                            Time interval since the last execution to result in a
                            warning state (seconds).

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

