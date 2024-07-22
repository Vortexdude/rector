import subprocess
from concurrent.futures import ProcessPoolExecutor
from app.api.services.ffmpeg import resolutions
from app.api.services.ffmpeg.ffmpeg import BaseFFMpeg
from app.api.services.ffmpeg.models import RESOLUTION_MAPPING


class Multiplexer(BaseFFMpeg):

    def __init__(self):
        super().__init__()

    def scale(self, resolution):
        self.cmd.append("-vf")
        width = resolution.width
        height = resolution.height
        self.cmd.append(f"scale={width}:{height}")
        outfile = self.output_file_name.stem + f"{width}x{height}.mp4"
        self.cmd.append(outfile)

    def run(self):
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


mm = Multiplexer()
mm.input_file_name = "/home/ncs/Downloads/ffm/video1.mp4"
mm.output_file_name = "/home/ncs/Downloads/ffm/video_out.mp4"
res_list = ["sd", 'hd']
mm.transcode(res_list)
