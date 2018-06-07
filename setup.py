# -*- coding: utf-8 -*-

# Copyright 2018 IBM RESEARCH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from setuptools import setup, find_packages

setup(
    name="qiskit_addon_sympy",
    version="0.1.0",
    author="QISKit Development Team",
    author_email="qiskit@us.ibm.com",
    description="QISKit statevector simulators whose backends are written in Sympy",
    long_description = "This module contains [QISKit](https://www.qiskit.org/) simulators whose backends are written in Sympy. These simulators simulate a Quantum circuit on a classical computer.",
    url="https://github.com/QISKit/qiskit_addon_sympy",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=['qiskit>=0.5'],
    keywords="qiskit quantum sympy simulator",
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    python_requires=">=3.5"
)
