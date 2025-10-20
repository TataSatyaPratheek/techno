"""
Test synthesis utilities
"""

import numpy as np

from ..core.synthesis import EnvelopeGenerator, WaveformGenerator


class TestWaveformGenerator:
    """Test waveform generation"""

    def test_sine_wave(self):
        """Test sine wave generation"""
        freq = 440
        duration = 1.0
        sample_rate = 44100
        wave = WaveformGenerator.sine(freq, duration, sample_rate)

        # Check shape
        expected_samples = int(sample_rate * duration)
        assert len(wave) == expected_samples

        # Check values are between -1 and 1
        assert np.all(wave >= -1)
        assert np.all(wave <= 1)

        # Check frequency (rough check)
        # Sine wave should complete freq cycles in duration
        zero_crossings = np.sum(np.diff(np.sign(wave)) != 0)
        expected_crossings = freq * 2  # approx
        assert abs(zero_crossings - expected_crossings) < 10  # tolerance

    def test_sawtooth_wave(self):
        """Test sawtooth wave generation"""
        freq = 220
        duration = 0.5
        wave = WaveformGenerator.sawtooth(freq, duration)

        assert len(wave) == int(44100 * duration)
        assert np.all(wave >= -1)
        assert np.all(wave <= 1)

        # Sawtooth should have more harmonics, check it's not sine
        sine_wave = WaveformGenerator.sine(freq, duration)
        assert not np.allclose(wave, sine_wave, rtol=0.1)

    def test_square_wave(self):
        """Test square wave generation"""
        freq = 110
        duration = 0.25
        wave = WaveformGenerator.square(freq, duration)

        assert len(wave) == int(44100 * duration)
        assert np.all(wave >= -1)
        assert np.all(wave <= 1)

        # Square wave should be mostly -1 or 1
        unique_vals = np.unique(np.round(wave))
        assert len(unique_vals) <= 3  # -1, 0, 1 approximately

    def test_triangle_wave(self):
        """Test triangle wave generation"""
        freq = 330
        duration = 0.33
        wave = WaveformGenerator.triangle(freq, duration)

        assert len(wave) == int(44100 * duration)
        assert np.all(wave >= -1)
        assert np.all(wave <= 1)

        # Triangle should be smoother than square
        square_wave = WaveformGenerator.square(freq, duration)
        assert not np.allclose(wave, square_wave, rtol=0.1)


class TestEnvelopeGenerator:
    """Test envelope generation"""

    def test_adsr_envelope(self):
        """Test ADSR envelope generation"""
        attack = 0.1
        decay = 0.2
        sustain = 0.7
        release = 0.3
        duration = 1.0

        envelope = EnvelopeGenerator.adsr(attack, decay, sustain, release, duration)

        # Check length
        expected_samples = int(44100 * duration)
        assert len(envelope) == expected_samples

        # Check values between 0 and 1
        assert np.all(envelope >= 0)
        assert np.all(envelope <= 1)

        # Check attack phase reaches 1
        attack_samples = int(44100 * attack)
        assert envelope[attack_samples - 1] >= 0.99

        # Check sustain level
        sustain_start = int(44100 * (attack + decay))
        sustain_end = int(44100 * (duration - release))
        sustain_values = envelope[sustain_start:sustain_end]
        assert np.all(sustain_values >= sustain - 0.01)
        assert np.all(sustain_values <= sustain + 0.01)

        # Check release goes to 0
        assert envelope[-1] < 0.01

    def test_adsr_edge_cases(self):
        """Test ADSR with edge case parameters"""
        # Very short phases
        envelope = EnvelopeGenerator.adsr(0.01, 0.01, 0.5, 0.01, 0.1)
        assert len(envelope) == int(44100 * 0.1)
        assert np.all(envelope >= 0)
        assert np.all(envelope <= 1)

        # Sustain level 0
        envelope = EnvelopeGenerator.adsr(0.1, 0.1, 0.0, 0.1, 0.5)
        sustain_start = int(44100 * 0.2)
        sustain_end = int(44100 * 0.4)
        assert np.all(envelope[sustain_start:sustain_end] < 0.01)

    def test_exponential_decay(self):
        """Test exponential decay envelope"""
        duration = 2.0
        decay_rate = 2.0

        envelope = EnvelopeGenerator.exponential_decay(duration, decay_rate)

        # Check length and values
        expected_samples = int(44100 * duration)
        assert len(envelope) == expected_samples
        assert np.all(envelope >= 0)
        assert np.all(envelope <= 1)

        # Check it starts at 1 and decays
        assert envelope[0] >= 0.99
        assert envelope[-1] < envelope[0]

        # Check exponential shape (rough check)
        # Should decay faster at the beginning
        mid_point = len(envelope) // 2
        assert envelope[mid_point] < envelope[0] * 0.5
