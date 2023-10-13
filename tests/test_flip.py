"""Tests for the rotate and flip methods of the Video class.

References:
    - https://kornia.readthedocs.io/en/latest/geometry.transform.html#kornia.geometry.transform.hflip
    - https://kornia.readthedocs.io/en/latest/geometry.transform.html#kornia.geometry.transform.vflip

"""

import pyclip
import pytest

def test_flip_horizontal(mock_video: pyclip.Video):
    """Test flipping a video horizontally."""
    flipped_once = mock_video.fliph()
    assert flipped_once != mock_video

    flipped_twice = flipped_once.fliph()
    assert flipped_twice == mock_video

def test_flip_vertical(mock_video: pyclip.Video):
    """Test flipping a video vertically."""
    flipped_once = mock_video.flipv()
    assert flipped_once != mock_video

    flipped_twice = flipped_once.flipv()
    assert flipped_twice == mock_video

def test_flip_both(mock_video: pyclip.Video):
    """Test flipping a video both horizontally and vertically."""
    assert mock_video.flip(horizontal=True, vertical=True) == mock_video.flipv().fliph() == mock_video.fliph().flipv()

def test_flip_without_args(mock_video: pyclip.Video):
    """Test flipping without any arguments should raise a ValueError."""
    with pytest.raises(ValueError):
        mock_video.flip()

def test_flip_audio_sync(mock_video: pyclip.Video):
    """Test audio synchronization after flipping."""
    flipped = mock_video.fliph()
    assert flipped.audio == mock_video.audio

def test_flip_horizontal_and_vertical(mock_video: pyclip.Video):
    """Test flipping a video horizontally and then vertically should equal flipping both at once."""
    flipped_sequentially = mock_video.fliph().flipv()
    flipped_simultaneously = mock_video.flip(horizontal=True, vertical=True)
    assert flipped_sequentially == flipped_simultaneously

def test_flip_vertical_audio_sync(mock_video: pyclip.Video):
    """Test audio synchronization after vertical flipping."""
    flipped = mock_video.flipv()
    assert flipped.audio == mock_video.audio

def test_flip_invalid_arguments(mock_video: pyclip.Video):
    """Test flipping with an invalid argument type should raise a TypeError."""
    with pytest.raises(TypeError):
        mock_video.flip(horizontal="True", vertical=True)

def test_fliph_method_vs_flip_function(mock_video: pyclip.Video):
    """Test equivalence of fliph method vs flip function with horizontal=True."""
    assert mock_video.fliph() == mock_video.flip(horizontal=True)

def test_flipv_method_vs_flip_function(mock_video: pyclip.Video):
    """Test equivalence of flipv method vs flip function with vertical=True."""
    assert mock_video.flipv() == mock_video.flip(vertical=True)

def test_flip_with_both_false(mock_video: pyclip.Video):
    """Test flipping with both horizontal and vertical set to False should return the original."""
    assert mock_video.flip(horizontal=False, vertical=False) == mock_video

def test_flip_idempotence(mock_video: pyclip.Video):
    """Test that flipping twice in any direction should return the original video."""
    assert mock_video.flip(horizontal=True, vertical=True).flip(horizontal=True, vertical=True) == mock_video.fliph().fliph() == mock_video.flipv().flipv() == mock_video

def test_flip_chain_operations(mock_video: pyclip.Video):
    """Test chaining multiple flip operations."""
    result = mock_video.fliph().flipv().fliph()
    assert result == mock_video.flipv()

def test_flip_no_audio(mock_video: pyclip.Video):
    """Test flipping a video with no audio."""
    # Assuming the Video class has a method to remove audio
    video_no_audio = mock_video.remove_audio()
    flipped = video_no_audio.fliph()
    assert flipped.audio is None
