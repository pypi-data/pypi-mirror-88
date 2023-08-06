#!/usr/bin/env python3

import numpy as np
# import fadScal
# import fadVect
# import revScal
# import revVect
from FADiff.fad.Gradients import Scal as fadScal
from FADiff.fad.Matrices import Vect as fadVect
from FADiff.rev.Gradients import Scal as revScal
from FADiff.rev.Matrices import Vect as revVect


def sin(x):
    """
    Calculates sine of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal/Vect
        val = np.sin(x._val)
        try:  # if fad mode
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der * np.cos(x._val)
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:  # if rev mode
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, np.cos(x._val)]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.sin(x)


def cos(x):
    """
    Calculates cosine of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.cos(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = -part_der * np.sin(x._val)
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, -np.sin(x._val)]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.cos(x)


def tan(x):
    """
    Calculates tangent of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.tan(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / (np.cos(x._val) * np.cos(x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / (np.cos(x._val) * np.cos(x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.tan(x)


def arcsin(x):
    """
    Calculates arcsine (inverse sine) of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.arcsin(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / np.sqrt(1 - (x._val * x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / np.sqrt(1 - (x._val * x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.arcsin(x)


def arccos(x):
    """
    Calculates arccosine (inverse cosine) of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.arccos(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = -part_der / np.sqrt(1 - (x._val * x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, -1 / np.sqrt(1 - (x._val * x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.arccos(x)


def arctan(x):
    """
    Calculates arctangent (inverse tangent) of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.arctan(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / (1 + (x._val * x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / (1 + (x._val * x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.arctan(x)


def sinh(x):
    """
    Calculates hyperbolic sine of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.sinh(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der * np.cosh(x._val)
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, np.cosh(x._val)]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.sinh(x)


def cosh(x):
    """
    Calculates hyperbolic cosine of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.cosh(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der * np.sinh(x._val)
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, np.sinh(x._val)]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.cosh(x)


def tanh(x):
    """
    Calculates hyperbolic tangent of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.tanh(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / (np.cosh(x._val) * np.cosh(x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / (np.cosh(x._val) * np.cosh(x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.tanh(x)


def exp(x):
    """
    Calculates e ** x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.exp(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der * np.exp(x._val)
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, np.exp(x._val)]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.exp(x)


def logistic(x):
    """
    Calculates logistic function f(x) = 1/(1 + e ** -x)

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = 1 / (1 + np.exp(-x._val))
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der * \
                    np.exp(x._val) / (1 + np.exp(x._val)) ** 2
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [
                    [x, np.exp(x._val) / (1 + np.exp(x._val)) ** 2]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return 1 / (1 + np.exp(-x))


def log(x, b=np.e):
    """
    Calculates logarithm of x of base b (default is the natural logarithm, base e)

    Inputs: x (either Scal/Vect object or constant), b (base for log, default is e)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.log(x._val) / np.log(b)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / (x._val * np.log(b))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / (x._val * np.log(b))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.log(x) / np.log(b)


def sqrt(x):
    """
    Calculates sqrt of x

    Inputs: x (either Scal/Vect object or constant)
    Returns: new object of type x (if x is a Scal or Vect) or a new constant (if x is a constant)
    """
    try:  # if x is a Scal
        val = np.sqrt(x._val)
        try:
            der = {}
            for var, part_der in x._der.items():
                der[var] = part_der / (2. * np.sqrt(x._val))
            parents = x._set_parents(x)
            return return_same_type(x, val, der, parents)
        except AttributeError:
            inputs = {}
            for root in x._inputs.keys():
                inputs[root] = [[x, 1 / (2. * np.sqrt(x._val))]]
            return return_same_rev(x, val, inputs)
    except AttributeError:  # if x is a constant
        return np.sqrt(x)


def return_same_type(x, val, der, parents):
    """
    Utility function that returns new object of same type as x for forward mode
    objects

    Inputs: a Scal/Vect forward mode object

    Returns: new object (same type as x)
    """
    if isinstance(x, fadScal):  # if input var is a scalar
        return fadScal(val, der, parents)
    else:  # if input var is a vector
        return fadVect(val, der, parents)


def return_same_rev(x, val, inputs):
    """
    Utility function that returns new object of same type as x for reverse mode
    objects

    Inputs: a Scal/Vect reverse mode object

    Returns: new object (same type as x)
    """
    if isinstance(x, revScal):
        return revScal(val, inputs)
    else:
        return revVect(val, inputs)
