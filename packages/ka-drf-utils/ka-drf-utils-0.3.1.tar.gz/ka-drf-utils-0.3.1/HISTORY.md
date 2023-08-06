# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2020 - 12 - 14
### Fixed
- fix signaling in LogViewSetMixin if user anonymous

## [0.3.0] - 2020 - 12 - 13
### Changed
- Simplify log module

### Removed
- Remove LogSerializerMixin

## [0.2.0] - 2020 - 12 - 13
### Removed
- Remove translation module

### Fixed
- Fix exchange on publisher 

## [0.1.1] - 2020 - 12 - 09
### Fixed
- Fix history.md in a setup.py 

## [0.1.0] - 2020 - 12 - 09
### Added
- TimestampedSerializerMixin for Timestamped Model
- SoftDeleteViewSetMixin for handling soft delete data 
- BaseModel for SoftDelete and Timestamped Model
- Helper for parse identity from href
- LinkHeaderPagination
- Custom receiver django signal
- Custom exception handler
- BasicPublisher class
- Translation module
- Activity Log module