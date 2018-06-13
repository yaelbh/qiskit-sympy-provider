# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring

from test.python.common import QiskitTestCase

import unittest

from sympy import sqrt

from qiskit import (qasm, unroll, QuantumProgram, QuantumJob, QuantumRegister,
                    ClassicalRegister, QuantumCircuit, wrapper)
from qiskit_addon_sympy import UnitarySimulatorSympy


class UnitarySimulatorSympyTest(QiskitTestCase):
    """Test local unitary simulator sympy."""

    def setUp(self):
        self.seed = 88
        self.qasm_filename = self._get_resource_path('qasm/simple.qasm')
        self.qp = QuantumProgram()

    def test_unitary_simulator(self):
        """test generation of circuit unitary"""
        self.qp.load_qasm_file(self.qasm_filename, name='example')
        basis_gates = []  # unroll to base gates
        unroller = unroll.Unroller(
            qasm.Qasm(data=self.qp.get_qasm('example')).parse(),
            unroll.JsonBackend(basis_gates))
        circuit = unroller.execute()
        # strip measurements from circuit to avoid warnings
        circuit['operations'] = [op for op in circuit['operations']
                                 if op['name'] != 'measure']
        # the simulator is expecting a JSON format, so we need to convert it
        # back to JSON
        qobj = {
            'id': 'unitary',
            'config': {
                'max_credits': None,
                'shots': 1,
                'backend_name': 'local_sympy_unitary_simulator'
            },
            'circuits': [
                {
                    'name': 'test',
                    'compiled_circuit': circuit,
                    'compiled_circuit_qasm': self.qp.get_qasm('example'),
                    'config': {
                        'coupling_map': None,
                        'basis_gates': None,
                        'layout': None,
                        'seed': None
                    }
                }
            ]
        }

        q_job = QuantumJob(qobj,
                           backend=UnitarySimulatorSympy(),
                           preformatted=True)

        result = UnitarySimulatorSympy().run(q_job).result()
        actual = result.get_data('test')['unitary']

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
