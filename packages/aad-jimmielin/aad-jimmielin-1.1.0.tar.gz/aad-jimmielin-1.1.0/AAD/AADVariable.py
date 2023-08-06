# use pip to install: pip install -r requirements.txt
import numpy as np
import math
import copy

if __name__ != "AAD.AADVariable": # not running in a package
    from AADUtils import AADUtils
else:
    from AADAADUtils import AADUtils

class AADVariable:
    """ 
    AAD VARIABLE CLASS: 
    PROVIDES OVERRIDEN OPERATORS FOR CORRECT OPERATIONS BETWEEN AAD VARIABLES WITH THEMSELVES AND WITH REAL NUMBERS 
    RETURNS AAD CLASS

    Support for multivariate: self.der now accepts an array or scalar.
    When passing in arrays, the positioning refers to the variable given, i.e.
    AADVariable(val=2.0, der=1.0)   -or- is one variable operation mode, or just "x"
    AADVariable(val=2.0, der=[1.0])
    AADVariable(val=1.5, der=[0.0, 1.0]) refers to "y"

    All calculations will expand the derivative list to the maximum required.
    Scalars or 1-variable case will be handled as an exceptional case, and will return a scalar when requested (the getter will shim this),
    and accept a scalar for the class constructor. However, internally, self.der is always a list. (hplin, 11/27/20)

    Vector-valued functions are not implemented here. Instead, since each element in a vector-valued function is independent,
    they can be handled as a list of AADVariables using an external component. AADVariable is a multivariate-input, scalar-output
    Dual number class in the forward mode.

    Example
    ------------------
    >>> x = AADVariable(1, [1,0])
    >>> y = AADVariable(2, [0,1])

    >>> z1 = x + y
    >>> z2 = z1**2
    >>> z3 = sin(z2)+cos(y)
    >>> z3.val
    -0.004028351305385813
    >>> z3.der
    array([-5.46678157, -6.376079  ])

    """
    def __init__(self, val, der=1.0, name=None):
        '''
        Inputs
        ------------
        val     : float
                value set for the AADVariable.
        der     : float
                derivat
                
        
        '''
        self.name = name
        self.val = val
        if val == 0: der = 0. # check if the value passing in is 0, if so than der must be 0 by definition.

        self.der = der        # this has hidden implications - see der.setter below for the expected behavior.
    
    @property
    def der(self):
        """
        Returns the self.der property. For compatibility, when there is only one variable tracked, it returns a scalar.
        For code that is explicitly aware of this and handles all derivatives as lists, use self._der directly.
        """

        return self._der if len(self._der) > 1 else self._der[0]

    @der.setter
    def der(self, new):
        """Set the derivative. Accepts either a list i.e. [1,2,3], np.array([1,2,3]) or scalar (i.e. 2)"""
        if isinstance(new, list): # accepts list, convert to np.ndarray internally
            self._der = np.array(new)
        elif isinstance(new, np.ndarray):
            self._der = new
        else:
            self._der = np.array([new])

    def jacobian(self):
        """Return the Jacobian (a scalar for a scalar 1-variable function, or a matrix/vector for multivariate)"""
        return self.der


    def __eq__(self, other):
        """
        Equality operator
        """
        if not isinstance(other, AADVariable):
            return False
        
        d1, d2 = AADUtils.align_lists(self._der, other._der)
        res = (self.val == other.val and np.array_equal(d1, d2))
        return res

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        '''
        OVERLOADING NEGATION OPERATOR IE -SELF
        '''
        new = AADVariable(-self.val, -self.der) 
        return new

    def __add__(self, other):
        '''
        OVERLOADING ADDITION OPERATOR IE SELF+OTHER
        '''
        new = AADVariable(self.val)

        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
        new.val = sv + ov
        new.der = sd + od

        return new

    def __mul__(self, other):
        '''
        OVERLOADING THE MULTIPLICATION OPERATOR IE SELF*OTHER
        '''
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)

        ## Computation
        new.val = sv * ov
        new.der = sd * ov + od * sv

        return new

    def __rmul__(self, other):
        '''
        OVERLOADING REVERSE MULTIPLICATION OPERATOR IE OTHER*SELF
        '''
        return self * other
        
    def __radd__(self, other):
        '''
        OVERLOADING REVERSE ADDITION OPERATOR IE OTHER+SELF
        '''
        return self + other

    def __sub__(self, other):
        '''
        OVERLOADING SUBTRACTION WITH NEGATION AND ADDITION IE SELF-OTHER
        '''
        return self + (-other)
    
    def __rsub__(self, other):
        '''
        OVERLOADING REVERSE SUBTRACTION WITH NEGATION AND ADDITION IE OTHER-SELF
        '''
        return -self + other

    def __truediv__(self, other): 
        '''
        OVERLOADING DIVISION OPERATOR IE SELF/OTHER
        '''
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)

        ## Computation
        # (f/g)' = (f'g - g'f)/g**2
        new.val = sv / ov
        new.der = (sd * ov - sv * od)/(ov**2)

        return new

    def __rtruediv__(self, other): 
        '''
        OVERLOADING REVERSE DIVISION OPERATOR IE OTHER/SELF
        '''

        ## Boilerplate: Create new target variable, padd multivariates
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
        ## Computation
        new.val = ov / sv
        new.der = (od * sv - sd * ov)/(sv**2)
        return new

    def __pow__(self, other):
        '''
        OVERLOADING POWER OPERATOR IE SELF**OTHER
        '''
        new = AADVariable(0.0, 0.0)
        try:
            new.val = self.val ** other.val
            new.der = (self.val ** (other.val - 1)) * (self.der * other.val + self.val * math.log(self.val) * other.der)
           #EVALUATING EDGE CASES
        except AttributeError: # just simple case of number...
            new.val = self.val ** other
            new.der = self.val ** (other - 1) * other * self.der
        return new

    def __rpow__(self, other):
        '''
        OVERLOADING REVERSE POWER OPERATOR IE OTHER**SELF
        '''
        new = AADVariable(0.0, 0.0)
        try:
            new.val = other.val ** self.val
           #EVALUATING EDGE CASES
        except AttributeError: # just "simple" case of number... other**self
            new.val = other ** self.val
            new.der = math.log(other) * other**(self.val) * self.der
        return new

    def __repr__(self):
        '''
        OVERLOADING REPR FUNCTION FOR CLEAN DISPLAY
        '''
        return "AADVariable fun = " + str(self.val) + ", der = " + str(self.der) 
