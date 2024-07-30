import boto3
from app.common.exceptions.errors import AwsConnectionError
REGION = 'ap-south-1'

__all__ = ["ec2"]


class BaseServiceArgs:

    @staticmethod
    def _create_filter(
            *,
            architecture=None,
            availability_zone=None,
            vpc_id=None,
            name=None,
            image_id=None,
            instance_id=None,
            instance_state_name=None,
            instance_state_code=None,
            instance_type=None,
            ip_address=None,
            key_name=None,
            metadata_options_state=None,
    ) -> list[dict[str, str | list]]:
        filters = []
        if architecture:
            filters.append({'Name': 'architecture', 'Values': [architecture]})
        if availability_zone:
            filters.append({'Name': 'availability-zone', 'Values': [availability_zone]})
        if vpc_id:
            filters.append({'Name': 'network-interface.vpc-id', 'Values': [vpc_id]})
        if name:
            filters.append({'Name': 'tag:Name', 'Values': [name]})
        if image_id:
            filters.append({'Name': 'image-id', 'Values': [image_id]})
        if instance_id:
            filters.append({'Name': 'instance-id', 'Values': [instance_id]})
        if instance_state_name:
            filters.append({'Name': 'instance-state-name', 'Values': [instance_state_name]})
        if instance_state_code:
            filters.append({'Name': 'instance-state-code', 'Values': [instance_state_code]})
        if instance_type:
            filters.append({'Name': 'instance-type', 'Values': [instance_type]})
        if ip_address:
            filters.append({'Name': 'ip-address', 'Values': [ip_address]})
        if key_name:
            filters.append({'Name': 'key-name', 'Values': [key_name]})

        return filters


class EC2(BaseServiceArgs):
    def __init__(self, region=None):
        self.client = boto3.client('ec2')

    def fetch_all(self, *args, **kwargs) -> list[dict[str, str | None]] | None:
        _instances = []
        filters = super()._create_filter(*args, **kwargs)
        response = self.client.describe_instances(Filters=filters)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AwsConnectionError

        if "Reservations" not in response:
            return []

        if not response['Reservations']:
            return []

        reservation = response['Reservations'][0]

        key_to_extract = [
            'ImageId', 'State', 'InstanceId', 'InstanceType', 'KeyName', 'LaunchTime', 'SubnetId', 'VpcId',
            'Architecture', 'PrivateDnsName', 'PrivateIpAddress', 'PublicDnsName', 'PublicIpAddress'
        ]

        for instance in reservation['Instances']:
            res = {}
            for key in key_to_extract:
                if key == 'State' and isinstance(instance[key], dict):
                    res['State'] = instance[key]['Name']
                else:
                    if key == 'LaunchTime':
                        res[key] = instance[key].strftime('%Y-%m-%d_%H:%M:%S')
                    else:
                        res[key] = instance[key]

            _instances.append(res)

        return _instances


ec2 = EC2()
