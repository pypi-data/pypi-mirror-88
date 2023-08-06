#!/usr/bin/env python3

# NOTE: See bottom of this module for imported modules/libraries

class FADiff:
    """
    This is the main API class of the package. It acts as an object factory
    from which a user can create objects that are used in automatic
    differentiation (AD) calculations. Each object has @property decorator
    methods called val and der which they can call using the object to get the
    value and derivative/jacobian associated with it.

    Attributes:
        _fadscal_inputs : Scal (forward mode version) list
            Global input scalar vars list, forward mode
        _fadvect_inputs : Vect (forward mode version) list
            Global input vector vars list, forward mode
        _revscal_inputs : Scal (reverse mode version) list
            Global input scalar vars list, reverse mode
        _revvect_inputs : Vect (reverse mode version) list
            Global input vector vars list, reverse mode
        _mode : str
            The mode in which to perform AD ('forward' or 'reverse')
    """
    _fadscal_inputs = []
    _fadvect_inputs = []
    _revscal_inputs = []
    _revvect_inputs = []
    _mode = 'forward'           # Default mode is forward mode

    @staticmethod
    def set_mode(mode):
        """
        This method is used to set the mode in which to perform automatic
        differentiation calculations and for determining which objects to
        return to the user (i.e., forward mode objects or reverse mode ones)

        Inputs:
            mode : str
                'forward' and 'reverse' are valid inputs

        Returns:
            None
        """
        if mode.lower() == 'forward' or mode.lower() == 'reverse':
            FADiff._mode = mode.lower()

    @staticmethod
    def new_scal(val, der=None, name=None):
        """
        This method allows the user to define a new scalar object that
        represents a variable, i.e., an input variable in an evaluation trace
        in AD that is scalar-valued.

        Inputs:
            val : int or float
                A user-defined value
            der : int/float or dict
                The initial derivative of the variable
            name : str
                User-defined name for variable

        Returns:
            A forward or reverse mode Scal instance
        """
        if FADiff._mode == 'forward':
            if not der:               # No der arg?
                der = 1               # Init der to 1
            return _fadScal(val, der=der, name=name, new_input=True)
        elif FADiff._mode == 'reverse':
            return _revScal(val, name=name, new_input=True)

    @staticmethod
    def new_vect(vect, der=None, name=None):
        """
        This method allows the user to define a new vector object that
        represents a variable, i.e., an input variable in an evaluation trace
        in AD that is vector-valued.

        Inputs:
            val : int or float
                A user-defined value
            der : int/float or dict
                The initial derivative of the variable
            name : str
                User-defined name for variable

        Returns:
            A forward or reverse mode Vect instance
        """
        if FADiff._mode == 'forward':
            vect = np.array(vect)
            if not der:                    # No der arg?
                der = np.ones(vect.shape)  # Init der to identity matrix
            return _fadVect(vect, der=der, name=name, new_input=True)
        elif FADiff._mode == 'reverse':
            return _revVect(vect, name=name, new_input=True)

    @staticmethod
    def new_funcvect(func_list):
        """
        This class allows the user to define a vector function where all
        functions in the vector are either all Scal forward mode objects or
        Scal reverse mode objects.

        Inputs:
            func_list : Scal (forward xor reverse mode objects) list
                The list of functions that comprise the vector function

        Returns:
            A FuncVect instance
        """
        return _funcVect(func_list)


# NOTE: Imports intentionally at bottom to prevent circular dependencies
from FADiff.fad.Gradients import Scal as _fadScal
from FADiff.fad.Matrices import Vect as _fadVect
from FuncVect import FuncVect as _funcVect
from FADiff.rev.Gradients import Scal as _revScal
from FADiff.rev.Matrices import Vect as _revVect
# import numpy as np
# import fadScal as _fadScal
# import fadVect as _fadVect
# from FuncVect import FuncVect as _funcVect
# import revScal as _revScal
# import revVect as _revVect

# References:
# - https://www.programiz.com/python-programming/docstrings
