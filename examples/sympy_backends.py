# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
"""
Example use of the symbolic simulator backends, which keep precise forms of
amplitudes.
"""

from qiskit_addon_sympy import SympyProvider
from qiskit import register, load_qasm_file, execute


def use_sympy_backends():
    """ Usage examples for the Sympy simulators """

    # register with the SympyProvider to get access to its simulators
    register(provider_class=SympyProvider)
    q_circuit = load_qasm_file('simple.qasm')

    # sympy statevector simulator
    result = execute(q_circuit, backend='sympy_statevector_simulator').result()
    print("final quantum amplitude vector: ")
    print(result.get_statevector(q_circuit))

    # sympy unitary simulator
    result = execute([q_circuit], backend='sympy_unitary_simulator').result()
    print("\nunitary matrix of the circuit: ")
    print(result.get_unitary(q_circuit))

if __name__ == "__main__":
    use_sympy_backends()
