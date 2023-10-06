from __future__ import annotations

class Model:
    pass

class Video(Model):

    def trim(self, t_start: float, t_end: float | None = None, unit: str = "s") -> Video:
        """
        Returns a clip playing the content of the current clip
        between times ``t_start`` and ``t_end``
        """
        ...

    def mute(self, channels: int | list[int] | None = None):
        ...

    def resize(self, **kwargs):
        ...

    def upscale(self, **kwargs):
        ...