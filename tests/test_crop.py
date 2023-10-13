import src as pyclip
import os
from .core.video import Video

def crop(self, mock_video: pyclip.Video, left: int, upper: int, right: int, lower: int) -> Video:

    # Check if the input video is opened
    assert mock_video.isOpened(), f"Unable to open video file: {mock_video.file_path}"
    
    # Ensure that left, upper, right, and lower are integers
    assert isinstance(left, int), "left must be an integer."
    assert isinstance(upper, int), "upper must be an integer."
    assert isinstance(right, int), "right must be an integer."
    assert isinstance(lower, int), "lower must be an integer."

    # get video details
    frame_width = int(mock_video.getWidth())
    frame_height = int(mock_video.getHeight())

    # calculate the dimensions of the cropped region
    new_width = right - left
    new_height = lower - upper


    # make assertions about the crop dimensions
    assert new_width > 0, "Crop width must be greater than 0."
    assert new_height > 0, "Crop height must be greater than 0."
    assert left >= 0, "Left position must be non-negative."
    assert upper >= 0, "Upper position must be non-negative."
    assert right <= frame_width, "Right position must be within the video width."
    assert lower <= frame_height, "Lower position must be within the video height."


    output = mock_video.save(crop=[left, upper, right, lower])

    return output




