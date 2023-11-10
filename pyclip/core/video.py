from __future__ import annotations
from functools import reduce
import math
import numbers

from pathlib import Path
from torch import Tensor
import torch

from ..utils.enums import TimeUnits

from pydantic import BaseModel, PositiveFloat


class Video(BaseModel, arbitrary_types_allowed=True):
    clip: Tensor
    fps: float
    audio: Tensor | None = None
    sampling_rate: int | None = None

    @classmethod
    def rand(cls):
        fps = 30
        sample_rate = 44100

        F, C, H, W = 120, 3, 170, 200
        
        SAMPLES = math.floor(F/fps * sample_rate)
        AUDIO_CHANNELS = 2

        random_clip = torch.rand([F, C, H, W])
        random_audio = torch.rand([SAMPLES, AUDIO_CHANNELS])

        return cls(clip=random_clip, fps=fps, audio=random_audio, sampling_rate=sample_rate)

    @property
    def duration(self) -> float:
        """Returns the duration of the video in milliseconds."""
        num_frames = self.clip.shape[0]
        return num_frames / self.fps * 1000

    @property
    def frames(self) -> int:
        return self.clip.shape[0]
    
    @property
    def channels(self) -> int:
        return self.clip.shape[1]
    
    @property
    def height(self) -> int:
        return self.clip.shape[2]

    @property
    def width(self) -> int:
        return self.clip.shape[3]

    def trim(self, start: float, end: float | None = None, step: float | None = None, unit: str = "ms") -> Video:
        """
        Returns a clip playing the content of the current clip
        between times `start` and `end`
        """
        from ..operations import Trim

        op = Trim(start=start, end=end, step=step, unit=unit)
        return op(self)
    
    def __getitem__(self, index: int | slice) -> Video:
        if isinstance(index, slice):
            return self.trim(start=index.start, end=index.stop, step=index.step, unit=TimeUnits.frame)
        elif isinstance(index, numbers.Integral):
            return self.trim(start=index, end=index+1, unit=TimeUnits.frame)
    
    def eq(self, other: Video) -> bool:
        from ..operations import Equality
        op = Equality()
        return op(self, other)
    
    def __eq__(self, other: object) -> bool:
        return self.eq(other)
    
    def apply(self, transforms: list[Video]) -> Video:
        return reduce(lambda video, op: op(video), transforms, self)

    def mute(self, channels: int | list[int] | None = None):
        return Video()

    def resize(self, **kwargs):
        return Video()

    def upscale(self, **kwargs):
        return Video()

    def open(self, path: str | Path):
        return Video()

    def save(self, path: str | Path):
        return Video()

    def __repr__(self) -> str:
        return f"Video(shape={list(self.clip.shape)}, fps={self.fps}, audio={list(self.audio.shape) if self.audio is not None else None}, sampling_rate={self.sampling_rate})"
    