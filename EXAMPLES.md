# Examples

Practical, copy-paste-ready examples for common use cases.

## Table of Contents

- [Quick Start](#quick-start)
- [Generating Tracks](#generating-tracks)
- [Working with Primitives](#working-with-primitives)
- [Custom Composition](#custom-composition)
- [Audio Processing](#audio-processing)
- [Advanced Techniques](#advanced-techniques)

---

## Quick Start

### Generate Your First Track

```
from techno.mixers.minimal import MinimalTechnoMixer

# Create mixer
mixer = MinimalTechnoMixer(bpm=124)

# Generate track
track = mixer.create_track()

# Export
track.export("my_first_track.wav", format="wav")

print("✓ Track generated!")
```

**Run it:**
```
python my_script.py
mpv my_first_track.wav
```

---

## Generating Tracks

### Minimal Techno

```
from techno.mixers.minimal import MinimalTechnoMixer

# Hypnotic minimal techno (Robert Hood style)
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()
track.export("minimal_124.wav", format="wav")

# Faster minimal
mixer = MinimalTechnoMixer(bpm=132)
track = mixer.create_track()
track.export("minimal_132.wav", format="wav")
```

---

### Industrial Techno

```
from techno.mixers.industrial import IndustrialTechnoMixer

# Aggressive industrial (Ancient Methods style)
mixer = IndustrialTechnoMixer(bpm=138)
track = mixer.create_track()
track.export("industrial_138.wav", format="wav")

# Faster, more intense
mixer = IndustrialTechnoMixer(bpm=145)
track = mixer.create_track()
track.export("industrial_145.wav", format="wav")
```

---

### Dub Techno

```
from techno.mixers.dub import DubTechnoMixer

# Deep dub techno (Basic Channel style)
mixer = DubTechnoMixer(bpm=118)
track = mixer.create_track()
track.export("dub_118.wav", format="wav")
```

---

### Compare All Subgenres

```
from techno.mixers.minimal import MinimalTechnoMixer
from techno.mixers.industrial import IndustrialTechnoMixer
from techno.mixers.dub import DubTechnoMixer

# Generate all styles
styles = [
    (MinimalTechnoMixer(124), "minimal_124.wav"),
    (IndustrialTechnoMixer(138), "industrial_138.wav"),
    (DubTechnoMixer(118), "dub_118.wav")
]

for mixer, filename in styles:
    print(f"Generating {filename}...")
    track = mixer.create_track()
    track.export(filename, format="wav")
    print(f"✓ {filename} complete")
```

---

## Working with Primitives

### Generate Individual Sounds

#### Kick Drums

```
from techno.core.primitives import Kick

kick = Kick(bpm=130)

# Clean minimal kick
minimal = kick.generate_minimal()
minimal.export("kick_minimal.wav", format="wav")

# Aggressive industrial kick
industrial = kick.generate_industrial()
industrial.export("kick_industrial.wav", format="wav")

# Default kick
default = kick.generate()
default.export("kick_default.wav", format="wav")
```

---

#### Bass Notes

```
from techno.core.primitives import Bass

bass = Bass(bpm=130)

# Generate specific notes
notes = {
    'A2': 110.0,
    'C3': 130.81,
    'E3': 164.81,
    'G3': 196.00
}

for name, freq in notes.items():
    note = bass.generate_note(frequency=freq, duration_bars=0.25)
    note.export(f"bass_{name}.wav", format="wav")
```

---

#### Hi-Hats

```
from techno.core.primitives import HiHat

hat = HiHat(bpm=130)

# Closed hi-hat (tight)
closed = hat.generate(closedness=0.95)
closed.export("hat_closed.wav", format="wav")

# Semi-open hi-hat
semi = hat.generate(closedness=0.5)
semi.export("hat_semi.wav", format="wav")

# Open hi-hat (splashy)
open_hat = hat.generate(closedness=0.1)
open_hat.export("hat_open.wav", format="wav")
```

---

### Build Drum Pattern

```
from techno.core.primitives import Kick, HiHat
from techno.core.timing import TimingCalculator
from pydub import AudioSegment

bpm = 130
timing = TimingCalculator(bpm=bpm)

# Generate sounds
kick = Kick(bpm=bpm).generate()
hat_closed = HiHat(bpm=bpm).generate(closedness=0.9)
hat_open = HiHat(bpm=bpm).generate(closedness=0.3)

# Build 1-bar pattern
bar_duration = timing.bars_to_ms(1)
pattern = AudioSegment.silent(duration=bar_duration)

# Kick on beats 1 and 3 (0ms and 923ms at 130 BPM)
beat_duration = timing.ms_per_beat
pattern = pattern.overlay(kick, position=0)
pattern = pattern.overlay(kick, position=int(beat_duration * 2))

# Hi-hats on 16th notes
for i in range(16):
    position = int(i * timing.ms_per_16th)
    # Alternate closed/open
    hat = hat_closed if i % 2 == 0 else hat_open
    pattern = pattern.overlay(hat, position=position)

pattern.export("drum_pattern_1bar.wav", format="wav")
```

---

### Build Bassline

```
from techno.core.primitives import Bass
from techno.core.timing import TimingCalculator
from pydub import AudioSegment

bpm = 124
timing = TimingCalculator(bpm=bpm)
bass = Bass(bpm=bpm)

# Note sequence (in Hz)
notes = [110.0, 123.47, 146.83, 164.81]  # A2, B2, D3, E3

# Build 4-bar bassline
bassline = AudioSegment.silent(duration=0)

for bar in range(4):
    # 4 notes per bar (1 per beat)
    for beat in range(4):
        note_idx = (bar * 4 + beat) % len(notes)
        freq = notes[note_idx]
        
        note = bass.generate_note(frequency=freq, duration_bars=0.25)
        bassline += note

bassline.export("bassline_4bars.wav", format="wav")
```

---

## Custom Composition

### Custom Track Structure

```
from techno.composition.structure import TrackComposer, TrackStructure

# Define custom structure
structure = TrackStructure(
    name="my_custom_track",
    sections=[
        # Minimal intro (8 bars)
        {'name': 'intro', 'bars': 8, 'style': 'minimal'},
        
        # Add bass (8 bars)
        {'name': 'develop', 'bars': 8, 'add': ['bass']},
        
        # Buildup with filter sweep (8 bars)
        {'name': 'buildup', 'bars': 8, 'filter_sweep': True},
        
        # Drop - full energy (16 bars)
        {'name': 'drop', 'bars': 16, 'energy': 1.0},
        
        # Breakdown - remove hats (8 bars)
        {'name': 'breakdown', 'bars': 8, 'remove': ['hats']},
        
        # Final drop (16 bars)
        {'name': 'drop2', 'bars': 16, 'energy': 1.0},
        
        # Fade out (8 bars)
        {'name': 'outro', 'bars': 8, 'fade_out': True}
    ],
    total_bars=72
)

# Compose
composer = TrackComposer(bpm=130)
track = composer.compose(structure)
track.export("custom_structure.wav", format="wav")
```

---

### Long-Form Track (5 minutes)

```
from techno.composition.structure import TrackComposer, TrackStructure

# 5-minute minimal techno (124 BPM, 160 bars)
structure = TrackStructure(
    name="5min_minimal",
    sections=[
        {'name': 'intro', 'bars': 16, 'style': 'minimal'},
        {'name': 'develop1', 'bars': 16, 'add': ['bass']},
        {'name': 'buildup1', 'bars': 16, 'filter_sweep': True},
        {'name': 'drop1', 'bars': 32, 'energy': 1.0},
        {'name': 'breakdown1', 'bars': 16, 'remove': ['hats']},
        {'name': 'buildup2', 'bars': 16, 'filter_sweep': True},
        {'name': 'drop2', 'bars': 32, 'energy': 1.0},
        {'name': 'outro', 'bars': 16, 'fade_out': True}
    ],
    total_bars=160
)

composer = TrackComposer(bpm=124)
track = composer.compose(structure)
track.export("5min_minimal.wav", format="wav")

print(f"Track duration: {len(track) / 1000:.1f} seconds")
```

---

## Audio Processing

### Apply Filters

```
from techno.processing.filters import TechnoFilters
from techno.mixers.minimal import MinimalTechnoMixer

# Generate track
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()

# Low-pass filter (muffled)
muffled = TechnoFilters.low_pass(track, cutoff_hz=2000)
muffled.export("track_lowpass_2k.wav", format="wav")

# High-pass filter (thin)
thin = TechnoFilters.high_pass(track, cutoff_hz=200)
thin.export("track_highpass_200.wav", format="wav")

# Band-pass filter (telephone effect)
telephone = TechnoFilters.band_pass(track, low_hz=300, high_hz=3000)
telephone.export("track_telephone.wav", format="wav")
```

---

### Apply Distortion

```
from techno.processing.distortion import DistortionProcessor
from techno.core.primitives import Kick

kick = Kick(bpm=130).generate()

# Soft saturation
warm = DistortionProcessor.soft_clip(kick, drive=0.3)
warm.export("kick_warm.wav", format="wav")

# Hard clipping
aggressive = DistortionProcessor.hard_clip(kick, drive=0.6)
aggressive.export("kick_aggressive.wav", format="wav")

# Bit crushing
crushed = DistortionProcessor.bit_crush(kick, bit_depth=8)
crushed.export("kick_crushed_8bit.wav", format="wav")
```

---

### Apply Compression and Limiting

```
from techno.processing.dynamics import DynamicsProcessor
from techno.mixers.minimal import MinimalTechnoMixer

# Generate track
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()

# Apply compression
compressed = DynamicsProcessor.compress(
    track,
    threshold_db=-20.0,
    ratio=4.0,
    attack_ms=5.0,
    release_ms=50.0
)

# Apply limiting (mastering)
mastered = DynamicsProcessor.limit(compressed, ceiling_db=-1.0)
mastered.export("track_mastered.wav", format="wav")
```

---

### Add Delay and Reverb

```
from techno.processing.spatial import SpatialProcessor
from techno.core.primitives import HiHat

hat = HiHat(bpm=130).generate()

# Delay (dotted 8th at 130 BPM)
delayed = SpatialProcessor.delay(
    hat,
    delay_ms=346,  # Dotted 8th = 346ms at 130 BPM
    feedback=0.6,
    mix=0.5
)
delayed.export("hat_delayed.wav", format="wav")

# Stereo widening
wide = SpatialProcessor.stereo_width(hat, width=2.0)
wide.export("hat_wide.wav", format="wav")
```

---

## Advanced Techniques

### Frequency Analysis

```
from techno.core.frequency import analyze_frequency_content
from techno.mixers.minimal import MinimalTechnoMixer

# Generate track
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()

# Analyze frequency distribution
analysis = analyze_frequency_content(track)

print("Frequency Distribution:")
for band, percentage in analysis.items():
    bar = '█' * int(percentage / 2)
    print(f"{band:10s} {bar:30s} {percentage:5.1f}%")
```

**Output:**
```
Frequency Distribution:
sub        ████████████████          32.5%
bass       █████████████████████     41.2%
low_mids   ████████                  16.8%
mids       ██                         4.2%
high_mids  █                          2.1%
highs      █                          2.4%
air        ░                          0.8%
```

---

### Build Processing Chain

```
from techno.mixers.minimal import MinimalTechnoMixer
from techno.processing.filters import TechnoFilters
from techno.processing.distortion import DistortionProcessor
from techno.processing.dynamics import DynamicsProcessor

# Generate raw track
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()

# Processing chain
# 1. High-pass filter (remove rumble)
track = TechnoFilters.high_pass(track, cutoff_hz=30)

# 2. Soft saturation (warmth)
track = DistortionProcessor.soft_clip(track, drive=0.2)

# 3. Compression (glue)
track = DynamicsProcessor.compress(
    track,
    threshold_db=-18.0,
    ratio=3.0
)

# 4. Limiting (loudness)
track = DynamicsProcessor.limit(track, ceiling_db=-0.5)

track.export("processed_track.wav", format="wav")
```

---

### Generate Stem Exports

```
from techno.generators.synth_generator import SynthGenerator

generator = SynthGenerator(bpm=130)

# Generate all stems
stems = generator.generate_all_stems(duration_bars=16, style='minimal')

# Export individually
stems['kick'].export("stem_kick.wav", format="wav")
stems['bass'].export("stem_bass.wav", format="wav")
stems['hats'].export("stem_hats.wav", format="wav")

print("✓ Stems exported")
```

---

### Batch Generate Tracks

```
from techno.mixers.minimal import MinimalTechnoMixer
from techno.mixers.industrial import IndustrialTechnoMixer

# Generate multiple variations
configs = [
    (MinimalTechnoMixer, 120, "minimal_120.wav"),
    (MinimalTechnoMixer, 124, "minimal_124.wav"),
    (MinimalTechnoMixer, 128, "minimal_128.wav"),
    (IndustrialTechnoMixer, 135, "industrial_135.wav"),
    (IndustrialTechnoMixer, 138, "industrial_138.wav"),
    (IndustrialTechnoMixer, 142, "industrial_142.wav"),
]

for MixerClass, bpm, filename in configs:
    print(f"Generating {filename}...")
    mixer = MixerClass(bpm=bpm)
    track = mixer.create_track()
    track.export(filename, format="wav")
    print(f"✓ {filename} complete ({len(track)/1000:.1f}s)")
```

---

### Custom Synthesis

```
import numpy as np
from pydub import AudioSegment
from techno.core.synthesis import WaveformGenerator, EnvelopeGenerator

# Generate waveform
wave_gen = WaveformGenerator()
waveform = wave_gen.sawtooth(frequency=55.0, duration=1.0)  # A1

# Generate envelope
env_gen = EnvelopeGenerator()
envelope = env_gen.adsr(
    attack=0.01,
    decay=0.2,
    sustain_level=0.6,
    release=0.3,
    duration=1.0
)

# Apply envelope
shaped = waveform * envelope

# Convert to audio
audio_array = (shaped * 32767).astype(np.int16)
audio = AudioSegment(
    data=audio_array.tobytes(),
    sample_width=2,
    frame_rate=44100,
    channels=1
)

audio.export("custom_synth_note.wav", format="wav")
```

---

### Analyze BPM Range

```
from techno.core.timing import TimingCalculator

# Test different BPMs
bpms =[1][2][3][4][5][6][7]

print("BPM Analysis:")
print(f"{'BPM':<5} {'ms/beat':<10} {'ms/bar':<10} {'bars/min':<10}")
print("-" * 40)

for bpm in bpms:
    timing = TimingCalculator(bpm=bpm)
    bars_per_min = 60 / (timing.ms_per_bar / 1000)
    
    print(f"{bpm:<5} {timing.ms_per_beat:<10.1f} {timing.ms_per_bar:<10.1f} {bars_per_min:<10.1f}")
```

**Output:**
```
BPM Analysis:
BPM   ms/beat    ms/bar     bars/min  
----------------------------------------
115   521.7      2087.0     28.8      
120   500.0      2000.0     30.0      
124   483.9      1935.5     31.0      
130   461.5      1846.2     32.5      
135   444.4      1777.8     33.8      
140   428.6      1714.3     35.0      
145   413.8      1655.2     36.3      
```

---

## Troubleshooting Examples

### Test FFmpeg

```
from pydub import AudioSegment
from techno.core.primitives import Kick

try:
    kick = Kick(bpm=130).generate()
    kick.export("test_ffmpeg.wav", format="wav")
    print("✓ FFmpeg working")
except Exception as e:
    print(f"✗ FFmpeg error: {e}")
    print("Install: sudo apt install ffmpeg")
```

---

### Verify Package Import

```
try:
    from techno.core.primitives import Kick
    from techno.core.timing import TimingCalculator
    from techno.mixers.minimal import MinimalTechnoMixer
    from techno.processing.filters import TechnoFilters
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Run: uv sync")
```

---

### Memory Usage Check

```
import psutil
from techno.mixers.minimal import MinimalTechnoMixer

# Check memory before
mem_before = psutil.Process().memory_info().rss / 1024**2  # MB

# Generate track
mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()

# Check memory after
mem_after = psutil.Process().memory_info().rss / 1024**2  # MB

print(f"Memory used: {mem_after - mem_before:.1f} MB")
```

---

## Next Steps

- Read [API.md](API.md) for complete API reference
- Check [README.md](README.md) for installation
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development

---

**Questions?** [Open an issue](https://github.com/TataSatyaPratheek/techno/issues) 🎵
