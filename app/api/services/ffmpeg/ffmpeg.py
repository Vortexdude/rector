from pathlib import Path


class BaseFFMpeg:
    AUDIO_EXTENSIONS = ['.mp3', '.wav']
    VIDEO_EXTENSIONS = ['.mp4', '.mov', '.flv', '.avi']

    def __init__(self, force=True):
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

    @staticmethod
    def _validator(file: Path, exists: bool = True):
        if exists:
            if not file.is_file():
                raise Exception(f"file not exists {file}")

        if file.is_file() and not exists:
            raise Exception(f"output {file} already exists")

    def reverse_video(self):
        self.cmd.extend(['-vf', 'reverse'])

    def reverse_audio(self):
        self.cmd.extend(['-af', 'areverse'])
