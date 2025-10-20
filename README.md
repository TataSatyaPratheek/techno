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

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/techno.git
cd techno

# Install with uv
uv sync

# For development
uv sync --dev
```

### Using pip

```bash
pip install techno
```

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

Generate a track from the command line:

```bash
# Generate a 4-minute minimal techno track
techno generate --bpm 128 --duration 240 --style minimal --output track.wav

# List available styles
techno styles

# Show help
techno --help
```

## Project Structure

```text
techno/
├── cli/                 # Command-line interface
├── core/                # Core audio primitives and utilities
├── composition/         # Musical composition algorithms
├── generators/          # Audio generators and synthesizers
├── mixers/              # Mixing and mastering tools
├── processing/          # Audio effects and processing
├── presets/            # Style presets and configurations
└── tests/              # Comprehensive test suite
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=techno --cov-report=html

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .
```

### Testing

The project maintains high test coverage with comprehensive unit and integration tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=techno --cov-report=term-missing

# Run specific test file
pytest tests/test_generators.py
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
