"""
Minimal techno
"""

from pydub import AudioSegment

from ..composition.structure import StructureTemplates, TrackComposer
from ..processing.filters import TechnoFilters


class MinimalTechnoMixer:
    """Minimal techno production"""

    def __init__(self, bpm: int = 124):
        self.bpm = bpm
        self.composer = TrackComposer(bpm)

    def create_track(self) -> AudioSegment:
        """
        Create complete minimal techno track

        Characteristics:
        - Clean, tight kick
        - Sparse percussion
        - Subtle bass
        - Glacial filter automation
        - Dynamic range preserved (no crushing)
        """
        print("🎵 Creating minimal techno track...")

        # Use minimal structure template
        structure = StructureTemplates.minimal_techno_30s()

        # Compose track
        track = self.composer.compose(structure)

        # Apply minimal-specific processing
        track = self._apply_minimal_processing(track)

        return track

    def _apply_minimal_processing(self, track: AudioSegment) -> AudioSegment:
        """
        Minimal-specific processing

        Key: Preserve dynamics, subtle effects only
        """
        # Very gentle compression (preserve dynamics)
        # In production: use compressor with low ratio

        # Subtle high-pass (remove rumble below 30Hz)
        track = TechnoFilters.high_pass(track, cutoff_hz=30)

        # NO heavy processing - minimal stays clean

        return track
