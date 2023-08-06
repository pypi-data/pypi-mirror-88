import numpy as np

class Variable:
    def __init__(self,**kwargs):
        self.val = 0
        self.der = 1    
        
        if 'val' in kwargs:
            self.val = kwargs['val']
        if 'der' in kwargs:
            self.der = kwargs['der']

    ### MATHEMATICAL OPERATORS AND BASIC OPERATIONS ###
    # 1) Multiplication, 2) Division, 3) Addition, 4) Subtraction, 5) Power, 6) Arithmetic Negation
    
    # 1) Multiplication
    def __mul__(self, other):
        out = Variable()
        # Assume `other` is a Node object
        try:
            out.val = self.val*other.val
            out.der = self.val*other.der + self.der*other.val
        except AttributeError:
            try:
                out.val = self.val*other
                out.der = other*self.der
            except Exception as e:
                raise TypeError('Multiplication failed: `other` not a `Variable` neither a real number.')
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    # 2) Division
    def __truediv__(self, other):
        out = Variable()
        try:
            out.val = self.val / other.val
            out.der = (other.val*self.der - self.val*other.der) / other.val**2
        except AttributeError:
            try:
                out.val = self.val / other
                out.der = self.der / other
            except Exception as e:
                raise TypeError('Division failed: `other` not a `Variable` neither a real number.')
        return out

    def __rtruediv__(self, other):
        out = Variable()
        try:
            out.val = other.val / self.val
            out.der = (self.val*other.der - other.val*self.der) / self.val**2 
        except AttributeError:
            try:
                out.val = other / self.val
                out.der = (-1*other / self.val**2) * self.der
            except Exception as e:
                raise TypeError('Division failed: `self` not a `Variable` neither a real number.')
        return out

    # 3) Addition
    def __add__(self, other):
        out = Variable()
        try:
            out.val = self.val + other.val
            out.der = self.der + other.der
        except AttributeError:
            try:
                out.val = self.val + other
                out.der = self.der
            except Exception as e:
                raise TypeError('Addition failed: `other` not a `Variable` neither a real number.')
        return out
    
    def __radd__(self, other):
        return self.__add__(other)  

    # 4) Subtraction
    def __sub__(self, other):
        out = Variable()
        try:
            out.val = self.val - other.val
            out.der = self.der - other.der
        except AttributeError:
            try:
                out.val = self.val - other
                out.der = self.der
            except Exception as e:
                raise TypeError('Subtraction failed: `self` is neither a `Variable` nor a real number.')
        return out
    
    def __rsub__(self, other):
        out = Variable()
        try:
            out.val = other.val - self.val
            out.der = other.der - self.der
        except AttributeError:
            try:
                out.val = other - self.val
                out.der = -self.der
            except Exception as e:
                raise TypeError('Subtraction failed: `other` is neither a `Variable` nor a real number.')
        return out

    # 5) Power
    def __pow__(self, other):
        out = Variable()
        try:
            out.val = self.val ** other.val
            # TODO need to check the math
            out.der = (np.log(self.val) + 1) * (self.val ** other.val)
        except Exception as e:
            try:
                out.val = self.val**other
                out.der = other*(self.val**(other-1))*self.der
            except Exception as e:
                raise TypeError('Power failed: `other` is neither a `Variable` nor a real number.')
        return out

    def __rpow__(self, other):
        out = Variable()
        try:
            out.val = other.val ** self.val
            out.der = (np.log(other.val) + 1) * (other.val ** self.val)
        except Exception as e:
            try:
                out.val = other ** self.val
                out.der = (other ** self.val) * np.log(other) * self.der
            except Exception as e:
                raise TypeError('Power  failed: `self` is neither a `Variable` nor a real number.')
        return out

    # 6) Negation (Arithmetic)
    def __neg__(self):
        out = Variable()
        try:
            out.val = - self.val
            out.der = - self.der
        except AttributeError:
            raise TypeError('Negation failed: `input` not a `Variable` object or a real number.')
        return out

    ### COMPARISON OPERATORS ###
    # 1) Equality, 2) Logical Negation
    
    # 1) Equality
    def __eq__(self, other):
        try:
            out = (other.val == self.val) and (other.der == self.der)
        except AttributeError:
            try:
                out = (other == self.val)
            except Exception as e:
                raise TypeError('Equality failed: `self` or `other` not a `Variable` object neither a real number.')
        return out

    # 2) Logical Negation
    def __ne__(self, other):
        try:
            out = ((other.val != self.val) or (other.der != self.der))
        except AttributeError:
            try:
                out = (other != self.val)
            except Exception as e:
                raise TypeError('Equality failed: `self` or `other` not a `Variable` object neither a real number.')
        return out  

    ### DUNDER INSTANCE METHODS ###
    # 1) str, 2) repr, etc.
    
    # 1) String representation of Variable object includes value and derivative
    def __repr__(self):
        return f'Variable({self.val}, {self.der})'
    
    # 2) Printable string which provides more information for the Variable object
    def __str__(self):
        return f'Variable with the following attributes:\nValue: {self.val} \nDerivative value: {self.der}'
    
    ### ELEMENTARY AND NUMPY FUNCTIONS ###
    # 1) log (i.e. ln), 2) exp, 3) sin, 4) cos, 5) tan, 6) arcsin, 7) arccos, 8) arctan, 9) sinh, 10) cosh, 11) tanh, 12) sqrt

# 1) Logarithm 
def log(a, base=None):
    out = Variable()
    if base == None:
        try: 
            if a.val == 0:
                out.val = -np.inf
            else:
                out.val = np.log(a.val)
            out.der = (1/a.val)*a.der
        except AttributeError:
            try:
                out.val = np.log(a)
                out.der = 1./a
            except Exception as e:
                raise TypeError('Logarithm failed: `input` not a `Variable` object, positive number or a real number.')
    else:
        try:
            out.val = np.log(a.val) / np.log(base)
            out.der = 1./(a.val*np.log(base))
        except AttributeError:
            try:
                out.val = np.log(a)
                out.der = 1./(a*np.log(base))
            except Exception as e:
                raise TypeError('Logarithm failed: `input` not a `Variable` object, positive number or a real number.')
    return out

# 2) Exponent
def exp(a):
    out = Variable()
    try:
        out.val = np.exp(a.val)
        out.der = np.exp(a.val)*a.der
    except AttributeError:
        try:
            out.val = np.exp(a)
        except Exception as e:
            raise TypeError('Exponential failed: `input` not a `Variable` object or a real number.')
    return out

# 3) Sin 
def sin(a):
    out = Variable()
    try:
        out.val = np.sin(a.val)
        out.der = np.cos(a.val)*a.der
    except AttributeError:
        try:
            out.val = np.sin(a)
        except Exception as e:
            raise TypeError('Sin failed: `input` not a `Variable` object or a real number.')
    return out

# 4) Cos 
def cos(a):
    out = Variable()
    try:
        out.val = np.cos(a.val)
        out.der = -np.sin(a.val)*a.der
    except AttributeError:
        try:
            out.val = np.cos(a)
        except Exception as e:
            raise TypeError('Cos failed: `input` not a `Variable` object or a real number.')
    return out

# 5) Tan        
def tan(a):
    out = Variable()
    try:
        out.val = np.tan(a.val)
        out.der = (1./(np.cos(a.val))**2)*a.der
    except AttributeError:
        try:
            out.val = np.tan(a)
        except Exception as e:
            raise TypeError('Tan failed: `input` not a `Variable` object or a real number.')
    return out

# 6) Arcsin        
def arcsin(a):
    out = Variable()
    try:
        out.val = np.arcsin(a.val)
        out.der = (1./(1-a.val**2)**0.5)*a.der
    except AttributeError:
        try:
            out.val = np.arcsin(a)
        except Exception as e:
            raise TypeError('Arcsin failed: `input` not a `Variable` object or a real number.')
    return out

# 7) Arccos        
def arccos(a):
    out = Variable()
    try:
        out.val = np.arccos(a.val)
        out.der = (-1./(1-a.val**2)**0.5)*a.der
    except AttributeError:
        try:
            out.val = np.arccos(a)
        except Exception as e:
            raise TypeError('Arccos failed: `input` not a `Variable` object or a real number.')
    return out

# 8) Arctan        
def arctan(a):
    out = Variable()
    try:
        out.val = np.arctan(a.val)
        out.der = (1./(1+a.val**2))*a.der
    except AttributeError:
        try:
            out.val = np.arctan(a)
        except Exception as e:
            raise TypeError('Arctan failed: `input` not a `Variable` object or a real number.')
    return out

# 9) sinh        
def sinh(a):
    out = Variable()
    try:
        out.val = np.sinh(a.val)
        out.der = (np.cosh(a.val))*a.der
    except AttributeError:
        try:
            out.val = np.sinh(a)
        except Exception as e:
            raise TypeError('sinh failed: `input` not a `Variable` object or a real number.')
    return out

# 10) cosh        
def cosh(a):
    out = Variable()
    try:
        out.val = np.cosh(a.val)
        out.der = (np.sinh(a.val))*a.der
    except AttributeError:
        try:
            out.val = np.cosh(a)
        except Exception as e:
            raise TypeError('cosh failed: `input` not a `Variable` object or a real number.')
    return out

# 11) Tanh
def tanh(a):
    out = Variable()
    try:
        out.val = np.tanh(a.val)
        out.der = (1/(np.cosh(a.val))**2)*a.der
    except AttributeError:
        try:
            out.val = np.tanh(a)
        except Exception as e:
            raise TypeError('tanh failed: `input` not a `Variable` object or a real number.')
    return out

# 12) Square Root
def sqrt(a):
    out = Variable()
    try:
        out.val = a.val**0.5
        out.der = (1./2*a.val**0.5)*a.der
    except AttributeError:
        try:
            out.val = a**0.5
        except Exception as e:
            raise TypeError('Square root failed: `input` not a `Variable` object or a real number.') 
    return out  

# 13) Logistic Sigmoid
def expit(a):
    out = Variable()
    try:
        out.val = 1./(1+np.exp(-a.val))
        out.der = (1./(1+np.exp(-a.val)))*a.der
    except AttributeError:
        try:
            return 1./(1+np.exp(-a))
        except Exception as e:
            raise TypeError('Logistic Sigmoid failed: `input` not a `Variable` object or a real number.')
    return out

