from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from ..utils.enums import TimeUnits
from ..core import Video


class Equality:

    def __call__(self, *videos: Video) -> bool:
        if any(not isinstance(video, Video) for video in videos):
            return False

        return all(self._is_equal(videos[0], video) for video in videos)
    
    def _is_equal(self, video1: Video, video2: Video) -> bool:
        return video1.clip.eq(video2.clip).all() and video1.fps == video2.fps and video1.audio.eq(video2.audio).all() and video1.sampling_rate == video2.sampling_rate