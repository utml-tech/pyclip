from __future__ import annotations
import math

from pathlib import Path
from torch import Tensor
import torch


class Video:

    def __init__(self, clip: Tensor, fps: float, audio: Tensor | None = None, sampling_rate: int | None = None) -> None:
        self.clip = clip
        self.audio = audio

        self.fps = fps
        self.sampling_rate = sampling_rate

    @classmethod
    def rand(cls):
        fps = 30
        sample_rate = 44100

        F, C, H, W = 120, 3, 170, 200
        
        S = math.floor(F/fps * sample_rate)
        K = 2

        random_clip = torch.rand([F, C, H, W])
        random_audio = torch.rand([S, K])

        return cls(clip=random_clip, fps=fps, audio=random_audio, sampling_rate=sample_rate)

    @property
    def duration(self) -> float:
        """Returns the duration of the video in seconds."""
        num_frames = self.clip.shape[0]
        return num_frames / self.fps

    @property
    def width(self) -> int:
        return None

    def trim(self, start: float, end: float | None = None, unit: str = "ms") -> Video:
        """
        Returns a clip playing the content of the current clip
        between times `start` and `end`
        """
        from ..operations import Trim

        op = Trim(start, end, unit)
        return op(self)

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

    