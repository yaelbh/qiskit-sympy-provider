# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,anomalous-backslash-in-string

# Copyright 2017 IBM RESEARCH. All Rights Reserved.
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
"""
Example use of the symbolic simulator backends, which keep precise forms of
amplitudes.
"""

from qiskit_addon_sympy import StatevectorSimulatorSympy, UnitarySimulatorSympy
from qiskit import execute, load_qasm_file


def use_sympy_backends():
    """ Usage examples for the Sympy simulators """
    q_circuit = load_qasm_file('simple.qasm')

    # sympy statevector simulator
    result = execute(q_circuit, backend=StatevectorSimulatorSympy()).result()
    print("final quantum amplitude vector: ")
    print(result.get_statevector(q_circuit))

    # sympy unitary simulator
    result = execute([q_circuit], backend=UnitarySimulatorSympy()).result()
    print("\nunitary matrix of the circuit: ")
    print(result.get_unitary(q_circuit))

if __name__ == "__main__":
    use_sympy_backends()
