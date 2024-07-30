from typing import Literal
from fastapi import APIRouter
from app.api.services.aws import ec2, s3

TAGS = ['aws']
_args: list = ['architecture', 'availability_zone', 'vpc_id', 'name', 'image_id', 'instance_id', 'instance_state_name', 'instance_state_code', 'instance_type', 'ip_address','key_name']
args = Literal[tuple(_args)]

router = APIRouter(tags=TAGS)


@router.get("/ec2/", tags=['ec2'])
def get_ec2_list(filter_key: args, filter_value: str):
    return {"ec2": ec2.fetch_all(**{filter_key: filter_value})}


@router.get("/s3/", tags=['s3'])
def get_buckets_list():
    return {"buckets": s3.fetch_all()}
