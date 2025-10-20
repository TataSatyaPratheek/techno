# 🎵 Techno Generator

[![CI/CD](https://github.com/TataSatyaPratheek/techno/actions/workflows/ci.yml/badge.svg)](https://github.com/TataSatyaPratheek/techno/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/TataSatyaPratheek/techno/branch/main/graph/badge.svg)](https://codecov.io/gh/TataSatyaPratheek/techno)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Fundamentals-first techno music production system built with Python.**

Generate authentic minimal, industrial, dub, and acid techno tracks from scratch using pure synthesis and composition algorithms.

## ✨ Features

- 🎹 **Pure Synthesis**: Generate kicks, bass, and hi-hats from scratch (no samples)
- 🎼 **Musical Structure**: Bar-aligned composition with proper timing
- 🎚️ **Frequency Management**: Intelligent EQ and frequency carving to prevent mud
- 🎨 **Multiple Subgenres**: Minimal (124 BPM), Industrial (138 BPM), Dub (118 BPM), Acid (135 BPM)
- 🧪 **95% Test Coverage**: Production-ready with 115+ passing tests
- ⚡ **Fast**: Generate 30-second tracks in ~10 seconds on modern hardware

## 🚀 Quick Start

### Prerequisites

- Python 3.10, 3.11, or 3.12
- FFmpeg (required for audio processing)
- Linux, macOS, or Windows (WSL recommended)

### Installation

#### Ubuntu/Debian

```
# 1. Install system dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv ffmpeg libavcodec-extra libsndfile1

# 2. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 3. Clone repository
git clone https://github.com/TataSatyaPratheek/techno.git
cd techno

# 4. Install package and dependencies
uv sync

# 5. Verify installation
uv run python -c "import techno; print('✓ Installation successful')"
```

#### macOS

```
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install dependencies
brew install python@3.11 ffmpeg

# 3. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc

# 4. Clone and install
git clone https://github.com/TataSatyaPratheek/techno.git
cd techno
uv sync

# 5. Verify
uv run python -c "import techno; print('✓ Installation successful')"
```

#### Windows (WSL2)

```
# Use Ubuntu WSL2 and follow Ubuntu instructions above
wsl --install Ubuntu-24.04
# Then follow Ubuntu installation steps
```

### Generate Your First Track

```
# Generate minimal techno (124 BPM, hypnotic)
uv run python -m techno.cli.main generate --subgenre minimal --output minimal.wav

# Generate industrial techno (138 BPM, aggressive)
uv run python -m techno.cli.main generate --subgenre industrial --output industrial.wav

# Generate with custom BPM
uv run python -m techno.cli.main generate --subgenre minimal --bpm 130 --output custom.wav

# List all available presets
uv run python -m techno.cli.main list-presets

# Analyze frequency content
uv run python -m techno.cli.main analyze minimal.wav
```

### Play Generated Tracks

```
# Install audio player
sudo apt install mpv  # Ubuntu/Debian
brew install mpv      # macOS

# Play track
mpv minimal.wav
```

## 📖 Usage

### Command Line Interface

```
# Help
uv run python -m techno.cli.main --help

# Generate tracks
uv run python -m techno.cli.main generate [OPTIONS]

Options:
  --subgenre TEXT    Subgenre: minimal, industrial, dub, acid [required]
  --bpm INTEGER      Override default BPM [optional]
  --output TEXT      Output filename [default: output.wav]
  --help            Show this message and exit

# List presets
uv run python -m techno.cli.main list-presets

# Analyze audio
uv run python -m techno.cli.main analyze <file.wav>
```

### Programmatic Usage

```
from techno.mixers.minimal import MinimalTechnoMixer
from techno.mixers.industrial import IndustrialTechnoMixer

# Generate minimal techno
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()
track.export("minimal_track.wav", format="wav")

# Generate industrial techno
mixer = IndustrialTechnoMixer(bpm=138)
track = mixer.create_track()
track.export("industrial_track.wav", format="wav")
```

### Custom Track Structure

```
from techno.composition.structure import TrackComposer, TrackStructure

composer = TrackComposer(bpm=130)

# Define custom structure
structure = TrackStructure(
    name="custom",
    sections=[
        {'name': 'intro', 'bars': 8, 'style': 'minimal'},
        {'name': 'buildup', 'bars': 16, 'filter_sweep': True},
        {'name': 'drop', 'bars': 24, 'energy': 1.0},
        {'name': 'breakdown', 'bars': 8, 'remove': ['hats']},
        {'name': 'outro', 'bars': 8, 'fade_out': True}
    ],
    total_bars=64
)

track = composer.compose(structure)
track.export("custom_track.wav", format="wav")
```

### Synthesis Examples

```
from techno.core.primitives import Kick, Bass, HiHat
from techno.core.timing import TimingCalculator

# Generate kick drum
kick = Kick(bpm=130)
kick_audio = kick.generate_minimal()  # Clean kick
kick_audio.export("kick.wav", format="wav")

# Generate bassline
bass = Bass(bpm=130)
note_freq = 110  # A2
bass_note = bass.generate_note(frequency=note_freq)
bass_note.export("bass_note.wav", format="wav")

# Generate hi-hats
hat = HiHat(bpm=130)
closed_hat = hat.generate(closedness=0.9)  # 0=open, 1=closed
closed_hat.export("hat.wav", format="wav")
```

## 🎛️ Available Subgenres

| Subgenre | BPM | Style | Characteristics |
|----------|-----|-------|-----------------|
| **Minimal** | 124 | Hypnotic, sparse | Robert Hood, Richie Hawtin style |
| **Industrial** | 138 | Aggressive, harsh | Ancient Methods, Surgeon style |
| **Dub** | 118 | Deep, spacious | Basic Channel, Deepchord style |
| **Acid** | 135 | 303-driven, squelchy | Phuture, Hardfloor style |

## 🧪 Testing

```
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=techno --cov-report=html
firefox htmlcov/index.html  # View report

# Run specific test file
uv run pytest tests/test_timing.py -v

# Run tests matching pattern
uv run pytest -k "minimal" -v
```

## 🛠️ Development

### Setup Development Environment

```
# Clone repo
git clone https://github.com/TataSatyaPratheek/techno.git
cd techno

# Install with dev dependencies
uv sync

# Verify setup
uv run pytest
```

### Code Quality

```
# Format code
uv run black src/techno tests

# Sort imports
uv run isort src/techno tests

# Type checking
uv run mypy src/techno

# Linting
uv run flake8 src/techno tests --max-line-length=127

# Run all checks
uv run black . && uv run isort . && uv run mypy src/techno && uv run pytest
```

### Project Structure

```
techno/
├── src/techno/           # Source code
│   ├── cli/              # Command-line interface
│   ├── core/             # Core primitives (Kick, Bass, HiHat)
│   ├── composition/      # Musical structure (Phrase, Section, Structure)
│   ├── generators/       # Stem generators (Synth, MusicGPT)
│   ├── mixers/           # Subgenre-specific mixers
│   ├── processing/       # Audio effects (Filters, Distortion, Dynamics)
│   └── presets/          # YAML configuration files
├── tests/                # Test suite (115+ tests, 95% coverage)
├── pyproject.toml        # Package configuration
└── README.md             # This file
```

## 🎼 Musical Architecture

### Fundamentals-First Design

The system is built in layers:

1. **Primitives** (`core/primitives.py`): Kick, Bass, HiHat synthesis
2. **Timing** (`core/timing.py`): Bar-aligned musical time
3. **Phrases** (`composition/phrase.py`): 8-bar loops
4. **Sections** (`composition/section.py`): Intro, buildup, drop, breakdown
5. **Structure** (`composition/structure.py`): Complete track assembly
6. **Mixers** (`mixers/`): Subgenre-specific processing

### Frequency Management

Intelligent frequency allocation prevents muddy mixes:

- **Sub-bass** (20-60 Hz): Kick fundamental
- **Bass** (60-250 Hz): Kick body + bass notes
- **Low-mids** (250-500 Hz): Bass harmonics
- **Mids** (500-2000 Hz): Body and presence
- **High-mids** (2-6 kHz): Transients
- **Highs** (6-12 kHz): Hi-hats, air

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Inspired by:
- **Minimal Techno**: Robert Hood, Richie Hawtin
- **Industrial Techno**: Ancient Methods, Surgeon, Regis
- **Dub Techno**: Basic Channel, Deepchord, cv313
- **Acid Techno**: Phuture, Hardfloor, Chris Liberator

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/TataSatyaPratheek/techno/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TataSatyaPratheek/techno/discussions)

## 🗺️ Roadmap

- [ ] MIDI export support
- [ ] Real-time parameter automation
- [ ] Audio input processing (remix mode)
- [ ] VST plugin wrapper
- [ ] Web interface (Gradio/Streamlit)
- [ ] More subgenres (Hard Techno, Detroit Techno)

---

**Made with 🎵 by the Techno Generator Team**
