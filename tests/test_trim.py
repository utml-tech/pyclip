"""
Tests for the trim method of the Video class.

References:
    - https://zulko.github.io/moviepy/ref/Clip.html?highlight=subclip#moviepy.Clip.Clip.subclip

"""

import pyclip
from pyclip import Trim

import pytest

def test_trim_basic(mock_video: pyclip.Video):
    """Test trimming a video using seconds as unit."""
    video = mock_video.trim(50, 1000)
    pytest.approx(video.duration, 950)

def test_trim_by_frames(mock_video: pyclip.Video):
    """Test trimming a video using frames as unit."""
    assert mock_video.trim(50, 100, unit="f") == mock_video[50:100]

def test_trim_negative(mock_video: pyclip.Video):
    """Test trimming with negative start frame raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(-100, 1000, unit="f")

def test_trim_class_operation(mock_video: pyclip.Video):
    """Test using Trim class operation to trim a video."""
    transforms = [
        Trim(start=50, end=100, unit="f")
    ]

    assert mock_video.apply(transforms) == mock_video.trim(50, 100, unit="f")

def test_trim_start_greater_than_end(mock_video: pyclip.Video):
    """Test trimming with start time greater than end time raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(1000, 100)

def test_trim_exceed_duration(mock_video: pyclip.Video):
    """Test trimming with time range exceeding video duration raises an IndexError."""
    with pytest.raises(ValueError):
        mock_video.trim(0, mock_video.duration + 1000)

def test_trim_invalid_unit(mock_video: pyclip.Video):
    """Test trimming with invalid unit raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(0, 100, unit="z")

def test_trim_without_end(mock_video: pyclip.Video):
    """Test trimming without specifying end trims to the end of the video."""
    trimmed = mock_video.trim(50)
    expected_duration = mock_video.duration - 50
    pytest.approx(trimmed.duration, expected_duration)


def test_trim_with_step(mock_video: pyclip.Video):
    """Test trimming a video using a step. Trimming from 0ms to 1000ms with step=2 should halve the frames."""
    trimmed = mock_video.trim(0, 1000, step=mock_video.fps * 3)
    assert trimmed.duration == 500  # duration is halved
    assert trimmed.frames == mock_video.frames // 2 // (3 + 1)

def test_trim_with_step_larger_than_duration(mock_video: pyclip.Video):
    """Test trimming a video with a step larger than video duration returns a video with one frame."""
    assert mock_video.trim(0, 1000, step=5000).frames == 1

def test_trim_with_invalid_step(mock_video: pyclip.Video):
    """Test trimming a video with a negative step raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(0, 1000, step=-10)

def test_trim_with_step_zero(mock_video: pyclip.Video):
    """Test trimming a video with a step of zero raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(0, 1000, step=0)
