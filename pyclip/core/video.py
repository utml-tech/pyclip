from __future__ import annotations

class Model:
    pass

class Video(Model):

    def trim(self, start: float, end: float | None = None, unit: str = "ms") -> Video:
        """
        Returns a clip playing the content of the current clip
        between times `start` and `end`
        """
        ...

    def mute(self, channels: int | list[int] | None = None):
        ...

    def resize(self, **kwargs):
        ...

    def upscale(self, **kwargs):
        ...

    def rand(self):
        ...

    def save(self, path: str | Path):
        ...