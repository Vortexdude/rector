import os
from typing import Literal
from app.core.config import settings
from app.api.services.aws import ec2, s3
from fastapi import APIRouter, File, UploadFile
from app.common.utils.files import upload_file, cleanup

TAGS = ['aws']
_args: list = ['architecture', 'availability_zone', 'vpc_id', 'name', 'image_id', 'instance_id', 'instance_state_name',
               'instance_state_code', 'instance_type', 'ip_address', 'key_name']

args = Literal[tuple(_args)]

router = APIRouter(tags=TAGS)


@router.get("/ec2/", tags=['ec2'])
def get_ec2_list(filter_key: args, filter_value: str):
    return {"ec2": ec2.fetch_all(**{filter_key: filter_value})}


@router.get("/s3/", tags=['s3'])
def get_buckets_list():
    return {"buckets": s3.fetch_all()}


@router.post("/upload_to_s3", tags=['s3'])
def upload_file_to_s3(file: UploadFile = File(...)):
    full_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    upload_file(file, settings.UPLOAD_DIR)
    s3.upload_file(file_name=full_path, bucket="butena-public", key=f"media/videos/original/{file.filename}")
    cleanup(files=[full_path])
    return {"status": "successfully uploaded file"}
