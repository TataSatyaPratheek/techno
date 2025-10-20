"""
Dynamics processing (compression, limiting)
Essential for controlling energy
"""

import numpy as np
from pydub import AudioSegment


class DynamicsProcessor:
    """Compression and limiting"""

    @staticmethod
    def compress(
        audio: AudioSegment,
        threshold_db: float = -20.0,
        ratio: float = 4.0,
        attack_ms: float = 5.0,
        release_ms: float = 50.0,
    ) -> AudioSegment:
        """
        Compressor (reduces dynamic range)

        Args:
            threshold_db: Level above which compression starts
            ratio: 4:1 = every 4dB above threshold becomes 1dB
            attack/release: How fast compressor reacts
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 32768.0  # Normalize to -1 to 1

        # Convert threshold to linear
        threshold_linear = 10 ** (threshold_db / 20.0)

        # Simple peak compression (production would use RMS)
        compressed = np.copy(samples)

        for i, sample in enumerate(samples):
            level = abs(sample)

            if level > threshold_linear:
                # Calculate gain reduction
                excess = level - threshold_linear
                reduction = excess * (1 - 1 / ratio)

                # Apply compression
                sign = 1 if sample >= 0 else -1
                compressed[i] = sign * (threshold_linear + excess - reduction)

        # Convert back
        compressed = compressed * 32768.0
        compressed = np.clip(compressed, -32768, 32767).astype(np.int16)

        return AudioSegment(
            data=compressed.tobytes(),
            sample_width=2,
            frame_rate=audio.frame_rate,
            channels=1,
        )

    @staticmethod
    def limit(audio: AudioSegment, ceiling_db: float = -1.0) -> AudioSegment:
        """
        Limiter (hard ceiling, prevents clipping)

        Args:
            ceiling_db: Maximum output level
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples = samples / 32768.0

        # Convert ceiling to linear
        ceiling_linear = 10 ** (ceiling_db / 20.0)

        # Hard limiting
        limited = np.clip(samples, -ceiling_linear, ceiling_linear)

        # Convert back
        limited = limited * 32768.0
        limited = limited.astype(np.int16)

        return AudioSegment(
            data=limited.tobytes(),
            sample_width=2,
            frame_rate=audio.frame_rate,
            channels=1,
        )
