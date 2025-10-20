# API Reference

Complete API documentation for programmatic usage of Techno Generator.

## Table of Contents

- [API Reference](#api-reference)
  - [Table of Contents](#table-of-contents)
  - [Core Modules](#core-modules)
    - [Primitives](#primitives)
      - [`Kick`](#kick)
      - [`Bass`](#bass)
      - [`HiHat`](#hihat)
    - [Timing](#timing)
      - [`TimingCalculator`](#timingcalculator)
    - [Frequency](#frequency)
      - [`FrequencyMap`](#frequencymap)
    - [Synthesis](#synthesis)
      - [`WaveformGenerator`](#waveformgenerator)
      - [`EnvelopeGenerator`](#envelopegenerator)
  - [Composition](#composition)
    - [Phrase](#phrase)
      - [`TechnoPhrase`](#technophrase)
    - [Section](#section)
      - [`SectionBuilder`](#sectionbuilder)
    - [Structure](#structure)
      - [`TrackComposer`](#trackcomposer)
  - [Mixers](#mixers)
    - [Minimal](#minimal)
      - [`MinimalTechnoMixer`](#minimaltechnomixer)
    - [Industrial](#industrial)
      - [`IndustrialTechnoMixer`](#industrialtechnomixer)
    - [Dub](#dub)
      - [`DubTechnoMixer`](#dubtechnomixer)
  - [Processing](#processing)
    - [Filters](#filters)
      - [`TechnoFilters`](#technofilters)
    - [Distortion](#distortion)
      - [`DistortionProcessor`](#distortionprocessor)
    - [Dynamics](#dynamics)
      - [`DynamicsProcessor`](#dynamicsprocessor)
    - [Spatial](#spatial)
      - [`SpatialProcessor`](#spatialprocessor)
  - [Generators](#generators)
    - [Synth Generator](#synth-generator)
      - [`SynthGenerator`](#synthgenerator)
  - [Type Hints](#type-hints)
  - [Error Handling](#error-handling)
  - [Further Reading](#further-reading)

---

## Core Modules

### Primitives

#### `Kick`

Generate kick drum sounds.

```
from techno.core.primitives import Kick

kick = Kick(bpm=130)
```

**Methods:**

```
# Generate clean minimal kick
kick_audio = kick.generate()
# Returns: AudioSegment

# Generate minimal kick (optimized)
kick_audio = kick.generate_minimal()
# Returns: AudioSegment

# Generate aggressive industrial kick
kick_audio = kick.generate_industrial()
# Returns: AudioSegment
```

**Parameters:**
- `bpm` (int): Beats per minute (default: 130)

**Example:**
```
from techno.core.primitives import Kick

kick = Kick(bpm=140)
kick_audio = kick.generate_industrial()
kick_audio.export("kick.wav", format="wav")
```

---

#### `Bass`

Generate bass sounds.

```
from techno.core.primitives import Bass

bass = Bass(bpm=130)
```

**Methods:**

```
# Generate single bass note
bass_note = bass.generate_note(
    frequency=110.0,      # Frequency in Hz (A2 = 110 Hz)
    duration_bars=0.25    # Duration in bars (0.25 = 1 beat)
)
# Returns: AudioSegment

# Generate bassline pattern
bassline = bass.generate()
# Returns: AudioSegment (8-bar pattern)
```

**Parameters:**
- `bpm` (int): Beats per minute (default: 130)

**Example:**
```
from techno.core.primitives import Bass

bass = Bass(bpm=124)

# Generate A2 note (110 Hz)
note = bass.generate_note(frequency=110.0, duration_bars=0.25)
note.export("bass_note.wav", format="wav")

# Generate full 8-bar bassline
bassline = bass.generate()
bassline.export("bassline.wav", format="wav")
```

---

#### `HiHat`

Generate hi-hat sounds.

```
from techno.core.primitives import HiHat

hat = HiHat(bpm=130)
```

**Methods:**

```
# Generate hi-hat
hat_audio = hat.generate(
    closedness=0.8,  # 0.0 = open, 1.0 = closed
    duration_ms=50   # Duration in milliseconds
)
# Returns: AudioSegment
```

**Parameters:**
- `bpm` (int): Beats per minute (default: 130)

**Example:**
```
from techno.core.primitives import HiHat

hat = HiHat(bpm=130)

# Closed hi-hat
closed = hat.generate(closedness=0.9)
closed.export("closed_hat.wav", format="wav")

# Open hi-hat
open_hat = hat.generate(closedness=0.3)
open_hat.export("open_hat.wav", format="wav")
```

---

### Timing

#### `TimingCalculator`

Musical time calculations.

```
from techno.core.timing import TimingCalculator

timing = TimingCalculator(bpm=130)
```

**Properties:**

```
timing.bpm               # BPM value
timing.ms_per_beat       # Milliseconds per beat
timing.ms_per_bar        # Milliseconds per bar (4 beats)
timing.ms_per_16th       # Milliseconds per 16th note
```

**Methods:**

```
# Convert bars to milliseconds
ms = timing.bars_to_ms(bars=8)
# Returns: float

# Convert milliseconds to bars
bars = timing.ms_to_bars(milliseconds=2000)
# Returns: float

# Snap to nearest bar boundary
snapped_ms = timing.nearest_bar(milliseconds=1950)
# Returns: int

# Create timing grid
grid = timing.create_grid(
    total_bars=1,
    subdivision=16  # 16th notes
)
# Returns: List[int] - positions in milliseconds
```

**Example:**
```
from techno.core.timing import TimingCalculator

timing = TimingCalculator(bpm=124)

# How long is 8 bars?
duration_ms = timing.bars_to_ms(8)
print(f"8 bars at 124 BPM = {duration_ms}ms")

# Create 16th note grid for 1 bar
grid = timing.create_grid(total_bars=1, subdivision=16)
print(f"16th note positions: {grid}")
```

---

### Frequency

#### `FrequencyMap`

Frequency band definitions for mixing.

```
from techno.core.frequency import FrequencyMap
```

**Predefined Bands:**

```
FrequencyMap.SUB_BASS     # 20-60 Hz
FrequencyMap.BASS         # 60-250 Hz
FrequencyMap.LOW_MIDS     # 250-500 Hz
FrequencyMap.MIDS         # 500-2000 Hz
FrequencyMap.HIGH_MIDS    # 2000-6000 Hz
FrequencyMap.HIGHS        # 6000-12000 Hz
FrequencyMap.AIR          # 12000-20000 Hz
```

**Methods:**

```
# Get frequency allocation for element
bands = FrequencyMap.get_allocation('kick')
# Returns: List[FrequencyBand]
# kick uses: SUB_BASS, BASS, HIGH_MIDS

bands = FrequencyMap.get_allocation('bass')
# Returns: List[FrequencyBand]
# bass uses: BASS, LOW_MIDS

bands = FrequencyMap.get_allocation('hats')
# Returns: List[FrequencyBand]
# hats use: HIGHS, AIR
```

**Functions:**

```
from techno.core.frequency import analyze_frequency_content, apply_highpass

# Analyze frequency distribution
analysis = analyze_frequency_content(audio)
# Returns: Dict[str, float]
# Example: {'sub': 32.5, 'bass': 41.2, 'mids': 16.8, ...}

# Apply high-pass filter
filtered = apply_highpass(audio, cutoff_hz=80)
# Returns: AudioSegment
```

**Example:**
```
from techno.core.frequency import FrequencyMap, analyze_frequency_content
from techno.core.primitives import Kick

# Generate kick
kick = Kick(bpm=130).generate()

# Analyze frequency content
analysis = analyze_frequency_content(kick)
print(f"Sub-bass energy: {analysis['sub']:.1f}%")
print(f"Bass energy: {analysis['bass']:.1f}%")

# Get frequency allocation
bands = FrequencyMap.get_allocation('kick')
for band in bands:
    print(f"{band.name}: {band.low}-{band.high} Hz")
```

---

### Synthesis

#### `WaveformGenerator`

Generate basic waveforms.

```
from techno.core.synthesis import WaveformGenerator

gen = WaveformGenerator()
```

**Methods:**

```
# Sine wave
sine = gen.sine(
    frequency=440.0,     # Hz
    duration=1.0,        # seconds
    sample_rate=44100
)
# Returns: np.ndarray

# Sawtooth wave (bright, rich harmonics)
saw = gen.sawtooth(frequency=110.0, duration=1.0)
# Returns: np.ndarray

# Square wave (hollow, 303-style)
square = gen.square(frequency=110.0, duration=1.0)
# Returns: np.ndarray

# Triangle wave (softer than square)
triangle = gen.triangle(frequency=110.0, duration=1.0)
# Returns: np.ndarray
```

**Example:**
```
import numpy as np
from pydub import AudioSegment
from techno.core.synthesis import WaveformGenerator

gen = WaveformGenerator()

# Generate 440 Hz sine wave (1 second)
sine_wave = gen.sine(frequency=440.0, duration=1.0)

# Convert to AudioSegment
audio_array = (sine_wave * 32767).astype(np.int16)
audio = AudioSegment(
    data=audio_array.tobytes(),
    sample_width=2,
    frame_rate=44100,
    channels=1
)
audio.export("sine_440hz.wav", format="wav")
```

---

#### `EnvelopeGenerator`

Generate ADSR envelopes.

```
from techno.core.synthesis import EnvelopeGenerator

gen = EnvelopeGenerator()
```

**Methods:**

```
# ADSR envelope
envelope = gen.adsr(
    attack=0.01,         # seconds
    decay=0.1,           # seconds
    sustain_level=0.7,   # 0-1
    release=0.2,         # seconds
    duration=1.0,        # total duration
    sample_rate=44100
)
# Returns: np.ndarray

# Exponential decay
envelope = gen.exponential_decay(
    duration=1.0,
    decay_rate=5.0,
    sample_rate=44100
)
# Returns: np.ndarray
```

**Example:**
```
import numpy as np
from techno.core.synthesis import EnvelopeGenerator, WaveformGenerator

# Generate tone
wave_gen = WaveformGenerator()
tone = wave_gen.sine(frequency=440.0, duration=1.0)

# Apply envelope
env_gen = EnvelopeGenerator()
envelope = env_gen.adsr(
    attack=0.01,
    decay=0.1,
    sustain_level=0.7,
    release=0.2,
    duration=1.0
)

# Multiply tone by envelope
shaped = tone * envelope
```

---

## Composition

### Phrase

#### `TechnoPhrase`

Build 8-bar musical phrases.

```
from techno.composition.phrase import TechnoPhrase

phrase_builder = TechnoPhrase(bpm=130)
```

**Methods:**

```
# Build phrase with specific elements
phrase = phrase_builder.build_phrase(
    elements=['kick', 'bass', 'hats'],  # List of elements
    volumes={'kick': 0.0, 'bass': -2.0, 'hats': -3.0}  # dB adjustments
)
# Returns: AudioSegment (8 bars)
```

**Example:**
```
from techno.composition.phrase import TechnoPhrase

phrase_builder = TechnoPhrase(bpm=124)

# Build minimal phrase (kick only)
minimal = phrase_builder.build_phrase(
    elements=['kick'],
    volumes={'kick': 0.0}
)
minimal.export("minimal_phrase.wav", format="wav")

# Build full phrase
full = phrase_builder.build_phrase(
    elements=['kick', 'bass', 'hats'],
    volumes={'kick': 0.0, 'bass': -1.0, 'hats': -2.0}
)
full.export("full_phrase.wav", format="wav")
```

---

### Section

#### `SectionBuilder`

Build track sections (intro, buildup, drop, breakdown).

```
from techno.composition.section import SectionBuilder

section_builder = SectionBuilder(bpm=130)
```

**Methods:**

```
# Create intro section
intro = section_builder.create_intro(
    bars=16,
    style='minimal'  # or 'industrial'
)
# Returns: AudioSegment

# Create buildup section
buildup = section_builder.create_buildup(
    bars=16,
    filter_sweep=True  # Gradually open filter
)
# Returns: AudioSegment

# Create drop/climax section
drop = section_builder.create_drop(
    bars=32,
    energy=1.0  # 0-1 scale
)
# Returns: AudioSegment

# Create breakdown section
breakdown = section_builder.create_breakdown(
    bars=16,
    remove_elements=['hats']  # Elements to remove
)
# Returns: AudioSegment
```

**Example:**
```
from techno.composition.section import SectionBuilder

section_builder = SectionBuilder(bpm=130)

# Build minimal intro
intro = section_builder.create_intro(bars=16, style='minimal')
intro.export("intro.wav", format="wav")

# Build buildup with filter sweep
buildup = section_builder.create_buildup(bars=16, filter_sweep=True)
buildup.export("buildup.wav", format="wav")

# Build drop
drop = section_builder.create_drop(bars=32, energy=1.0)
drop.export("drop.wav", format="wav")
```

---

### Structure

#### `TrackComposer`

Compose complete tracks from structures.

```
from techno.composition.structure import TrackComposer

composer = TrackComposer(bpm=130)
```

**Methods:**

```
# Compose track from structure
track = composer.compose(structure)
# Returns: AudioSegment

# Structure can be:
# - TrackStructure object
# - Preset name string ('minimal_30s', 'industrial_30s', etc.)
```

**TrackStructure:**

```
from techno.composition.structure import TrackStructure

structure = TrackStructure(
    name="custom",
    sections=[
        {'name': 'intro', 'bars': 16, 'style': 'minimal'},
        {'name': 'buildup', 'bars': 16, 'filter_sweep': True},
        {'name': 'drop', 'bars': 32, 'energy': 1.0},
        {'name': 'outro', 'bars': 16, 'fade_out': True}
    ],
    total_bars=80
)
```

**Preset Templates:**

```
from techno.composition.structure import StructureTemplates

# Get minimal 30s structure
structure = StructureTemplates.minimal_30s()

# Get industrial 30s structure
structure = StructureTemplates.industrial_30s()

# Get dub 30s structure
structure = StructureTemplates.dub_30s()
```

**Example:**
```
from techno.composition.structure import TrackComposer, StructureTemplates

composer = TrackComposer(bpm=124)

# Use preset structure
structure = StructureTemplates.minimal_30s()
track = composer.compose(structure)
track.export("minimal_track.wav", format="wav")

# Custom structure
from techno.composition.structure import TrackStructure

custom = TrackStructure(
    name="my_track",
    sections=[
        {'name': 'intro', 'bars': 8},
        {'name': 'buildup', 'bars': 8, 'filter_sweep': True},
        {'name': 'drop', 'bars': 16, 'energy': 1.0}
    ],
    total_bars=32
)

track = composer.compose(custom)
track.export("custom_track.wav", format="wav")
```

---

## Mixers

### Minimal

#### `MinimalTechnoMixer`

Generate minimal techno tracks.

```
from techno.mixers.minimal import MinimalTechnoMixer

mixer = MinimalTechnoMixer(bpm=124)
```

**Methods:**

```
# Create complete track
track = mixer.create_track()
# Returns: AudioSegment
```

**Characteristics:**
- BPM: 124 (default)
- Style: Hypnotic, sparse, repetitive
- Inspiration: Robert Hood, Richie Hawtin

**Example:**
```
from techno.mixers.minimal import MinimalTechnoMixer

mixer = MinimalTechnoMixer(bpm=124)
track = mixer.create_track()
track.export("minimal_techno.wav", format="wav")
```

---

### Industrial

#### `IndustrialTechnoMixer`

Generate industrial techno tracks.

```
from techno.mixers.industrial import IndustrialTechnoMixer

mixer = IndustrialTechnoMixer(bpm=138)
```

**Methods:**

```
# Create complete track
track = mixer.create_track()
# Returns: AudioSegment
```

**Characteristics:**
- BPM: 138 (default)
- Style: Aggressive, harsh, dystopian
- Inspiration: Ancient Methods, Surgeon, Regis

**Example:**
```
from techno.mixers.industrial import IndustrialTechnoMixer

mixer = IndustrialTechnoMixer(bpm=140)
track = mixer.create_track()
track.export("industrial_techno.wav", format="wav")
```

---

### Dub

#### `DubTechnoMixer`

Generate dub techno tracks.

```
from techno.mixers.dub import DubTechnoMixer

mixer = DubTechnoMixer(bpm=118)
```

**Methods:**

```
# Create complete track
track = mixer.create_track()
# Returns: AudioSegment
```

**Characteristics:**
- BPM: 118 (default)
- Style: Deep, spacious, atmospheric
- Inspiration: Basic Channel, Deepchord

**Example:**
```
from techno.mixers.dub import DubTechnoMixer

mixer = DubTechnoMixer(bpm=118)
track = mixer.create_track()
track.export("dub_techno.wav", format="wav")
```

---

## Processing

### Filters

#### `TechnoFilters`

Audio filtering tools.

```
from techno.processing.filters import TechnoFilters
```

**Methods:**

```
# Low-pass filter (remove highs)
filtered = TechnoFilters.low_pass(
    audio,
    cutoff_hz=2000  # Frequencies above 2kHz are removed
)
# Returns: AudioSegment

# High-pass filter (remove lows)
filtered = TechnoFilters.high_pass(
    audio,
    cutoff_hz=80  # Frequencies below 80Hz are removed
)
# Returns: AudioSegment

# Band-pass filter (keep specific range)
filtered = TechnoFilters.band_pass(
    audio,
    low_hz=100,
    high_hz=5000
)
# Returns: AudioSegment

# Resonant filter (emphasize specific frequency)
filtered = TechnoFilters.resonant_filter(
    audio,
    center_hz=1000,
    resonance=0.7  # 0-1 scale
)
# Returns: AudioSegment
```

**Example:**
```
from techno.processing.filters import TechnoFilters
from techno.core.primitives import Kick

kick = Kick(bpm=130).generate()

# Muffled kick (low-pass at 2kHz)
muffled = TechnoFilters.low_pass(kick, cutoff_hz=2000)
muffled.export("muffled_kick.wav", format="wav")

# Remove sub-bass (high-pass at 80Hz)
thin = TechnoFilters.high_pass(kick, cutoff_hz=80)
thin.export("thin_kick.wav", format="wav")
```

---

### Distortion

#### `DistortionProcessor`

Audio distortion effects.

```
from techno.processing.distortion import DistortionProcessor
```

**Methods:**

```
# Soft clipping (warm saturation)
distorted = DistortionProcessor.soft_clip(
    audio,
    drive=0.5  # 0-1 scale
)
# Returns: AudioSegment

# Hard clipping (aggressive)
distorted = DistortionProcessor.hard_clip(
    audio,
    drive=0.7
)
# Returns: AudioSegment

# Bit crushing (digital degradation)
crushed = DistortionProcessor.bit_crush(
    audio,
    bit_depth=8  # 1-16 bits
)
# Returns: AudioSegment
```

**Example:**
```
from techno.processing.distortion import DistortionProcessor
from techno.core.primitives import Kick

kick = Kick(bpm=130).generate()

# Warm saturation
warm = DistortionProcessor.soft_clip(kick, drive=0.3)
warm.export("warm_kick.wav", format="wav")

# Aggressive distortion
aggressive = DistortionProcessor.hard_clip(kick, drive=0.7)
aggressive.export("aggressive_kick.wav", format="wav")
```

---

### Dynamics

#### `DynamicsProcessor`

Compression and limiting.

```
from techno.processing.dynamics import DynamicsProcessor
```

**Methods:**

```
# Compression (reduce dynamic range)
compressed = DynamicsProcessor.compress(
    audio,
    threshold_db=-20.0,  # Compress above this level
    ratio=4.0,           # 4:1 compression
    attack_ms=5.0,       # Fast attack
    release_ms=50.0      # Medium release
)
# Returns: AudioSegment

# Limiting (prevent clipping)
limited = DynamicsProcessor.limit(
    audio,
    ceiling_db=-1.0  # Maximum output level
)
# Returns: AudioSegment
```

**Example:**
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
    ratio=4.0
)

# Apply limiting
final = DynamicsProcessor.limit(compressed, ceiling_db=-1.0)
final.export("mastered_track.wav", format="wav")
```

---

### Spatial

#### `SpatialProcessor`

Reverb and delay effects.

```
from techno.processing.spatial import SpatialProcessor
```

**Methods:**

```
# Delay effect
delayed = SpatialProcessor.delay(
    audio,
    delay_ms=250,      # Delay time
    feedback=0.5,      # Amount fed back (0-1)
    mix=0.3           # Wet/dry mix (0-1)
)
# Returns: AudioSegment

# Stereo widening
wide = SpatialProcessor.stereo_width(
    audio,
    width=1.5  # 1.0 = normal, >1.0 = wider
)
# Returns: AudioSegment
```

**Example:**
```
from techno.processing.spatial import SpatialProcessor
from techno.core.primitives import HiHat

hat = HiHat(bpm=130).generate()

# Add delay
delayed = SpatialProcessor.delay(
    hat,
    delay_ms=375,  # Dotted 8th at 130 BPM
    feedback=0.6,
    mix=0.4
)
delayed.export("delayed_hat.wav", format="wav")

# Widen stereo image
wide = SpatialProcessor.stereo_width(hat, width=1.8)
wide.export("wide_hat.wav", format="wav")
```

---

## Generators

### Synth Generator

#### `SynthGenerator`

Generate stems from pure synthesis.

```
from techno.generators.synth_generator import SynthGenerator

generator = SynthGenerator(bpm=130)
```

**Methods:**

```
# Generate single stem
stem = generator.generate_stem(
    element='kick',        # 'kick', 'bass', or 'hats'
    duration_bars=8,
    style='minimal'        # 'minimal' or 'industrial'
)
# Returns: AudioSegment

# Generate all stems
stems = generator.generate_all_stems(
    duration_bars=8,
    style='minimal'
)
# Returns: Dict[str, AudioSegment]
# {'kick': AudioSegment, 'bass': AudioSegment, 'hats': AudioSegment}
```

**Example:**
```
from techno.generators.synth_generator import SynthGenerator

generator = SynthGenerator(bpm=130)

# Generate kick stem
kick_stem = generator.generate_stem('kick', duration_bars=8, style='industrial')
kick_stem.export("kick_stem.wav", format="wav")

# Generate all stems
stems = generator.generate_all_stems(duration_bars=8, style='minimal')
stems['kick'].export("kick.wav", format="wav")
stems['bass'].export("bass.wav", format="wav")
stems['hats'].export("hats.wav", format="wav")
```

---

## Type Hints

All functions support type hints for better IDE integration:

```
from pydub import AudioSegment
from techno.core.primitives import Kick

kick: Kick = Kick(bpm=130)
audio: AudioSegment = kick.generate()
duration: int = len(audio)  # milliseconds
```

---

## Error Handling

Common exceptions:

```
# ValueError: Invalid BPM
kick = Kick(bpm=9999)  # Raises ValueError

# ValueError: Invalid frequency
bass = Bass(bpm=130)
bass.generate_note(frequency=-100)  # Raises ValueError

# FileNotFoundError: FFmpeg not installed
audio.export("output.wav", format="wav")  # Raises if FFmpeg missing
```

---

## Further Reading

- [EXAMPLES.md](EXAMPLES.md) - Practical examples
- [README.md](README.md) - Quick start guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide

---

**Questions?** [Open an issue](https://github.com/TataSatyaPratheek/techno/issues) 🎵
