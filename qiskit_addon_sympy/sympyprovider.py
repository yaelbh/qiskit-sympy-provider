# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name, bad-continuation

"""Provider for local Sympy backends."""

import logging

from qiskit.backends import BaseProvider
from .statevector_simulator_sympy import StatevectorSimulatorSympy
from .unitary_simulator_sympy import UnitarySimulatorSympy


logger = logging.getLogger(__name__)


class SympyProvider(BaseProvider):
    """Provider for local Sympy backends."""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        # Populate the list of local Sympy backends.
        self.backends = {'local_statevector_simulator_sympy': StatevectorSimulatorSympy(),
                         'local_unitary_simulator_sympy': UnitarySimulatorSympy()}

    def get_backend(self, name):
        return self.backends[name]

    def available_backends(self, filters=None):
        # pylint: disable=arguments-differ
        backends = self.backends

        filters = filters or {}
        for key, value in filters.items():
            backends = {name: instance for name, instance in backends.items()
                        if instance.configuration.get(key) == value}

        return list(backends.values())
