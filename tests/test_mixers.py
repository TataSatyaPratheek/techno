"""
Test mixers
"""

from unittest.mock import MagicMock, patch

import pytest
from pydub import AudioSegment

from ..mixers.base import BaseMixer
from ..mixers.dub import DubTechnoMixer
from ..mixers.industrial import IndustrialTechnoMixer
from ..mixers.minimal import MinimalTechnoMixer


class TestBaseMixer:
    """Test base mixer (abstract)"""

    def test_init(self):
        """Test base mixer initialization"""
        # Can't instantiate abstract class directly
        with pytest.raises(TypeError):
            BaseMixer(120)

    def test_abstract_methods(self):
        """Test that abstract methods are defined"""
        # Check that the abstract methods exist
        assert hasattr(BaseMixer, "create_track")
        assert hasattr(BaseMixer, "_apply_processing")


class TestMinimalTechnoMixer:
    """Test minimal techno mixer"""

    def test_init(self):
        """Test initialization"""
        mixer = MinimalTechnoMixer()
        assert mixer.bpm == 124

        mixer = MinimalTechnoMixer(130)
        assert mixer.bpm == 130

    @patch("techno.mixers.minimal.TrackComposer")
    @patch("techno.composition.structure.StructureTemplates.minimal_techno_30s")
    def test_create_track(self, mock_template, mock_composer):
        """Test track creation"""
        # Mock the structure
        mock_structure = MagicMock()
        mock_template.return_value = mock_structure

        # Mock the composer
        mock_composer_instance = MagicMock()
        mock_composer.return_value = mock_composer_instance
        mock_track = MagicMock(spec=AudioSegment)
        mock_composer_instance.compose.return_value = mock_track

        # Mock processing
        with patch.object(MinimalTechnoMixer, "_apply_minimal_processing", return_value=mock_track) as mock_process:
            mixer = MinimalTechnoMixer()
            result = mixer.create_track()

            assert result == mock_track
            mock_template.assert_called_once()
            mock_composer_instance.compose.assert_called_once_with(mock_structure)
            mock_process.assert_called_once_with(mock_track)

    def test_apply_minimal_processing(self):
        """Test minimal processing"""
        mixer = MinimalTechnoMixer()

        # Create a test audio segment
        test_audio = AudioSegment.silent(duration=1000)

        # Mock the filter functions
        with patch("techno.processing.filters.TechnoFilters.high_pass") as mock_hp:
            mock_hp.return_value = test_audio

            result = mixer._apply_minimal_processing(test_audio)

            # Should apply high-pass filter
            mock_hp.assert_called_once_with(test_audio, cutoff_hz=30)
            assert result == test_audio


class TestIndustrialTechnoMixer:
    """Test industrial techno mixer"""

    def test_init(self):
        """Test initialization"""
        mixer = IndustrialTechnoMixer()
        assert mixer.bpm == 138

        mixer = IndustrialTechnoMixer(140)
        assert mixer.bpm == 140

    @patch("techno.mixers.industrial.TrackComposer")
    @patch("techno.composition.structure.StructureTemplates.industrial_techno_30s")
    def test_create_track(self, mock_template, mock_composer):
        """Test track creation"""
        mock_structure = MagicMock()
        mock_template.return_value = mock_structure

        mock_composer_instance = MagicMock()
        mock_composer.return_value = mock_composer_instance
        mock_track = MagicMock(spec=AudioSegment)
        mock_composer_instance.compose.return_value = mock_track

        with patch.object(
            IndustrialTechnoMixer,
            "_apply_industrial_processing",
            return_value=mock_track,
        ) as mock_process:
            mixer = IndustrialTechnoMixer()
            result = mixer.create_track()

            assert result == mock_track
            mock_template.assert_called_once()
            mock_composer_instance.compose.assert_called_once_with(mock_structure)
            mock_process.assert_called_once_with(mock_track)

    def test_apply_industrial_processing(self):
        """Test industrial processing"""
        mixer = IndustrialTechnoMixer()
        test_audio = AudioSegment.silent(duration=1000)

        with (
            patch("techno.processing.distortion.Distortion.waveshaper") as mock_waveshaper,
            patch("techno.processing.distortion.Distortion.bit_crush") as mock_bitcrush,
            patch("pydub.effects.normalize") as mock_normalize,
        ):

            mock_waveshaper.return_value = test_audio
            mock_bitcrush.return_value = test_audio
            mock_normalize.return_value = test_audio

            mixer._apply_industrial_processing(test_audio)

            # Should apply all processing steps
            mock_waveshaper.assert_called_once_with(test_audio, drive=0.7, curve="hard")
            mock_bitcrush.assert_called_once_with(test_audio, bit_depth=14)
            mock_normalize.assert_called_once_with(test_audio, headroom=0.5)


class TestDubTechnoMixer:
    """Test dub techno mixer"""

    def test_init(self):
        """Test initialization"""
        mixer = DubTechnoMixer()
        assert mixer.bpm == 118

        mixer = DubTechnoMixer(120)
        assert mixer.bpm == 120

    @patch("techno.mixers.base.TrackComposer")
    @patch("techno.composition.structure.StructureTemplates.dub_techno_30s")
    def test_create_track(self, mock_template, mock_composer):
        """Test track creation"""
        mock_structure = MagicMock()
        mock_template.return_value = mock_structure

        mock_composer_instance = MagicMock()
        mock_composer.return_value = mock_composer_instance
        mock_track = MagicMock(spec=AudioSegment)
        mock_composer_instance.compose.return_value = mock_track

        with patch.object(DubTechnoMixer, "_apply_processing", return_value=mock_track) as mock_process:
            mixer = DubTechnoMixer()
            result = mixer.create_track()

            assert result == mock_track
            mock_template.assert_called_once()
            mock_composer_instance.compose.assert_called_once_with(mock_structure)
            mock_process.assert_called_once_with(mock_track)

    def test_apply_processing(self):
        """Test dub processing"""
        mixer = DubTechnoMixer()
        test_audio = AudioSegment.silent(duration=1000)

        with (
            patch("techno.processing.filters.TechnoFilters.low_pass") as mock_lp,
            patch("techno.processing.spatial.SpatialProcessor.delay") as mock_delay,
            patch("techno.processing.filters.TechnoFilters.high_pass") as mock_hp,
        ):

            mock_lp.return_value = test_audio
            mock_delay.return_value = test_audio
            mock_hp.return_value = test_audio

            mixer._apply_processing(test_audio)

            # Should apply all processing steps
            mock_lp.assert_called_once_with(test_audio, cutoff_hz=4000)
            mock_delay.assert_called_once_with(test_audio, delay_ms=500, feedback=0.7, mix=0.6)
            mock_hp.assert_called_once_with(test_audio, cutoff_hz=30)
