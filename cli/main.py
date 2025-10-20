"""
Main CLI for techno production system
Single entry point for all operations
"""

from pathlib import Path

import click
import yaml

from ..mixers.industrial import IndustrialTechnoMixer
from ..mixers.minimal import MinimalTechnoMixer


@click.group()
def cli():
    """Techno Production System - Fundamentals-First Approach"""
    pass


@cli.command()
@click.option(
    "--subgenre", type=click.Choice(["minimal", "industrial", "dub"]), default="minimal"
)
@click.option("--bpm", type=int, default=None, help="Override default BPM")
@click.option("--output", type=str, default="output.wav", help="Output filename")
def generate(subgenre, bpm, output):
    """Generate techno track from scratch"""

    click.echo(f"🎵 Generating {subgenre} techno track...")

    # Load preset
    preset_path = Path(__file__).parent.parent / f"presets/{subgenre}_techno.yaml"
    with open(preset_path) as f:
        preset = yaml.safe_load(f)

    # Override BPM if specified
    if bpm:
        preset["bpm"] = bpm

    # Create mixer
    if subgenre == "minimal":
        mixer = MinimalTechnoMixer(bpm=preset["bpm"])
    elif subgenre == "industrial":
        mixer = IndustrialTechnoMixer(bpm=preset["bpm"])
    else:
        click.echo(f"❌ Subgenre {subgenre} not yet implemented")
        return

    # Generate track
    track = mixer.create_track()

    # Export
    output_path = Path(output)
    track.export(output_path, format="wav")

    click.echo(f"✅ Track saved to {output_path}")
    click.echo(f"   Duration: {len(track) / 1000:.1f}s")
    click.echo(f"   BPM: {preset['bpm']}")


@cli.command()
def list_presets():
    """List available presets"""

    presets_dir = Path(__file__).parent.parent / "presets"
    presets = list(presets_dir.glob("*.yaml"))

    click.echo("\n📁 Available presets:\n")

    for preset_path in presets:
        with open(preset_path) as f:
            data = yaml.safe_load(f)

        click.echo(f"  • {data['name']}")
        click.echo(f"    {data['description']}")
        click.echo(f"    BPM: {data['bpm']}\n")


@cli.command()
@click.argument("audio_file")
def analyze(audio_file):
    """Analyze frequency content of audio file"""

    from pydub import AudioSegment

    from core.frequency import analyze_frequency_content

    audio = AudioSegment.from_file(audio_file)

    click.echo(f"\n🔍 Analyzing {audio_file}...\n")

    results = analyze_frequency_content(audio)

    click.echo("Frequency distribution:")
    for band, percentage in results.items():
        bar = "█" * int(percentage / 2)
        click.echo(f"  {band:12} {bar:40} {percentage:.1f}%")


if __name__ == "__main__":
    cli()
