#!/usr/bin/env python3

from FADiff.FADiff import FADiff
from FADiff.fad.Gradients import Scal as fadScal
from FADiff.fad.Matrices import Vect as fadVect
from FADiff.rev.Gradients import Scal as revScal
from FADiff.rev.Matrices import Vect as revVect
import numpy as np


class FuncVect:
    """


    """
    def __init__(self, funcs):
        try:                                   # All fxns all Scal xor all Vect?
            func_type = type(funcs[0])         # Check the first element
            for func in funcs[1:]:
                if type(func) != func_type:    # Check for consistency
                    raise Exception('All functions must be of same type (Scalar '
                                    'or Vector).')
        except Exception:
            raise
        else:
            # Set inputs list based on type (Scal or Vect) of functions
            self._inputs = []
            if func_type is fadScal:
                self._inputs = FADiff._fadscal_inputs
            elif func_type is fadVect:
                self._inputs = FADiff._fadvect_inputs
            elif func_type is revScal:
                self._inputs = FADiff._revscal_inputs
            elif func_type is revVect:
                self._inputs = FADiff._revvect_inputs
            # List of objects (Scal or Vect) used in fxns
            self._f_vect = funcs
            self._input_vars = []  # Get complete list of input vars of f_vect
            for func in funcs:
                try:
                    if func._parents:  # Has parents?
                        for var in func._der.keys():  # Loop through existing roots
                            if var in func._parents:  # If var is in parent/root list
                                self._input_vars.append(var)
                    # Otherwise input var, i.e., f(x) = x?
                    elif func in self._inputs:
                        self._input_vars.append(func)
                except AttributeError:
                    for var in func._inputs.keys():
                        self._input_vars.append(var)
            self._input_vars = list(set(self._input_vars))

    @property
    def val(self):
        func_vals = []
        for func in self._f_vect:   # For each fxn, add its value to list
            func_vals.append(func._val)
        return np.squeeze(np.array(func_vals))  # Return list

    @property
    def der(self):
        all_fxns_jacobs = []
        for func in self._f_vect:
            one_fxn_jacob = []
            try:
                for var, part_der in func._der.items():
                    if var in self._input_vars:
                        one_fxn_jacob.append(part_der)
            except AttributeError:
                func_der = func.der
                idx = 0
                for var in self._inputs:  # Using this keeps order of vars
                    if var in self._input_vars:
                        if var in func._inputs.keys():
                            one_fxn_jacob.append(func_der[idx])
                            idx += 1
                        else:
                            one_fxn_jacob.append(0)
            all_fxns_jacobs.append(one_fxn_jacob)
        return np.squeeze(np.array(all_fxns_jacobs))
