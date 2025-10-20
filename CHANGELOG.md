# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release of the Techno Music Generator
- Algorithmic composition system with structured sections
- Modular synthesis engine for kicks, bass, and percussion
- Audio processing effects (distortion, filtering, compression, spatial)
- Multiple techno styles (minimal, industrial, dub)
- Command-line interface for easy music generation
- Comprehensive test suite with 96% coverage
- CI/CD pipeline with GitHub Actions
- UV package manager integration

### Features

- Generate techno tracks with configurable BPM and duration
- Support for multiple audio formats (WAV, MP3, etc.)
- Extensible plugin architecture
- High-quality audio synthesis using numpy/scipy
- Real-time audio processing capabilities

### Technical

- Python 3.10+ compatibility (development and CI validated on 3.10/3.11/3.12)
- Uses a `src/` development layout (`src/techno`) for reliable static analysis and packaging
- Modern packaging with `pyproject.toml` and Hatchling as the build backend
- Type hints throughout the codebase and strict mypy checks in CI
- CI release/publishing is intentionally disabled in this repository; the
	project is maintained for local development and research and is not
	automatically published to PyPI.
- Professional code quality standards (Black/isort/flake8/mypy/pytest)
