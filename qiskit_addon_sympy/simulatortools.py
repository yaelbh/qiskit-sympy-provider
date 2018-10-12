# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name

"""Functions used by the sympy simulators."""

from sympy import E, I, Matrix, N, cos, pi, sin, sympify


def index1(b, i, k):
    """Magic index1 function.

    Takes a bitstring k and inserts bit b as the ith bit,
    shifting bits >= i over to make room.
    """
    retval = k
    lowbits = k & ((1 << i) - 1)  # get the low i bits

    retval >>= i
    retval <<= 1

    retval |= b

    retval <<= i
    retval |= lowbits

    return retval


def index2(b1, i1, b2, i2, k):
    """Magic index1 function.

    Takes a bitstring k and inserts bits b1 as the i1th bit
    and b2 as the i2th bit
    """
    assert i1 != i2

    if i1 > i2:
        # insert as (i1-1)th bit, will be shifted left 1 by next line
        retval = index1(b1, i1-1, k)
        retval = index1(b2, i2, retval)
    else:  # i2>i1
        # insert as (i2-1)th bit, will be shifted left 1 by next line
        retval = index1(b2, i2-1, k)
        retval = index1(b1, i1, retval)
    return retval


def regulate(theta):
    """
    Return the regulated symbolic representation of `theta`::
        * if it has a representation close enough to `pi` transformations,
            return that representation (for example, `3.14` -> `sympy.pi`).
        * otherwise, return a sympified representation of theta (for example,
            `1.23` ->  `sympy.Float(1.23)`).

    See also `UGateGeneric`.

    Args:
        theta (float or sympy.Basic): the float value (e.g., 3.14) or the
            symbolic value (e.g., pi)

    Returns:
        sympy.Basic: the sympy-regulated representation of `theta`
    """
    error_margin = 0.01
    targets = [pi, pi/2, pi * 2, pi / 4]

    for t in targets:
        if abs(N(theta - t)) < error_margin:
            return t

    return sympify(theta)


def compute_ugate_matrix(parameters):
    """Compute the matrix associated with a parameterized U gate.

    Args:
        parameters (list[float]): parameters carried by the U gate
    Returns:
        sympy.Matrix: the matrix associated with a parameterized U gate
    """
    theta = regulate(parameters[0])
    phi = regulate(parameters[1])
    lamb = regulate(parameters[2])

    left_up = cos(theta/2)
    right_up = (-E**(I*lamb)) * sin(theta/2)
    left_down = (E**(I*phi)) * sin(theta/2)
    right_down = (E**(I*(phi + lamb))) * cos(theta/2)

    return Matrix([[left_up, right_up], [left_down, right_down]])
