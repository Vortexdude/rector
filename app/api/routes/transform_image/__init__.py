from typing import Literal
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.core.config import logger
from app.common.utils.files import model_list
from app.core.pathconf import BasePath

from .main import RectorImageService

router = APIRouter(tags=["Image Processing"])
models: list = model_list(BasePath)
modelLiteral = Literal[tuple(models)]


@router.post("/upload_file/")
def create_upload_file(model: modelLiteral, file: UploadFile = File()):
    logger.debug(f"POST /upload_file > with file {file.filename}")
    logger.debug(f"Starts Uploading file {file.filename}")
    output_image_path = RectorImageService(model, file).process()
    return FileResponse(output_image_path)
