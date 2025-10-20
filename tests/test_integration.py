"""
Integration tests - end-to-end functionality
"""

from unittest import mock

from pydub import AudioSegment

from ..generators.synth_generator import SynthGenerator
from ..mixers.minimal import MinimalTechnoMixer
from ..processing.dynamics import DynamicsProcessor
from ..processing.filters import TechnoFilters
from .conftest import create_sine_wave


class TestEndToEndGeneration:
    """Test complete generation pipelines"""

    def test_full_synth_generation_pipeline(self):
        """Test generating a complete track with synth generator"""
        # This tests the integration of SynthGenerator with primitives
        gen = SynthGenerator(128)

        # Generate all stems
        stems = gen.generate_all_stems(duration_bars=2, style="minimal")

        assert len(stems) == 3
        assert "kick" in stems
        assert "bass" in stems
        assert "hats" in stems

        # Each stem should be audio
        for stem in stems.values():
            assert isinstance(stem, AudioSegment)
            assert len(stem) > 1000  # Should have content

        # Combine stems
        max_length = max(len(stem) for stem in stems.values())
        combined = AudioSegment.silent(duration=max_length)
        for stem in stems.values():
            combined = combined.overlay(stem)

        assert isinstance(combined, AudioSegment)
        assert len(combined) > 2000

    def test_mixer_with_processing_pipeline(self):
        """Test mixer creating track with processing"""
        mixer = MinimalTechnoMixer(124)

        # Mock the composition parts to avoid complexity
        with mock.patch.object(mixer, "composer") as mock_composer:
            mock_track = create_sine_wave(440, 5000)  # 5 second test track
            mock_composer.compose.return_value = mock_track

            # Create track (this will apply minimal processing)
            result = mixer.create_track()

            assert isinstance(result, AudioSegment)
            # Should be processed (different from original)
            assert len(result) == len(mock_track)

    def test_frequency_analysis_pipeline(self):
        """Test frequency analysis on generated audio"""
        from ..core.frequency import analyze_frequency_content

        # Create test audio with known frequency content
        # Mix of low, mid, and high frequencies
        low_freq = create_sine_wave(60, 2000)  # Sub-bass
        low_freq = low_freq + (-10)  # Apply volume
        mid_freq = create_sine_wave(1000, 2000)  # Mids
        mid_freq = mid_freq + (-5)  # Apply volume
        high_freq = create_sine_wave(8000, 2000)  # Highs
        high_freq = high_freq + (-15)  # Apply volume

        test_audio = low_freq.overlay(mid_freq).overlay(high_freq)

        results = analyze_frequency_content(test_audio)

        assert isinstance(results, dict)
        assert "sub" in results
        assert "bass" in results

        # Should have some content in each band
        assert sum(results.values()) > 95  # Should account for most energy

    def test_filter_processing_chain(self):
        """Test applying multiple filters in sequence"""
        # Create test audio
        test_audio = create_sine_wave(1000, 3000)  # 1kHz tone

        # Apply high-pass
        filtered = TechnoFilters.high_pass(test_audio, cutoff_hz=500)
        assert isinstance(filtered, AudioSegment)

        # Apply low-pass
        filtered = TechnoFilters.low_pass(filtered, cutoff_hz=2000)
        assert isinstance(filtered, AudioSegment)

        # Apply compression
        compressed = DynamicsProcessor.compress(filtered, threshold_db=-20, ratio=3.0)
        assert isinstance(compressed, AudioSegment)

        # Final result should still be valid audio
        assert len(compressed) == len(test_audio)

    def test_cross_module_integration(self):
        """Test interaction between different modules"""
        # Generate stems
        synth = SynthGenerator(120)
        stems = synth.generate_all_stems(duration_bars=1, style="minimal")

        # Apply processing to each stem
        processed_stems = {}
        for name, stem in stems.items():
            if name == "kick":
                # Apply compression to kick
                processed = DynamicsProcessor.compress(
                    stem, threshold_db=-15, ratio=4.0
                )
            elif name == "bass":
                # Apply low-pass to bass
                processed = TechnoFilters.low_pass(stem, cutoff_hz=3000)
            else:
                processed = stem
            processed_stems[name] = processed

        # Mix together
        max_length = max(len(stem) for stem in processed_stems.values())
        final_mix = AudioSegment.silent(duration=max_length)
        for stem in processed_stems.values():
            final_mix = final_mix.overlay(stem)

        assert isinstance(final_mix, AudioSegment)
        assert len(final_mix) > 1000
