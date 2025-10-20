"""
Spatial effects (reverb, delay, stereo)
Essential for dub techno and atmosphere
"""

import numpy as np
from pydub import AudioSegment


class SpatialProcessor:
    """Reverb and delay effects"""

    @staticmethod
    def delay(
        audio: AudioSegment,
        delay_ms: int = 250,
        feedback: float = 0.5,
        mix: float = 0.3,
    ) -> AudioSegment:
        """
        Simple delay effect

        Args:
            delay_ms: Delay time in milliseconds
            feedback: Amount fed back (0-1)
            mix: Wet/dry mix (0=dry, 1=wet)
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        sample_rate = audio.frame_rate

        # Calculate delay in samples
        delay_samples = int((delay_ms / 1000) * sample_rate)

        # Create delay buffer
        output = np.copy(samples)

        # Apply delay with feedback
        for i in range(delay_samples, len(samples)):
            output[i] += output[i - delay_samples] * feedback

        # Mix dry/wet
        result = samples * (1 - mix) + output * mix

        # Normalize
        result = result / np.max(np.abs(result)) * 32767
        result = result.astype(np.int16)

        return AudioSegment(
            data=result.tobytes(), sample_width=2, frame_rate=sample_rate, channels=1
        )

    @staticmethod
    def stereo_width(audio: AudioSegment, width: float = 1.5) -> AudioSegment:
        """
        Increase stereo width (convert mono to pseudo-stereo)

        Args:
            width: 1.0 = normal, >1.0 = wider
        """
        if audio.channels == 1:
            # For mono audio, create pseudo-stereo with delay
            samples = np.array(audio.get_array_of_samples()).astype(np.float32)

            # Create delay for one channel (10-20ms is typical)
            delay_samples = int(0.015 * audio.frame_rate)  # 15ms delay

            # Left channel: original
            left = samples

            # Right channel: delayed and attenuated slightly
            right = np.zeros_like(samples)
            right[delay_samples:] = samples[:-delay_samples] * 0.8

            # Apply width
            if width != 1.0:
                # Mix some of left into right and vice versa
                cross_mix = (width - 1.0) * 0.3
                left_new = left * (1 - cross_mix) + right * cross_mix
                right_new = right * (1 - cross_mix) + left * cross_mix
                left, right = left_new, right_new

            # Interleave
            stereo = np.column_stack((left, right)).flatten()
        else:
            # For stereo audio, use mid/side processing
            samples = np.array(audio.get_array_of_samples()).astype(np.float32)
            samples = samples.reshape(-1, 2)  # Shape: (n_samples, 2)

            # Apply Haas effect (slight delay on one channel)
            mid = (samples[:, 0] + samples[:, 1]) / 2
            side = (samples[:, 0] - samples[:, 1]) / 2

            # Widen
            side = side * width

            # Reconstruct L/R
            left = mid + side
            right = mid - side

            # Interleave
            stereo = np.column_stack((left, right)).flatten()

        # Normalize
        stereo = stereo / np.max(np.abs(stereo)) * 32767
        stereo = stereo.astype(np.int16)

        return AudioSegment(
            data=stereo.tobytes(),
            sample_width=2,
            frame_rate=audio.frame_rate,
            channels=2,
        )
