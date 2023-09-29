import src as pyclip

import pytest

def test_video_resize(mock_video):
    video = mock_video.resize(640, 480)
    assert video.size == (640, 480)

def test_video_upscale(mock_video):
    video = mock_video.upscale(2, model="vapoursynth")
    assert video.size == 2 * mock_video.size

def test_other_interface(mock_video):
    transforms = [
        Upscale(2, model="vapoursynth"),
        Resize(640, 480)
    ]

    video = mock_video.apply(transforms)

    assert video.size == (640, 480)