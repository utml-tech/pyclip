
class Video(Model):

    def trim(self):
        ...

    def mute(self, channels: int | list[int] | None = None):
        ...

    def resize(self, **kwargs):
        ...

    def upscale(self, **kwargs):
        ...