# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG COVALENT_BASE_IMAGE
FROM ${COVALENT_BASE_IMAGE}

RUN apt-get update \
  && apt-get install -y --no-install-recommends rsync \
  && rm -rf /var/lib/apt/lists/* \
  && pip install boto3

RUN cat <<EOF > /covalent/exec.py
import os
import boto3
import cloudpickle as pickle

s3_bucket = os.environ["S3_BUCKET_NAME"]
if not s3_bucket:
    raise ValueError("Environment variable S3_BUCKET_NAME was not found")

func_filename = os.environ["COVALENT_TASK_FUNC_FILENAME"]
if not func_filename:
    raise ValueError("Environment variable FUNC_FILENAME was not found")

result_filename = os.environ["RESULT_FILENAME"]
if not result_filename:
    raise ValueError("Environment variable RESULT_FILENAME was not found")

local_func_filename = os.path.join("/covalent", func_filename)
local_result_filename = os.path.join("/covalent", result_filename)

s3 = boto3.client("s3")
s3.download_file(s3_bucket, func_filename, local_func_filename)

with open(local_func_filename, "rb") as f:
    function, args, kwargs = pickle.load(f)

result = function(*args, **kwargs)

with open(local_result_filename, "wb") as f:
    pickle.dump(result, f)

s3.upload_file(local_result_filename, s3_bucket, result_filename)
EOF

ENTRYPOINT [ "python" ]
CMD [ "/covalent/exec.py" ]
