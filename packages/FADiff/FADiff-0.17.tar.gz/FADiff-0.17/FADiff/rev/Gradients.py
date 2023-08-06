#!/usr/bin/env python3

from FADiff import FADiff
# import FADiff
import numpy as np


class Scal:
    """
    A class for automatic differentiation (AD) representing reverse mode
    scalar variables
    """
    def __init__(self, val, inputs=None, name=None, new_input=False):
        """
        Inputs:
            val :
                The value of the Scal instance defined by user
            inputs:
                The root inputs of a Scal instance and associated parents and
                their partial derivatives (no chain rule)
            name : str
                the name of the variable defined by the user
            new_input : boolean
                if variable is an input variable
        """
        self._val = val
        if inputs is None:
            inputs = {}
        self._inputs = inputs
        if new_input:
            self._inputs[self] = []
            FADiff._revscal_inputs.append(self)
        self._name = name
        self._tmp_der = 0

    def __add__(self, other):
        """
        Adds self with other (self + other)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, 1]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, 1])
                else:
                    inputs[root] = [[self, 1]]
            return Scal(self._val + other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1]]
            return Scal(self._val + other, inputs)

    def __radd__(self, other):
        """
        Adds other with self (other + self)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtracts other from self (self - other)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, -1]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, 1])
                else:
                    inputs[root] = [[self, 1]]
            return Scal(self._val - other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1]]
            return Scal(self._val - other, inputs)

    def __rsub__(self, other):
        """
        Subtracts self from other (other - self)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        return self.__sub__(other)

    def __mul__(self, other):
        """
        Multiplies self with other (self * other)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, self._val]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, other._val])
                else:
                    inputs[root] = [[self, other._val]]
            return Scal(self._val * other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, other]]
            return Scal(self._val * other, inputs)

    def __rmul__(self, other):
        """
        Multiplies other with self (other * self)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divides self by other (self / other)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
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
            return Scal(self._val / other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, 1 / other]]
            return Scal(self._val / other, inputs)

    def __rtruediv__(self, other):
        """
        Divides other by self (other / self)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        inputs = {}
        for root in self._inputs.keys():
            inputs[root].append([self, -1 * other / (self._val ** 2)])
        return Scal(other / self._val, inputs)

    def __pow__(self, other):
        """
        Raises self the other power (self ** other)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        try:
            inputs = {}
            for root in other._inputs.keys():
                inputs[root] = [[other, np.log(self._val) * self._val ** other._val]]
            for root in self._inputs.keys():
                if root in inputs:
                    inputs[root].append([self, self._val ** (other._val - 1) * other._val])
                else:
                    inputs[root] = [[self, self._val ** (other._val - 1) * other._val]]
            return Scal(self._val ** other._val, inputs)
        except AttributeError:
            inputs = {}
            for root in self._inputs.keys():
                inputs[root] = [[self, self._val ** (other - 1) * other]]
            return Scal(self._val ** other, inputs)

    def __rpow__(self, other):
        """
        Raises other the self power (other ** self)

        Inputs: self (Scal object), other (either Scal object or constant)
        Returns: new Scal object
        """
        inputs = {}
        for root in self._inputs.keys():
            inputs[root] = [[self, np.log(other) * other ** self._val]]
        return Scal(other ** self._val, inputs)

    def __neg__(self):
        """
        Negates self (-self)

        Inputs: self (Scal object)
        Returns: new Scal object
        """
        inputs = {}
        for root in self._inputs.keys():
            inputs[root] = [[self, -1]]
        return Scal(-1 * self._val, inputs)

    ### Comparison Operators ###

    def __eq__(self, other):
        """
        Compares other to self based on key values defined in Scal (in this case
        the value returned from running id() Python built-in on a Scal instance)

        Inputs: self (Scal object), other (Scal object)
        Returns: True if their key values are equal, False otherwise
        """
        if isinstance(other, Scal):
            return self.__key() == other.__key()
        return NotImplemented

    def __ne__(self, other):
        """
        Compares other to self based on key values defined in Scal (in this case
        the value returned from running id() Python built-in on a Scal instance)

        Inputs: self (Scal object), other (Scal object)
        Returns: False if their key values are equal, True otherwise
        """
        if isinstance(other, Scal):
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
        objects like Scal instances into collections based on a way defined by
        the user.

        Returns: a key value to use for hashing
        """
        return hash(self.__key())

    @property
    def val(self):
        """
        Inputs: self (Scal object)
        Returns: NumPy array of values
        """
        return np.squeeze(np.array(self._val))

    @property
    def der(self):
        """
        Returns jacobian wrt all root/parent input vars used

        Inputs: self (Scal object)
        Returns: NumPy array of derivative
        """
        part_ders = []
        for root in FADiff._revscal_inputs:  # Iterating w/this keeps var order
            if root in self._inputs.keys():
                self._tmp_der = 1
                self._back_trace(root)
                part_ders.append(root._tmp_der)
                self._tmp_der = 0
                self._undo_back_trace(root)
        return np.array(part_ders)

    def _back_trace(self, root):
        """
        Performs the backward pass of an evaluation trace for reverse mode wrt
        a particular root of a variable. It does this recursively.

        Inputs: The root to evaluate the backward pass wrt
        Returns: None
        """
        if self._inputs[root]:             # (Base case: no parents @ root)
            for parent, part_der in self._inputs[root]:
                parent._tmp_der += self._tmp_der * part_der
                parent._back_trace(root)

    def _undo_back_trace(self, root):
        """
        Undoes the changes _back_trace() did on self's (and affected parents)
        derivative variables (in this case restoring them back to 0). Like
        _back_trace, this is a recursive method.

        Inputs: The root in which to undo the changes on self wrt
        Returns: None
        """
        if self._inputs[root]:
            for parent, part_der in self._inputs[root]:
                parent._tmp_der = 0
                parent._undo_back_trace(root)
