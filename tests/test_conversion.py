"""Conversion operation tests

References: 
    - https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save

"""

from pyclip import Video
import tempfile

def test_convert_to_mp4(mock_video: Video):
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        mock_video.save(f.name)

    assert Video.from_file(f.name) == mock_video