# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.

import os
from typing import Dict, Union
import boto3

from covalent.executor.executor_plugins.remote_executor import RemoteExecutor
from .exceptions.client_exception import ClientError
from .exceptions.invalid_credentials import InvalidCredentials

"""Base Executor class for all AWS Executor Plugins"""

class AWSExecutor(RemoteExecutor):
    """
    AWSExecutor which provides a base class for all other AWS Executors to inherit from.

    Attributes:
        profile: (optional) Named AWS profile, default profile is "default" or defined from AWS_PROFILE env var.
        credentials_file: (optional) Location of AWS credentials file, default is $HOME/.aws/credentials or defined from AWS_SHARED_CREDENTIALS_FILE env var
        region: (optional) Region to use in order to access AWS Resources, default is defined from ~/.aws/config or defined from AWS_DEFAULT_REGION env var
        s3_bucket_name: (May be required depending on executor) S3 Bucket Name to use in order to store covalent execution artifacts.
        execution_role: (May be required depending on executor) AWS IAM Role for covalent to assume when executing tasks.
        log_group_name: (May be required depending on executor) AWS Log Group which will hold any relevant logs regarding workflow execution.
    """

    def __init__(self, profile: str = None, region: str = None, s3_bucket_name: str = None, execution_role: str = None, log_group_name: str = None, credentials_file: str = None, **kwargs) -> None:

        super().__init__(**kwargs)

        self.execution_role = execution_role
        self.log_group_name = log_group_name

        if s3_bucket_name:
            self.s3_bucket_name = s3_bucket_name

        if region:
            self.region = region
        else:
            self.region = os.getenv("AWS_DEFAULT_REGION")

        if profile:
            self.profile = profile
        else:
            self.profile = os.getenv("AWS_PROFILE")

        if credentials_file:
            self.credentials_file = credentials_file
        else:
            self.credentials_file = os.getenv("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials")

    @property
    def s3_bucket_name(self):
        return self.remote_cache

    @s3_bucket_name.setter
    def s3_bucket_name(self, s3_bucket_name):
        self.remote_cache = s3_bucket_name

    @property
    def credentials_file(self):
        return self._credentials_file

    @credentials_file.setter
    def credentials_file(self, credentials_file):
        # only override default set by aws sdk if credentials_file is truthy
        if credentials_file:
            os.environ["AWS_SHARED_CREDENTIALS_FILE"] = credentials_file
        self._credentials_file = credentials_file or None

    def boto_session_options(self) -> Dict[str,str]:
        """
        Returns a dictionary of kwargs to populate a new boto3.Session() instance with proper auth, region, and profile options.
        """
        session_options = {}
        if self.profile:
            session_options["profile_name"] = self.profile
        if self.region:
            session_options["region_name"] = self.region
        return session_options

    def _validate_credentials(self, raise_exception = True) -> Union[Dict[str, str], bool]:
        """
        Validate AWS Credentials from supplied profile and credentials file

        Args:
            raises_exception: Boolean to determine if exception should be raised if AWS STS Client get_caller_identity() fails

        Returns:
            A dictionary of the form {"UserId": "The unique identifier of the calling entity.", "Arn": "The Amazon Web Services ARN associated with the calling entity.", "Account": "The Amazon Web Services account ID number of the account that owns or contains the calling entity."}

        Raises:
            InvalidCredentials: If AWS STS Client get_caller_identity() fails
        """
        try:
            sts = boto3.Session(**self.boto_session_options()).client("sts")
            return sts.get_caller_identity()
        except ClientError as e:
            if raise_exception:
                raise InvalidCredentials(e, self.profile, self.credentials_file) from e
            else:
                return False
