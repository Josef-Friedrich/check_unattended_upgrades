# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-alpha.1] - 2026-02-16

### Added

- Description field in pyproject.toml

## [2.0.0-alpha] - 2026-02-16

### Added
- Add test
- Add more tests
- Add more tests
- Add more log files
- Add some tests
- Add some tests
- Add some tests
- Add some type hints
- Add mypy to check types
- Add first resource
- Add rewritte notice to the readme
- Add description and epilog to the argparser
- Add dependency
- Add some boilerplate files to start a rewrite in Python

### Changed
- Update tooling
- Clean up
- Migrate from poetry to uv
- Install pytest as a dev dependency
- Fix tests
- Update dependencies
- Update tooling
- Update dependencies
- Update dependencies
- Regenerate readme
- Update dependencies
- Reformat using black
- Clean up help
- Update READMEs and fix a typo. in [#19](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/19)
- Fix config context #18
- Merge pull request #17 from dorkmaneuver/main in [#17](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/17)
- Human readable time formats for choice with '--format' implemented
- Fixed a forgotten semicolon
- Changed also the ok messages to have an idea what is monitored in the web frontend if set to --verbose
- Changed to custom_repos for the array of repos and repo for the single repository as variable or as switch --repo
- Changed the name to the original one: custom_repo - without s in the end. Sorry for messing up in the first place.
- Check the presence of the `custom_repos` option in [#16](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/16)
- Handle multiple repositories in [#14](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/14)
- Handle multiline config values from apt-config dump
- Extend test helper for apt config
- Reorder if statements for the scope selection
- Implement --security
- Refactor
- Update
- Implement --repo, --custom-repo
- Reformat imports
- Test reboot
- Test --dry-run
- Test some scopes
- Upgrade the lock
- Reorder scopes
- Reformat
- Try to fix tests
- Upgrade
- Fix some tests
- Test systemd-timers
- Use test.assertEqual()
- Implement --systemd-timers
- Reformat
- Improve the tests
- Tox.ini
- Pyproject.toml
- Fix all tests
- Fix some linting issues
- Upgrade
- Use freezegun
- Mock open
- Test version
- Fix all tests
- Fix some tests
- Set check name
- Reformat
- Improve testing
- Fix mocking
- Implement warnings-in-log resource and context
- Implement last run
- Parse the log files
- Poetry.lock
- Implement --reboot
- Implement --reboot
- Implement --dry-run
- Check configs
- Check_unattended_upgrades
- Check configs
- Upgrade to nagiosplugin-stubs v0.4.0
- Read the log file using python
- Shebang /bin/zsh
- Extend argparse interface
- Implement --version
- Configure argparse arguments
- Fix dependencies
- Clean up
- Update lock file
- Use /bin/sh instead of /bin/zsh
- Merge pull request #12 from Salzi/Salzi-patch-1 in [#12](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/12)
- Check all line in the log file
- Merge pull request #10 from cicerops/propagate-warnings-errors in [#10](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/10)
- Propagate last-line WARNING and ERROR log messages to check message
- Fix false CRICITAL state by an empty log file

### Fixed
- Fix build

### Removed
- Remove dependency to unittest where possible
- Remove unused variable


## [1.4] - 2019-08-14

### Added
- Add missing test bin to fix tests
- Add more docs and improve the CRITICAL message to fix the file system permission issue #9
- Add warning for the option --dry-run

### Changed
- Bump version 1.4


## [1.3] - 2019-03-08

### Added
- Add some OPT_* variables to the default section
- Add short option -t for --systemd-timers
- Apt timers: add tests
- Apt timers: add long opt, populate USAGE
- Add logs with errors

### Changed
- Version 1.3
- Make plugin output more robust. Use single quotes instead of the unicode characters “ ”
- Fix whitespaces
- Fix whitespaces
- Test the options -n, --dry-run
- Merge pull request #8 from ezbik/apt_timers in [#8](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/8)
- _check_systemd_timer, 1st version
- Merge pull request #6 from ezbik/fix-error-status in [#6](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/6)
- Update tests with `dry run`; updated last line detection
- Readme fix
- Changed cat to echo; added file presense check;
- +embrace dry run with if; add --dry-run check
- +embrace dry run with if; add --dry-run check
- Check the last log line for ERROR and WARNING messages #3
- CRITICAL if unattended-upgrades exists with a non-zero status #3
- Fix tests
- Do not consider log lines containing WARNING or ERROR
- Create description
- Update boilerplate files
- Update project url
- Update README

### Fixed
- Fix systemd path check ( for trusty )


## [1.2] - 2017-09-08

### Added
- Add missing tests
- Add support for checking custom repository

### Changed
- Version 1.2
- Update README
- Merge pull request #2 from MedicMomcilo/master in [#2](https://github.com/Josef-Friedrich/check_unattended_upgrades/pull/2)


## [1.1] - 2017-09-07

### Added
- Add long options
- Add more long options
- Add some long options
- Add more _getopts tests
- Add function _getopts
- Add performance data
- Add more tests
- Add unix timestamps
- Add readme for the tests
- Add debug code
- Add bash unit test file
- Add tests
- Add one more tests
- Add log files
- Add project pages
- Add icingaexchange.yml
- Add if for anacron.
- Add check for anacron.
- Add line breaks.
- Add line breaks.
- Add supprot for Unattended-Upgrade::Origins-Pattern.
- Add descriptions to the default values.
- Add check if apt-config is installed.
- Add reverse sorting for compressed log files.
- Add comment.
- Add state variables.
- Add check for reboot.
- Add informations to check file.
- Add check for configuration APT::Periodic::RandomSleep.
- Add check for -c and -w option.
- Add a check if log file is empty.
- Add -e option to check configuration Apt::Perodic:Enable.
- Add basic documentation.
- Add default check values section.
- Add plugin.

### Changed
- Version 1.1
- Fix test
- Update README
- Small change
- Test all options
- Refactor tests
- Test some options
- Use patch function from test-helper.sh
- Sync skeleton
- Clean up
- Test apt-config
- Refactor
- Fix test
- ASCII art
- Fix tests on arch linux
- Clean up
- Use patched script for testing
- Sync skeleton
- Use bash
- Debug
- Debugging
- Fix test (hopefully)
- Sync with skeleton
- Move logs into separate folder
- Merge branch 'master' of github.com:JosefFriedrich-shell/check_unattended_upgrades
- Update version
- Sync with skeleton.sh
- Sync with skeleton
- Sync with skeleton
- Update icingaexchange.yml
- Sync with skeleton
- Update license
- Short description
- Fix typo
- Fix check for anacron.
- Implement check for security updates.
- Fix if log file is cleared by logrotate.
- Update documentation.
- Rename variable.
- Quotes to if statement.
- Change single quotes to double.
- Initial commit

### Removed
- Remove debug code
- Remove some wrong text in the check messages.
- Remove test log file.


[2.0.0-alpha.1]: https://github.com/Josef-Friedrich/check_unattended_upgrades/compare/v2.0.0-alpha..v2.0.0-alpha.1
[2.0.0-alpha]: https://github.com/Josef-Friedrich/check_unattended_upgrades/compare/1.4..v2.0.0-alpha
[1.4]: https://github.com/Josef-Friedrich/check_unattended_upgrades/compare/1.3..1.4
[1.3]: https://github.com/Josef-Friedrich/check_unattended_upgrades/compare/1.2..1.3
[1.2]: https://github.com/Josef-Friedrich/check_unattended_upgrades/compare/1.1..1.2

<!-- generated by git-cliff -->
