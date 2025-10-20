"""
Base mixer class (abstract)
All subgenre mixers inherit from this
"""

from abc import ABC, abstractmethod

from pydub import AudioSegment

from ..composition.structure import TrackComposer


class BaseMixer(ABC):
    """Abstract base class for all mixers"""

    def __init__(self, bpm: int):
        self.bpm = bpm
        self.composer = TrackComposer(bpm)

    @abstractmethod
    def create_track(self) -> AudioSegment:
        """Generate complete track - must be implemented by subclass"""
        pass

    @abstractmethod
    def _apply_processing(self, track: AudioSegment) -> AudioSegment:
        """Apply subgenre-specific processing"""
        pass
