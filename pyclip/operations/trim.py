from typing import Any, Union, Optional
from pydantic import BaseModel, NonNegativeFloat, validator
from ..utils.enums import TimeUnits
from ..core import Video

class Trim(BaseModel):
    """Class to trim a video based on specified start, end times, and a step value, with a given unit (either frames or milliseconds)."""
    
    start: NonNegativeFloat
    end: Optional[NonNegativeFloat] = None
    step: Optional[NonNegativeFloat] = None  # Default step is 1 to get every frame or millisecond.
    unit: TimeUnits = TimeUnits.milliseconds

    @validator("end", pre=True, always=True) 
    def validate_end_not_before_start(cls, end: Optional[NonNegativeFloat], values: dict) -> Optional[NonNegativeFloat]:
        """Ensures that end is not before start."""
        if end is not None and "start" in values and end < values["start"]:
            raise ValueError("End time cannot be before start time.")
        return end

    def __call__(self, video: Video) -> Video:
        """Trims the video based on the unit specified (frames or milliseconds)."""
        match self.unit:
            case TimeUnits.milliseconds:
                return self._trim_milliseconds(video)
            case TimeUnits.frame:
                return self._trim_frames(video)

    def _compute_audio_indices(self, video: Video, start_frame: int, end_frame: Optional[int]) -> tuple[int, int]:
        """Computes the starting and ending indices for the audio segment corresponding to the trimmed video."""
        audio_start = int((start_frame / video.fps) * video.sampling_rate)
        audio_end = int((end_frame / video.fps) * video.sampling_rate) if end_frame is not None else None
        return audio_start, audio_end

    def _trim_frames(self, video: Video) -> Video:
        """Trims the video based on frame indices."""
        start_frame = int(self.start)
        end_frame = int(self.end) if self.end is not None else None
        step = int(self.step) if self.step is not None else None

        new_video = video.clip[start_frame:end_frame:step]
        audio_start, audio_end = self._compute_audio_indices(video, start_frame, end_frame)
        
        new_audio = video.audio[audio_start:audio_end:step]

        return Video(clip=new_video, fps=video.fps, audio=new_audio, sampling_rate=video.sampling_rate)

    def _trim_milliseconds(self, video: Video) -> Video:
        """Trims the video based on time in milliseconds."""
        start_frame = int(self.start * video.fps // 1000)
        end_frame = int(self.end * video.fps // 1000) if self.end is not None else None
        step = int(self.step * video.fps // 1000) if self.step is not None else None
        step = None if step and step <= 1 else step
        
        new_video = video.clip[start_frame:end_frame:step]
        audio_start, audio_end = self._compute_audio_indices(video, start_frame, end_frame)
        
        new_audio = video.audio[audio_start:audio_end:step]

        return Video(clip=new_video, fps=video.fps, audio=new_audio, sampling_rate=video.sampling_rate)
