"""
Pure synthesis option
"""

from typing import Dict

from pydub import AudioSegment

from ..core.primitives import Bass, HiHat, Kick
from ..core.timing import TimingCalculator


class SynthGenerator:
    """Generate stems using pure synthesis"""

    def __init__(self, bpm: int):
        self.bpm = bpm
        self.timing = TimingCalculator(bpm)

        # Initialize primitives
        self.kick_gen = Kick(bpm)
        self.bass_gen = Bass(bpm)
        self.hat_gen = HiHat(bpm)

    def generate_stem(
        self, element: str, duration_bars: int = 8, style: str = "minimal"
    ) -> AudioSegment:
        """
        Generate single stem

        Args:
            element: 'kick', 'bass', 'hats'
            duration_bars: Length in bars
            style: 'minimal', 'industrial'
        """
        duration_ms = self.timing.bars_to_ms(duration_bars)

        if element == "kick":
            if style == "minimal":
                kick = self.kick_gen.generate_minimal()
            elif style == "industrial":
                kick = self.kick_gen.generate_industrial()
            else:
                kick = self.kick_gen.generate()

            # Repeat kick pattern
            stem = AudioSegment.silent(duration=0)
            while len(stem) < duration_ms:
                stem += kick
                stem += AudioSegment.silent(
                    duration=int(self.timing.ms_per_beat - len(kick))
                )

            return stem[:duration_ms]

        elif element == "bass":
            # Generate bassline pattern
            notes = [40, 42, 45, 47]  # E, F#, A, B
            stem = AudioSegment.silent(duration=0)

            notes_per_bar = 8  # 8th notes
            total_notes = duration_bars * notes_per_bar

            for i in range(total_notes):
                note_idx = i % len(notes)
                note_midi = notes[note_idx]
                freq = 440 * (2 ** ((note_midi - 69) / 12))

                bass_note = self.bass_gen.generate_note(
                    frequency=freq, duration_bars=0.125
                )
                stem += bass_note

            return stem[:duration_ms]

        elif element == "hats":
            # Generate hi-hat pattern
            stem = AudioSegment.silent(duration=0)

            hats_per_bar = 16  # 16th notes
            total_hats = duration_bars * hats_per_bar

            for i in range(total_hats):
                closedness = 0.9 if i % 2 == 0 else 0.7
                hat = self.hat_gen.generate(closedness=closedness)

                stem += hat
                # Add silence to reach 16th note duration
                gap = int(self.timing.ms_per_16th - len(hat))
                if gap > 0:
                    stem += AudioSegment.silent(duration=gap)

            return stem[:duration_ms]

        else:
            return AudioSegment.silent(duration=duration_ms)

    def generate_all_stems(
        self, duration_bars: int = 8, style: str = "minimal"
    ) -> Dict[str, AudioSegment]:
        """Generate all stems for a track"""
        return {
            "kick": self.generate_stem("kick", duration_bars, style),
            "bass": self.generate_stem("bass", duration_bars, style),
            "hats": self.generate_stem("hats", duration_bars, style),
        }
