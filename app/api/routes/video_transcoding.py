from fastapi import APIRouter, File, UploadFile
from app.common.utils.files import upload_file

router = APIRouter()


@router.post("/transcode")
def convert_to_all_formats(file: UploadFile = File(...)):
    upload_file(file, "/home/ncs/opt/workspace/vortexdude/rector/app/api/services")
    return {"status": "file uploaded successfully"}
