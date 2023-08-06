import numpy as np
from AutoDiffGroup23andMe import AutoDiff as ad
import math

def sin(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's sin and the derivative of the input's sin
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object


    >>> print(sin(ad.AutoDiff(np.pi)))
    0.0, -1.0
    
    '''
    try:
        return ad.AutoDiff(np.sin(AD_obj.val),AD_obj.der*np.cos(AD_obj.val))
    except AttributeError:
        return np.sin(AD_obj)
    
def arcsin(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's arcsin and the derivative of the input's arcsin
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(arcsin(ad.AutoDiff(0)))
    0.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(np.arcsin(AD_obj.val),AD_obj.der* 1 / (1-AD_obj.val**2)**.5)
    except AttributeError:
        return np.arcsin(AD_obj)
        
def sinh(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's sinh and the derivative of the input's sinh
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(sinh(ad.AutoDiff(0)))
    0.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(np.sinh(AD_obj.val),AD_obj.der*np.cosh(AD_obj.val))
    except AttributeError:
        return np.sinh(AD_obj)
    



def cos(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's cos and the derivative of the input's cos
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(cos(ad.AutoDiff(np.pi)))
    -1.0, 0.0
    
    '''
    try:
        return ad.AutoDiff(np.cos(AD_obj.val),-1*AD_obj.der*np.sin(AD_obj.val))
    except AttributeError:
        return np.cos(AD_obj)


def arccos(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's arccos and the derivative of the input's arccos
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(arccos(ad.AutoDiff(0)))
    1.5708, -1.0
    
    '''
    try:
        return ad.AutoDiff(np.arccos(AD_obj.val),AD_obj.der * -1 / (1-AD_obj.val**2)**.5)
    except AttributeError:
        return np.arccos(AD_obj)
        
def cosh(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's cosh and the derivative of the input's cosh
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(cosh(ad.AutoDiff(0)))
    1.0, 0.0
    
    '''
    try:
        return ad.AutoDiff(np.cosh(AD_obj.val),AD_obj.der*np.sinh(AD_obj.val))
    except AttributeError:
        return np.cosh(AD_obj)


def tan(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's tan and the derivative of the input's tan
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(tan(AutoDiff(np.pi)))
    -0.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(np.tan(AD_obj.val),AD_obj.der*(1/np.cos(AD_obj.val)**2))
    except AttributeError:
        return np.tan(AD_obj)


def arctan(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's arctan and the derivative of the input's arctan
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(arctan(ad.AutoDiff(0)))
    0.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(np.arctan(AD_obj.val),AD_obj.der * 1 / (1+AD_obj.val**2))
    except AttributeError:
        return np.arctan(AD_obj)
        

def tanh(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's tanh and the derivative of the input's tanh
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(tanh(ad.AutoDiff(0)))
    0.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(np.tanh(AD_obj.val),AD_obj.der*(1-np.tanh(AD_obj.val)**2))
    except AttributeError:
        return np.tanh(AD_obj)



def sqrt(AD_obj):
    '''
    Function taking as input an autodiff object or scalar and returning an autodiff object of the input's square root and the derivative of the input's square root
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object

    >>> print(sqrt(AutoDiff(100)))
    10.0, 0.05
    
    '''
    try:
        return ad.AutoDiff(np.sqrt(AD_obj.val), .5 * (1/AD_obj.val**.5) * AD_obj.der)
    except AttributeError:
        return np.sqrt(AD_obj)
    
    
    
def log(AD_obj, base = np.e):
    '''
    Function taking as input an autodiff object or scalar and an optional base and returning an autodiff object of the input's logarithm and the derivative of the input's logarithm. If base is specified, the logarithm's base is set to this value.
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object
    base : int, float, optional (default = np.e)
    
    >>> print(log(AutoDiff(np.e)))
    1.0, 0.3679
    
    '''
    try:
        return ad.AutoDiff(math.log(AD_obj.val, base),(1/(np.log(base)*AD_obj.val)  * AD_obj.der))
    except AttributeError:
        return np.log(AD_obj)
    

def exp(AD_obj, base= np.e):
    '''
    Function taking as input an autodiff object or scalar and an optional base and returning an autodiff object of the base raised to the input and the derivative of the base raised to the input.
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object
    base : int, float, optional (default = np.e)

    >>> print(exp(AutoDiff(0)))
    1.0, 1.0
    
    '''
    try:
        return ad.AutoDiff(base**(AD_obj.val),base**(AD_obj.val) * AD_obj.der)
    except AttributeError:
        return base**(AD_obj)
    
    
def logistic(AD_obj):
    
    '''
    Function taking as input an autodiff object or scalar and an optional base and returning an autodiff object of the input's logistic transformation and the derivative of the input's logistic transformation.
    
    Parameters:
    AD_obj : int, float, ad.AutoDiff object
    

    >>> print(logistic(AutoDiff(0)))
    .5, .25
    
    '''
    try:
        return ad.AutoDiff(1 / (1 + np.exp(-1*AD_obj.val)),
                           (1 / (1 + np.exp(-1*AD_obj.val))) * (1-(1 / (1 + np.exp(-1*AD_obj.val)))) * AD_obj.der)
    except AttributeError:
        return 1 / (1 + np.exp(-1*AD_obj))
    

