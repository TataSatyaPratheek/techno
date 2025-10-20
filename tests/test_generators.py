"""
Test stem generators
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
from pydub import AudioSegment

from ..generators.musicgpt_generator import MusicGPTGenerator
from ..generators.synth_generator import SynthGenerator


class TestMusicGPTGenerator:
    """Test MusicGPT generator"""

    def test_init(self):
        """Test initialization"""
        gen = MusicGPTGenerator()
        assert gen.model == "small"

        gen = MusicGPTGenerator("large")
        assert gen.model == "large"

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_generate_stem_success(self, mock_exists, mock_run):
        """Test successful stem generation"""
        mock_exists.return_value = True
        mock_run.return_value = MagicMock(returncode=0)

        with patch("pydub.AudioSegment.from_wav") as mock_from_wav:
            mock_audio = MagicMock(spec=AudioSegment)
            mock_from_wav.return_value = mock_audio

            gen = MusicGPTGenerator()
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test.wav"
                result = gen.generate_stem("test prompt", 10, output_path)

                assert result == mock_audio
                mock_run.assert_called_once()
                args = mock_run.call_args[0][0]
                assert "musicgpt" in args
                assert "test prompt" in args
                assert "--secs" in args
                assert "10" in args

    @patch("subprocess.run")
    def test_generate_stem_failure(self, mock_run):
        """Test stem generation failure"""
        mock_run.return_value = MagicMock(returncode=1, stderr="error")

        gen = MusicGPTGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.wav"
            result = gen.generate_stem("test prompt", 10, output_path)

            assert result is None

    @patch("subprocess.run")
    def test_generate_stem_file_not_found(self, mock_run):
        """Test when MusicGPT is not installed"""
        mock_run.side_effect = FileNotFoundError

        gen = MusicGPTGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.wav"
            result = gen.generate_stem("test prompt", 10, output_path)

            assert result is None

    @patch("subprocess.run")
    def test_generate_stem_timeout(self, mock_run):
        """Test timeout handling"""
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 180)

        gen = MusicGPTGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.wav"
            result = gen.generate_stem("test prompt", 10, output_path)

            assert result is None

    def test_generate_all_stems(self):
        """Test generating all stems"""
        gen = MusicGPTGenerator()

        prompts = {"kick": "kick drum pattern", "bass": "bassline", "hats": "hi hats"}

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "stems"
            # Since generate_stem returns None (no MusicGPT), should return empty dict
            result = gen.generate_all_stems(prompts, 8, output_dir)

            assert isinstance(result, dict)
            assert len(result) == 0  # No stems generated without MusicGPT


class TestSynthGenerator:
    """Test synthesis generator"""

    def test_init(self):
        """Test initialization"""
        gen = SynthGenerator(128)
        assert gen.bpm == 128
        assert hasattr(gen, "timing")
        assert hasattr(gen, "kick_gen")
        assert hasattr(gen, "bass_gen")
        assert hasattr(gen, "hat_gen")

    def test_generate_stem_kick_minimal(self):
        """Test kick stem generation - minimal style"""
        gen = SynthGenerator(128)
        stem = gen.generate_stem("kick", 1, "minimal")

        assert isinstance(stem, AudioSegment)
        # Should be approximately 1 bar at 128 BPM = 1875ms
        expected_duration = 1875  # roughly
        assert abs(len(stem) - expected_duration) < 100  # tolerance

    def test_generate_stem_kick_industrial(self):
        """Test kick stem generation - industrial style"""
        gen = SynthGenerator(138)
        stem = gen.generate_stem("kick", 2, "industrial")

        assert isinstance(stem, AudioSegment)
        # Should be approximately 2 bars
        expected_duration = 2 * 60 / 138 * 1000 * 4  # 2 bars in ms
        assert abs(len(stem) - expected_duration) < 200

    def test_generate_stem_bass(self):
        """Test bass stem generation"""
        gen = SynthGenerator(124)
        stem = gen.generate_stem("bass", 1, "minimal")

        assert isinstance(stem, AudioSegment)
        # Should contain multiple notes
        assert len(stem) > 1000

    def test_generate_stem_hats(self):
        """Test hi-hat stem generation"""
        gen = SynthGenerator(130)
        stem = gen.generate_stem("hats", 1, "minimal")

        assert isinstance(stem, AudioSegment)
        # Should have many quick hi-hats
        assert len(stem) > 1000

    def test_generate_stem_unknown_element(self):
        """Test unknown element returns silence"""
        gen = SynthGenerator(120)
        stem = gen.generate_stem("unknown", 1, "minimal")

        assert isinstance(stem, AudioSegment)
        # Should be silence of correct duration
        expected_duration = 60 / 120 * 1000 * 4  # 1 bar in ms
        assert abs(len(stem) - expected_duration) < 100

    def test_generate_all_stems(self):
        """Test generating all stems"""
        gen = SynthGenerator(128)
        stems = gen.generate_all_stems(2, "minimal")

        assert isinstance(stems, dict)
        assert "kick" in stems
        assert "bass" in stems
        assert "hats" in stems

        for stem in stems.values():
            assert isinstance(stem, AudioSegment)
            # Should be approximately 2 bars
            expected_duration = 2 * 60 / 128 * 1000 * 4
            assert abs(len(stem) - expected_duration) < 500

    def test_generate_stem_different_styles(self):
        """Test different styles produce different results"""
        gen = SynthGenerator(128)

        minimal_kick = gen.generate_stem("kick", 1, "minimal")
        industrial_kick = gen.generate_stem("kick", 1, "industrial")

        # Should be different (rough check)
        assert not np.allclose(
            np.array(minimal_kick.get_array_of_samples()),
            np.array(industrial_kick.get_array_of_samples()),
            rtol=0.1,
        )
