# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- improve interoperability with Jabref/fix file encoding issues when dumping bibtex
- parse keywords, summary from posts and replies

### Changed
- Add type hint to prevent hard-to-find bugs

## [0.13.0] - 2020-06-20
### Added
- reload after posting a new paper to list
- implement CI and capture test coverage
- add --debug argument
- improve interoperability with Mac/Windows
- save config, data and log files to system paths
- add --paths argument to print config file paths for easier cleanup
- add Changelog, LICENSE and Makefile

### Fixed
- fixed crash when opening details for "Theme issue: Stokes at 200" (no author)
- harden against failing DOI requests
- fix and improve --dump-posts

### Changed
- reload list after posting a new paper to list


## [0.12.0] - 2020-09-03
### Added
- cache data in a tinydb database to speed up start time and save on api calls
- add --version argument
- write log files

### Fixed
- retrieve *all* mattermost posts


## [0.7.0] - 2020-
### Changed
- massively increase search by doi performance by debouncing query


## [0.6.0] - 2020-
### Added
- options to dump posts and bib to stdout


## [0.5.0] - 2020-
### Added
- add "submit new paper" feature
- escape program on esc

### Changed
- make buttons prettier


## [Initial] - 2020-08-09
- publish to pip
- Add interactive configuration and use channel name instead of channel id
- add loading indicator and info popup for papers with data from doi.org
- make bibtex export more robust
- start to try to prettify button
- add experimental export-to-bibtex support
- add doi link
- highlight searchterm in matches
- get, display and also search by reporter
- open paper discussion thread in browser
- make paper list stretch vertically
