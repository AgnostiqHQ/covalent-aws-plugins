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
    "license": "GNU Affero GPL v3.0",
    "author": "Agnostiq",
    "author_email": "support@agnostiq.ai",
    "description": "Covalent AWS Plugins",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "install_requires": required,
    "extras_require": {
        "all": [
            "covalent-awsbatch-plugin>=0.11.0<1",
            "covalent-ecs-plugin>=0.11.0<1",
            "covalent-ec2-plugin>=0.4.0.post1<1",
            "covalent-awslambda-plugin>=0.5.0<1",
            "covalent-braket-plugin>=0.4.1<1"
        ],
        "batch": "covalent-awsbatch-plugin>=0.11.0<1",
        "ec2": "covalent-ec2-plugin>=0.4.0.post1<1",
        "lambda": "covalent-awslambda-plugin>=0.5.0<1",
        "braket": "covalent-braket-plugin>=0.4.1<1",
        "ecs": "covalent-ecs-plugin>=0.11.0<1",
    },
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
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
