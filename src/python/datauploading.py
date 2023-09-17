import boto3


LINK_EXPIRE = 3600*24
DEFAULT_BUCKET = 'ozwbsync'


class DataUploader():
    def __init__(self) -> None:
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def upload_file(self, file_path, obj_name, bucket=DEFAULT_BUCKET):
        return self.s3.upload_file(file_path, bucket, obj_name)

    def make_public(self, obj_name, bucket=DEFAULT_BUCKET):
        return self.s3.generate_presigned_url('get_object',
                                              Params={'Bucket': bucket,
                                                      'Key': obj_name},
                                              ExpiresIn=LINK_EXPIRE)
