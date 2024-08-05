from pathlib import Path


class BaseFFMpeg:
    """
    Base class for handling FFMpeg operations.

    Attributes:
        AUDIO_EXTENSIONS (list): Supported audio file extensions.
        VIDEO_EXTENSIONS (list): Supported video file extensions.
        force (bool): Flag to force overwriting files.
        cmd (list): List of FFMpeg command arguments.
        _input_file_name (Path): Path to the input file.
        _output_file_name (Path): Path to the output file.
    """

    AUDIO_EXTENSIONS = ['.mp3', '.wav']
    VIDEO_EXTENSIONS = ['.mp4', '.mov', '.flv', '.avi']

    def __init__(self, force=True):
        """
        Initializes the BaseFFMpeg class.

        Args:
            force (bool): Flag to force overwriting files. Defaults to True.
        """
        self.force: bool = force
        self.cmd = ['ffmpeg']
        self._input_file_name: Path = Path()
        self._output_file_name = Path()
        self._video_codec = ['-c:v']
        self._video_bit_rate = ['-b:v']
        self._video_buffer_size = ['-bufsize:v']
        self._max_video_bit_rate = ['-maxrate:v']
        self._audio_codec = ['-c:a']
        self._audio_bitrate = ['-b:a']

    @property
    def input_file_name(self) -> Path:
        return self._input_file_name

    @property
    def output_file_name(self) -> Path:
        return Path(self._output_file_name)

    @input_file_name.setter
    def input_file_name(self, value) -> None:
        if not isinstance(value, Path):
            value = Path(value)
        self._validator(value, exists=True)
        self._input_file_name = value
        self.cmd.extend(["-i", str(value.resolve())])

    @output_file_name.setter
    def output_file_name(self, value) -> None:
        if not isinstance(value, Path):
            value = Path(value)

        self._validator(value, exists=False)
        self._output_file_name = value

    @property
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value):
        """please validate the value first"""
        self._video_codec.append(value)

    @property
    def video_bit_rate(self):
        return self._video_bit_rate

    @video_bit_rate.setter
    def video_bit_rate(self, value):
        """please validate the value first"""
        self._video_bit_rate.append(value)

    @property
    def video_buffer_size(self):
        return self._video_buffer_size

    @video_buffer_size.setter
    def video_buffer_size(self, value):
        """please validate the value first"""
        self._video_buffer_size.append(value)

    @property
    def max_video_bit_rate(self):
        return self._max_video_bit_rate

    @max_video_bit_rate.setter
    def max_video_bit_rate(self, value):
        """please validate the value first"""
        self._max_video_bit_rate.append(value)

    @property
    def audio_bitrate(self):
        return self._audio_bitrate

    @audio_bitrate.setter
    def audio_bitrate(self, value):
        """validate the data here"""
        self._audio_bitrate.append(value)

    @property
    def audio_codec(self):
        return self._audio_codec

    @audio_codec.setter
    def audio_codec(self, value):
        self._audio_codec.append(value)

    @staticmethod
    def _validator(file: Path, exists: bool = True):
        """
        check for input should be existed and output file should not.
        Validates the existence or non-existence of a file.

        Args:
            file (Path): The file to validate.
            exists (bool): Whether the file should exist. Defaults to True.

        Raises:
            Exception: If the file existence does not match the expected condition.
        """
        if exists:
            if not file.is_file():
                raise Exception(f"file not exists {file}")

        if file.is_file() and not exists:
            raise Exception(f"output {file} already exists")
