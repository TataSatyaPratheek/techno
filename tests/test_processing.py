"""
Test processing effects
"""

import numpy as np
from pydub import AudioSegment

from techno.processing.distortion import Distortion
from techno.processing.dynamics import DynamicsProcessor
from techno.processing.spatial import SpatialProcessor

from .conftest import create_sine_wave


class TestDistortion:
    """Test distortion effects"""

    def test_waveshaper_soft(self):
        """Test soft waveshaping"""
        # Create test audio (sine wave)
        test_audio = create_sine_wave(440, 1000)

        result = Distortion.waveshaper(test_audio, drive=0.5, curve="soft")

        assert isinstance(result, AudioSegment)
        assert result.frame_rate == test_audio.frame_rate
        assert result.channels == 1

        # Should be distorted (different from original)
        original_samples = np.array(test_audio.get_array_of_samples())
        result_samples = np.array(result.get_array_of_samples())
        assert not np.allclose(original_samples, result_samples, rtol=0.1)

    def test_waveshaper_hard(self):
        """Test hard waveshaping"""
        test_audio = create_sine_wave(440, 1000)

        result = Distortion.waveshaper(test_audio, drive=0.8, curve="hard")

        assert isinstance(result, AudioSegment)

        # Hard clipping should create flat tops
        samples = np.array(result.get_array_of_samples())
        # Check for clipping (many samples at the clipping level)
        clipped_count = np.sum(np.abs(samples) >= 25000)  # Check for clipping near max
        assert clipped_count > 100  # Should have significant clipping

    def test_bit_crush(self):
        """Test bit crushing"""
        test_audio = create_sine_wave(440, 1000)

        result = Distortion.bit_crush(test_audio, bit_depth=8)

        assert isinstance(result, AudioSegment)

        # Bit crushing should introduce quantization noise
        original_samples = np.array(test_audio.get_array_of_samples())
        result_samples = np.array(result.get_array_of_samples())
        assert not np.allclose(original_samples, result_samples)

        # 8-bit should have fewer unique values
        unique_original = len(np.unique(original_samples))
        unique_result = len(np.unique(result_samples))
        assert unique_result < unique_original

    def test_bit_crush_extreme(self):
        """Test extreme bit crushing"""
        test_audio = create_sine_wave(440, 1000)

        result = Distortion.bit_crush(test_audio, bit_depth=4)

        assert isinstance(result, AudioSegment)

        # 4-bit should have very few unique values
        samples = np.array(result.get_array_of_samples())
        unique_vals = len(np.unique(samples))
        assert unique_vals < 50  # Very quantized


class TestDynamicsProcessor:
    """Test dynamics processing"""

    def test_compress(self):
        """Test compression"""
        # Create dynamic test signal (quiet to loud)
        samples = np.concatenate(
            [
                np.full(1000, 5000, dtype=np.int16),  # Quiet
                np.full(1000, 20000, dtype=np.int16),  # Loud
                np.full(1000, 5000, dtype=np.int16),  # Quiet again
            ]
        )
        test_audio = AudioSegment(data=samples.tobytes(), sample_width=2, frame_rate=44100, channels=1)

        result = DynamicsProcessor.compress(test_audio, threshold_db=-20, ratio=4.0)

        assert isinstance(result, AudioSegment)

        # Compression should reduce dynamic range
        result_samples = np.array(result.get_array_of_samples())
        original_range = np.ptp(samples)  # Peak-to-peak
        result_range = np.ptp(result_samples)
        assert result_range <= original_range * 1.1  # Slight tolerance

    def test_limit(self):
        """Test limiting"""
        # Create signal that exceeds ceiling
        samples = np.full(1000, 30000, dtype=np.int16)  # Very loud
        test_audio = AudioSegment(data=samples.tobytes(), sample_width=2, frame_rate=44100, channels=1)

        result = DynamicsProcessor.limit(test_audio, ceiling_db=-6.0)

        assert isinstance(result, AudioSegment)

        # Should be limited
        result_samples = np.array(result.get_array_of_samples())
        max_level = np.max(np.abs(result_samples))
        expected_max = 10 ** (-6.0 / 20.0) * 32768
        assert max_level <= expected_max + 100  # Small tolerance


class TestSpatialProcessor:
    """Test spatial effects"""

    def test_delay(self):
        """Test delay effect"""
        test_audio = create_sine_wave(440, 1000)

        result = SpatialProcessor.delay(test_audio, delay_ms=100, feedback=0.3, mix=0.5)

        assert isinstance(result, AudioSegment)
        assert result.frame_rate == test_audio.frame_rate

        # Should be different from dry signal
        original_samples = np.array(test_audio.get_array_of_samples())
        result_samples = np.array(result.get_array_of_samples())
        assert not np.allclose(original_samples, result_samples)

    def test_delay_no_feedback(self):
        """Test delay with no feedback"""
        test_audio = create_sine_wave(440, 1000)

        result = SpatialProcessor.delay(test_audio, delay_ms=200, feedback=0.0, mix=1.0)

        assert isinstance(result, AudioSegment)

        # With no feedback and full wet, should have echoes
        samples = np.array(result.get_array_of_samples())
        # Check that signal repeats (rough check)
        delay_samples = int(0.2 * 44100)  # 200ms delay
        if len(samples) > delay_samples * 2:
            # Compare sections
            first_echo_start = delay_samples
            first_echo_end = delay_samples + 1000
            original_section = samples[:1000]
            echo_section = samples[first_echo_start:first_echo_end]
            # Should be similar (allowing for amplitude)
            correlation = np.correlate(original_section, echo_section)[0]
            assert abs(correlation) > 1000  # Some correlation

    def test_stereo_width(self):
        """Test stereo widening"""
        # Start with mono audio
        mono_audio = create_sine_wave(440, 1000)

        result = SpatialProcessor.stereo_width(mono_audio, width=1.5)

        assert isinstance(result, AudioSegment)
        assert result.channels == 2  # Should be stereo
        assert result.frame_rate == mono_audio.frame_rate

        # Stereo samples should be different
        samples = np.array(result.get_array_of_samples())
        left = samples[::2]  # Even indices
        right = samples[1::2]  # Odd indices
        assert not np.allclose(left, right)

    def test_stereo_width_already_stereo(self):
        """Test stereo widening on already stereo audio"""
        # Create stereo audio
        mono = create_sine_wave(440, 1000)
        stereo_audio = mono.set_channels(2)

        result = SpatialProcessor.stereo_width(stereo_audio, width=2.0)

        assert isinstance(result, AudioSegment)
        assert result.channels == 2

    def test_limit(self):
        """Test limiting"""
        # Create signal that exceeds ceiling
        samples = np.full(1000, 30000, dtype=np.int16)  # Very loud
        test_audio = AudioSegment(data=samples.tobytes(), sample_width=2, frame_rate=44100, channels=1)

        result = DynamicsProcessor.limit(test_audio, ceiling_db=-6.0)

        assert isinstance(result, AudioSegment)

        # Should be limited
        result_samples = np.array(result.get_array_of_samples())
        max_level = np.max(np.abs(result_samples))
        expected_max = 10 ** (-6.0 / 20.0) * 32768
        assert max_level <= expected_max + 100  # Small tolerance
