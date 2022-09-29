# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [UNRELEASED]

### Added 

- Logic to check if only the base requirements file in the plugins repo is to be installed. When not True, the `requirements-plugins-suite.txt` packages are also installed in addition to the `requirements.txt` packages.
- Added aws plugins to be installed in `requirement-plugins-suite.txt`.

## [0.1.0] - 2022-09-15

### Added

- `Dockerfile` for the base docker image for all AWS cloud executor plugins
- `CHANGELOG` file
- Added first iteration of `AWSExecutor` and AWS Executor exceptions
