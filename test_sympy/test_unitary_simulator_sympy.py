# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring

from test.python.common import QiskitTestCase

import unittest

from sympy import sqrt

from qiskit import (load_qasm_file, execute, QuantumRegister,
                    ClassicalRegister, QuantumCircuit, wrapper)
from qiskit_addon_sympy import UnitarySimulatorSympy


class UnitarySimulatorSympyTest(QiskitTestCase):
    """Test local unitary simulator sympy."""

    def setUp(self):
        self.qasm_filename = self._get_resource_path('qasm/simple.qasm')
        self.q_circuit = load_qasm_file(self.qasm_filename)

    def test_unitary_simulator(self):
        """test generation of circuit unitary"""

        result = execute(self.q_circuit, backend=UnitarySimulatorSympy()).result()
        actual = result.get_unitary(self.q_circuit)

        self.assertEqual(actual[0][0], sqrt(2)/2)
        self.assertEqual(actual[0][1], sqrt(2)/2)
        self.assertEqual(actual[0][2], 0)
        self.assertEqual(actual[0][3], 0)
        self.assertEqual(actual[1][0], 0)
        self.assertEqual(actual[1][1], 0)
        self.assertEqual(actual[1][2], sqrt(2)/2)
        self.assertEqual(actual[1][3], -sqrt(2)/2)
        self.assertEqual(actual[2][0], 0)
        self.assertEqual(actual[2][1], 0)
        self.assertEqual(actual[2][2], sqrt(2)/2)
        self.assertEqual(actual[2][3], sqrt(2)/2)
        self.assertEqual(actual[3][0], sqrt(2)/2)
        self.assertEqual(actual[3][1], -sqrt(2)/2)
        self.assertEqual(actual[3][2], 0)
        self.assertEqual(actual[3][3], 0)


class TestQobj(QiskitTestCase):
    """Check the objects compiled for this backend create names properly"""

    def setUp(self):
        qr = QuantumRegister(2, name="qr2")
        cr = ClassicalRegister(2, name=None)
        qc = QuantumCircuit(qr, cr, name="qc10")
        qc.h(qr[0])
        qc.measure(qr[0], cr[0])
        self.qr_name = qr.name
        self.cr_name = cr.name
        self.circuits = [qc]

    def test_qobj_statevector_simulator_sympy(self):
        qobj = wrapper.compile(self.circuits, backend=UnitarySimulatorSympy())
        cc = qobj['circuits'][0]['compiled_circuit']
        ccq = qobj['circuits'][0]['compiled_circuit_qasm']
        self.assertIn(self.qr_name, map(lambda x: x[0], cc['header']['qubit_labels']))
        self.assertIn(self.qr_name, ccq)
        self.assertIn(self.cr_name, map(lambda x: x[0], cc['header']['clbit_labels']))
        self.assertIn(self.cr_name, ccq)


if __name__ == '__main__':
    unittest.main()
