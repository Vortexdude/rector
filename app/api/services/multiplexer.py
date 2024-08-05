import os
from fastapi import UploadFile
from app.core.config import settings
from app.common.utils.files import upload_file
from app.api.services.ffmpeg.multimedia import HLSStream

__all__ = ["HLSStreaming"]


class HLSStreaming:

    HLS_LIST_SIZE = 0
    HLS_VIDEO_SIZE = 6
    VIDEO_URL = "../video/{{ video_name }}/"
    HLS_PLAYLIST_DIR = "../data/playlist"
    HLS_VIDEO_DIR = "../data/video"
    SEGMENT_FORMAT = "segment_%03d.ts"

    def __init__(self, input_file: UploadFile, *, upload_dir=settings.UPLOAD_DIR):
        self.input_file = input_file
        self.upload_dir = upload_dir
        self.uploaded_file_path = os.path.join(self.upload_dir, self.input_file.filename)
        self.hls_stream_path = os.path.join(
            settings.BASE_PATH, self.HLS_VIDEO_DIR, input_file.filename.split(".")[0]
        )
        self.hls_segment_filename = os.path.join(self.hls_stream_path, self.SEGMENT_FORMAT)
        self.hls_playlist_file = os.path.join(
            settings.BASE_PATH,
            self.HLS_PLAYLIST_DIR,
            input_file.filename.split(".")[0] + '.m3u8'
        )

    @staticmethod
    def validate_path(path) -> bool:
        """check the path exists or not"""
        return os.path.exists(path)

    def generate_stream(self):
        if not self.validate_path(self.uploaded_file_path):
            upload_file(self.input_file, self.upload_dir)

        if not self.validate_path(self.hls_stream_path):
            os.makedirs(self.hls_stream_path)

        hls = HLSStream(
            debug=False,
            hls_vide_url=self.VIDEO_URL,
            hls_list_size=self.HLS_LIST_SIZE,
            segment_size=self.HLS_VIDEO_SIZE,
            segment_filename=self.hls_segment_filename
        )
        hls.input_file_name = self.uploaded_file_path
        hls.output_file_name = self.hls_playlist_file
        hls.video_codec = 'libx264'
        hls.video_bit_rate = '3000k'
        hls.video_buffer_size = '6000k'
        hls.max_video_bit_rate = '6000k'
        hls.audio_codec = 'aac'
        hls.audio_bitrate = '128k'
        hls.run()
