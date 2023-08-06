import json

s3_client = None


# improves speed for connecting on subsequent calls
# TODO: find a better way to do this, like profiling?
def _get_s3_client():
    global s3_client
    import boto3
    s3_client = boto3.client('s3') if s3_client is None else s3_client
    return s3_client


def _load_from_bucket(bucket: str, key: str):
    from botocore.exceptions import ClientError
    try:
        return json.loads(_get_s3_client().get_object(Bucket=bucket, Key=key)['Body'].read())
    except ClientError:
        return None
