# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [UNRELEASED]

### Changed

- Not setting default AWS_SHARED_CREDENTIALS, using AWS_REGION then AWS_DEFAULT_REGION if not defined.

### Documentation

- Added reference to RTD of aws plugins
- Added warning about not including [all] to install plugins, minor adjustments.

## [0.12.0] - 2022-10-28

### Changed

- Updated README to contain new UX for installing plugins

## [0.11.0] - 2022-10-27

### Changed

- Updated requirements.txt to contain commas separating gte, and lt inequalities in covalent version

## [0.10.0] - 2022-10-27

### Changed

- Updated setup.py to contain commas separating gte, and lt inequalities in the plugin versions

## [0.9.0] - 2022-10-27

### Changed

- Added Alejandro to paul blart

## [0.8.0] - 2022-10-27

### Added

- Update individual plugin version in `setup.py`

## [0.7.0] - 2022-10-25

### Changed

- Removed file based approach to distinguish plugin installs, simply use `extras_require` parameter in `setup_info`

## [0.6.2] - 2022-10-25

### Fixed

- Make plugin version requirements more flexible.

## [0.6.1] - 2022-10-25

### Fixed

- Premature covalent base plugins only file removal.

## [0.6.0] - 2022-10-25

### Changed

- Updated version of covalent to 0.202.0

### Docs

- Updated README to reflect the fact that this plugin now installs each individual executor plugin
- Added a few lines about the plugin ecosystem and covalent

## [0.5.0] - 2022-10-06

### Fixed

- `BASE_COVALENT_AWS_PLUGINS_ONLY` needs to be removed after all the installations are complete.

### Changed

- Pre-release versions of the plugins in the corresponding requirements file.

## [0.4.1] - 2022-10-05

### Fixed

- Store / Read `BASE_COVALENT_AWS_PLUGINS_ONLY` in a temporary file rather than storing it as an environment variable.

## [0.4.0] - 2022-10-04

### Changed

- Setting `BASE_COVALENT_AWS_PLUGINS_ONLY` environment system wide to circumvent `setup.py` subprocesses when installing.

## [0.3.0] - 2022-10-03

### Changed

- Added back import of `AWSExecutor` in `covalent_aws_plugins/__init__.py` to enable `from covalent_aws_plugins import AWSExecutor`.

## [0.2.0] - 2022-10-03
### Operations

- Added license workflow


### Added 

- Logic to check if only the base requirements file in the plugins repo is to be installed. When not True, the `requirements-plugins-suite.txt` packages are also installed in addition to the `requirements.txt` packages.
- Added aws plugins to be installed in `requirement-plugins-suite.txt`.

## [0.1.0] - 2022-09-15

### Added

- `Dockerfile` for the base docker image for all AWS cloud executor plugins
- `CHANGELOG` file
- Added first iteration of `AWSExecutor` and AWS Executor exceptions
