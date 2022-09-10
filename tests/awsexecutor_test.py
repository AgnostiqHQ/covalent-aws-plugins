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

"""Unit tests for AWS batch executor."""

import os
from pathlib import Path
import sys
from unittest import mock
from unittest.mock import MagicMock

import pytest

from covalent_aws_plugins import AWSExecutor
from covalent_aws_plugins.exceptions.invalid_credentials import InvalidCredentials

@pytest.fixture
def MockAWSExecutor() -> AWSExecutor:
    class _MockAWSExecutor(AWSExecutor):
        async def _upload_task(self):
            pass

        async def submit_task(self, task_metadata):
            pass

        async def get_status(self):
            pass

        async def _poll_task(self):
            pass

        async def query_result(self):
            pass

        async def cancel(self):
            pass

        async def run(self, function, args, kwargs, task_metadata):
            pass

    aws_executor = _MockAWSExecutor(
        profile="default",
        region="us-east-1",
        s3_bucket_name="covalent-s3bucket",
        execution_role="covalent_execution_role",
        log_group_name="covalent-log-group",
        credentials_file="~/.aws/some-config-file"
    )
    return _MockAWSExecutor


class TestAWSExecutor:

    MOCK_PROFILE = "my_profile"
    MOCK_REGION = "us-east-1"
    MOCK_S3_BUCKET = "covalent-s3-bucket"
    MOCK_EXECUTION_ROLE = "covalent-execution-role"
    MOCK_LOG_GROUP_NAME = "covalent-log-group"

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_init_and_config(self, MockAWSExecutor, tmp_path):

        mock_credentials_file: Path = tmp_path / "credentials"
        mock_credentials_file.touch()

        # 1. test aws executor sets provided params

        executor = MockAWSExecutor(
            profile=self.MOCK_PROFILE,
            region=self.MOCK_REGION,
            s3_bucket_name=self.MOCK_S3_BUCKET,
            execution_role=self.MOCK_EXECUTION_ROLE,
            log_group_name=self.MOCK_LOG_GROUP_NAME,
            credentials_file=str(mock_credentials_file.resolve())
        )

        assert executor.profile == self.MOCK_PROFILE
        assert executor.region == self.MOCK_REGION
        assert executor.s3_bucket_name == self.MOCK_S3_BUCKET
        assert executor.execution_role == self.MOCK_EXECUTION_ROLE
        assert executor.log_group_name == self.MOCK_LOG_GROUP_NAME
        assert executor.credentials_file == str(mock_credentials_file.resolve())
        # test that env var has been set for boto client to pick up
        assert os.environ["AWS_SHARED_CREDENTIALS_FILE"] == str(mock_credentials_file.resolve())


        # 2. test aws executor with AWS specific environment variables set

        os.environ["AWS_PROFILE"] = self.MOCK_PROFILE
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = str(mock_credentials_file.resolve())
        os.environ["AWS_DEFAULT_REGION"] = self.MOCK_REGION

        executor = MockAWSExecutor()

        assert executor.profile == self.MOCK_PROFILE
        assert executor.region == self.MOCK_REGION
        assert executor.credentials_file == str(mock_credentials_file.resolve())


    @pytest.mark.parametrize("is_profile_defined,is_region_defined", [
        (False, False),
        (True, True),
        (False, True),
        (True, False)
    ])
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_boto_options(self, MockAWSExecutor, is_profile_defined, is_region_defined):

        executor_config = {}
        expected_boto_options = {}

        if is_profile_defined:
            executor_config["profile"] = self.MOCK_PROFILE
            expected_boto_options["profile_name"] = executor_config["profile"]

        if is_region_defined:
            executor_config["region"] = self.MOCK_REGION
            expected_boto_options["region_name"] = executor_config["region"]

        executor = MockAWSExecutor(**executor_config)
        boto_options = executor.boto_session_options()

        assert boto_options == expected_boto_options


    @pytest.mark.parametrize("is_credentials_valid", [(True),(False)])
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_validate_credentials(self, mocker, MockAWSExecutor, is_credentials_valid):

        CALLER_IDENTITY_MOCK = {
                'Account': '123',
                'Arn': 'arn:aws:iam::123:user/Alice',
                'UserId': 'USERID123'
            }
        if is_credentials_valid:
            boto3_mock = mocker.patch("covalent_aws_plugins.awsexecutor.boto3")
            boto3_mock.Session().client().get_caller_identity.return_value = CALLER_IDENTITY_MOCK

        executor = MockAWSExecutor()

        # 1. test we can validate credentials without exceptions

        identity = executor._validate_credentials(raise_exception=False)
        is_valid = bool(identity)

        if is_credentials_valid:
            assert identity == CALLER_IDENTITY_MOCK
            assert is_valid == True
        else:
            assert is_valid == False

        # 2. test we can validate credentials with exceptions

        if is_credentials_valid:
            identity = executor._validate_credentials(raise_exception=True)
            assert identity == CALLER_IDENTITY_MOCK
        else:
            with pytest.raises(InvalidCredentials):
                executor._validate_credentials(raise_exception=True)
