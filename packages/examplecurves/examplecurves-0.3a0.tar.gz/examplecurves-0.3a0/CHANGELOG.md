# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3a0] - 2020-12-17
### Added
- New families of curves *HorizontalLinear1*, *HorizontalLinear2* and
 *HorizontalLinear3*.

## [0.2a1] - 2020-12-17
### Fixed
- Missing parameter leading to broken installation.
- Missing requirement 'dicthandling'

## [0.2a0] - 2020-12-15
### Added
- A normal distributed linear family of curves with *LinearHorizontal0*.
- Support for loading curve creation parameters from json files.
- *resources* subpackage for parameter files.

### Changed
- Turned module `examplecurves.py` into a `examplecurves` package.
- Shifted project to *setuptools_scm*; updated setup.py

### Removed
- Constant \_\_version\_\_ is removed; package version is now managed solely by git
  tags.

## [0.1a0] - 2020-12-05
### Changed
- added class `Static` to distinguish static curves from random curves, which
  are on the way.

### deprecated
- Method `create` will be moved to `Static` in the next release.

## [0.0a1] - 2020-12-05
- First code release of examplecurves