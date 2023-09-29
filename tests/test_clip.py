import src as pyclip

import pytest

def test_sanity():
    assert 1 == 1

@pytest.fixture
def mock_video():
    return pyclip.RandomVideo()

def test_trim(mock_video):
    video = mock_video.trim(50, 1000, unit="ms")
    assert video.duration == 950

