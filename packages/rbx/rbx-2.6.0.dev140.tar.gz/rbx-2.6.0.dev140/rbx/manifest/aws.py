import boto3
import botocore


class S3Bucket:
    """An AWS S3 Bucket.

    Wraps the boto3.Bucket class to provide a higher level of abstraction.
    """
    def __init__(self, name):
        """Takes the bucket name and sets the S3Bucket instance to use that bucket."""
        self.name = name
        self.resource = boto3.resource('s3')
        self.bucket = self.resource.Bucket(name)

    def get_key(self, key):
        """Check whether the given key exists in the bucket.
        Will return the object or None.
        """
        object = self.bucket.Object(key)
        try:
            object.load()
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                return
            else:
                print(e)
        else:
            return object
