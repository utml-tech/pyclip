from enum import StrEnum
from typing import Any, TYPE_CHECKING

from ..core import Video

class TimeUnits(StrEnum):
    milliseconds = "ms"
    frame = "f"

class Trim:
    
    def __init__(self, start: float, end: float | None = None, unit: TimeUnits = "ms") -> None:
        self.start = start
        self.end = end
        self.unit = unit

    def __call__(self, video: Video) -> Video:
        match self.unit:
            case TimeUnits.milliseconds:
                return self._trim_milliseconds(video)
            case TimeUnits.frame:
                return self._trim_frames(video)
        
    def _trim_frames(self, video: Video) -> Any:
        new_video = video.clip[self.start:self.end]

        audio_start = (self.start // video.fps) * video.sampling_rate
        audio_end = (self.end // video.fps) * video.sampling_rate if self.end is not None else None
        
        new_audio = video.audio[audio_start:audio_end]

        return Video(new_video, video.fps, new_audio, video.sampling_rate)
    
    def _trim_milliseconds(self, video: Video) -> Any:
        start = self.start * video.fps // 1000
        end = self.end * video.fps // 1000 if self.end is not None else None

        new_video = video.clip[start:end]

        audio_start = (start // video.fps) * video.sampling_rate
        audio_end = (end // video.fps) * video.sampling_rate if self.end is not None else None
        
        new_audio = video.audio[audio_start:audio_end]

        return Video(new_video, video.fps, new_audio, video.sampling_rate)
