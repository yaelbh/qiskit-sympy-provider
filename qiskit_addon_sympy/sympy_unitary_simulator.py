# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Contains a (slow) Python simulator that returns the unitary of the circuit.

It produces the unitary of a quantum circuit in the symbolic form.
In particular, it simulates the quantum computation with the sympy APIs,
which preserve the symbolic form of numbers, e.g., sqrt(2), e^{i*pi/2}.

How to use this simulator:
see examples/sympy_backends.py

Example output:
[[sqrt(2)/2 sqrt(2)/2 0 0]
 [0 0 sqrt(2)/2 -sqrt(2)/2]
 [0 0 sqrt(2)/2 sqrt(2)/2]
 [sqrt(2)/2 -sqrt(2)/2 0 0]]

Warning: it is slow.
"""
import logging
import uuid
import time
import numpy as np
from sympy import Matrix, pi
from sympy.matrices import eye, zeros
from sympy.physics.quantum import TensorProduct

from qiskit import Result
from qiskit.backends import BaseBackend
from qiskit.backends.aer.aerjob import AerJob
from qiskit.backends.aer._simulatortools import compute_ugate_matrix, index2
from qiskit.backends.aer._simulatorerror import SimulatorError

logger = logging.getLogger(__name__)


class SympyUnitarySimulator(BaseBackend):
    """Sympy implementation of a unitary simulator."""

    DEFAULT_CONFIGURATION = {
        'name': 'unitary_simulator_sympy',
        'url': 'https://github.com/QISKit/qiskit-addon-sympy',
        'simulator': True,
        'local': True,
        'description': 'A sympy simulator for unitary matrix',
        'coupling_map': 'all-to-all',
        'basis_gates': 'u1,u2,u3,cx,id'
    }

    def __init__(self, configuration=None):
        """Initialize the SympyUnitarySimulator object."""
        super().__init__(configuration or self.DEFAULT_CONFIGURATION.copy())

        self._unitary_state = None
        self._number_of_qubits = None

    @staticmethod
    def compute_ugate_matrix_wrap(parameters):
        """
            convert the parameter lists used by U1, U2 to the same form as U3.
            then computes the matrix for the u gate based on the parameter list
            Args:
                parameters (list): list of parameters, of which the length may be 1, 2, or 3
            Returns:
                Matrix: the matrix that represents the ugate
        """
        if len(parameters) == 1:  # [theta=0, phi=0, lambda]
            parameters.insert(0, 0.0)
            parameters.insert(0, 0.0)
        elif len(parameters) == 2:  # [theta=pi/2, phi, lambda]
            parameters.insert(0, pi / 2)
        elif len(parameters) == 3:  # [theta, phi, lambda]
            pass
        else:
            return NotImplemented

        u_mat = compute_ugate_matrix(parameters)
        return u_mat

    def enlarge_single_opt_sympy(self, opt, qubit, number_of_qubits):
        """Enlarge single operator to n qubits.

        It is exponential in the number of qubits.

        Args:
            opt (object): the single-qubit opt.
            qubit (int): the qubit to apply it on counts from 0 and order
                is q_{n-1} ... otimes q_1 otimes q_0.
            number_of_qubits (int): the number of qubits in the system.

        Returns:
            Matrix: the enlarged matrix that operates on all qubits in the system.
        """
        temp_1 = eye(2**(number_of_qubits-qubit-1))
        temp_2 = eye(2**(qubit))
        enlarge_opt = TensorProduct(temp_1, TensorProduct(opt, temp_2))
        return enlarge_opt

    def _add_unitary_single(self, gate, qubit):
        """Apply the single-qubit gate.
        Args:
            gate (Matrix): The matrix for a single-qubit gate. It looks like this:
                        Matrix([
                            [sqrt(2)/2,  sqrt(2)/2],
                            [sqrt(2)/2, -sqrt(2)/2]])
                        Matrix is a type from sympy.
            qubit (int): the id of the qubit being operated on
        """
        unitaty_add = self.enlarge_single_opt_sympy(gate, qubit, self._number_of_qubits)
        self._unitary_state = unitaty_add*self._unitary_state  # * means "dot product"

    def enlarge_two_opt_sympy(self, opt, qubit0, qubit1, num):
        """Enlarge two-qubit operator to n qubits.

        It is exponential in the number of qubits.

        Args:
            opt (Matrix): the matrix that represents a two-qubit gate.
                It looks like this::

                    Matrix([
                        [1, 0, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0],
                        [0, 1, 0, 0]])

            qubit0 (int): id of the control qubit
            qubit1 (int): id of the target qubit
            num (int): the number of qubits in the system.

        Returns:
            Matrix: the enlarged matrix that operates on all qubits in the system.
                    It is basically a tensorproduct of the gates applied on each qubit
                    (Identity gate if no gate is applied to the qubit).
        """
        enlarge_opt = zeros(2**num, 2**num)  # np.zeros([1 << (num), 1 << (num)])
        for i in range(2**(num-2)):
            for j in range(2):
                for k in range(2):
                    for m in range(2):
                        for n in range(2):
                            enlarge_index1 = index2(j, qubit0, k, qubit1, i)
                            enlarge_index2 = index2(m, qubit0, n, qubit1, i)
                            enlarge_opt[enlarge_index1, enlarge_index2] = opt[j+2*k, m+2*n]
        return enlarge_opt

    def _add_unitary_two(self, gate, qubit0, qubit1):
        """Apply the two-qubit gate
         It first extends the two-qubit gate to all-qubit gate and then applying it to all qubits.
         The result stored in self.__unitary_state is a unitary matrix, which looks like this:
                    Matrix([
                        [sqrt(2)/2,  sqrt(2)/2,         0,          0],
                        [        0,          0, sqrt(2)/2, -sqrt(2)/2],
                        [        0,          0, sqrt(2)/2,  sqrt(2)/2],
                        [sqrt(2)/2, -sqrt(2)/2,         0,          0]])
        Args:
            gate (Matrix): the matrix that represents a two-qubit gate
            qubit0 (int): id of the control qubit
            qubit1 (int): id of the target qubit
        """
        unitaty_add = self.enlarge_two_opt_sympy(gate, qubit0, qubit1, self._number_of_qubits)
        self._unitary_state = unitaty_add*self._unitary_state

    def run(self, qobj):
        """Run qobj asynchronously.

        Args:
            qobj (dict): job description

        Returns:
            LocalJob: derived from BaseJob
        """
        return LocalJob(self._run_job, qobj)

    def _run_job(self, qobj):
        """Run qobj

        Args:
            qobj (dict): all the information necessary
                (e.g., circuit, backend and resources) for running a circuit

        Returns:
            Result: Result is a class including the information to be returned to users.
            Specifically, result_list in the return looks is important and it like this::

                [
                    {'data': {'unitary':
                        array([[sqrt(2)/2, sqrt(2)/2, 0, 0],
                              [0, 0, sqrt(2)/2, -sqrt(2)/2],
                              [0, 0, sqrt(2)/2, sqrt(2)/2],
                              [sqrt(2)/2, -sqrt(2)/2, 0, 0]], dtype=object)},
                    'status': 'DONE'}
                ]
        """
        result_list = []
        start = time.time()
        for circuit in qobj['circuits']:
            result_list.append(self.run_circuit(circuit))
        end = time.time()
        job_id = str(uuid.uuid4())
        result = {'backend': self._configuration['name'],
                  'id': qobj['id'],
                  'job_id': job_id,
                  'result': result_list,
                  'status': 'COMPLETED',
                  'success': True,
                  'time_taken': (end - start)}
        return Result(result)

    def run_circuit(self, circuit):
        """Run a circuit and return the results.
        Args:
            circuit (dict): JSON that describes the circuit

        Returns:
            dict: A dictionary of results which looks something like::

                {'data': {'unitary': array([[sqrt(2)/2, sqrt(2)/2, 0, 0],
                                            [0, 0, sqrt(2)/2, -sqrt(2)/2],
                                             [0, 0, sqrt(2)/2, sqrt(2)/2],
                                             [sqrt(2)/2, -sqrt(2)/2, 0, 0]], dtype=object)
                           },
                'status': 'DONE'}

        Raises:
            SimulatorError: if unsupported operations passed
        """
        ccircuit = circuit['compiled_circuit']
        self._number_of_qubits = ccircuit['header']['number_of_qubits']
        result = {}
        result['data'] = {}
        self._unitary_state = eye(2 ** self._number_of_qubits)
        for operation in ccircuit['operations']:
            if 'conditional' in operation:
                raise SimulatorError('conditional operations not supported in unitary simulator')
            if operation['name'] == 'measure' or operation['name'] == 'reset':
                raise SimulatorError('operation {} not supported by '
                                     'sympy unitary simulator.'.format(operation['name']))
            if operation['name'] in ['U', 'u1', 'u2', 'u3']:
                if 'params' in operation:
                    params = operation['params']
                else:
                    params = None
                qubit = operation['qubits'][0]
                gate = SympyUnitarySimulator.compute_ugate_matrix_wrap(params)
                self._add_unitary_single(gate, qubit)
            elif operation['name'] in ['id']:
                logger.info('Identity gate is ignored by sympy-based unitary simulator.')
            elif operation['name'] in ['barrier']:
                logger.info('Barrier is ignored by sympy-based unitary simulator.')
            elif operation['name'] in ['CX', 'cx']:
                qubit0 = operation['qubits'][0]
                qubit1 = operation['qubits'][1]
                gate = Matrix([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])
                self._add_unitary_two(gate, qubit0, qubit1)
            else:
                result['status'] = 'ERROR'
                return result
        result['data']['unitary'] = np.array(self._unitary_state)
        result['status'] = 'DONE'
        result['name'] = circuit['name']

        return result
