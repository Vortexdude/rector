import subprocess
from pathlib import Path
from os import path, remove
from app.api.services.ffmpeg import resolutions
from concurrent.futures import ProcessPoolExecutor
from app.api.services.ffmpeg.ffmpeg import BaseFFMpeg
from app.api.services.ffmpeg.models import RESOLUTION_MAPPING


class Multiplexer(BaseFFMpeg):
    """
    Class for handling FFMpeg multiplexing operations, inheriting from BaseFFMpeg.

    This class provides functionality to transcode videos to different resolutions,
    scale videos, and execute FFMpeg commands. It supports handling audio and video
    codecs, and can run in debug mode to suppress logging output.

    Attributes:
        debug (bool): Flag to enable debug mode. When set to True, detailed logging
                      output is shown. Defaults to False.

    Methods:
        scale(resolution):
            Adds a scale filter to the FFMpeg command to resize the video to the specified resolution.

        run():
            Executes the FFMpeg command and prints the output, errors, and return code.

        transcode(resolution_list):
            Transcodes the video to multiple resolutions using multiprocessing. This method
            takes a list of resolution names and processes each resolution in parallel.

        _process_res(resolution):
            Helper method to process the given resolution by scaling and running the FFMpeg command.
            This method is used internally by the transcode method.
    """

    def __init__(self, debug=False):
        """
        Initializes the Multiplexer class.

        Args:
            debug (bool): Flag to enable debug mode. When set to True, detailed logging
                          output is shown. Defaults to False.
        """
        self.debug: bool = debug
        super().__init__()
        if not self.debug:
            self.cmd.extend(["-loglevel", "quiet"])

    def scale(self, resolution):
        """
        Adds a scale filter to the FFMpeg command to resize the video.

        Args:
            resolution (Resolution): The resolution object with width and height attributes.

        Raises:
            Exception: If the output file already exists and force flag is not set.
        """
        self.cmd.append("-vf")
        width = resolution.width
        height = resolution.height
        self.cmd.append(f"scale={width}:{height}")

        # check if the output file is given or not
        if self.output_file_name:
            file_path, _ = path.splitext(str(self.output_file_name.resolve()))
        else:
            file_path, _ = path.splitext(str(self.input_file_name.resolve()))

        outfile = file_path + f"_{width}x{height}.mp4"
        if path.exists(outfile) and self.force:
            remove(outfile)

        self.cmd.append(outfile)

    def run(self):
        """
        Executes the FFMpeg command.

        Raises:
            subprocess.CalledProcessError: If the FFMpeg command fails.
        """
        #  check for cmd has the file added at the end of the command using extension
        if self.output_file_name and not any(ext in self.cmd[-1] for ext in self.VIDEO_EXTENSIONS):
            self.cmd.append(str(self.output_file_name))
        result = subprocess.run(self.cmd, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)

    def _process_res(self, resolution):
        """
        Processes the given resolution by scaling and running the FFMpeg command.

        Args:
            resolution (Resolution): The resolution object to process.
        """
        print(
            f"Processing {resolution.name} resolution with size {resolution.pixel_size} {resolution.width}x{resolution.height})")
        self.scale(resolution)
        self.run()

    def transcode(self, resolution_list: list[str]):
        """
        Transcodes the video to multiple resolutions using multiprocessing.

        This method takes a list of resolution names, maps them to resolution objects,
        and processes each resolution in parallel using a ProcessPoolExecutor.

        Args:
            resolution_list (list[str]): List of resolution names to transcode to.

        Raises:
            KeyError: If a resolution name is not found in the RESOLUTION_MAPPING.
        """
        _resolution_list: list[resolutions] = [RESOLUTION_MAPPING.get(rec) for rec in resolution_list]

        with ProcessPoolExecutor(max_workers=len(_resolution_list)) as executor:
            futures = {
                executor.submit(self._process_res, res): res
                for res in _resolution_list
            }
            for future in futures:
                future.result()

            print("completed processing")


class HLSStream(BaseFFMpeg):
    """
    Examples:
    >>> hls = HLSStream()
    >>> hls.input_file_name = Path(__file__).parent.resolve() / "models.py"
    >>> hls.video_codec = 'libx264'
    >>> hls.video_bit_rate = '3000k'
    >>> hls.run()


    """

    def __init__(self):
        super().__init__()
        self._video_codec = ['-c:v']
        self._video_bit_rate = ['-b:v']
        self._video_buffer_size = ['-bufsize:v']
        self._max_video_bit_rate = ['-maxrate:v']

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

    def run(self):
        if len(self.video_codec) > 1:
            self.cmd.extend(self.video_codec)

        if len(self.video_bit_rate) > 1:
            self.cmd.extend(self.video_bit_rate)
