from pathlib import Path


class BaseFFMpeg:
    """
    Base class for handling FFMpeg operations.

    Attributes:
        AUDIO_EXTENSIONS (list): Supported audio file extensions.
        VIDEO_EXTENSIONS (list): Supported video file extensions.
        force (bool): Flag to force overwriting files.
        cmd (list): List of FFMpeg command arguments.
        _a_codec_name (str): Audio codec name.
        _v_codec_name (str): Video codec name.
        a_codecs (list): List of supported audio codecs.
        v_codecs (list): List of supported video codecs.
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
        self._a_codec_name: str = ""
        self._v_codec_name: str = ""
        self.a_codecs: list = ["libshine", ]
        self.v_codecs: list = ["libx264", ]
        self._input_file_name: Path = Path()
        self._output_file_name = Path()

    @property
    def input_file_name(self) -> Path:
        """
        Gets the input file name.

        Returns:
            Path: The input file name.
        """
        return self._input_file_name

    @property
    def output_file_name(self) -> Path:
        """
        Gets the output file name.

        Returns:
            Path: The output file name.
        """
        return Path(self._output_file_name)

    @input_file_name.setter
    def input_file_name(self, value) -> None:
        """
        Sets the input file name and validates its existence.

        Args:
            value (str or Path): The input file name.

        Raises:
            Exception: If the file does not exist.
        """
        if not isinstance(value, Path):
            value = Path(value)
        self._validator(value, exists=True)
        self._input_file_name = value
        self.cmd.extend(["-i", str(value.resolve())])

    @output_file_name.setter
    def output_file_name(self, value) -> None:
        """
        Sets the output file name and validates that it does not already exist.

        Args:
            value (str or Path): The output file name.

        Raises:
            Exception: If the file already exists.
        """
        if not isinstance(value, Path):
            value = Path(value)

        self._validator(value, exists=False)
        self._output_file_name = value

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

    def reverse_video(self):
        """
        Adds a command to reverse the video stream.
        """
        self.cmd.extend(['-vf', 'reverse'])

    def reverse_audio(self):
        """
        Adds a command to reverse the audio stream.
        """
        self.cmd.extend(['-af', 'areverse'])
