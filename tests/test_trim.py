import src as pyclip

import pytest

def test_sanity():
    assert 1 == 1

@pytest.fixture
def mock_video():
    return pyclip.RandomVideo()

def test_trim(mock_video):
    video = mock_video.trim(50, 1000)
    assert video.duration == 950

def test_trim_by_frames(mock_video):
    assert mock_video.trim(50, 100, unit="f") == mock_video[50:100]

def test_trim_negative(mock_video):
    with pytest.raises(ValueError):
        mock_video.trim(-100, 1000, unit="f")

