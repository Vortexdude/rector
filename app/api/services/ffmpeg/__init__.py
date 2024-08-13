from .models import resolutions

"""define all the audio and video `codes` """


class VideoCodecs:
    """FFMPEG Video Encoders"""
    X264 = 'libx264'
    hevc = 'libxhevc'
    VP9 = 'libvpx-vp9'
    AV1 = 'libaom-av1'
    VPX = 'libvpx'


class AudioCodes:
    """FFMPEG Audio Encoders"""
    AAC = 'aac'
    FLAC = 'flac'
    OPUS = 'libopus'
