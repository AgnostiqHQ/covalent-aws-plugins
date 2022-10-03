from typing import Dict
from botocore.exceptions import ClientError

class AWSClientException(Exception):
    """Exception raised when AWS Client has an error response from API.

    Attributes:
        client_error: ClientError Exception raised by Boto client
    """

    def __init__(self, client_error: ClientError, message: str = 'Error'):

        self.client_code = client_error.response['Error']['Code']
        self.client_message = client_error.response['Error']['Message']
        super().__init__(message)
