

class Audio:
    def __init__(self):
        self._audio_codec: list = ['-c:a']
        self._audio_bitrate: list = ['-b:a']

    @property
    def audio_codec(self):
        return self._audio_codec

    @audio_codec.setter
    def audio_codec(self, value):
        self._audio_codec.append(value)

    @property
    def audio_bitrate(self):
        return self._audio_bitrate

    @audio_bitrate.setter
    def audio_bitrate(self, value):
        self._audio_bitrate.append(value)


class Video:

    def __init__(self):
        self._video_codec = ['-c:v']
        self._video_bit_rate = ['-b:v']
        self._video_buffer_size = ['-bufsize:v']
        self._max_video_bit_rate = ['-maxrate:v']

    @property
    def video_codec(self):
        return self._video_codec

    @property
    def video_bit_rate(self):
        return self._video_bit_rate

    @property
    def video_buffer_size(self):
        return self._video_buffer_size

    @property
    def max_video_bit_rate(self):
        return self._max_video_bit_rate

    @video_codec.setter
    def video_codec(self, value):
        """please validate the value first"""
        self._video_codec.append(value)

    @video_bit_rate.setter
    def video_bit_rate(self, value):
        """please validate the value first"""
        self._video_bit_rate.append(value)

    @video_buffer_size.setter
    def video_buffer_size(self, value):
        """please validate the value first"""
        self._video_buffer_size.append(value)

    @max_video_bit_rate.setter
    def max_video_bit_rate(self, value):
        """please validate the value first"""
        self._max_video_bit_rate.append(value)
