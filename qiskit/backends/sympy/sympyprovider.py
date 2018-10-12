# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Provider for local Sympy backends."""

from qiskit.backends import BaseProvider
from qiskit.backends.providerutils import filter_backends
from .sympy_statevector_simulator import SympyStatevectorSimulator
from .sympy_unitary_simulator import SympyUnitarySimulator

class SympyProvider(BaseProvider):
    """Provider for local Sympy backends."""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        # Populate the list of local Sympy backends.
<<<<<<< HEAD:qiskit/backends/sympy/sympyprovider.py
        statevector_simulator = SympyStatevectorSimulator()
        unitary_simulator = SympyUnitarySimulator()
        self.backends = {statevector_simulator.name(): statevector_simulator,
                         unitary_simulator.name(): unitary_simulator}
=======
        self._backends = [SympyStatevectorSimulator(), SympyUnitarySimulator()]
>>>>>>> Adding changes:qiskit_addon_sympy/sympyprovider.py

    def get_backend(self, name):
        return super().get_backend(name=name)

    def backends(self, name=None, filters=None, **kwargs):
        # pylint: disable=arguments-differ
        if name:
            return filter_backends(self._backends, name=name, filters=filters, **kwargs)
        else:
            return filter_backends(self._backends, filters=filters, **kwargs)

    def __str__(self):
        return 'SympyProvider'