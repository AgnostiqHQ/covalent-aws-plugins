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

import os
import site
import sys

from setuptools import find_packages, setup

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

with open("VERSION") as f:
    version = f.read().strip()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup_info = {
    "name": "covalent-aws-plugins",
    "packages": find_packages(exclude=["tests"]),
    "version": version,
    "maintainer": "Agnostiq",
    "url": "https://github.com/AgnostiqHQ/covalent-aws-plugins",
    "download_url": f"https://github.com/AgnostiqHQ/covalent-aws-plugins/archive/v{version}.tar.gz",
    "license": "Apache License 2.0",
    "author": "Agnostiq",
    "author_email": "support@agnostiq.ai",
    "description": "Covalent AWS Plugins",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "install_requires": required,
    "extras_require": {
        "all": [
            "covalent-awsbatch-plugin>=0.11.0,<1",
            "covalent-ecs-plugin>=0.11.0,<1",
            "covalent-ec2-plugin>=0.4.0.post1,<1",
            "covalent-awslambda-plugin>=0.5.0,<1",
            "covalent-braket-plugin>=0.4.1,<1"
        ],
        "batch": "covalent-awsbatch-plugin>=0.11.0,<1",
        "ec2": "covalent-ec2-plugin>=0.4.0.post1,<1",
        "lambda": "covalent-awslambda-plugin>=0.5.0,<1",
        "braket": "covalent-braket-plugin>=0.4.1,<1",
        "ecs": "covalent-ecs-plugin>=0.11.0,<1",
    },
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Adaptive Technologies",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development",
        "Topic :: System :: Distributed Computing",
    ],
}

if __name__ == "__main__":
    setup(**setup_info)  # Install base covalent-aws-plugins package.
