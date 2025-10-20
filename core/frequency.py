"""
Frequency allocation and analysis
Prevents muddy mixes through intelligent carving
"""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from pydub import AudioSegment
from scipy import signal


@dataclass
class FrequencyBand:
    """Represents a frequency range"""

    low: int  # Hz
    high: int  # Hz
    name: str
    role: str  # What occupies this band


class FrequencyMap:
    """Standard frequency allocation for techno"""

    # Techno frequency bands (from master report)
    SUB_BASS = FrequencyBand(20, 60, "sub", "kick_fundamental")
    BASS = FrequencyBand(60, 250, "bass", "kick_body_and_bass")
    LOW_MIDS = FrequencyBand(250, 500, "low_mids", "bass_harmonics")
    MIDS = FrequencyBand(500, 2000, "mids", "synth_pads")
    HIGH_MIDS = FrequencyBand(2000, 6000, "high_mids", "transients")
    HIGHS = FrequencyBand(6000, 12000, "highs", "hi_hats")
    AIR = FrequencyBand(12000, 20000, "air", "shimmer")

    @classmethod
    def get_allocation(cls, element: str) -> List[FrequencyBand]:
        """Get frequency allocation for specific element"""
        allocations = {
            "kick": [cls.SUB_BASS, cls.BASS, cls.HIGH_MIDS],  # Sub + body + click
            "bass": [cls.BASS, cls.LOW_MIDS],  # Sits above kick
            "hats": [cls.HIGHS, cls.AIR],
            "synth": [cls.MIDS, cls.HIGH_MIDS],
            "pad": [cls.MIDS],
        }
        return allocations.get(element, [])


def analyze_frequency_content(audio: AudioSegment, sample_rate: int = 44100) -> Dict[str, float]:
    """
    Analyze which frequencies are present

    Returns:
        Dict of band name -> energy percentage
    """
    # Convert to numpy
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples = samples / 32768.0  # Normalize

    # Compute FFT
    fft = np.fft.rfft(samples)
    freqs = np.fft.rfftfreq(len(samples), 1 / sample_rate)
    magnitudes = np.abs(fft)

    # Analyze each band
    results = {}
    bands = [
        FrequencyMap.SUB_BASS,
        FrequencyMap.BASS,
        FrequencyMap.LOW_MIDS,
        FrequencyMap.MIDS,
        FrequencyMap.HIGH_MIDS,
        FrequencyMap.HIGHS,
        FrequencyMap.AIR,
    ]

    total_energy = np.sum(magnitudes**2)

    for band in bands:
        # Find frequencies in this band
        band_mask = (freqs >= band.low) & (freqs <= band.high)
        band_energy = np.sum(magnitudes[band_mask] ** 2)

        # Calculate percentage
        percentage = (band_energy / total_energy) * 100 if total_energy > 0 else 0
        results[band.name] = percentage

    return results


def carve_frequency_space(
    stems: Dict[str, AudioSegment], allocations: Dict[str, List[FrequencyBand]]
) -> Dict[str, AudioSegment]:
    """
    Apply EQ to prevent frequency conflicts

    Example:
        kick gets 20-120Hz (full range)
        bass gets high-pass at 100Hz (removes kick's fundamental)
    """
    carved_stems = {}

    for stem_name, audio in stems.items():
        if stem_name not in allocations:
            carved_stems[stem_name] = audio
            continue

        # Get target bands for this stem
        target_bands = allocations[stem_name]

        # Apply filters to isolate target bands
        # (Simplified - in production use parametric EQ)
        carved = audio  # Start with original

        # For now, just apply high-pass if needed
        if stem_name == "bass":
            # High-pass at 80Hz to remove kick's sub
            carved = apply_highpass(carved, cutoff_hz=80)

        carved_stems[stem_name] = carved

    return carved_stems


def apply_highpass(audio: AudioSegment, cutoff_hz: int) -> AudioSegment:
    """Apply high-pass filter"""
    # Convert to numpy
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    sample_rate = audio.frame_rate

    # Design filter
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff_hz / nyquist
    b, a = signal.butter(4, normalized_cutoff, btype="high")

    # Apply filter
    filtered = signal.filtfilt(b, a, samples)

    # Convert back
    filtered_int = (filtered).astype(np.int16)
    return AudioSegment(data=filtered_int.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1)
