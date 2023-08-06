from AAD import AADVariable
import numpy as np

"""
Wrapper class for vector-valued functions in AAD.
"""
class AADFunction:
    """
    Initializer
    
    Example
    ----------

    Accepts input in AADVariables, like
    
    >>> x = AADVariable(1.0, [1.0])
    >>> y = AADVariable(2.0, [0.0, 1.0])
    >>> f = AADFunction([x*y, x+y])
    >>> print(f)
    [AADFunction fun = [2.0, 3.0], der = [[2. 1.]
     [1. 1.]]]
    """
    def __init__(self, fn):
        """
        Get the value of the vector-valued function.

        Input
        -----------
        fn      :function
                function to get the vector-valued function

        Example
        -----
        >>> x = AADVariable(1.0, [1.0])
        >>> y = AADVariable(2.0, [0.0, 1.0])
        >>> f = AADFunction([x*y, x+y])
        >>> print(f.val())
        [2.0, 3.0]
        """
        self.fn = fn
    

    def val(self):
        fn = self.fn
        if isinstance(fn, AADVariable):
            return self.fn.val
        elif isinstance(fn, np.ndarray) or isinstance(fn, list):
            return [v.val for v in self.fn]
        else: # const
            return self.fn


    def der(self):
        """
        Example
        -----------
        Get the Jacobian of the vector-valued function.
        >>> x = AADVariable(1.0, [1.0])
        >>> y = AADVariable(2.0, [0.0, 1.0])
        >>> f = AADFunction([x*y, x+y])
        >>> print(f.der())
        [[2. 1.]
         [1. 1.]]
        """
        fn = self.fn
        if isinstance(fn, AADVariable):
            return self.fn.der
        elif isinstance(fn, np.ndarray) or isinstance(fn, list):
            return np.array([v.der for v in self.fn])
        else: # const
            return 0
    
    def __str__(self):
        return "[AADFunction fun = " + self.val().__str__() + ", der = " + self.der().__str__() + "]"
