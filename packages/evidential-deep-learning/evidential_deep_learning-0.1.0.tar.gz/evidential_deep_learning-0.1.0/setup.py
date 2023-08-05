# Copyright 2020 Alexander Amini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name="evidential_deep_learning",
    version="0.1.0",
    packages=find_packages(),
    description=
    "Learn fast, scalable, and calibrated measures of uncertainty using neural networks!",
    url="https://github.com/aamini/evidential_deep_learning",
    download_url="https://github.com/aamini/evidential-deep-learning/archive/v0.1.0.tar.gz",
    author="Alexander Amini",
    author_email="amini@mit.edu",
    license="Apache License 2.0",
    install_requires=[
        "numpy",
        "matplotlib",
    ],  # Tensorflow must be installed manually
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
)
