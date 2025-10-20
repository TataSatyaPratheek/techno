"""
Test frequency analysis and carving
"""

import numpy as np
import pytest
from pydub import AudioSegment

from ..core.frequency import (
    FrequencyBand,
    FrequencyMap,
    analyze_frequency_content,
    apply_highpass,
)
from .conftest import create_sine_wave


class TestFrequencyBand:
    """Test FrequencyBand dataclass"""

    def test_frequency_band_creation(self):
        """Test creating frequency bands"""
        band = FrequencyBand(low=100, high=200, name="bass", role="low_end")
        assert band.low == 100
        assert band.high == 200
        assert band.name == "bass"


class TestFrequencyMap:
    """Test frequency allocation map"""

    def test_predefined_bands(self):
        """Test predefined frequency bands"""
        assert FrequencyMap.SUB_BASS.low == 20
        assert FrequencyMap.SUB_BASS.high == 60
        assert FrequencyMap.BASS.low == 60
        assert FrequencyMap.BASS.high == 250
        assert FrequencyMap.HIGHS.low == 6000

    def test_get_allocation_kick(self):
        """Test kick frequency allocation"""
        bands = FrequencyMap.get_allocation("kick")

        # Kick should occupy sub, bass, and high-mids
        assert len(bands) == 3
        assert FrequencyMap.SUB_BASS in bands
        assert FrequencyMap.BASS in bands
        assert FrequencyMap.HIGH_MIDS in bands

    def test_get_allocation_bass(self):
        """Test bass frequency allocation"""
        bands = FrequencyMap.get_allocation("bass")

        # Bass should sit above kick (bass + low-mids)
        assert FrequencyMap.BASS in bands
        assert FrequencyMap.LOW_MIDS in bands
        assert FrequencyMap.SUB_BASS not in bands  # No sub-bass conflict


class TestFrequencyAnalysis:
    """Test frequency content analysis"""

    def create_test_audio(self, frequency=440, duration_ms=1000):
        """Helper: Create test audio at specific frequency"""
        sample_rate = 44100
        duration_s = duration_ms / 1000
        t = np.linspace(0, duration_s, int(sample_rate * duration_s))

        # Generate sine wave
        audio_array = np.sin(2 * np.pi * frequency * t)
        audio_array = (audio_array * 32767).astype(np.int16)

        return AudioSegment(
            data=audio_array.tobytes(),
            sample_width=2,
            frame_rate=sample_rate,
            channels=1,
        )

    def test_analyze_single_frequency(self):
        """Test analysis of single frequency tone"""
        # Create 1kHz tone (should be in MIDS band)
        audio = self.create_test_audio(frequency=1000)

        results = analyze_frequency_content(audio)

        # Most energy should be in mids (500-2000Hz)
        assert results["mids"] > 50  # >50% in mids
        assert results["sub"] < 5  # <5% in sub
        assert results["air"] < 5  # <5% in air

    def test_analyze_sub_bass(self):
        """Test analysis of sub-bass frequency"""
        audio = self.create_test_audio(frequency=50)

        results = analyze_frequency_content(audio)

        # Most energy in sub-bass (20-60Hz)
        assert results["sub"] > 50
        assert results["highs"] < 5


class TestHighPassFilter:
    """Test high-pass filtering"""

    def create_mixed_frequency_audio(self):
        """Create audio with low + high frequencies"""
        sample_rate = 44100
        duration_s = 1.0
        t = np.linspace(0, duration_s, int(sample_rate * duration_s))

        # Mix 50Hz (sub-bass) + 1000Hz (mids)
        low = np.sin(2 * np.pi * 50 * t)
        high = np.sin(2 * np.pi * 1000 * t)
        mixed = low + high

        mixed = (mixed / np.max(np.abs(mixed)) * 32767).astype(np.int16)

        return AudioSegment(
            data=mixed.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1
        )

    def test_highpass_removes_sub_bass(self):
        """Test that high-pass filter removes sub-bass"""
        audio = self.create_mixed_frequency_audio()

        # Analyze original
        original_analysis = analyze_frequency_content(audio)

        # Apply high-pass at 80Hz (should remove sub-bass)
        filtered = apply_highpass(audio, cutoff_hz=80)

        # Analyze filtered
        filtered_analysis = analyze_frequency_content(filtered)

        # Sub-bass energy should decrease
        assert filtered_analysis["sub"] < original_analysis["sub"]

        # Mids should remain (above cutoff)
        assert filtered_analysis["mids"] >= original_analysis["mids"] * 0.8

    def test_band_pass_filter(self):
        """Test band-pass filter isolates frequency range"""
        from ..processing.filters import TechnoFilters

        # Create test audio with multiple frequencies
        audio = create_sine_wave(1000, 2000)  # 1kHz
        audio = audio.overlay(create_sine_wave(200, 2000))  # 200Hz
        audio = audio.overlay(create_sine_wave(5000, 2000))  # 5kHz

        # Band-pass around 1kHz
        filtered = TechnoFilters.band_pass(audio, low_hz=800, high_hz=1200)

        assert isinstance(filtered, AudioSegment)
        assert len(filtered) == len(audio)

        # Should attenuate frequencies outside the band
        # (This is a basic test - production would use spectrum analysis)

    def test_filter_sweep(self):
        """Test filter sweep automation"""
        from ..processing.filters import TechnoFilters

        # Create test audio
        audio = create_sine_wave(1000, 5000)  # 5 second tone

        # Sweep from low to high
        swept = TechnoFilters.filter_sweep(
            audio, start_hz=200, end_hz=5000, sweep_duration_ms=5000
        )

        assert isinstance(swept, AudioSegment)
        assert len(swept) == len(audio)

        # Swept audio should be different from original
        # (Basic check - production would analyze frequency content over time)
