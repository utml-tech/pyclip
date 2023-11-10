from typing_extensions import Self

from typing import Any, Union, Optional
from pydantic import BaseModel, NonNegativeFloat, field_validator, model_validator, validator
from ..utils.enums import TimeUnits
from ..core import Video

class Trim(BaseModel):
    """Class to trim a video based on specified start, end times, and a step value, with a given unit (either frames or milliseconds)."""
    
    start: NonNegativeFloat
    end: Optional[NonNegativeFloat] = None
    step: Optional[NonNegativeFloat] = None  # Default step is 1 to get every frame or millisecond.
    unit: TimeUnits = TimeUnits.milliseconds

    @model_validator(mode='after')
    def validate_end_not_before_start(self) -> Self:
        """Ensures that end is not before start."""
        if self.end is not None and self.end < self.start:
            raise ValueError("End time cannot be before start time.")
        return self
    
    def _convert_to_frames(self, video: Video, value: int | None) -> int | None:
        """
        Converts a time in milliseconds or a frame count to a frame count based on the unit.

        Args:
            video (Video): The video from which frame rate is obtained.
            value (NonNegativeFloat): The value to be converted.

        Returns:
            int: The value converted to frames.
        """
        if value is not None:
            return int(value) if self.unit == TimeUnits.frame else int(value * video.fps // 1000)

    def _compute_indices(self, video: Video, start: int, end: Optional[int], step: Optional[int]) -> tuple[tuple[int, Optional[int]], tuple[int, Optional[int]]]:
        """
        Computes the starting and ending indices for the video clip and audio segment.

        Args:
            video (Video): The video from which indices are being computed.
            start (int): The starting index.
            end (Optional[int]): The ending index.
            step (Optional[int]): The step size.

        Returns:
            Tuple[Tuple[int, Optional[int]], Tuple[int, Optional[int]]]: The video and audio indices.
        """
        audio_start = int((start / video.fps) * video.sampling_rate)
        audio_end = int((end / video.fps) * video.sampling_rate) if end is not None else None
        return slice(start, end, step), slice(audio_start, audio_end, step)

    def __call__(self, video: Video) -> Video:
        """
        Trims the video based on the specified unit (frames or milliseconds).

        Args:
            video (Video): The video to be trimmed.

        Returns:
            Video: The trimmed video.
        """
        start, end, step = map(lambda x: self._convert_to_frames(video, x), (self.start, self.end, self.step))
        video_slice, audio_slice = self._compute_indices(video, start, end, step)
        return Video(clip=video.clip[video_slice], fps=video.fps, audio=video.audio[audio_slice], sampling_rate=video.sampling_rate)
