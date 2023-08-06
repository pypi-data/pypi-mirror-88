import numpy as np

class AutoDiff():
    """Class which performs forward automatic differentiation
    
    ATTRIBUTES
    ==========
    val: the value of the object, can be scalar of vector
    der: the derivative of the object
    Optional
    variables: number of variables used in a multivariable function
    position : position of this variable in the function
    
    EXAMPLES
    ========
    >>>x = AutoDiff(4)
    >>>x.val
    4
    >>>x.der
    1
    >>>f = x**2 +2x
    >>>f.der
    10
    
    >>> x1 = AutoDiff(2,1,2,0)
    >>> x2 = AutoDiff(4,1,2,1)
    >>> f = x1**2 +2*x2
    [4. 2.]
    
    """
    def __init__(self, value, deriv=1.0, variables = 1, position = 0):         
        if isinstance(value, list):
            self.val = np.array([value]).T
            self.der = np.ones((len(self.val),1))*deriv
            
        else:
            self.val = value
            self.der = deriv

        if variables >1:
            try:
                self.der = np.zeros((len(self.val),variables))
                self.der[ : , position] = deriv
            except TypeError:
                 self.der = np.zeros(variables)
                 self.der[position] = deriv
            
    def __neg__(self):
        return AutoDiff(-self.val, -self.der)

    def __add__(self, other):
        try:
            return AutoDiff(self.val+other.val, self.der+other.der)
        except AttributeError:
            return AutoDiff(self.val+other, self.der)
        
    def __radd__(self, other): 
        return self.__add__(other)
          
    def __mul__(self, other):
        try:
            return AutoDiff(self.val*other.val, self.der*other.val + self.val*other.der)
        except AttributeError:
            return AutoDiff(self.val*other, self.der*other)

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        try:
            return AutoDiff(self.val-other.val, self.der-other.der)
        except AttributeError:
            return AutoDiff(self.val-other, self.der)
    
    def __rsub__(self, other): 
        try:
            return AutoDiff(other.val-self.val, other.der-self.der)
        except AttributeError:
            return AutoDiff(other-self.val, -self.der)
    
    def __truediv__(self, other): 
        try:
            return AutoDiff(self.val/other.val, (self.der*other.val - self.val*other.der)/(other.val**2))
        except AttributeError:
            return AutoDiff(self.val/other, self.der/other)
    
    def __rtruediv__(self, other): 
        try:
            return AutoDiff(other.val/self.val, (self.val*other.der- self.der*other.val)/(self.val**2))
        except AttributeError:
            return AutoDiff(other/self.val, -self.der*other/(self.val**2))
    
    def __pow__(self, other):
        try:
            if isinstance(self.val, (np.ndarray, np.generic)):
                self.val = self.val.astype(float)
            return AutoDiff(self.val**other.val, other.val*(self.val**(other.val-1))*self.der+np.log(np.abs(self.val))*(self.val**other.val)*other.der)
        except AttributeError:
            if isinstance(self.val, (np.ndarray, np.generic)):
                self.val = self.val.astype(float)
            return AutoDiff(self.val**other, other*(self.val**(other-1))*self.der)
        
    def __rpow__(self, other):
        try:
            return AutoDiff(other.val**self.val, self.val*(other.val**(self.val-1))*other.der+np.log(np.abs(other.val))*(other.val**self.val)*self.der)
        except AttributeError:
            return AutoDiff(other**self.val, np.log(np.abs(other))*(other**self.val)*self.der)
    
    def __str__(self):
        return 'value: {}, derivative: {}'.format(self.val,self.der)
    
    def __eq__ (self, other):
        try:
            return ((self.val == other.val) and (self.der == other.der))
        except AttributeError:
            return False
    
    def __ne__(self, other):
        try:
            return ((self.val != other.val) or (self.der != other.der))
        except AttributeError:
            return True
    
    def reverse_mode(self):
        # recurse only if the value is not yet cached
        if self.grad_value is None:
            # calculate derivative using chain rule
            self.grad_value = sum(weight * var.reverse_mode()for weight, var in self.children)
        return self.grad_value


def sin(x):
    try:
        return AutoDiff(np.sin(x.val), x.der*np.cos(x.val))
    except AttributeError:
        return np.sin(x)

def cos(x):
    try:
        return AutoDiff(np.cos(x.val), x.der*(-np.sin(x.val)))
    except AttributeError:
        return np.cos(x)

def tan(x):
    try:
        return AutoDiff(np.tan(x.val), x.der*(1/np.cos(x.val)**2))
    except AttributeError:
        return np.tan(x)
    
def arcsin(x):
    try:
        return AutoDiff(np.arcsin(x.val), x.der/(np.sqrt(1-x.val**2)))
    except AttributeError:
        return np.arcsin(x)

def arccos(x):
    try:
        return AutoDiff(np.arccos(x.val), -x.der/(np.sqrt(1-x.val**2)))
    except AttributeError:
        return np.arccos(x)
    
def arctan(x):
    try:
        return AutoDiff(np.arctan(x.val), x.der/((1+x.val**2)))
    except AttributeError:
        return np.arctan(x)

def exp(x):
    try:
        return AutoDiff(np.exp(x.val), x.der*np.exp(x.val))
    except AttributeError:
        return np.exp(x)

def sinh(x):
    try:
        return AutoDiff(np.sinh(x.val), x.der*np.cosh(x.val))
    except AttributeError:
        return np.sinh(x)

def cosh(x):
    try:
        return AutoDiff(np.cosh(x.val), x.der*(np.sinh(x.val)))
    except AttributeError:
        return np.cosh(x)

def tanh(x):
    try:
        return AutoDiff(np.tanh(x.val), x.der*(1-np.tanh(x.val)**2))
    except AttributeError:
        return np.tanh(x)
    
def logistic(x):
    return 1/(1+exp(-x))
    
def log(x,base = np.e):
    try:
        return AutoDiff(np.log(x.val)/np.log(base), (x.der/(x.val*np.log(base))))
    except AttributeError:
        return np.log(x)/np.log(base)
    
def sqrt(x):
    try:
        return AutoDiff(np.sqrt(x.val), (1/2)*x.der/(np.sqrt(x.val)))
    except AttributeError:
        return np.sqrt(x)
        
def jacobian (variables, functions):
    jacobian_array = np.empty((len(functions), len(variables)))                             
    autodiff_list = []
    var_size = len(variables)
    
    for idx_val, val in enumerate(variables):
        autodiff_list.append(AutoDiff(val,1,var_size,idx_val))
        
    for idx_f, function  in enumerate(functions):
        jacobian_array[idx_f] = function(*autodiff_list).der

    return jacobian_array

