"""
Fundamental audio primitives for techno
Each function creates ONE perfect element
"""

import numpy as np
from pydub import AudioSegment
from scipy import signal


class TechnoPrimitive:
    """Base class for all techno elements"""

    def __init__(self, bpm: int, sample_rate: int = 44100):
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.samples_per_beat = int((60 / bpm) * sample_rate)

    def to_audio_segment(self, samples: np.ndarray) -> AudioSegment:
        """Convert numpy array to AudioSegment"""
        # Normalize to 16-bit int
        samples_int = (samples * 32767).astype(np.int16)

        # Create AudioSegment
        byte_array = samples_int.tobytes()
        return AudioSegment(data=byte_array, sample_width=2, frame_rate=self.sample_rate, channels=1)


class Kick(TechnoPrimitive):
    """Generate perfect techno kick from scratch"""

    def generate(
        self,
        sub_freq: float = 50,  # Sub-bass fundamental
        punch_freq: float = 80,  # Body/punch
        attack_ms: float = 5,  # Transient
        decay_ms: float = 200,  # Tail length
        punch: float = 0.8,  # Punch amount (0-1)
    ) -> AudioSegment:
        """
        Generate kick using synthesis

        Three-layer approach:
        1. Sub sine wave (40-60Hz)
        2. Punchy body (60-120Hz)
        3. Click transient (2-4kHz)
        """
        duration_samples = int((decay_ms / 1000) * self.sample_rate)
        t = np.linspace(0, decay_ms / 1000, duration_samples)

        # Layer 1: Sub bass (sine wave with pitch envelope)
        sub_envelope = np.exp(-8 * t)  # Fast decay
        sub_pitch = sub_freq * (1 + sub_envelope * 0.5)  # Pitch drops
        sub = np.sin(2 * np.pi * sub_pitch * t) * sub_envelope

        # Layer 2: Punch (filtered noise + sine)
        punch_envelope = np.exp(-15 * t)
        punch_sine = np.sin(2 * np.pi * punch_freq * t) * punch_envelope
        punch_noise = np.random.randn(duration_samples) * punch_envelope * 0.3
        punch_layer = (punch_sine + punch_noise) * punch

        # Layer 3: Click (filtered noise)
        click_envelope = np.exp(-100 * t)  # Very fast
        click = np.random.randn(duration_samples) * click_envelope * 0.5

        # Combine layers
        kick = sub * 0.7 + punch_layer * 0.5 + click * 0.3

        # Normalize
        kick = kick / np.max(np.abs(kick))

        return self.to_audio_segment(kick)

    def generate_minimal(self) -> AudioSegment:
        """Preset: Minimal techno kick (clean, tight)"""
        return self.generate(
            sub_freq=55,
            punch_freq=75,
            attack_ms=3,
            decay_ms=150,
            punch=0.6,  # Less punchy, more subtle
        )

    def generate_industrial(self) -> AudioSegment:
        """Preset: Industrial kick (aggressive, distorted)"""
        kick = self.generate(
            sub_freq=45,
            punch_freq=90,
            attack_ms=2,
            decay_ms=250,
            punch=1.0,  # Maximum punch
        )
        # Add distortion
        from techno.processing.distortion import Distortion

        return Distortion.waveshaper(kick, drive=0.7)


class Bass(TechnoPrimitive):
    """Generate techno bassline"""

    def generate_note(
        self,
        frequency: float = 110,  # A2 (common techno bass)
        duration_bars: float = 0.25,  # Quarter note
        waveform: str = "saw",
        filter_cutoff: float = 800,
        resonance: float = 0.7,
    ) -> AudioSegment:
        """
        Generate single bass note with filter

        Techno bass = Sawtooth wave + resonant low-pass filter
        """
        if frequency < 20 or frequency > 2000:
            raise ValueError(f"Bass frequency {frequency}Hz out of range (20-2000Hz)")

        duration_samples = int(duration_bars * 4 * self.samples_per_beat)
        t = np.linspace(0, duration_bars * 4 * (60 / self.bpm), duration_samples)

        # Generate waveform
        if waveform == "saw":
            # Sawtooth (rich harmonics)
            bass = signal.sawtooth(2 * np.pi * frequency * t)
        elif waveform == "square":
            # Square (hollow, 303-style)
            bass = signal.square(2 * np.pi * frequency * t)
        else:
            # Sine (pure sub)
            bass = np.sin(2 * np.pi * frequency * t)

        # Apply envelope (slight decay)
        envelope = np.exp(-0.5 * t)
        bass = bass * envelope

        # Apply resonant filter (simplified - in production use pedalboard)
        # For now, just low-pass
        nyquist = self.sample_rate / 2
        normalized_cutoff = filter_cutoff / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype="low")
        bass = signal.filtfilt(b, a, bass)

        # Normalize
        bass = bass / np.max(np.abs(bass))

        return self.to_audio_segment(bass)

    def generate_303_pattern(self, notes: list, pattern: str = "x-x-x-x-") -> AudioSegment:
        """
        Generate acid bassline pattern

        Args:
            notes: List of MIDI note numbers [40, 42, 45, 47]
            pattern: 'x' = note, '-' = rest, '.' = accent
        """
        result = AudioSegment.silent(duration=0)

        for i, char in enumerate(pattern):
            if char == "x" or char == ".":
                # Play note
                note_idx = i % len(notes)
                freq = 440 * (2 ** ((notes[note_idx] - 69) / 12))

                accent = 1.0 if char == "." else 0.7
                note = self.generate_note(
                    frequency=freq,
                    duration_bars=0.25,
                    waveform="saw",
                    filter_cutoff=int(800 * accent),
                    resonance=0.8,
                )

                # Apply accent
                note = note + (3 if char == "." else 0)

                result += note
            else:
                # Rest
                rest_duration = int(0.25 * 4 * self.samples_per_beat / self.sample_rate * 1000)
                result += AudioSegment.silent(duration=rest_duration)

        return result


class HiHat(TechnoPrimitive):
    """Generate hi-hat from noise"""

    def generate(
        self,
        frequency_center: int = 8000,
        duration_ms: float = 50,
        closedness: float = 0.8,  # 0=open, 1=closed
    ) -> AudioSegment:
        """
        Generate hi-hat using filtered noise
        """
        if not (0.0 <= closedness <= 1.0):
            raise ValueError(f"Closedness {closedness} must be between 0.0 and 1.0")

        duration_samples = int((duration_ms / 1000) * self.sample_rate)

        # Generate white noise
        noise = np.random.randn(duration_samples)

        # Apply high-pass filter (remove low frequencies)
        nyquist = self.sample_rate / 2
        hp_cutoff = 4000 / nyquist
        b_hp, a_hp = signal.butter(4, hp_cutoff, btype="high")
        noise = signal.filtfilt(b_hp, a_hp, noise)

        # Apply band-pass for tone (around 8-12kHz)
        bp_low = 6000 / nyquist
        bp_high = 12000 / nyquist
        b_bp, a_bp = signal.butter(2, [bp_low, bp_high], btype="band")
        noise = signal.filtfilt(b_bp, a_bp, noise)

        # Apply envelope (shorter for closed, longer for open)
        t = np.linspace(0, duration_ms / 1000, duration_samples)
        decay_rate = 50 * closedness + 10 * (1 - closedness)
        envelope = np.exp(-decay_rate * t)

        hat = noise * envelope

        # Normalize
        hat = hat / np.max(np.abs(hat))

        return self.to_audio_segment(hat)
