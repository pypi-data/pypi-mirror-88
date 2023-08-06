from src import aws_credentials
from unittest.mock import patch


@patch.object(aws_credentials, "AWS4Auth")
@patch.object(aws_credentials, "credentials")
def test_aws_auth(credentials, aws_4_auth):
    credentials.return_value = {
        'access_key': 123,
        'secret_key': 321,
        'token': 'bla',
    }
    aws_credentials.aws_auth()

    aws_4_auth.assert_called_once()
