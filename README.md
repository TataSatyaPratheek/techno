# Techno Music Generator

A comprehensive Python library for generating techno music using algorithmic composition, synthesis, and audio processing techniques.

## Features

- **Algorithmic Composition**: Generate techno tracks with structured sections (intro, breakdown, build-up, drop)
- **Modular Synthesis**: Create kicks, basslines, hi-hats, and percussion using various synthesis techniques
- **Audio Processing**: Apply effects like distortion, filtering, compression, and spatial processing
- **Multiple Styles**: Support for minimal, industrial, and dub techno variants
- **CLI Interface**: Command-line tools for easy music generation
- **Extensible Architecture**: Plugin system for custom generators and processors

## Installation

This project uses a "src/" development layout (sources live under `src/techno`). The recommended workflow for local development is an editable install so your source edits are available immediately.

### Development (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/techno.git
cd techno

# Create the project environment and install development dependencies
# The recommended workflow is an editable install so source edits apply immediately.
uv sync --dev
pip install -e .
```

If you prefer to use only the environment manager/task runner provided in this project, `uv sync --dev` will create the environment and perform an editable install as configured.

NOTE: This repository is intended as a local research/development project and is not published to PyPI. Prefer editable installs or locally-built wheels for private distribution.

## Quick Start

Generate a basic techno track:

```python
from techno.generators import SynthGenerator
from techno.mixers import MinimalTechnoMixer

# Create a generator
generator = SynthGenerator(bpm=128)

# Generate stems
stems = generator.generate_all_stems(duration_bars=16, style='minimal')

# Mix the track
mixer = MinimalTechnoMixer()
final_track = mixer.mix(stems)

# Export
final_track.export("my_track.wav", format="wav")
```

## CLI Usage

After installing (editable or from a locally-built wheel) you can use the `techno` command-line entry points installed into your environment.

```bash
# Generate a 4-minute minimal techno track (example)
techno generate --bpm 128 --duration 240 --style minimal --output track.wav

# List available styles
techno styles

# Show help
techno --help
```

## Project Structure (development layout)

Sources live under `src/techno/` for clean packaging and reliable static analysis. The working tree looks like this:

```text
src/techno/
├── cli/                 # Command-line interface
├── core/                # Core audio primitives and utilities
├── composition/         # Musical composition algorithms
├── generators/          # Audio generators and synthesizers
├── mixers/              # Mixing and mastering tools
├── processing/          # Audio effects and processing
├── presets/             # Style presets and configurations
└── tests/               # Comprehensive test suite (also available at tests/)
```

When installed into an environment (editable or from a wheel built locally) the package is importable as `import techno`.

## Development

### Setup Development Environment

```bash
# Install development dependencies and activate the environment
uv sync --dev

# (optional) run the environment's task commands via uv
uv run pytest --cov=techno --cov-report=html

# Format and lint
uv run black --check --diff .
uv run isort --check-only --diff .
uv run flake8 techno tests

# Type checking
uv run mypy techno
```

### Testing

The project maintains comprehensive unit and integration tests. Run them from the repo root (the test runner is configured to find `src`):

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=techno --cov-report=term-missing

# Run a specific test file
uv run pytest tests/test_generators.py
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Architecture

## Developer quickstart

A compact set of copy-paste commands to get a new developer productive quickly.

1. Clone and create the development environment

```bash
# From the project root
git clone https://github.com/yourusername/techno.git
cd techno
uv sync --dev
```

1. Editable install (recommended while developing)

```bash
# Installs the package in editable mode so changes take effect immediately
pip install -e .
```

1. Common developer commands

```bash
# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_cli.py

# Format and check formatting
uv run black .
uv run isort .

# Run linters and type checks
uv run flake8 techno tests
uv run mypy techno

# Run the CLI locally (after editable install)
techno --help
techno generate --bpm 120 --duration 60 --style minimal --output ./out.wav
```

## Local release / private wheel (HOWTO)

When you need to build a distributable artifact for private sharing (not PyPI), use a locally-built wheel and install it into an isolated virtual environment for testing.

1. Build a wheel locally

```bash
# Ensure build tools are installed in the dev env
uv run pip install build

# Build a wheel into dist/
uv run python -m build --wheel --outdir dist
```

2. Create an isolated virtualenv and install the wheel

```bash
# Create an isolated venv
python -m venv /tmp/techno-test-venv
source /tmp/techno-test-venv/bin/activate

# Install the wheel (replace with exact wheel filename)
pip install dist/techno-*.whl

# Smoke-test the CLI
techno --help
techno styles

# When done, deactivate
deactivate
```

Notes:

- Use a private artifact repository (internal Nexus/Artifactory) if you need to share wheels across a team.
- Avoid adding publishing automation to CI unless you have a secure, audited process and a maintainer-approved policy.

The system follows a layered architecture:

- **Primitives**: Basic audio building blocks (Kick, Bass, HiHat)
- **Composition**: Musical structure and arrangement
- **Generation**: Audio synthesis and pattern creation
- **Processing**: Effects and audio manipulation
- **Mixing**: Final track assembly and mastering

## Dependencies

- **numpy**: Numerical computing and DSP
- **scipy**: Scientific computing and signal processing
- **pydub**: Audio manipulation and file I/O
- **click**: Command-line interface framework
- **pyyaml**: Configuration file parsing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic techno production techniques
- Built with modern Python audio processing libraries
- Designed for algorithmic music composition research
