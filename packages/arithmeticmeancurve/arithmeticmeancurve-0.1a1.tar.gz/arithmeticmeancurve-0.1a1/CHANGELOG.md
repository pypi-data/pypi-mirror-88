# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
## [0.1a1] - 2020-12-17
### Fixed
- Bug resulting in missing mean curve values, if the mean value of the ending abscissa
  values (x-values) was less then the *end cap or end section*.

### Changed
- Versioning via setuptools purely by git tags.
- *examplecurves>=0.2a1* are required.

## [0.1a0] - 2020-12-06
### Added
- Class *VisualIterationTester* for calculating and plotting the iterations
  during the extrapolation process of the mean curve calculation.

### Changed
- Outsourced *examplecurves* into an individual module at 
  http://gitlab.com/david.scheliga/examplecurves
- Fixed documentation in regard of the outsourced *examplecurves* module

### Removed
- Unintentional private method in arithmeticmeancurves.\_\_all\_\_
- Module *examplecurves* from setup.py.

## [0.0a1.post3] - 2020-12-03
### Added
- Basic usage to README.md and the sphinx documentation

### Fixed
- Minor wrong definitions within README.md
- Wrong compilation of basic_usage.rst at readthedocs.org

## [0.0a1] - 2020-12-02
- First code release of arithmeticmeancurve