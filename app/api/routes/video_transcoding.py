import os
from typing import List
from fastapi import APIRouter, File, UploadFile, Query, Depends
from app.common.utils.files import upload_file
from app.core.config import settings
from app.api.services.ffmpeg.multimedia import Multiplexer
from app.api.models.ffmpeg import ExportQualities

router = APIRouter(tags=['ffmpeg'])


@router.post("/transcode")
def convert_to_all_formats(quality: List[ExportQualities] = Query(), file: UploadFile = File(...)):
    _qualities = [q.value for q in quality]
    upload_file(file, settings.UPLOAD_DIR)
    mm = Multiplexer()
    mm.input_file_name = os.path.join(settings.UPLOAD_DIR, file.filename)
    mm.output_file_name = os.path.join(settings.OUTPUT_DIR, file.filename)
    mm.transcode(_qualities)
    return {"status": "file uploaded successfully"}
