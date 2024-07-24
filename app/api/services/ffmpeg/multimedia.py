from os import path, remove
import subprocess
from concurrent.futures import ProcessPoolExecutor
from app.api.services.ffmpeg import resolutions
from app.api.services.ffmpeg.ffmpeg import BaseFFMpeg
from app.api.services.ffmpeg.models import RESOLUTION_MAPPING


class Multiplexer(BaseFFMpeg):

    def __init__(self, debug=False):
        self.debug: bool = debug
        super().__init__()
        if not self.debug:
            self.cmd.extend(["-loglevel", "quiet"])

    def scale(self, resolution):
        self.cmd.append("-vf")
        width = resolution.width
        height = resolution.height
        self.cmd.append(f"scale={width}:{height}")
        if self.output_file_name:
            file_path, _ = path.splitext(str(self.output_file_name.resolve()))
        else:
            file_path, _ = path.splitext(str(self.input_file_name.resolve()))

        outfile = file_path + f"_{width}x{height}.mp4"
        if path.exists(outfile) and self.force:
            remove(outfile)

        self.cmd.append(outfile)

    def run(self):
        #  check for cmd has the file added at the end of the command using extension
        if self.output_file_name and not any(ext in self.cmd[-1] for ext in self.VIDEO_EXTENSIONS):
            self.cmd.append(str(self.output_file_name))
        result = subprocess.run(self.cmd, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)

    def _process_res(self, resolution):
        print(f"Processing {resolution.name} resolution with size {resolution.pixel_size} {resolution.width}x{resolution.height})")
        self.scale(resolution)
        self.run()

    def transcode(self, resolution_list: list[str]):
        _resolution_list: list[resolutions] = [RESOLUTION_MAPPING.get(rec) for rec in resolution_list]

        with ProcessPoolExecutor(max_workers=len(_resolution_list)) as executor:
            futures = {
                executor.submit(self._process_res, res): res
                for res in _resolution_list
            }
            for future in futures:
                future.result()

            print("completed processing")
