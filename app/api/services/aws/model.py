from datetime import datetime
from pydantic import BaseModel


class Ec2(BaseModel):
    name: str
    image_id: str
    InstanceId: str
    InstanceType: str
    KeyName: str
    LaunchTime: datetime
    vpc_id: str
    state: str
    SubnetId: str
    Architecture: str
