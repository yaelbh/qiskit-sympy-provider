# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

""" Usage examples for the Sympy Provider """

from qiskit_addon_sympy import SympyProvider


SyQ = SympyProvider()

# prints the symp
print(SyQ.backends())

print(SyQ.backends(name='statevector_simulator'))

backend = SyQ.get_backend('statevector_simulator')
print(backend)


# gets the name of the backend.
print(backend.name())

# gets the status of the backend.
print(backend.status())

# returns the provider of the backend
print(backend.provider) 

# gets the configuration of the backend.
print(backend.configuration())

# gets the properties of the backend.
print(backend.properties())
