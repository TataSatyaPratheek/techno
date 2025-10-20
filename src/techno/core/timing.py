"""
Musical timing calculations
Everything in bars/beats, not milliseconds
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class MusicalTime:
    """Represents a point in musical time"""

    bars: int
    beats: int
    sixteenths: int

    def __post_init__(self) -> None:
        """Validate inputs"""
        if self.bars < 0:
            raise ValueError("Bars cannot be negative")
        if self.beats < 0 or self.beats >= 4:
            raise ValueError("Beats must be between 0 and 3")
        if self.sixteenths < 0 or self.sixteenths > 4:
            raise ValueError("Sixteenths must be between 0 and 4")

    def to_beats(self) -> float:
        """Convert to total beats"""
        return self.bars * 4 + self.beats + self.sixteenths / 4

    def to_ms(self, bpm: int) -> int:
        """Convert to milliseconds"""
        total_beats = self.to_beats()
        ms_per_beat = (60 / bpm) * 1000
        return int(total_beats * ms_per_beat)


class TimingCalculator:
    """Calculate musical timings from BPM"""

    def __init__(self, bpm: int, time_signature: Tuple[int, int] = (4, 4)):
        if bpm <= 0:
            raise ValueError("BPM must be positive")
        self.bpm = bpm
        self.beats_per_bar = time_signature[0]
        self.note_value = time_signature[1]

        # Pre-calculate common values
        self.ms_per_beat = (60 / bpm) * 1000
        self.ms_per_bar = self.ms_per_beat * self.beats_per_bar
        self.ms_per_16th = self.ms_per_beat / 4

    def bars_to_ms(self, bars: int) -> int:
        """Convert bars to milliseconds"""
        return int(bars * self.ms_per_bar)

    def ms_to_bars(self, ms: int) -> float:
        """Convert milliseconds to bars"""
        return ms / self.ms_per_bar

    def nearest_bar(self, ms: int) -> int:
        """Snap milliseconds to nearest bar"""
        bars = round(ms / self.ms_per_bar)
        return int(bars * self.ms_per_bar)

    def nearest_beat(self, ms: int) -> int:
        """Snap to nearest beat"""
        beats = round(ms / self.ms_per_beat)
        return int(beats * self.ms_per_beat)

    def create_grid(self, total_bars: int, subdivision: int = 16) -> list:
        """
        Create timing grid for quantization

        Args:
            total_bars: Number of bars
            subdivision: 16 = 16th notes, 8 = 8th notes

        Returns:
            List of millisecond positions
        """
        ms_per_division = self.ms_per_bar / subdivision
        total_divisions = total_bars * subdivision

        return [int(i * ms_per_division) for i in range(total_divisions)]
