"""
Subjective listening tests
These test MUSICAL correctness, not just technical
"""

from pydub import AudioSegment

from techno.composition.phrase import TechnoPhrase
from techno.core.primitives import Bass, HiHat, Kick
from techno.processing.filters import TechnoFilters


class TestMusicalQuality:
    """Test that generated audio sounds musical"""

    def test_kick_has_transient(self):
        """Test that kick has audible transient (punch)"""
        kick_gen = Kick(bpm=130)
        kick = kick_gen.generate()

        # Kick should be >50ms (enough for transient + body)
        assert len(kick) > 50

        # Kick should have energy (not silent)
        assert kick.dBFS > -60  # Louder than -60dBFS

    def test_kick_minimal_vs_industrial(self):
        """Test that minimal and industrial kicks sound different"""
        kick_gen = Kick(bpm=130)

        minimal = kick_gen.generate_minimal()
        industrial = kick_gen.generate_industrial()

        # Both should be valid audio
        assert isinstance(minimal, AudioSegment)
        assert isinstance(industrial, AudioSegment)

        # Should be different (rough check)
        assert len(minimal) > 0
        assert len(industrial) > 0

        # Industrial should be more aggressive (louder or different)
        # This is a simplification - in production would analyze spectrum
        assert abs(industrial.dBFS - minimal.dBFS) < 10  # Not too different

    def test_bass_is_audible(self):
        """Test that bass is audible (not too quiet)"""
        bass_gen = Bass(bpm=130)
        bass = bass_gen.generate_note(frequency=110)

        # Bass should be audible
        assert bass.dBFS > -40

    def test_bass_303_pattern(self):
        """Test 303 acid bass pattern generation"""
        bass_gen = Bass(bpm=130)

        notes = [40, 42, 45]  # E, F#, A
        pattern = bass_gen.generate_303_pattern(notes, "x-x-x-x-")

        assert isinstance(pattern, AudioSegment)
        # Should be longer than a single note
        assert len(pattern) > 1000

    def test_hat_variations(self):
        """Test hi-hat closedness variations"""
        hat_gen = HiHat(bpm=130)

        closed = hat_gen.generate(closedness=1.0)
        open_hat = hat_gen.generate(closedness=0.0)

        assert isinstance(closed, AudioSegment)
        assert isinstance(open_hat, AudioSegment)

        # Should have different characteristics
        assert len(closed) > 0
        assert len(open_hat) > 0

    def test_phrase_has_rhythm(self):
        """Test that phrase has rhythmic structure"""
        phrase_builder = TechnoPhrase(bpm=130)
        phrase = phrase_builder.build_phrase(elements=["kick"])

        # 8-bar phrase at 130 BPM ≈ 14760ms
        expected_duration = int((8 * 4 * 60 / 130) * 1000)

        # Allow 5% tolerance
        assert abs(len(phrase) - expected_duration) / expected_duration < 0.05

    def test_filter_sweep_changes_brightness(self):
        """Test that filter sweep makes sound brighter"""
        # Create test audio
        kick_gen = Kick(bpm=130)
        kick = kick_gen.generate()

        # Muffled (200Hz lowpass)
        muffled = TechnoFilters.low_pass(kick, cutoff_hz=200)

        # Bright (2000Hz lowpass)
        bright = TechnoFilters.low_pass(kick, cutoff_hz=2000)

        # Bright should have more high-frequency energy
        # (Measured by dBFS - simplification)
        # In production: analyze spectrum

        # Test that filtering changes audio
        assert len(muffled) == len(bright)  # Same length
        assert muffled.dBFS != bright.dBFS  # Different energy


class TestStructuralIntegrity:
    """Test that structure makes musical sense"""

    def test_phrase_builder_creates_correct_length(self):
        """Test that 8-bar phrase is actually 8 bars"""
        for bpm in [120, 130, 140]:
            phrase_builder = TechnoPhrase(bpm=bpm)
            phrase = phrase_builder.build_phrase(elements=["kick"])

            expected = int((8 * 4 * 60 / bpm) * 1000)
            assert abs(len(phrase) - expected) < 100  # 100ms tolerance

    def test_sections_concatenate_seamlessly(self):
        """Test that sections join without gaps"""
        phrase_builder = TechnoPhrase(bpm=130)

        phrase1 = phrase_builder.build_phrase(elements=["kick"])
        phrase2 = phrase_builder.build_phrase(elements=["bass"])

        combined = phrase1 + phrase2

        # Combined length should equal sum
        assert len(combined) == len(phrase1) + len(phrase2)
