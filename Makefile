# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
.PHONY: style lint test profile

# Ignoring generated ones with .py extension.
lint:
	pylint -rn qiskit_addon_sympy test

style:
	pycodestyle --max-line-length=100 qiskit_addon_sympy test

# Use the -s (starting directory) flag for "unittest discover" is necessary,
# otherwise the QuantumCircuit header will be modified during the discovery.
test:
	python3 -m unittest discover -v

profile:
	python3 -m unittest discover -p "profile*.py" -v

