"""
Test timing calculations (critical for bar alignment)
"""

import pytest

from ..core.timing import MusicalTime, TimingCalculator


class TestMusicalTime:
    """Test MusicalTime dataclass"""

    def test_to_beats(self):
        """Test conversion to beats"""
        time = MusicalTime(bars=2, beats=1, sixteenths=4)
        assert time.to_beats() == 2 * 4 + 1 + 4 / 4  # 10.0 beats

    def test_to_ms_at_120_bpm(self):
        """Test millisecond conversion at 120 BPM"""
        time = MusicalTime(bars=1, beats=0, sixteenths=0)
        ms = time.to_ms(bpm=120)
        expected = (60 / 120) * 1000 * 4  # 2000ms (1 bar at 120 BPM)
        assert ms == expected


class TestTimingCalculator:
    """Test timing calculator"""

    def test_init_defaults(self):
        """Test initialization with defaults"""
        calc = TimingCalculator(bpm=130)
        assert calc.bpm == 130
        assert calc.beats_per_bar == 4
        assert pytest.approx(calc.ms_per_beat, rel=1e-2) == (60 / 130) * 1000

    def test_bars_to_ms(self):
        """Test bars to milliseconds conversion"""
        calc = TimingCalculator(bpm=120)
        ms = calc.bars_to_ms(1)
        assert ms == 2000  # 1 bar at 120 BPM = 2000ms

        ms = calc.bars_to_ms(8)
        assert ms == 16000  # 8 bars

    def test_ms_to_bars(self):
        """Test milliseconds to bars conversion"""
        calc = TimingCalculator(bpm=120)
        bars = calc.ms_to_bars(2000)
        assert bars == 1.0

        bars = calc.ms_to_bars(16000)
        assert bars == 8.0

    def test_nearest_bar_snapping(self):
        """Test snapping to nearest bar"""
        calc = TimingCalculator(bpm=120)

        # 1900ms should snap to 2000ms (1 bar)
        snapped = calc.nearest_bar(1900)
        assert snapped == 2000

        # 2100ms should also snap to 2000ms
        snapped = calc.nearest_bar(2100)
        assert snapped == 2000

    def test_create_grid(self):
        """Test grid generation"""
        calc = TimingCalculator(bpm=120)
        grid = calc.create_grid(total_bars=1, subdivision=16)

        assert len(grid) == 16  # 16 divisions per bar
        assert grid[0] == 0  # First position
        assert grid[-1] == pytest.approx(calc.ms_per_bar * 15 / 16, rel=1e-2)

    def test_different_bpm(self):
        """Test with different BPM"""
        calc_fast = TimingCalculator(bpm=140)
        calc_slow = TimingCalculator(bpm=100)

        # Same bars, different ms
        fast_ms = calc_fast.bars_to_ms(1)
        slow_ms = calc_slow.bars_to_ms(1)

        assert fast_ms < slow_ms  # Faster BPM = shorter bar duration
