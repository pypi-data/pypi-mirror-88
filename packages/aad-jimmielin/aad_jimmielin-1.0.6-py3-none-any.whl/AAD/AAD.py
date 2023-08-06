# use pip to install: pip install -r requirements.txt
import numpy as np
import math
import copy

if __name__ != "AAD.AAD": # not running in a package
    from AADUtils import AADUtils
    from AADVariable import AADVariable

def exp(obj: AADVariable) -> AADVariable:
    """ 
    EXP OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.exp(val)
    n_der = der * np.exp(val)
    return AADVariable(n_val,n_der,name=name)

def log(obj: AADVariable) -> AADVariable:
    """
    LOG BASE E OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.log(val)
    n_der = der * 1/(val)
    return AADVariable(n_val,n_der,name=name)

def sin(obj: AADVariable) -> AADVariable:
    """
    SIN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sin(val)
    n_der = np.cos(val) * der
    return AADVariable(n_val,n_der,name=name)

def sinh(obj: AADVariable) -> AADVariable:
    """
    SINH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sinh(val)
    n_der = der * np.cosh(val)
    return AADVariable(n_val,n_der,name=name)

def cos(obj: AADVariable) -> AADVariable:
    """
    COS OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cos(val)
    n_der = der * -np.sin(val)
    return AADVariable(n_val,n_der,name=name)

def cosh(obj: AADVariable) -> AADVariable:
    """
    SINH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cosh(val)
    n_der = der * np.sinh(val)
    return AADVariable(n_val,n_der,name=name)

def tan(obj: AADVariable) -> AADVariable:
    """
    TAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tan(val)
    n_der = der * 1/(np.cos(val)**2)
    return AADVariable(n_val,n_der,name=name)

def tanh(obj: AADVariable) -> AADVariable:
    """
    TANH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tanh(val)
    n_der = der * (1-(np.tanh(val)**2))
    return AADVariable(n_val,n_der,name=name)

def arcsin(obj: AADVariable) -> AADVariable:
    """
    ARCSIN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arcsin(val)
    n_der = der * 1/(np.sqrt(1-(val**2))) # 
    return AADVariable(n_val,n_der,name=name)

def arccos(obj: AADVariable) -> AADVariable:
    """
    ARCCOS OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = der * -1/(np.sqrt(1-(val**2))) #
    return AADVariable(n_val,n_der,name=name)

def arctan(obj: AADVariable) -> AADVariable:
    """
    ARCTAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arctan(val)
    n_der = der * 1/(val**2+1) # 
    return AADVariable(n_val,n_der,name=name)

def sqrt(obj: AADVariable) -> AADVariable:
    """
    ARCTAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sqrt(val)
    n_der = der * 0.5 * 1/(np.sqrt(val))
    return AADVariable(n_val,n_der,name=name)

def abs(obj: AADVariable) -> AADVariable:
    """
    ABSOLUTE VALUE OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.abs(val)
    n_der = der * val/np.abs(val)
    return AADVariable(n_val,n_der,name=name)
