from pydantic import BaseModel

__all__ = ["resolutions", "RESOLUTION_MAPPING"]


class BaseQuality(BaseModel):
    name: str
    aspect_ratio: str = "16:9"
    pixel_size: str
    width: int
    height: int


class StandardDefinition(BaseQuality):
    name: str = "480p"
    aspect_ratio: str = "4:3"
    pixel_size: str = "640x480"
    width: int = 640
    height: int = 480


class HighDefinition(BaseQuality):
    name: str = "720p"
    pixel_size: str = "1280x720"
    width: int = 1280
    height: int = 720


class FullHighDefinition(BaseQuality):
    name: str = "1080p"
    pixel_size: str = "1920x1080"
    width: int = 1920
    height: int = 1080


class QuadHighDefinition(BaseQuality):
    name: str = "1440p"
    pixel_size: str = "2560x1440"
    width: int = 2560
    height: int = 1440


class UltraHighDefinition(BaseQuality):
    name: str = "2160p"
    pixel_size: str = "3840x2160"
    width: int = 3840
    height: int = 2160


class Resolutions(BaseModel):
    SD: StandardDefinition
    HD: HighDefinition
    FHD: FullHighDefinition
    QHD: QuadHighDefinition
    UHD: UltraHighDefinition


sd = StandardDefinition()
hd = HighDefinition()
fhd = FullHighDefinition()
qhd = QuadHighDefinition()
uhd = UltraHighDefinition()

resolutions = Resolutions(SD=sd, HD=hd, FHD=fhd, QHD=qhd, UHD=uhd)

RESOLUTION_MAPPING = {
    "sd": resolutions.SD,
    "hd": resolutions.HD,
    "fhd": resolutions.FHD,
    "qhd": resolutions.QHD,
    "uhd": resolutions.UHD
}
