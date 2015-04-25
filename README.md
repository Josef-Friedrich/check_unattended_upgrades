# check_unattended_upgrades

Nagios / Ichinga plugin to check automatic updates (unattended-upgrades) on debian / ubuntu.

## Commandline arguments

```
check_unattended_upgrades 
Copyright (c) 2015 Josef Friedrich <jf@josef-friedrich.de>

This plugin checks if automatic updates (unattended_upgrades) are working.

  
Usage: check_unattended_upgrades <options>

Options:
 -a
    Check if the configuration 'APT::Periodic::AutocleanInterval' is set properly.
 -c
    Critical in seconds.
 -d
    Check if the configuration 'APT::Periodic:Download-Upgradeable-Packages' is set properly.
 -h
    Show this help message.
 -l
    Check if the configuration 'APT::Periodic::Update-Package-Lists' is set properly.
 -m
    Check if the configuration 'Unattended-Upgrade::Mail' is set properly.
 -r
    Check if the configuration 'Unattended-Upgrade::Remove-Unused-Dependencies' is set properly.
 -u
    Check if the configuration 'APT::Periodic::Unattended-Upgrade' is set properly.
 -w
    Warning in seconds.

```

