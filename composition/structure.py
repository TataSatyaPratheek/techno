"""
Assemble complete tracks from sections
Implements subgenre-specific structures
"""

from dataclasses import dataclass
from typing import Dict, List

from pydub import AudioSegment
from pydub.effects import normalize

from ..core.timing import TimingCalculator
from .section import SectionBuilder


@dataclass
class TrackStructure:
    """Define track structure"""

    name: str
    sections: List[Dict]  # [{'name': 'intro', 'bars': 16}, ...]
    total_bars: int


class StructureTemplates:
    """Pre-defined track structures for subgenres"""

    @staticmethod
    def minimal_techno_30s() -> TrackStructure:
        """Minimal techno structure for 30-second Reel (124 BPM)"""
        return TrackStructure(
            name="minimal_30s",
            sections=[
                {"name": "intro", "bars": 16, "style": "minimal"},
                {"name": "develop", "bars": 16, "filter_sweep": True},
                {"name": "climax", "bars": 16, "energy": 0.8},  # Restrained
                {"name": "outro", "bars": 16, "fade_out": True},
            ],
            total_bars=64,
        )

    @staticmethod
    def industrial_techno_30s() -> TrackStructure:
        """Industrial techno structure (138 BPM)"""
        return TrackStructure(
            name="industrial_30s",
            sections=[
                {"name": "intro", "bars": 8, "style": "industrial"},
                {"name": "buildup", "bars": 16, "intensity": "rising"},
                {"name": "drop", "bars": 24, "energy": 1.0},  # Long climax
                {"name": "breakdown", "bars": 8, "remove": ["hats"]},
                {"name": "outro", "bars": 8, "fade_out": True},
            ],
            total_bars=64,
        )

    @staticmethod
    def dub_techno_30s() -> TrackStructure:
        """Dub techno structure (118 BPM) - long, looping"""
        return TrackStructure(
            name="dub_30s",
            sections=[
                {"name": "intro", "bars": 16, "style": "minimal"},
                {"name": "main", "bars": 64, "loop": True},  # Very long main
                {"name": "outro", "bars": 16, "fade_out": True},
            ],
            total_bars=96,
        )


class TrackComposer:
    """Compose complete tracks from structure templates"""

    def __init__(self, bpm: int):
        self.bpm = bpm
        self.timing = TimingCalculator(bpm)
        self.section_builder = SectionBuilder(bpm)

    def compose(self, structure: TrackStructure) -> AudioSegment:
        """
        Compose complete track from structure definition

        This is where sections become a full track
        """
        print(f"🎼 Composing {structure.name}...")

        track = AudioSegment.silent(duration=0)

        for section_def in structure.sections:
            section_name = section_def["name"]
            bars = section_def["bars"]

            print(f"   Building {section_name} ({bars} bars)...")

            # Build section based on type
            if section_name == "intro":
                section = self.section_builder.create_intro(
                    bars=bars, style=section_def.get("style", "minimal")
                )

            elif section_name in ["buildup", "develop"]:
                section = self.section_builder.create_buildup(
                    bars=bars, filter_sweep=section_def.get("filter_sweep", True)
                )

            elif section_name in ["drop", "climax", "main"]:
                section = self.section_builder.create_drop(
                    bars=bars, energy=section_def.get("energy", 1.0)
                )

            elif section_name == "breakdown":
                section = self.section_builder.create_breakdown(
                    bars=bars, remove_elements=section_def.get("remove", ["hats"])
                )

            elif section_name == "outro":
                # Outro is like breakdown but with fade
                section = self.section_builder.create_breakdown(
                    bars=bars, remove_elements=["hats"]
                )

                if section_def.get("fade_out"):
                    section = section.fade_out(len(section) // 2)

            else:
                # Generic section
                section = self.section_builder.create_drop(bars=bars)

            # Append to track
            track += section

        # Final processing
        track = self._finalize_track(track, structure)

        print(f"✅ Track composed: {len(track) / 1000:.1f}s")
        return track

    def _finalize_track(
        self, track: AudioSegment, structure: TrackStructure
    ) -> AudioSegment:
        """
        Final processing: normalization, trim
        """
        # Normalize (preserve dynamics)
        headroom = 1.0 if "minimal" in structure.name else 0.5
        track = normalize(track, headroom=headroom)

        # Trim to exact duration if needed
        target_duration = self.timing.bars_to_ms(structure.total_bars)
        if len(track) > target_duration:
            track = track[:target_duration]

        return track
