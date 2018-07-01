# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Provider for local Sympy backends."""

from qiskit.backends import BaseProvider
from .statevector_simulator_sympy import StatevectorSimulatorSympy
from .unitary_simulator_sympy import UnitarySimulatorSympy


class SympyProvider(BaseProvider):
    """Provider for local Sympy backends."""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        # Populate the list of local Sympy backends.
        statevector_simulator = StatevectorSimulatorSympy()
        unitary_simulator = UnitarySimulatorSympy()
        self.backends = {statevector_simulator.name: statevector_simulator,
                         unitary_simulator.name: unitary_simulator}

    def get_backend(self, name):
        return self.backends[name]

    def available_backends(self):
        # pylint: disable=arguments-differ
        return list(self.backends.values())
