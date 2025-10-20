# Installation Guide

Complete installation instructions for all platforms.

## Table of Contents

- [Ubuntu/Debian](#ubuntudebian)
- [macOS](#macos)
- [Windows (WSL)](#windows-wsl)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Ubuntu/Debian

### Step 1: Update System

```
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Python 3.11

```
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip
```

### Step 3: Install FFmpeg

```
sudo apt install -y \
    ffmpeg \
    libavcodec-extra \
    libsndfile1 \
    libsndfile1-dev \
    portaudio19-dev
```

### Step 4: Install UV

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### Step 5: Clone Repository

```
cd ~/Desktop
git clone https://github.com/TataSatyaPratheek/techno.git
cd techno
```

### Step 6: Install Package

```
uv sync
```

### Step 7: Verify

```
uv run python -c "import techno; print('✓ Success')"
uv run python -m techno.cli.main --help
```

---

## macOS

### Step 1: Install Homebrew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Dependencies

```
brew install python@3.11 ffmpeg portaudio
```

### Step 3: Install UV

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc
```

### Step 4: Clone and Install

```
cd ~/Desktop
git clone https://github.com/TataSatyaPratheek/techno.git
cd techno
uv sync
```

### Step 5: Verify

```
uv run python -c "import techno; print('✓ Success')"
```

---

## Windows (WSL)

### Step 1: Install WSL2

```
# In PowerShell (as Administrator)
wsl --install Ubuntu-24.04
```

### Step 2: Restart and Open Ubuntu

```
# WSL opens automatically after restart
```

### Step 3: Follow Ubuntu Instructions

Inside WSL, follow the [Ubuntu/Debian](#ubuntudebian) steps above.

---

## Verification

### Test Installation

```
# Import check
uv run python -c "
import techno
from techno.core.primitives import Kick
from techno.mixers.minimal import MinimalTechnoMixer
print('✓ All imports successful')
"

# Generate test track
uv run python -m techno.cli.main generate --subgenre minimal --output test.wav

# Play test track
mpv test.wav  # or: vlc test.wav
```

### Run Test Suite

```
uv run pytest
```

Expected output:
```
==================== 115 passed in ~30s ====================
```

---

## Troubleshooting

### Issue: `uv: command not found`

**Solution:**
```
# Reload shell
source ~/.bashrc  # or: source ~/.zshrc

# Or add to PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: `FFmpeg not found`

**Solution:**
```
# Ubuntu/Debian
sudo apt install -y ffmpeg libavcodec-extra

# macOS
brew install ffmpeg

# Verify
ffmpeg -version
which ffmpeg
```

### Issue: `ModuleNotFoundError: No module named 'techno'`

**Solution:**
```
cd ~/Desktop/techno
rm -rf .venv
uv sync
uv run python -c "import techno; print('OK')"
```

### Issue: Tests fail

**Solution:**
```
# Check Python version
python3 --version  # Should be 3.10+

# Reinstall
uv sync --reinstall

# Run tests with verbose output
uv run pytest -vv
```

### Issue: Permission denied (audio)

**Solution:**
```
# Add user to audio group
sudo usermod -aG audio $USER

# Log out and back in for changes to take effect
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4 GB | 8+ GB |
| **Storage** | 2 GB free | 5+ GB free |
| **OS** | Ubuntu 20.04+ | Ubuntu 24.04+ |
| **Python** | 3.10 | 3.11 or 3.12 |

---

## Next Steps

1. Read [README.md](README.md) for usage examples
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
3. Generate your first track!

```
uv run python -m techno.cli.main generate --subgenre minimal --output my_track.wav
mpv my_track.wav
```

---

**Need help?** [Open an issue](https://github.com/TataSatyaPratheek/techno/issues) 🎵
```