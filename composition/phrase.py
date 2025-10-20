"""
Build 8-bar phrases (fundamental techno unit)
"""

from typing import Dict, List

from pydub import AudioSegment

from ..core.primitives import Bass, HiHat, Kick
from ..core.timing import TimingCalculator


class TechnoPhrase:
    """8-bar phrase builder"""

    def __init__(self, bpm: int):
        self.bpm = bpm
        self.timing = TimingCalculator(bpm)
        self.duration_ms = self.timing.bars_to_ms(8)

        # Initialize primitives
        self.kick_gen = Kick(bpm)
        self.bass_gen = Bass(bpm)
        self.hat_gen = HiHat(bpm)

    def create_kick_pattern(self, style: str = "four_on_floor") -> AudioSegment:
        """
        Generate kick pattern for 8 bars

        Styles:
        - 'four_on_floor': Standard techno (kick on every beat)
        - 'broken': Syncopated (skip some beats)
        - 'double': Double-time (kick on 8th notes)
        """
        phrase = AudioSegment.silent(duration=self.duration_ms)

        if style == "four_on_floor":
            # Kick on every quarter note (1, 2, 3, 4)
            kicks_per_bar = 4
            total_kicks = kicks_per_bar * 8  # 8 bars

            kick = self.kick_gen.generate_minimal()

            for i in range(total_kicks):
                position_ms = int(i * self.timing.ms_per_beat)
                phrase = phrase.overlay(kick, position=position_ms)

        return phrase

    def create_bass_pattern(
        self,
        notes: List[int] = [40, 42, 45, 47],  # E, F#, A, B (minor pentatonic)
        rhythm: str = "eighth_notes",
    ) -> AudioSegment:
        """
        Generate bassline for 8 bars
        """
        phrase = AudioSegment.silent(duration=self.duration_ms)

        if rhythm == "eighth_notes":
            # Bass on every 8th note
            notes_per_bar = 8
            total_notes = notes_per_bar * 8

            for i in range(total_notes):
                note_idx = i % len(notes)
                note_midi = notes[note_idx]
                freq = 440 * (2 ** ((note_midi - 69) / 12))

                bass_note = self.bass_gen.generate_note(
                    frequency=freq, duration_bars=0.125, waveform="saw"  # 8th note
                )

                position_ms = int(i * self.timing.ms_per_beat / 2)
                phrase = phrase.overlay(bass_note, position=position_ms)

        return phrase

    def create_hat_pattern(self, density: str = "16th_notes") -> AudioSegment:
        """
        Generate hi-hat pattern for 8 bars
        """
        phrase = AudioSegment.silent(duration=self.duration_ms)

        if density == "16th_notes":
            # Hi-hat on every 16th note
            hats_per_bar = 16
            total_hats = hats_per_bar * 8

            for i in range(total_hats):
                # Alternate closed/open slightly
                closedness = 0.9 if i % 2 == 0 else 0.7

                hat = self.hat_gen.generate(closedness=closedness)

                position_ms = int(i * self.timing.ms_per_16th)
                phrase = phrase.overlay(hat, position=position_ms)

        return phrase

    def build_phrase(
        self, elements: List[str], volumes: Dict[str, float] = None
    ) -> AudioSegment:
        """
        Build complete 8-bar phrase from elements

        Args:
            elements: ['kick', 'bass', 'hats']
            volumes: {'kick': 0.0, 'bass': -2.0, 'hats': -1.0} (dB)
        """
        phrase = AudioSegment.silent(duration=self.duration_ms)
        volumes = volumes or {}

        for element in elements:
            if element == "kick":
                layer = self.create_kick_pattern()
            elif element == "bass":
                layer = self.create_bass_pattern()
            elif element == "hats":
                layer = self.create_hat_pattern()
            else:
                continue

            # Apply volume
            if element in volumes:
                layer = layer + volumes[element]

            phrase = phrase.overlay(layer)

        return phrase
