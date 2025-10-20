"""
Test CLI commands
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from ..cli.main import analyze, cli, generate, list_presets


class TestCLI:
    """Test CLI commands"""

    def test_cli_group(self):
        """Test CLI group exists"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Techno Production System" in result.output

    @patch("techno.cli.main.MinimalTechnoMixer")
    def test_generate_minimal(self, mock_mixer_class):
        """Test generate command for minimal techno"""
        mock_mixer = MagicMock()
        mock_track = MagicMock()
        mock_mixer.create_track.return_value = mock_track
        mock_mixer_class.return_value = mock_mixer

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a mock preset file
            preset_dir = Path("presets")
            preset_dir.mkdir()
            preset_file = preset_dir / "minimal_techno.yaml"
            preset_file.write_text(
                """
name: Minimal Techno
description: Clean, hypnotic techno
bpm: 124
"""
            )

            result = runner.invoke(
                cli, ["generate", "--subgenre", "minimal", "--output", "test.wav"]
            )

            assert result.exit_code == 0
            assert "Generating minimal techno track" in result.output
            assert "Track saved to test.wav" in result.output
            mock_mixer.create_track.assert_called_once()

    @patch("techno.cli.main.IndustrialTechnoMixer")
    def test_generate_industrial(self, mock_mixer_class):
        """Test generate command for industrial techno"""
        mock_mixer = MagicMock()
        mock_track = MagicMock()
        mock_mixer.create_track.return_value = mock_track
        mock_mixer_class.return_value = mock_mixer

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create mock preset
            preset_dir = Path("presets")
            preset_dir.mkdir()
            preset_file = preset_dir / "industrial_techno.yaml"
            preset_file.write_text(
                """
name: Industrial Techno
description: Harsh, aggressive techno
bpm: 138
"""
            )

            result = runner.invoke(cli, ["generate", "--subgenre", "industrial"])

            assert result.exit_code == 0
            assert "Generating industrial techno track" in result.output
            mock_mixer.create_track.assert_called_once()

    def test_generate_invalid_subgenre(self):
        """Test generate with invalid subgenre"""
        runner = CliRunner()
        result = runner.invoke(cli, ["generate", "--subgenre", "invalid"])

        assert result.exit_code == 2  # Click exits with error for invalid choice
        assert "Invalid value for" in result.output

    def test_list_presets(self):
        """Test list presets command"""
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create mock presets
            preset_dir = Path("presets")
            preset_dir.mkdir()

            # Minimal preset
            minimal_file = preset_dir / "minimal_techno.yaml"
            minimal_file.write_text(
                """
name: Minimal Techno
description: Clean techno
bpm: 124
"""
            )

            # Industrial preset
            industrial_file = preset_dir / "industrial_techno.yaml"
            industrial_file.write_text(
                """
name: Industrial Techno
description: Aggressive techno
bpm: 138
"""
            )

            result = runner.invoke(cli, ["list-presets"])

            assert result.exit_code == 0
            assert "Available presets" in result.output
            assert "minimal_techno" in result.output
            assert "industrial_techno" in result.output

    @patch("pydub.AudioSegment.from_file")
    @patch("techno.core.frequency.analyze_frequency_content")
    def test_analyze_audio(self, mock_analyze, mock_from_file):
        """Test analyze command"""
        mock_audio = MagicMock()
        mock_from_file.return_value = mock_audio
        mock_analyze.return_value = {
            "sub-bass": 25.0,
            "bass": 30.0,
            "mids": 20.0,
            "highs": 15.0,
            "air": 10.0,
        }

        # Mock the audio to have some samples
        from array import array

        import numpy as np

        mock_audio.get_array_of_samples.return_value = array(
            "h", np.random.randint(-32768, 32767, 44100)
        )
        mock_audio.frame_rate = 44100

        mock_analyze.return_value = {
            "sub-bass": 25.0,
            "bass": 30.0,
            "mids": 20.0,
            "highs": 15.0,
            "air": 10.0,
        }

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a dummy audio file
            audio_file = Path("test.wav")
            audio_file.write_bytes(b"dummy audio data")

            result = runner.invoke(cli, ["analyze", "test.wav"])

            assert result.exit_code == 0
            assert "Analyzing test.wav" in result.output
            assert "Frequency distribution" in result.output
            assert "sub" in result.output
            assert "bass" in result.output
