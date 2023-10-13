"""Tests for the rotate and flip methods of the Video class.

References:
    - https://kornia.readthedocs.io/en/latest/geometry.transform.html#kornia.geometry.transform.rotate

"""

import pyclip
import pytest

def test_rotate_90_degrees(mock_video: pyclip.Video):
    """Test rotating a video 90 degrees counter-clockwise."""
    rotated = mock_video.rotate(90)
    assert rotated.width == mock_video.height
    assert rotated.height == mock_video.width

def test_rotate_with_center(mock_video: pyclip.Video):
    """Test rotating a video about a specific center."""
    center = [mock_video.width // 2, mock_video.height // 2]
    assert mock_video.rotate(45, center=center) == mock_video.rotate(45)

def test_rotate_with_non_centered_axis(mock_video: pyclip.Video):
    """Test rotating a video about a specific axis."""
    rotated = mock_video.rotate(45, center=[0, 0])

def test_rotate_180_degrees(mock_video: pyclip.Video):
    """Test rotating a video 180 degrees counter-clockwise and checking its properties."""
    assert mock_video.rotate(180) == mock_video.flipv()

def test_rotate_360_degrees(mock_video: pyclip.Video):
    """Test rotating a video 360 degrees should be equal to the original."""
    assert mock_video.rotate(360) == mock_video

def test_rotate_with_interpolation(mock_video: pyclip.Video):
    """Test rotating a video with a specific interpolation."""
    rotated_bilinear = mock_video.rotate(45, mode='bilinear')
    rotated_nearest = mock_video.rotate(45, mode='nearest')

    assert rotated_bilinear != rotated_nearest
    assert rotated_bilinear.is_close(rotated_nearest)

def test_rotate_with_padding_mode(mock_video: pyclip.Video):
    """Test rotating a video with different padding modes."""
    rotated_zeros = mock_video.rotate(45, padding_mode='zeros')
    rotated_border = mock_video.rotate(45, padding_mode='border')
    rotated_reflection = mock_video.rotate(45, padding_mode='reflection')
    
    # Assuming Video class has a method to compare video content, e.g., is_close()
    assert not rotated_zeros.is_close(rotated_border)
    assert not rotated_zeros.is_close(rotated_reflection)
    assert not rotated_border.is_close(rotated_reflection)

def test_rotate_audio_sync(mock_video: pyclip.Video):
    """Test audio synchronization after rotation."""
    rotated = mock_video.rotate(45)
    assert rotated.audio == mock_video.audio

def test_rotate_invalid_angle(mock_video: pyclip.Video):
    """Test rotating with an invalid angle type should raise a TypeError."""
    with pytest.raises(TypeError):
        mock_video.rotate("invalid_angle")

def test_rotate_invalid_interpolation(mock_video: pyclip.Video):
    """Test rotating with an invalid interpolation mode should raise a ValueError."""
    with pytest.raises(ValueError):
        mock_video.rotate(45, mode='invalid_mode')

def test_rotate_invalid_padding_mode(mock_video: pyclip.Video):
    """Test rotating with an invalid padding mode should raise a ValueError."""
    with pytest.raises(ValueError):
        mock_video.rotate(45, padding_mode='invalid_padding')

def test_rotate_invalid_center(mock_video: pyclip.Video):
    """Test rotating with an invalid center type should raise a TypeError."""
    with pytest.raises(TypeError):
        mock_video.rotate(45, center="invalid_center")
