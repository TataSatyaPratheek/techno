"""
Section arranger (intro/drop/etc)
"""

from typing import Dict, List

import numpy as np
from pydub import AudioSegment

from ..core.timing import TimingCalculator
from .phrase import TechnoPhrase


class SectionBuilder:
    """Build complete track sections with musical evolution"""

    def __init__(self, bpm: int):
        self.bpm = bpm
        self.timing = TimingCalculator(bpm)
        self.phrase_builder = TechnoPhrase(bpm)

    def create_intro(self, bars: int = 16, style: str = "minimal") -> AudioSegment:
        """
        Create intro section

        Minimal style: Kick only, establish groove
        Industrial style: Kick + noise from start
        """
        intro = AudioSegment.silent(duration=self.timing.bars_to_ms(bars))

        if style == "minimal":
            # Start with just kick for first half
            half_bars = bars // 2
            first_half = self.phrase_builder.build_phrase(
                elements=["kick"], volumes={"kick": -2.0}  # Quieter intro
            )
            # Repeat/truncate to match half duration
            target_ms = self.timing.bars_to_ms(half_bars)
            if len(first_half) > target_ms:
                first_half = first_half[:target_ms]
            else:
                while len(first_half) < target_ms:
                    first_half += self.phrase_builder.build_phrase(
                        elements=["kick"], volumes={"kick": -2.0}
                    )
                first_half = first_half[:target_ms]

            # Add subtle bass in second half
            second_half = self.phrase_builder.build_phrase(
                elements=["kick", "bass"], volumes={"kick": -1.0, "bass": -4.0}
            )
            if len(second_half) > target_ms:
                second_half = second_half[:target_ms]
            else:
                while len(second_half) < target_ms:
                    second_half += self.phrase_builder.build_phrase(
                        elements=["kick", "bass"], volumes={"kick": -1.0, "bass": -4.0}
                    )
                second_half = second_half[:target_ms]

            intro = first_half + second_half

        elif style == "industrial":
            # Aggressive from start
            intro = self.phrase_builder.build_phrase(
                elements=["kick"], volumes={"kick": 2.0}  # Loud immediately
            )
            # Repeat for full intro length
            while len(intro) < self.timing.bars_to_ms(bars):
                intro += self.phrase_builder.build_phrase(
                    elements=["kick"], volumes={"kick": 2.0}
                )
            intro = intro[: self.timing.bars_to_ms(bars)]

        return intro

    def create_buildup(self, bars: int = 16, filter_sweep: bool = True) -> AudioSegment:
        """
        Create buildup section with tension

        Key technique: Filter sweep on bass (opens over time)
        """
        buildup = AudioSegment.silent(duration=self.timing.bars_to_ms(bars))

        # Build in stages (every 4 bars)
        num_stages = bars // 4

        for stage in range(num_stages):
            stage_start = stage * 4

            # Gradually add elements
            if stage == 0:
                elements = ["kick", "bass"]
                volumes = {"kick": 0.0, "bass": -3.0}
            elif stage == 1:
                elements = ["kick", "bass"]
                volumes = {"kick": 0.0, "bass": -2.0}  # Bass louder
            elif stage == 2:
                elements = ["kick", "bass", "hats"]
                volumes = {"kick": 1.0, "bass": -1.0, "hats": -2.0}
            else:
                elements = ["kick", "bass", "hats"]
                volumes = {"kick": 1.5, "bass": 0.0, "hats": -1.0}

            # Build phrase for this stage
            phrase = AudioSegment.silent(duration=self.timing.bars_to_ms(4))
            for _ in range(4 // 8):  # 4 bars = 0.5 phrases (8-bar phrase)
                phrase += self.phrase_builder.build_phrase(elements, volumes)
            phrase = phrase[: self.timing.bars_to_ms(4)]

            # Add to buildup
            position = self.timing.bars_to_ms(stage_start)
            buildup = buildup.overlay(phrase, position=position)

        # Apply filter sweep if requested (simulated with volume automation)
        if filter_sweep:
            buildup = self._apply_buildup_automation(buildup)

        return buildup

    def create_drop(self, bars: int = 16, energy: float = 1.0) -> AudioSegment:
        """
        Create drop/climax section

        Full energy, all elements, maximum impact
        """
        # All elements at full volume
        volumes = {"kick": 2.0 * energy, "bass": 0.0 * energy, "hats": 1.0 * energy}

        drop = AudioSegment.silent(duration=0)

        # Build drop by repeating phrases
        phrases_needed = bars // 8
        for _ in range(phrases_needed):
            phrase = self.phrase_builder.build_phrase(
                elements=["kick", "bass", "hats"], volumes=volumes
            )
            drop += phrase

        # Ensure exact length
        drop = drop[: self.timing.bars_to_ms(bars)]

        return drop

    def create_breakdown(
        self, bars: int = 8, remove_elements: List[str] = None
    ) -> AudioSegment:
        """
        Create breakdown section

        Remove elements for contrast (usually hats)
        """
        remove_elements = remove_elements or ["hats"]

        # Keep only remaining elements
        all_elements = ["kick", "bass", "hats"]
        keep_elements = [e for e in all_elements if e not in remove_elements]

        # Lower volumes (space/breath)
        volumes = {
            "kick": -1.0,
            "bass": -2.0,
        }

        breakdown = AudioSegment.silent(duration=0)

        # Build phrases to fill the required duration
        target_ms = self.timing.bars_to_ms(bars)
        while len(breakdown) < target_ms:
            phrase = self.phrase_builder.build_phrase(
                elements=keep_elements, volumes=volumes
            )
            breakdown += phrase

        breakdown = breakdown[:target_ms]

        return breakdown

    def _apply_buildup_automation(self, audio: AudioSegment) -> AudioSegment:
        """
        Apply gradual volume increase to simulate filter opening

        In production, this would be actual filter automation
        For now, use volume fade-in
        """
        # Split into chunks
        chunk_size = len(audio) // 4
        processed = AudioSegment.silent(duration=0)

        for i in range(4):
            chunk = audio[i * chunk_size : (i + 1) * chunk_size]

            # Gradually increase volume
            boost = i * 1.5  # 0, 1.5, 3.0, 4.5 dB
            chunk = chunk + boost

            processed += chunk

        return processed
