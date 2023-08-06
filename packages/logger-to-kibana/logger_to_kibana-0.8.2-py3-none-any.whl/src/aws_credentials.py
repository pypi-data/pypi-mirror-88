from requests_aws4auth import AWS4Auth
import boto3

region = 'eu-west-1'
service = 'es'
session = boto3.Session(region_name=region)
credentials = session.get_credentials()


def aws_auth() -> dict:
    return AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token
    )
