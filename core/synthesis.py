"""
Advanced synthesis utilities
Optional higher-level synthesis tools
"""

import numpy as np
from scipy import signal


class WaveformGenerator:
    """Generate basic waveforms for synthesis"""
    
    @staticmethod
    def sine(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """Generate sine wave"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return np.sin(2 * np.pi * frequency * t)
    
    @staticmethod
    def sawtooth(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """Generate sawtooth wave (rich harmonics)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return signal.sawtooth(2 * np.pi * frequency * t)
    
    @staticmethod
    def square(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """Generate square wave (hollow, 303-style)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return signal.square(2 * np.pi * frequency * t)
    
    @staticmethod
    def triangle(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """Generate triangle wave (softer than square)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return signal.sawtooth(2 * np.pi * frequency * t, width=0.5)


class EnvelopeGenerator:
    """Generate ADSR envelopes"""
    
    @staticmethod
    def adsr(
        attack: float,
        decay: float,
        sustain_level: float,
        release: float,
        duration: float,
        sample_rate: int = 44100
    ) -> np.ndarray:
        """
        Generate ADSR envelope
        
        Args:
            attack, decay, release: in seconds
            sustain_level: 0-1
            duration: total duration in seconds
        """
        total_samples = int(sample_rate * duration)
        
        # Calculate samples for each phase
        attack_samples = int(sample_rate * attack)
        decay_samples = int(sample_rate * decay)
        release_samples = int(sample_rate * release)
        sustain_samples = total_samples - attack_samples - decay_samples - release_samples
        
        # Build envelope
        envelope = np.zeros(total_samples)
        
        # Attack (0 → 1)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay (1 → sustain_level)
        start = attack_samples
        end = start + decay_samples
        envelope[start:end] = np.linspace(1, sustain_level, decay_samples)
        
        # Sustain (constant)
        start = attack_samples + decay_samples
        end = start + sustain_samples
        envelope[start:end] = sustain_level
        
        # Release (sustain_level → 0)
        start = total_samples - release_samples
        envelope[start:] = np.linspace(sustain_level, 0, release_samples)
        
        return envelope
    
    @staticmethod
    def exponential_decay(duration: float, decay_rate: float, sample_rate: int = 44100) -> np.ndarray:
        """Exponential decay envelope (common for techno)"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return np.exp(-decay_rate * t)
