"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path
import tempfile
import numpy as np
from pydub import AudioSegment


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_bpm():
    """Standard test BPM"""
    return 130


def create_sine_wave(frequency: float, duration_ms: int, sample_rate: int = 44100) -> AudioSegment:
    """Create a sine wave AudioSegment for testing"""
    duration_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, duration_samples)
    samples = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit integers
    samples_int = (samples * 32767).astype(np.int16)
    
    return AudioSegment(
        data=samples_int.tobytes(),
        sample_width=2,
        frame_rate=sample_rate,
        channels=1
    )


@pytest.fixture
def sample_rate():
    """Standard sample rate"""
    return 44100
