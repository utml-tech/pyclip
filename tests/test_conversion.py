"""Conversion operation tests

References: 
    - https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save

"""

from pyclip import Video
import tempfile

import pytest

@pytest.mark.parametrize("file_format", [("mp4"), ("avi")])
def test_video_conversion(mock_video: Video, file_format: str):
    with tempfile.NamedTemporaryFile(suffix=f".{file_format}") as f:
        mock_video.save(f.name, format=file_format.upper())
        assert Video.open(f.name) == mock_video