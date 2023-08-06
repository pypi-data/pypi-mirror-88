#!/usr/bin/env python3

import numpy as np
from FADiff.FADiff import FADiff
# import FADiff

class Vect:
    """
    A class for automatic differentiation (AD) for representing vector variables
    (NumPy arrays) in reverse mode
    """
    def __init__(self, val, inputs=None, name=None, new_input=False):
        """
        Inputs:
            val :
                The value of the Vect instance defined by user
            inputs:
                The root inputs of a Vect instance and associated parents and
                their partial derivatives (no chain rule)
            name : str
                the name of the variable defined by the user
            new_input : boolean
                if variable is an input variable
        """
        self._val = np.array(val)
        if inputs is None:
            inputs = {}
        self._inputs = inputs  # Roots of an instance
        if new_input:
            self._inputs[self] = []
            FADiff._revvect_inputs.append(self)
        self._name = name
        self._tmp_der = np.zeros(self._val.shape)

    def __add__(self, other):
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, 1]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, 1])
                else:
                    inputs[root] = [[self, 1]]
            return Vect(self._val + other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1]]
            return Vect(self._val + other, inputs)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, -1]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, 1])
                else:
                    inputs[root] = [[self, 1]]
            return Vect(self._val - other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1]]
            return Vect(self._val - other, inputs)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, self._val]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, other._val])
                else:
                    inputs[root] = [[self, other._val]]
            return Vect(self._val * other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, other]]
            return Vect(self._val * other, inputs)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divides self by other (self / other)

        Inputs: self (Vect object), other (either Vect object or constant)
        Returns: new Vect object
        """
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, -1 * self._val / (other._val ** 2)]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, 1 / other._val])
                else:
                    inputs[root] = [[self, 1 / other._val]]
            return Vect(self._val / other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1 / other]]
            return Vect(self._val / other, inputs)

    def __rtruediv__(self, other):
        """
        Divides other by self (other / self)

        Inputs: self (Vect object), other (either Vect object or constant)
        Returns: new Vect object
        """
        inputs = {}
        for root in self._inputs.keys():
            inputs[root].append([self, -1 * other / (self._val ** 2)])
        return Vect(other / self._val, inputs)

    def __pow__(self, other):
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, np.log(self._val) * self._val ** other._val]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, self._val ** (other._val - 1) * other._val])
                else:
                    inputs[root] = [[self, self._val ** (other._val - 1) * other._val]]
            return Vect(self._val ** other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, self._val ** (other - 1) * other]]
            return Vect(self._val ** other, inputs)

    def __rpow__(self, other):
        inputs = {}
        for root in self._inputs.keys():
            inputs[root] = [[self, np.log(other) * other ** self._val]]
        return Vect(other ** self._val, inputs)

    def __neg__(self):
        inputs = {}
        for root in self._inputs.keys():
            inputs[root] = [[self, -1]]
        return Vect(-1 * self._val, inputs)

    ### Comparison Operators ###

    def __eq__(self, other):
        """
        Compares other to self based on key values defined in Vect (in this case
        the value returned from running id() Python built-in on a Vect instance)

        Inputs: self (Vect object), other (Vect object)
        Returns: True if their key values are equal, False otherwise
        """
        if isinstance(other, Vect):
            return self.__key() == other.__key()
        return NotImplemented

    def __ne__(self, other):
        """
        Compares other to self based on key values defined in Vect (in this case
        the value returned from running id() Python built-in on a Vect instance)

        Inputs: self (Vect object), other (Vect object)
        Returns: False if their key values are equal, True otherwise
        """
        if isinstance(other, Vect):
            return self.__key() != other.__key()
        return NotImplemented

    def __key(self):
        """
        Defines the key value to use, e.g, for hashing Python objects in
        collections.

        Returns: The value of self when id() Python huilt-in is run on it.
        """
        return id(self)

    def __hash__(self):
        """
        Used in conjuction with comparison operators to enable Python to put
        objects like Vect instances into collections based on a way defined by
        the user.

        Returns: a key value to use for hashing
        """
        return hash(self.__key())

    @property
    def val(self):
        return np.array(self._val)

    @property
    def der(self):
        part_ders = []
        for root in FADiff._revvect_inputs:  # Iterating w/this keeps var order
            if root in self._inputs.keys():
                self._tmp_der = np.ones(self._val.shape)
                self._back_trace(root)
                part_ders.append(root._tmp_der)
                self._tmp_der = np.zeros(self._val.shape)
                self._undo_back_trace(root)
        return np.array(part_ders)

    def _back_trace(self, root):
        if self._inputs[root]:  # (Base case: list is empty @ root)
            for parent, part_der in self._inputs[root]:
                parent._tmp_der += self._tmp_der * part_der
                parent._back_trace(root)

    def _undo_back_trace(self, root):
        if self._inputs[root]:
            for parent, part_der in self._inputs[root]:
                parent._tmp_der = np.zeros(self._val.shape)
                parent._undo_back_trace(root)
