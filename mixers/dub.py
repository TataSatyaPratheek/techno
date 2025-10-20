"""
Dub techno
"""

from pydub import AudioSegment

from ..composition.structure import StructureTemplates, TrackComposer
from ..processing.filters import TechnoFilters
from ..processing.spatial import SpatialProcessor
from .base import BaseMixer


class DubTechnoMixer(BaseMixer):
    """Dub techno production"""

    def __init__(self, bpm: int = 118):
        super().__init__(bpm)

    def create_track(self) -> AudioSegment:
        """
        Create dub techno track

        Characteristics:
        - Deep, muffled kick
        - Chord progressions (not single bass notes)
        - Heavy reverb and delay
        - Underwater, floating feel
        """
        print("🎵 Creating dub techno track...")

        structure = StructureTemplates.dub_techno_30s()
        track = self.composer.compose(structure)

        # Apply dub processing
        track = self._apply_processing(track)

        return track

    def _apply_processing(self, track: AudioSegment) -> AudioSegment:
        """
        Dub-specific processing

        Key: Heavy reverb/delay, muffled sound
        """
        # Muffled sound (low-pass filter)
        track = TechnoFilters.low_pass(track, cutoff_hz=4000)

        # Tape delay (500ms, high feedback)
        track = SpatialProcessor.delay(
            track, delay_ms=500, feedback=0.7, mix=0.6  # Heavy wet mix
        )

        # Subtle high-pass (remove rumble)
        track = TechnoFilters.high_pass(track, cutoff_hz=30)

        return track
