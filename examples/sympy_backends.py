# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
"""
Example use of the symbolic simulator backends, which keep precise forms of
amplitudes.
"""

<<<<<<< HEAD
from qiskit import register, load_qasm_file, execute
from qiskit.backends.sympy import SympyProvider
=======
from qiskit_addon_sympy import SympyProvider
>>>>>>> Adding changes



""" Usage examples for the Sympy simulators """

SyQ = SympyProvider()

print(SyQ.backends())

<<<<<<< HEAD

if __name__ == "__main__":
    use_sympy_backends()
=======
print(SyQ.backends(name='statevector_simulator_sympy'))
>>>>>>> Adding changes
