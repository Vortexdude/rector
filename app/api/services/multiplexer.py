import os
from app.core.config import settings
from app.api.services.ffmpeg.multimedia import HLSStream
from app.api.services.ffmpeg import VideoCodecs, AudioCodes


__all__ = ["HLSStreaming"]


class HLSStreaming:

    HLS_LIST_SIZE = 0  # for restart the position from head
    HLS_VIDEO_SIZE = 6  # video stream size in minutes
    VIDEO_URL = "../video/{{ video_name }}/"  # variable that will print in the playlist file .m3u8
    HLS_PLAYLIST_DIR = "../data/playlist"  # the playlist dir where the playlist will be stored
    HLS_VIDEO_DIR = "../data/video"  # video directory where the segment will reside
    SEGMENT_FORMAT = "segment_%03d.ts"  # the segment file name that should be constant

    def __init__(self, input_file, *, upload_dir=settings.UPLOAD_DIR):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"file not found {input_file}")
        input_file_name = os.path.basename(input_file)
        self.uploaded_file_path = input_file
        self.hls_stream_path = os.path.join(
            settings.BASE_PATH, self.HLS_VIDEO_DIR, input_file_name.split(".")[0]
        )
        self.hls_segment_filename = os.path.join(str(self.hls_stream_path), self.SEGMENT_FORMAT)
        self.hls_playlist_file = os.path.join(
            settings.BASE_PATH,
            self.HLS_PLAYLIST_DIR,
            input_file_name.split(".")[0] + '.m3u8'
        )

    @staticmethod
    def validate_path(path) -> bool:
        """check the path exists or not"""
        return os.path.exists(path)

    def generate_stream(self):

        # check if the video dir exists
        if not self.validate_path(self.hls_stream_path):
            os.makedirs(self.hls_stream_path)

        hls = HLSStream(
            debug=False,
            hls_vide_url=self.VIDEO_URL,
            hls_list_size=self.HLS_LIST_SIZE,
            segment_size=self.HLS_VIDEO_SIZE,
            segment_filename=self.hls_segment_filename
        )
        try:
            hls.input_file_name = self.uploaded_file_path
            hls.output_file_name = self.hls_playlist_file
        except Exception as e:
            print("file already exists from HLC class")

        hls.video_codec = VideoCodecs.X264
        hls.audio_codec = AudioCodes.AAC
        hls.video_bit_rate = '3000k'
        hls.video_buffer_size = '6000k'
        hls.max_video_bit_rate = '6000k'
        hls.audio_bitrate = '128k'
        hls.run()
