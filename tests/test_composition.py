"""
Test composition modules
"""

import pytest
from pydub import AudioSegment

from ..composition.phrase import TechnoPhrase
from ..composition.section import SectionBuilder
from ..composition.structure import StructureTemplates, TrackComposer, TrackStructure


class TestTechnoPhrase:
    """Test phrase building"""

    def test_init(self):
        """Test initialization"""
        phrase = TechnoPhrase(128)
        assert phrase.bpm == 128
        assert phrase.duration_ms == 8 * 60 / 128 * 1000 * 4  # 8 bars in ms

    def test_create_kick_pattern_four_on_floor(self):
        """Test standard kick pattern"""
        phrase = TechnoPhrase(120)
        pattern = phrase.create_kick_pattern("four_on_floor")

        assert isinstance(pattern, AudioSegment)
        expected_duration = 8 * 60 / 120 * 1000 * 4  # 8 bars
        assert abs(len(pattern) - expected_duration) < 100

    def test_create_bass_pattern(self):
        """Test bass pattern generation"""
        phrase = TechnoPhrase(128)
        pattern = phrase.create_bass_pattern()

        assert isinstance(pattern, AudioSegment)
        expected_duration = 8 * 60 / 128 * 1000 * 4
        assert abs(len(pattern) - expected_duration) < 100

    def test_create_hat_pattern(self):
        """Test hi-hat pattern"""
        phrase = TechnoPhrase(130)
        pattern = phrase.create_hat_pattern()

        assert isinstance(pattern, AudioSegment)
        expected_duration = 8 * 60 / 130 * 1000 * 4
        assert abs(len(pattern) - expected_duration) < 100

    def test_build_phrase_kick_only(self):
        """Test building phrase with kick only"""
        phrase = TechnoPhrase(124)
        result = phrase.build_phrase(["kick"])

        assert isinstance(result, AudioSegment)
        expected_duration = 8 * 60 / 124 * 1000 * 4
        assert abs(len(result) - expected_duration) < 100

    def test_build_phrase_all_elements(self):
        """Test building phrase with all elements"""
        phrase = TechnoPhrase(128)
        result = phrase.build_phrase(["kick", "bass", "hats"])

        assert isinstance(result, AudioSegment)
        expected_duration = 8 * 60 / 128 * 1000 * 4
        assert abs(len(result) - expected_duration) < 100

    def test_build_phrase_with_volumes(self):
        """Test building phrase with custom volumes"""
        phrase = TechnoPhrase(120)
        volumes = {"kick": -2.0, "bass": -1.0, "hats": -3.0}
        result = phrase.build_phrase(["kick", "bass", "hats"], volumes)

        assert isinstance(result, AudioSegment)
        # Should be same duration regardless of volume
        expected_duration = 8 * 60 / 120 * 1000 * 4
        assert abs(len(result) - expected_duration) < 100


class TestSectionBuilder:
    """Test section building"""

    def test_init(self):
        """Test initialization"""
        builder = SectionBuilder(128)
        assert builder.bpm == 128

    def test_create_intro_minimal(self):
        """Test minimal intro creation"""
        builder = SectionBuilder(124)
        intro = builder.create_intro(8, "minimal")

        assert isinstance(intro, AudioSegment)
        expected_duration = 8 * 60 / 124 * 1000 * 4  # 8 bars
        assert abs(len(intro) - expected_duration) < 200

    def test_create_intro_industrial(self):
        """Test industrial intro creation"""
        builder = SectionBuilder(138)
        intro = builder.create_intro(4, "industrial")

        assert isinstance(intro, AudioSegment)
        expected_duration = 4 * 60 / 138 * 1000 * 4  # 4 bars
        assert abs(len(intro) - expected_duration) < 200

    def test_create_buildup(self):
        """Test buildup creation"""
        builder = SectionBuilder(128)
        buildup = builder.create_buildup(16, filter_sweep=True)

        assert isinstance(buildup, AudioSegment)
        expected_duration = 16 * 60 / 128 * 1000 * 4  # 16 bars
        assert abs(len(buildup) - expected_duration) < 500

    def test_create_drop(self):
        """Test drop creation"""
        builder = SectionBuilder(130)
        drop = builder.create_drop(8, energy=0.8)

        assert isinstance(drop, AudioSegment)
        expected_duration = 8 * 60 / 130 * 1000 * 4  # 8 bars
        assert abs(len(drop) - expected_duration) < 200

    def test_create_breakdown(self):
        """Test breakdown creation"""
        builder = SectionBuilder(120)
        breakdown = builder.create_breakdown(4, remove_elements=["hats"])

        assert isinstance(breakdown, AudioSegment)
        expected_duration = 4 * 60 / 120 * 1000 * 4  # 4 bars
        assert abs(len(breakdown) - expected_duration) < 200


class TestStructureTemplates:
    """Test structure templates"""

    def test_minimal_techno_30s(self):
        """Test minimal techno template"""
        structure = StructureTemplates.minimal_techno_30s()

        assert isinstance(structure, TrackStructure)
        assert structure.name == "minimal_30s"
        assert structure.total_bars == 64
        assert len(structure.sections) == 4

        # Check sections
        section_names = [s["name"] for s in structure.sections]
        assert "intro" in section_names
        assert "develop" in section_names
        assert "climax" in section_names
        assert "outro" in section_names

    def test_industrial_techno_30s(self):
        """Test industrial techno template"""
        structure = StructureTemplates.industrial_techno_30s()

        assert isinstance(structure, TrackStructure)
        assert structure.name == "industrial_30s"
        assert structure.total_bars == 64
        assert len(structure.sections) == 5

        section_names = [s["name"] for s in structure.sections]
        assert "intro" in section_names
        assert "buildup" in section_names
        assert "drop" in section_names
        assert "breakdown" in section_names
        assert "outro" in section_names

    def test_dub_techno_30s(self):
        """Test dub techno template"""
        structure = StructureTemplates.dub_techno_30s()

        assert isinstance(structure, TrackStructure)
        assert structure.name == "dub_30s"
        assert structure.total_bars == 96
        assert len(structure.sections) == 3

        section_names = [s["name"] for s in structure.sections]
        assert "intro" in section_names
        assert "main" in section_names
        assert "outro" in section_names


class TestTrackComposer:
    """Test track composition"""

    def test_init(self):
        """Test initialization"""
        composer = TrackComposer(128)
        assert composer.bpm == 128

    def test_compose_minimal_structure(self):
        """Test composing minimal structure"""
        composer = TrackComposer(124)

        structure = StructureTemplates.minimal_techno_30s()
        track = composer.compose(structure)

        assert isinstance(track, AudioSegment)
        # Should be approximately 64 bars at 124 BPM
        expected_duration = 64 * 60 / 124 * 1000 * 4
        assert (
            abs(len(track) - expected_duration) < 2000
        )  # Larger tolerance for complex composition
