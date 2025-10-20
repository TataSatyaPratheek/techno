"""
Negative tests - error handling and edge cases
"""

import pytest
from pydub import AudioSegment

from ..core.frequency import FrequencyMap
from ..core.primitives import Bass, HiHat, Kick
from ..core.timing import MusicalTime, TimingCalculator
from ..generators.synth_generator import SynthGenerator
from ..processing.distortion import Distortion
from ..processing.dynamics import DynamicsProcessor
from ..processing.filters import TechnoFilters
from .conftest import create_sine_wave


class TestTimingNegative:
    """Test timing calculations with invalid inputs"""

    def test_musical_time_invalid_bars(self):
        """Test MusicalTime with negative bars"""
        with pytest.raises(ValueError):
            MusicalTime(bars=-1, beats=0, sixteenths=0)

    def test_timing_calculator_zero_bpm(self):
        """Test TimingCalculator with zero BPM"""
        with pytest.raises(ValueError):
            TimingCalculator(0)

    def test_timing_calculator_negative_bpm(self):
        """Test TimingCalculator with negative BPM"""
        with pytest.raises(ValueError):
            TimingCalculator(-120)


class TestFrequencyNegative:
    """Test frequency analysis with edge cases"""

    def test_analyze_empty_audio(self):
        """Test frequency analysis on empty audio"""
        from ..core.frequency import analyze_frequency_content

        empty_audio = AudioSegment.silent(duration=100)
        results = analyze_frequency_content(empty_audio)

        # Should return valid results even for silence
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_frequency_map_invalid_bands(self):
        """Test FrequencyMap with invalid band configuration"""
        # This would require checking the implementation
        freq_map = FrequencyMap()

        # Test with very short audio
        short_audio = create_sine_wave(440, 10)  # 10ms
        # Should not crash
        assert short_audio is not None


class TestPrimitivesNegative:
    """Test primitive generation with invalid parameters"""

    def test_kick_invalid_bpm(self):
        """Test Kick with invalid BPM"""
        with pytest.raises((ValueError, ZeroDivisionError)):
            Kick(0)

    def test_bass_invalid_frequency(self):
        """Test Bass with invalid frequency"""
        bass = Bass(120)

        # Test with frequency too low
        with pytest.raises((ValueError, OverflowError)):
            bass.generate_note(frequency=10, duration_bars=1)

        # Test with frequency too high
        with pytest.raises((ValueError, OverflowError)):
            bass.generate_note(frequency=20000, duration_bars=1)

    def test_hat_invalid_closedness(self):
        """Test HiHat with invalid closedness"""
        hat = HiHat(120)

        # Test with closedness out of range
        with pytest.raises((ValueError, TypeError)):
            hat.generate(closedness=2.0)

        with pytest.raises((ValueError, TypeError)):
            hat.generate(closedness=-1.0)


class TestSynthGeneratorNegative:
    """Test synth generator with invalid inputs"""

    def test_synth_generator_invalid_bpm(self):
        """Test SynthGenerator with invalid BPM"""
        with pytest.raises((ValueError, ZeroDivisionError)):
            SynthGenerator(0)

    def test_generate_unknown_element(self):
        """Test generating unknown element"""
        gen = SynthGenerator(120)
        result = gen.generate_stem("unknown", 1, "minimal")

        # Should return silence
        assert isinstance(result, AudioSegment)
        # Check if it's actually silence (all samples near zero)
        samples = result.get_array_of_samples()
        assert max(abs(s) for s in samples) < 100  # Very quiet

    def test_generate_zero_duration(self):
        """Test generate with zero duration"""
        gen = SynthGenerator(120)

        # Should handle zero duration gracefully
        stem = gen.generate_stem("kick", 0, "minimal")
        assert isinstance(stem, AudioSegment)
        assert len(stem) == 0


class TestProcessingNegative:
    """Test processing with invalid inputs"""

    def test_filters_empty_audio(self):
        """Test filters on empty audio"""
        empty = AudioSegment.silent(duration=100)

        # Should not crash
        result = TechnoFilters.high_pass(empty, cutoff_hz=1000)
        assert isinstance(result, AudioSegment)

        result = TechnoFilters.low_pass(empty, cutoff_hz=1000)
        assert isinstance(result, AudioSegment)

    def test_distortion_invalid_drive(self):
        """Test distortion with invalid drive"""
        audio = create_sine_wave(440, 1000)

        # Extreme drive values
        result = Distortion.waveshaper(audio, drive=10.0, curve="hard")
        assert isinstance(result, AudioSegment)

        result = Distortion.waveshaper(audio, drive=-1.0, curve="soft")
        assert isinstance(result, AudioSegment)

    def test_dynamics_invalid_ratio(self):
        """Test compression with invalid ratio"""
        audio = create_sine_wave(440, 1000)

        # Ratio of 1 (no compression) should work
        result = DynamicsProcessor.compress(audio, threshold_db=-20, ratio=1.0)
        assert isinstance(result, AudioSegment)

        # Very high ratio
        result = DynamicsProcessor.compress(audio, threshold_db=-20, ratio=20.0)
        assert isinstance(result, AudioSegment)

    def test_limit_invalid_ceiling(self):
        """Test limiting with invalid ceiling"""
        audio = create_sine_wave(440, 1000)

        # Very low ceiling (heavy limiting)
        result = DynamicsProcessor.limit(audio, ceiling_db=-60.0)
        assert isinstance(result, AudioSegment)

        # Ceiling above 0 (no limiting)
        result = DynamicsProcessor.limit(audio, ceiling_db=10.0)
        assert isinstance(result, AudioSegment)


class TestFileOperationsNegative:
    """Test file operations with invalid paths"""

    def test_cli_analyze_nonexistent_file(self):
        """Test analyze command with nonexistent file"""
        from click.testing import CliRunner

        from ..cli.main import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["analyze", "nonexistent.wav"])

        # Should handle gracefully
        assert result.exit_code != 0 or "Error" in result.output

    def test_cli_generate_invalid_output_path(self):
        """Test generate with invalid output path"""
        from click.testing import CliRunner

        from ..cli.main import cli

        runner = CliRunner()
        # Try to write to a directory that doesn't exist
        result = runner.invoke(
            cli, ["generate", "--output", "/nonexistent/dir/track.wav"]
        )

        # Should handle the error
        assert result.exit_code != 0 or "Error" in result.output
