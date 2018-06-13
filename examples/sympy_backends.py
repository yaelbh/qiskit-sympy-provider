# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
"""
Example use of the symbolic simulator backends, which keep precise forms of
amplitudes.
"""

import os
from qiskit_addon_sympy import StatevectorSimulatorSympy, UnitarySimulatorSympy
from qiskit import execute, load_qasm_file


def use_sympy_backends():
    q_circuit = load_qasm_file('simple.qasm')
   
    # sympy statevector simulator
    result = execute(q_circuit, backend=StatevectorSimulatorSympy(), shots=1).result()
    print("final quantum amplitude vector: ")
    print(result.get_data(q_circuit)['statevector'])

    # sympy unitary simulator
    result = execute([q_circuit], backend=UnitarySimulatorSympy(), shots=1).result()
    print("\nunitary matrix of the circuit: ")
    print(result.get_data(q_circuit)['unitary'])

if __name__ == "__main__":
    use_sympy_backends()
