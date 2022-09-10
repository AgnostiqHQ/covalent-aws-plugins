from typing import Dict
from .client_exception import ClientError, AWSClientException

class InvalidCredentials(AWSClientException):
    """Exception raised when invalid AWS credentials supplied.

    Attributes:
        credentials_file: AWS credentials file being used
        profile: AWS profile being used
    """

    def __init__(self, client_error: ClientError, profile: str, credentials_file: str):
        self.profile = profile
        self.credentials_file = credentials_file

        super().__init__(client_error, f"Invalid AWS Credentials supplied to Covalent Executor, please ensure credentials file '{credentials_file}' and profile '{profile}' have the correct aws_access_key_id and aws_secret_access_key defined")
