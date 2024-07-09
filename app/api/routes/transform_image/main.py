from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from typing import Literal
from app.core.utils import get_models_list
from app.api.routes.transform_image.engine import create_image
from app.core.config import settings


router = APIRouter()
upload_dir = settings.UPLOAD_DIR
output_dir = settings.OUTPUT_DIR
nural_net_model_path = settings.NURAL_NETWORK_STYLE_PATH
models = get_models_list(f"{nural_net_model_path}/*/*")
modelLiteral = Literal[tuple(models)]


@router.post("/upload_file/")
async def create_file_upload(model: modelLiteral, file: UploadFile = File()):
    """Upload file for model manipulation"""
    try:
        with open(f"{upload_dir}/{file.filename}", 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        return {"message": "There was an error while uploading the image."}
    finally:
        file.file.close()
    model_path = f"{nural_net_model_path}/{model}"
    input_image_path = f"{upload_dir}/{file.filename}"
    output_image_path = f"{output_dir}/{model.split('/')[1].split('.')[0]}_{file.filename}"
    create_image(model_path, _image=input_image_path, output_image=output_image_path)
    return FileResponse(output_image_path)
