"""
Distortion and saturation effects
Essential for industrial techno
"""

import numpy as np
from pydub import AudioSegment


class Distortion:
    """Distortion effects for industrial/aggressive techno"""

    @staticmethod
    def waveshaper(
        audio: AudioSegment, drive: float = 0.5, curve: str = "soft"  # 0-1
    ) -> AudioSegment:
        """
        Waveshaping distortion

        drive: 0 = clean, 1 = maximum distortion
        curve: 'soft' (warm) or 'hard' (aggressive)
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 32768.0  # Normalize to -1 to 1

        # Apply drive (pre-gain)
        samples = samples * (1 + drive * 10)

        # Apply waveshaping curve
        if curve == "soft":
            # Soft clipping (tanh)
            shaped = np.tanh(samples)
        elif curve == "hard":
            # Hard clipping
            shaped = np.clip(samples, -0.8, 0.8)
        else:
            shaped = samples

        # Scale back
        shaped = shaped * 32768.0
        shaped = np.clip(shaped, -32768, 32767).astype(np.int16)

        return AudioSegment(
            data=shaped.tobytes(),
            sample_width=2,
            frame_rate=audio.frame_rate,
            channels=1,
        )

    @staticmethod
    def bit_crush(
        audio: AudioSegment, bit_depth: int = 12  # 16 = clean, 8 = lo-fi, 4 = extreme
    ) -> AudioSegment:
        """
        Bit depth reduction (digital distortion)

        Use for industrial/glitch techno
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # Reduce bit depth
        levels = 2**bit_depth
        max_val = 32768.0

        # Quantize
        crushed = np.round(samples / max_val * levels) / levels * max_val
        crushed = np.clip(crushed, -32768, 32767).astype(np.int16)

        return AudioSegment(
            data=crushed.tobytes(),
            sample_width=2,
            frame_rate=audio.frame_rate,
            channels=1,
        )
