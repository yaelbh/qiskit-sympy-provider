# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring

from test.common import QiskitSympyTestCase

import unittest

from sympy import sqrt

# The following import will be replaced by an import of register
# once register is written
from qiskit.wrapper._wrapper import _DEFAULT_PROVIDER
from qiskit import (load_qasm_file, execute, QuantumRegister,
                    ClassicalRegister, QuantumCircuit, wrapper)
from qiskit_addon_sympy import SympyProvider


class StatevectorSimulatorSympyTest(QiskitSympyTestCase):
    """Test local statevector simulator."""

    def setUp(self):
        # The following lines will be replaced by a usage of register
        provider = SympyProvider()
        _DEFAULT_PROVIDER.add_provider(provider)

        self.qasm_filename = self._get_resource_path('simple.qasm')
        self.q_circuit = load_qasm_file(self.qasm_filename)

    def test_statevector_simulator_sympy(self):
        """Test final state vector for single circuit run."""
        result = execute(self.q_circuit, backend='local_statevector_simulator_sympy').result()
        actual = result.get_statevector(self.q_circuit)

        self.assertEqual(result.get_status(), 'COMPLETED')
        self.assertEqual(actual[0], sqrt(2)/2)
        self.assertEqual(actual[1], 0)
        self.assertEqual(actual[2], 0)
        self.assertEqual(actual[3], sqrt(2)/2)


class TestQobj(QiskitSympyTestCase):
    """Check the objects compiled for this backend create names properly"""

    def setUp(self):
        # The following lines will be replaced by a usage of register
        provider = SympyProvider()
        _DEFAULT_PROVIDER.add_provider(provider)

        qr = QuantumRegister(2, name="qr2")
        cr = ClassicalRegister(2, name=None)
        qc = QuantumCircuit(qr, cr, name="qc10")
        qc.h(qr[0])
        qc.measure(qr[0], cr[0])
        self.qr_name = qr.name
        self.cr_name = cr.name
        self.circuits = [qc]

    def test_qobj_statevector_simulator_sympy(self):
        qobj = wrapper.compile(self.circuits, backend='local_statevector_simulator_sympy')
        cc = qobj['circuits'][0]['compiled_circuit']
        ccq = qobj['circuits'][0]['compiled_circuit_qasm']
        self.assertIn(self.qr_name, map(lambda x: x[0], cc['header']['qubit_labels']))
        self.assertIn(self.qr_name, ccq)
        self.assertIn(self.cr_name, map(lambda x: x[0], cc['header']['clbit_labels']))
        self.assertIn(self.cr_name, ccq)


if __name__ == '__main__':
    unittest.main()
