# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Provider for local Sympy backends."""

from qiskit.backends import BaseProvider
from qiskit.backends.providerutils import filter_backends
from .statevector_simulator import SympyStatevectorSimulator
from .unitary_simulator import SympyUnitarySimulator


class SympyProvider(BaseProvider):
    """Provider for local Sympy backends."""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        # Populate the list of local Sympy backends.
        self._backends = [SympyStatevectorSimulator(provider=self),
                          SympyUnitarySimulator(provider=self)]

    def get_backend(self, name=None, **kwargs):
        return super().get_backend(name=name, **kwargs)

    def backends(self, name=None, filters=None, **kwargs):
        # pylint: disable=arguments-differ
        if name:
            kwargs.update({'name': name})

        return filter_backends(self._backends, filters=filters, **kwargs)

    def __str__(self):
        return 'SympyProvider'
