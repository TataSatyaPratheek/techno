"""
Audio filtering for techno production
Low-pass, high-pass, resonant filters
"""

from typing import Optional

import numpy as np
from pydub import AudioSegment
from scipy import signal


class TechnoFilters:
    """Production-grade filters for techno"""

    @staticmethod
    def low_pass(
        audio: AudioSegment, cutoff_hz: int, resonance: float = 0.7, order: int = 4
    ) -> AudioSegment:
        """
        Low-pass filter (removes highs)

        Use cases:
        - Muffled intro
        - Filter sweep automation
        - Sub-bass isolation
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        sample_rate = audio.frame_rate

        # Design filter
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_hz / nyquist

        # Add resonance by using Butterworth with Q factor
        b, a = signal.butter(order, normalized_cutoff, btype="low")

        # Apply filter
        filtered = signal.filtfilt(b, a, samples)

        # Add resonance peak (simplified - in production use pedalboard)
        if resonance > 0:
            # Boost at cutoff frequency
            boost_freq = cutoff_hz
            boost_q = resonance * 10
            b_peak, a_peak = signal.iirpeak(boost_freq / nyquist, boost_q)
            filtered = signal.filtfilt(b_peak, a_peak, filtered)

        return TechnoFilters._array_to_audio(filtered, audio)

    @staticmethod
    def high_pass(audio: AudioSegment, cutoff_hz: int, order: int = 4) -> AudioSegment:
        """
        High-pass filter (removes lows)

        Use cases:
        - Bass frequency carving (remove kick's sub)
        - Thin out pads
        - Remove rumble
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        sample_rate = audio.frame_rate

        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_hz / nyquist

        b, a = signal.butter(order, normalized_cutoff, btype="high")
        filtered = signal.filtfilt(b, a, samples)

        return TechnoFilters._array_to_audio(filtered, audio)

    @staticmethod
    def band_pass(audio: AudioSegment, low_hz: int, high_hz: int) -> AudioSegment:
        """
        Band-pass filter (isolate frequency range)

        Use cases:
        - Isolate kick body (60-120Hz)
        - Isolate hi-hats (6-12kHz)
        """
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        sample_rate = audio.frame_rate

        nyquist = sample_rate / 2
        low_norm = low_hz / nyquist
        high_norm = high_hz / nyquist

        b, a = signal.butter(4, [low_norm, high_norm], btype="band")
        filtered = signal.filtfilt(b, a, samples)

        return TechnoFilters._array_to_audio(filtered, audio)

    @staticmethod
    def filter_sweep(
        audio: AudioSegment,
        start_hz: int,
        end_hz: int,
        sweep_duration_ms: Optional[int] = None,
    ) -> AudioSegment:
        """
        Sweep filter cutoff over time (classic techno technique)

        Example: Start at 200Hz (muffled), sweep to 2kHz (bright)
        """
        sweep_duration_ms = sweep_duration_ms or len(audio)

        # Split into chunks and apply progressive filters
        chunk_size = 500  # 500ms chunks
        num_chunks = sweep_duration_ms // chunk_size

        filtered_chunks = []

        for i in range(num_chunks):
            # Calculate cutoff for this chunk
            progress = i / num_chunks
            cutoff = int(start_hz + (end_hz - start_hz) * progress)

            # Extract chunk
            chunk_start = i * chunk_size
            chunk_end = chunk_start + chunk_size
            chunk = audio[chunk_start:chunk_end]

            # Apply filter
            filtered_chunk = TechnoFilters.low_pass(chunk, cutoff)
            filtered_chunks.append(filtered_chunk)

        # Handle remainder
        if len(audio) % chunk_size != 0:
            remainder = audio[num_chunks * chunk_size :]
            filtered_remainder = TechnoFilters.low_pass(remainder, end_hz)
            filtered_chunks.append(filtered_remainder)

        return sum(filtered_chunks, AudioSegment.silent(duration=0))

    @staticmethod
    def _array_to_audio(samples: np.ndarray, reference: AudioSegment) -> AudioSegment:
        """Convert numpy array back to AudioSegment"""
        # Clip to prevent overflow
        samples = np.clip(samples, -32768, 32767)
        samples_int = samples.astype(np.int16)

        return AudioSegment(
            data=samples_int.tobytes(),
            sample_width=2,
            frame_rate=reference.frame_rate,
            channels=1,
        )
