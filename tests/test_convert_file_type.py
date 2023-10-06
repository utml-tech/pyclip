import src as pyclip
import os
import pytest
import subprocess
from PIL import Image

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


# convert file to mp4
def assert_and_convert_to_mp4(input_file, output_file):
    check_file_extension(input_file, ['.gif', '.mp4', '.webm'])
    
    # check if the input file is already in MP4 format
    _, ext = os.path.splitext(input_file)
    if ext == '.mp4':
        print(f"'{input_file}' is already in MP4 format.")
    else:
        # convert to MP4 using ffmpeg
        try:
            subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'aac', '-strict', 'experimental', output_file])
            print(f"'{input_file}' converted to MP4: {output_file}")
        except Exception as e:
            print(f'Error converting to MP4: {str(e)}')

# convert file to gif
def assert_and_convert_to_gif(input_file, output_file):
    check_file_extension(input_file, ['.gif', '.mp4', '.webm'])
    
    # check if the input file is already in gif format
    _, ext = os.path.splitext(input_file)
    if ext == '.gif':
        print(f"'{input_file}' is already in GIF format.")
    else:
        # convert to GIF using pillow
        try:
            with Image.open(input_file) as im:
                im.save(output_file, 'gif')
            print(f"'{input_file}' converted to GIF: {output_file}")
        except Exception as e:
            print(f'Error converting to GIF: {str(e)}')

# convert file to webm
def assert_and_convert_to_webm(input_file, output_file):
    check_file_extension(input_file, ['.gif', '.mp4', '.webm'])
    
    # check if the input file is already in webm format
    _, ext = os.path.splitext(input_file)
    if ext == '.webm':
        print(f"'{input_file}' is already in WebM format.")
    else:
        # convert to webm using ffmpeg
        try:
            subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis', output_file])
            print(f"'{input_file}' converted to WebM: {output_file}")
        except Exception as e:
            print(f'Error converting to WebM: {str(e)}')