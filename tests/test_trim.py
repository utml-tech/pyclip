"""
Tests for the trim method of the Video class.

References:
    - https://zulko.github.io/moviepy/ref/Clip.html?highlight=subclip#moviepy.Clip.Clip.subclip

"""

import pyclip
from pyclip import Trim

import pytest

def test_trim(mock_video: pyclip.Video):
    """Test trimming a video using seconds as unit."""
    video = mock_video.trim(50, 1000)
    assert video.duration == 950

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
        Trim(50, 100, unit="f")
    ]

    assert mock_video.apply(transforms) == mock_video.trim(50, 100, unit="f")

def test_trim_start_greater_than_end(mock_video: pyclip.Video):
    """Test trimming with start time greater than end time raises a ValueError."""
    with pytest.raises(ValueError):
        mock_video.trim(1000, 100)

def test_trim_exceed_duration(mock_video: pyclip.Video):
    """Test trimming with time range exceeding video duration raises an IndexError."""
    with pytest.raises(IndexError):
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
