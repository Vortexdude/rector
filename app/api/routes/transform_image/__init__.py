import os
from typing import Literal
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.core.config import settings
from app.common.utils.files import upload_file
from .main import create_image

router = APIRouter(prefix='/manipulation', tags=["Image Processing"])

models: list = settings.MODEL_LIST
upload_dir = settings.UPLOAD_DIR
output_dir = settings.OUTPUT_DIR

modelLiteral = Literal[tuple(models)]


@router.post("/upload_file/")
def create_upload_file(model: modelLiteral, file: UploadFile = File()):
    upload_file(file, upload_dir)
    model_base_path = f"{model.replace('-', '/')}.t7" if "-" in model else f"{model}.t7"
    model_full_path = os.path.join(settings.NURAL_NETWORK_STYLE_PATH, model_base_path)
    input_file_path = f"{upload_dir}/{file.filename}"
    output_image_path = os.path.join(settings.OUTPUT_DIR, f"{model}_{file.filename}")
    create_image(model_full_path, input_file_path, output_image_path)
    return FileResponse(output_image_path)
