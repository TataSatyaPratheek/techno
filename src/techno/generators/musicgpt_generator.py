"""
MusicGPT wrapper for stem generation
Alternative to pure synthesis
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional

from pydub import AudioSegment


class MusicGPTGenerator:
    """Generate stems using MusicGPT"""

    def __init__(self, model: str = "small"):
        self.model = model

    def generate_stem(self, prompt: str, duration: int, output_path: Path) -> Optional[AudioSegment]:
        """
        Generate single stem with MusicGPT

        Args:
            prompt: Text prompt for generation
            duration: Duration in seconds
            output_path: Where to save
        """
        cmd = [
            "musicgpt",
            prompt,
            "--secs",
            str(duration),
            "--model",
            self.model,
            "--output",
            str(output_path),
            "--no-playback",
            "--no-interactive",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

            if result.returncode == 0 and output_path.exists():
                return AudioSegment.from_wav(output_path)
            else:
                print(f"MusicGPT failed: {result.stderr}")
                return None

        except FileNotFoundError:
            print("MusicGPT not found. Using synthesis instead.")
            return None
        except subprocess.TimeoutExpired:
            print("MusicGPT timed out")
            return None

    def generate_all_stems(self, prompts: Dict[str, str], duration: int, output_dir: Path) -> Dict[str, AudioSegment]:
        """Generate all stems from prompts"""
        output_dir.mkdir(parents=True, exist_ok=True)

        stems = {}
        for stem_name, prompt in prompts.items():
            output_path = output_dir / f"{stem_name}.wav"

            print(f"Generating {stem_name}...")
            audio = self.generate_stem(prompt, duration, output_path)

            if audio:
                stems[stem_name] = audio

        return stems
