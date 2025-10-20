"""
Industrial techno
"""

from pydub import AudioSegment
from ..composition.structure import TrackComposer, StructureTemplates
from ..processing.distortion import Distortion
from ..processing.filters import TechnoFilters


class IndustrialTechnoMixer:
    """Industrial techno production"""
    
    def __init__(self, bpm: int = 138):
        self.bpm = bpm
        self.composer = TrackComposer(bpm)
    
    def create_track(self) -> AudioSegment:
        """
        Create complete industrial techno track
        
        Characteristics:
        - Aggressive, distorted kick
        - Harsh metallic percussion
        - Grinding bass
        - Heavy saturation
        - Crushed dynamics (loud!)
        """
        print("🎵 Creating industrial techno track...")
        
        structure = StructureTemplates.industrial_techno_30s()
        track = self.composer.compose(structure)
        
        # Apply industrial processing
        track = self._apply_industrial_processing(track)
        
        return track
    
    def _apply_industrial_processing(self, track: AudioSegment) -> AudioSegment:
        """
        Industrial-specific processing
        
        Key: Maximum aggression, crush dynamics
        """
        # Heavy saturation
        track = Distortion.waveshaper(track, drive=0.7, curve='hard')
        
        # Bit crush for digital grit
        track = Distortion.bit_crush(track, bit_depth=14)
        
        # Boost overall level (industrial is LOUD)
        track = track + 3.0  # +3dB
        
        # Heavy limiting (crush dynamics)
        from pydub.effects import normalize
        track = normalize(track, headroom=0.5)  # Minimal headroom
        
        return track

