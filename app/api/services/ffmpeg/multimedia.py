import subprocess
from os import path, remove
from app.api.services.ffmpeg import resolutions
from concurrent.futures import ProcessPoolExecutor
from app.api.services.ffmpeg.ffmpeg import BaseFFMpeg
from app.api.services.ffmpeg.models import RESOLUTION_MAPPING


class Multiplexer(BaseFFMpeg):
    """
    Class for handling FFMpeg multiplexing operations, inheriting from BaseFFMpeg.

    Attributes:
        debug (bool): Flag to enable debug mode.
    """

    def __init__(self, debug=False):
        """
        Initializes the Multiplexer class.

        Args:
            debug (bool): Flag to enable debug mode. Defaults to False.
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
        print(f"Processing {resolution.name} resolution with size {resolution.pixel_size} {resolution.width}x{resolution.height})")
        self.scale(resolution)
        self.run()

    def transcode(self, resolution_list: list[str]):
        """
        Transcodes the video to multiple resolutions using multiprocessing.

        Args:
            resolution_list (list[str]): List of resolution names to transcode to.
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
