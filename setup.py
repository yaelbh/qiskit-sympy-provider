# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

from setuptools import setup, find_packages

setup(
    name="qiskit_addon_sympy",
    version="0.1.0",
    author="QISKit Development Team",
    author_email="qiskit@us.ibm.com",
    description="QISKit simulators whose backends are written in Sympy",
    long_description = "This module contains [QISKit](https://www.qiskit.org/) simulators whose backends are written in Sympy. These simulators simulate a Quantum circuit on a classical computer.",
    url="https://github.com/QISKit/qiskit-addon-sympy",
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
