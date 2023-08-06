import numpy as np

class AutoDiff():
    '''Class for generating objects to perform auto-differentiation and basic operations
    
    Parameters:
    ----------
    val : scalar representing value of object
    der : scalar or numpy.ndarray representing derivative(s) of object, optional (default der = 1.0)
    
    Methods:
    ----------
    Overloads addition, multiplication, negation, subtraction, division, power, equality
    
    '''
    
    def __init__(self, val, der = 1.0):
        self.val = val
        self.der = der
        if hasattr(der, "__len__"):
            if not isinstance(der,np.ndarray):
                raise ValueError('If derivative is not a scalar it must be a Numpy array')
    
    def __add__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = self.val + other.val, der = self.der + other.der)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return self + ad_other
    
    def __radd__(self,other):
        return self.__add__(other)
    
    def __neg__(self):
        return AutoDiff(val = self.val * -1, der = self.der * -1)

    def __mul__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = self.val * other.val, der = self.der * other.val + self.val * other.der)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return self * ad_other
        
    def __rmul__(self,other):
        return self.__mul__(other)        
    
    def __sub__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = self.val - other.val, der = self.der - other.der)
            else:
                raise ValueError('Derivatives are not conformable')         
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return self - ad_other
    
    def __rsub__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = other.val - self.val, der = other.der - self.der)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return ad_other - self
    
    def __truediv__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = self.val / other.val, der = self.der/other.val - self.val*other.der/other.val**2)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return self / ad_other
    
    def __rtruediv__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = other.val / self.val, der = other.der/self.val - other.val*self.der/self.val**2)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return ad_other / self 

    def __pow__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                if self.val == 0:
                    return AutoDiff(0, der = self.der*other.val*(self.val**(other.val-1)))
                else:
                    return AutoDiff(self.val**other.val, der = self.der*other.val*(self.val**(other.val-1))+other.der*np.log(np.abs(self.val))*self.val**other.val)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return self ** ad_other

    def __rpow__(self, other):
        try:
            if _check_conformable_der(self.der, other.der):
                return AutoDiff(val = other.val**self.val, der = other.der*self.val*(other.val**(self.val-1))+other.val**self.val*np.log(other.val)*self.self)
            else:
                raise ValueError('Derivatives are not conformable')           
        except AttributeError:
            ad_other = AutoDiff(other, der = self._make_scalar_der(self.der))
            return ad_other**self
            
    def __eq__(self, other):
        try:
            if hasattr(self.der, "__len__") and hasattr(other.der, "__len__"):
                if len(self.der) == len(other.der) and len(self.der) == sum([1 for i, j in zip(self.der, other.der) if i == j]):
                    return (self.val == other.val) 
            elif hasattr(self.der, "__len__") or hasattr(other.der, "__len__"):
                return False
            else:
                return (self.val == other.val) and (self.der == other.der)
        except AttributeError:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        '''
        defines what to print
        '''
        val = round(self.val,5)
        if isinstance(self.der,np.ndarray):
            der = np.round(self.der,5)
        else:
            der = round(self.der,5)
        return (f'Value: {val}\nGradient: {der}')
    
    def __repr__(self):
        '''
        defines what to show when returned
        '''
        val = round(self.val)
        if isinstance(self.der,np.ndarray):
            der = np.round(self.der, 5)
        else:
            der = round(self.der)
        return (f'AutoDiffVar({val},{der})')

    def _make_scalar_der(self, copy_der):
        if hasattr(copy_der, "__len__"):
            return np.zeros(len(copy_der))
        else:
            return 0

def makeVars(vals, seed = None):
    '''
    utility function that accepts a list of values and an optional list of derivative seeds and returns a list of AutoDiff variables initializated with comformable der attributes.
    
    Parameters:
    ----------
    vals : list or numpy.ndarray of values (must be same length as seeds)
    seed : list or numpy.ndarray of derivatives (must be same length as vals) (default = None)
        if seed is None, the derivatives are initialized at 1 for each AutoDiff in the list
    
    Returns:
    ----------
    ad_vars : a list of AutoDiff variables with values from vals and a derivative vector with all zeros except for the element in the vector corresponding to the AutoDiff object's position in the list, which is initialized at 1
    
    '''
    if hasattr(vals, "__len__") and not seed:
        seed = np.ones(len(vals)) #seed is all ones
    elif hasattr(vals, "__len__") and hasattr(seed, "__len__"):
        if not len(vals) == len(seed):
            raise ValueError('Values must be the same length as seeds')
    else:
        raise ValueError('makeVars requires at least one array')
    ad_vars = []
    for ind, (v, d) in enumerate(zip(vals, seed)):
        der_seed = np.zeros(len(seed))
        der_seed[ind] = d
        ad_vars.append(AutoDiff(v, der_seed))
    return ad_vars

class multivar():
    '''
    class for combining multiple AutoDiff variables
    
    Parameters:
    ----------
    func_list : list or numpy.ndarray of AutoDiff variables
    
    Methods:
    ----------
    makeJacobian : returns the derivatives of the AutoDiff variables stacked in a 2d numpy.ndarray
    makeValList : returns the values of the AutoDiff variables stacked in a 1d numpy.ndarray
    __str__ : overloads the __str__ dunder method which prints rounded values for the value vector and jacobian matrix
    
    '''
    def __init__(self, func_list):
        self.func_list = func_list
    def makeJacobian(self):
        jacobian = []
        for func in self.func_list:
            jacobian.append(func.der)#stick the derivatives together
        return np.stack(jacobian)
    def makeValList(self):
        vallist = []
        for func in self.func_list:
            vallist.append(func.val)#stick the values together
        return np.stack(vallist)
    def __str__(self):
        return(f'Values: {np.round(self.makeValList(),5)}\nJacobian: {np.round(self.makeJacobian(),5)}')

def _check_conformable_der(der1,der2):
    # helper function for checking if two der attributes of AutoDiff variables are the same length.
    if hasattr(der1, "__len__") and hasattr(der2, "__len__"):
        return len(der1) == len(der2)
    elif hasattr(der1, "__len__") or hasattr(der2, "__len__"):
        return False
    else:
        if isinstance(der1, (np.number,int, float)) and isinstance(der2, (np.number,int, float)):
            return True
        else:
            return False