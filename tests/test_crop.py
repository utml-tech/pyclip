import src as pyclip
from moviepy.editor import VideoFileClip
import os

def check_file_extension(file_path, allowed_extensions):
    """
    Assert that a file has one of the specified allowed extensions.

    Args:
    - file_path (str): The path to the file to check.
    - allowed_extensions (list): A list of allowed file extensions (e.g., ['.gif', '.mp4', '.webm']).

    Raises:
    - AssertionError: If the file does not have an allowed extension.
    """
    assert os.path.isfile(file_path), f"'{file_path}' is not a valid file path."

    # get the file extension (including the dot) from the file path
    _, file_extension = os.path.splitext(file_path)

    # check if the file extension is in the list of allowed extensions
    assert file_extension in allowed_extensions, f"'{file_path}' has an invalid file extension."


def assert_and_crop_video_dimensions(input_file, output_file, width, height):
    check_file_extension(input_file, ['.gif', '.mp4', '.webm'])
    
    # Check if the input file is a video file (MP4, GIF, or WebM)
    _, ext = os.path.splitext(input_file)
    assert ext in ['.mp4', '.gif', '.webm'], f"'{input_file}' is not a supported video format."

    # Use moviepy to crop video dimensions
    try:
        clip = VideoFileClip(input_file)
        cropped_clip = clip.crop(x1=0, y1=0, x2=width, y2=height)
        cropped_clip.write_videofile(output_file, codec='libx264')
        print(f"'{input_file}' cropped to {width}x{height} and saved as '{output_file}'.")
    except Exception as e:
        print(f'Error cropping video dimensions: {str(e)}')