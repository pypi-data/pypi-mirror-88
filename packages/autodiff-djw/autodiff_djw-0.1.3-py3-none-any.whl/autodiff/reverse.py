import numpy as np

class Node:
    def __init__(self, **kwargs):
        self.val = 0
        self.children = [] 
        self.grad_value = None #the adjoint
        
        # QUESTION - HOW DO WE HANDLE CHILDREN IN kwargs?
        if 'val' in kwargs: 
            self.val = kwargs['val']
            
    ### KEY TO THE REVERSE MODE: ###
    # The recursive differentiation function 
    # Source (Adapted From): https://rufflewind.com/2016-12-30/reverse-mode-automatic-differentiation
    def grad(self):
        # Note a non-Node type object tries to access .grad(), it will automatically throw an Attribute Error
        
        # recurse only if the value is not yet cached
        if self.grad_value is None:
            # recursively calculate derivative (adjoint) using chain rule
            self.grad_value = sum(weight * node.grad()
                                  for weight, node in self.children)
        return self.grad_value



    ### MATHEMATICAL OPERATORS AND BASIC OPERATIONS ###
    # 1) Multiplication, 2) Division, 3) Addition, 4) Subtraction, 5) Power, 6) Arithmetic Negation
    
    # 1) Multiplication
    def __mul__(self, other):
        out = Node()
        # Assume `other` is a Node object
        try:
            out.val = self.val*other.val
            self.children.append((other.val, out)) # weight = ∂z/∂self = other.value
            other.children.append((self.val, out)) # weight = ∂z/∂other = self.value
        except AttributeError:
            try:
                out.val = self.val*other
                self.children.append((other, out)) # weight = ∂z/∂self = other.value
            except Exception as e:
                raise TypeError('Multiplication failed: `other` not an `Node` object neither a real number.')
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    # 2) Division
    def __truediv__(self, other):
        out = Node()
        try:
            out.val = self.val / other.val
            self.children.append((1/other.val, out)) # weight = ∂z/∂self = 1/other.value
            other.children.append((-1*self.val/other.val**2, out)) # weight = ∂z/∂other = -1*self.value/ other.value**2
        except AttributeError:
            try:
                out.val = self.val/other
                self.children.append((1/other, out)) # weight = ∂z/∂self = 1/other
            except Exception as e:
                raise TypeError('Division failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __rtruediv__(self, other):
        out = Node()
        
        try:
            out.val = other.val / self.val
            self.children.append((-1*other.val/ self.val**2, out)) # weight = ∂z/∂self = -1*other.value/ self.value**2
            other.children.append((1/self.val, out)) # weight = ∂z/∂other = 1 / self.value
        except AttributeError:
            try:
                out.val = other / self.val
                self.children.append((-1*other/ self.val**2, out)) # weight = ∂z/∂self = -1*other/ self.value**2
            except Exception as e:
                raise TypeError('Reverse Division failed: `self` not an `Node` object neither a real number.')
        
        return out
        
    # 3) Addition
    def __add__(self, other):
        out = Node()
        try:
            out.val = self.val + other.val
            self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            other.children.append((1.0, out)) # weight = ∂z/∂other = 1            
        except AttributeError:
            try:
                out.val = self.val + other
                self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Addition failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __radd__(self, other):
        return self.__add__(other)  
    
    # 4) Subtraction
    def __sub__(self, other):
        out = Node()
        try:
            out.val = self.val - other.val
            self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            other.children.append((-1.0, out)) # weight = ∂z/∂other = -1            
        except AttributeError:
            try:
                out.val = self.val - other
                self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Subtraction failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __rsub__(self, other):
        out = Node()
        try:
            out.val = other.val - self.val
            self.children.append((-1.0, out)) # weight = ∂z/∂self = -1
            other.children.append((1.0, out)) # weight = ∂z/∂other = 1            
        except AttributeError:
            try:
                out.val = other - self.val
                self.children.append((-1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Reverse Subtraction failed: `self` not an `Node` object neither a real number.')
        return out
    
    # 5) Power
    #NOTE left argument (self) MUST BE > 0
    def __pow__(self, other):    
        out = Node()
        try:
            out.val = self.val**other.val
            self.children.append((other.val * self.val ** (other.val - 1), out)) # weight = ∂z/∂self = other.value * self.value ** (other.value - 1)
            other.children.append((self.val ** other.val * np.log(self.val), out)) # weight = ∂z/∂other = self.value ** other.value * log(self.value)
        except AttributeError:
            try:
                out.val = self.val**other
                self.children.append((other * self.val ** (other - 1), out)) # weight = ∂z/∂self = other * self.value ** (other - 1)
            except Exception as e:
                raise TypeError('Power failed: `other` not an `Node` object neither a real number.')
        return out

    def __rpow__(self, other):    
        out = Node()
        try:
            out.val = other.val ** self.val
            self.children.append((other.val ** self.val * np.log(other.val), out)) # weight = ∂z/∂self = self.value ** other.value * log(self.value)
            other.children.append((self.val * other.val ** (self.val - 1), out)) # weight = ∂z/∂other = other.value * self.value ** (other.value - 1)
        except AttributeError:
            try:
                out.val = other ** self.val
                self.children.append((other ** self.val * np.log(other), out)) # weight = ∂z/∂self = self.value ** other.value * log(self.value)
            except Exception as e:
                raise TypeError('Reverse Power failed: `self` not an `Node` object neither a real number.')
        return out
    
    # 6) Negation (Arithmetic)
    def __neg__(self):    
        out = Node()
        try:
            out.val = - self.val
            self.children.append((-1, out)) # weight = ∂z/∂self = -1
        except AttributeError:
            raise TypeError('Negation failed: `input` not an `Node` object or a real number.')
        return out
    
    ### COMPARISON OPERATORS ###
    # 1) Equality, 2) Logical Negation
    
    # 1) Equality
    def __eq__(self, other):
        try:
            out = other.val == self.val
        except AttributeError:
            try:
                out = other == self.val
            except Exception as e:
                raise TypeError('Equality failed: `self` or `other` not an `Node` object neither a real number.')
        return out
    
    # 2) Logical Negation
    def __ne__(self, other):
        try:
            out = other.val != self.val
        except AttributeError:
            try:
                out = other != self.val
            except Exception as e:
                raise TypeError('Equality failed: `self` or `other` not an `Node` object neither a real number.')
        return out    

    
    ### DUNDER INSTANCE METHODS ###
    # 1) len, 2) str, 3) repr, etc.
    
    # 1) Len returns the number of children of the Node object
    def __len__(self):
        return len(self.children)
    
    # 2) String representation of Node object includes value and grad_value
    def __repr__(self):
        return 'Node({!r}, {!r})'.format(self.val, self.grad_value)
    
    # 3) Printable string which provides more information for the Node object
    def __str__(self):
        return 'Node with the following attributes:\nValue: {:.4f} \nGradient value: {:.4f} \nNumber of children: {}'.format(self.val, self.grad_value, self.__len__())
    
### ELEMENTARY AND NUMPY FUNCTIONS ###
# 1) log (i.e. ln), 2) exp, 3) sin, 4) cos, 5) tan, 6) arcsin, 7) arccos, 8) arctan, 9) sinh, 10) cosh, 11) tanh, 12) sqrt

# 1) Logarithm    
def log(a, base = None):
    out = Node()
    if base == None:
        try:
            if a.val == 0:
                out.val = -np.inf
                Print('Logarithm computed on 0; negative infinity returned.')
            else:
                out.val = np.log(a.val)
            a.children.append((1/a.val, out)) # weight = ∂z/∂self = 1 / self
        except AttributeError:
            try:
                out.val = np.log(a)
            except Exception as e:
                raise TypeError('Logarithm failed: `input` not an `Node` object, positive number or a real number.')
    else:
        try:
            out.val = np.log(a.val) / np.log(base)
            a.children.append((1/(a.val*np.log(base)), out)) # weight = ∂z/∂self = 1 / (self*log(b))
        except AttributeError:
            try:
                out.val = np.log(a)/ np.log(base)
            except Exception as e:
                raise TypeError('Logarithm with custom base failed: `input` not an `Node` object, positive number or a real number or the base is not a real number')        
    return out

# 2) Exponent
def exp(a):
    out = Node()
    try:
        out.val = np.exp(a.val)
        a.children.append((np.exp(a.val), out)) # weight = ∂z/∂self = exp(self)
    except AttributeError:
        try:
            out.val = np.exp(a)
        except Exception as e:
            raise TypeError('Exponential failed: `input` not an `Node` object or a real number.')
    return out

# 3) Sin        
def sin(a):
    out = Node()
    try:
        out.val = np.sin(a.val)
        a.children.append((np.cos(a.val), out)) # weight = ∂z/∂self = cos(self)
    except AttributeError:
        try:
            out.val = np.sin(a)
        except Exception as e:
            raise TypeError('Sin failed: `input` not an `Node` object or a real number.')
    return out

# 4) Cos        
def cos(a):
    out = Node()
    try:
        out.val = np.cos(a.val)
        a.children.append((-1*np.sin(a.val), out)) # weight = ∂z/∂self = -sin(self)
    except AttributeError:
        try:
            out.val = np.cos(a)
        except Exception as e:
            raise TypeError('Cos failed: `input` not an `Node` object or a real number.')
    return out

# 5) Tan        
def tan(a):
    out = Node()
    try:
        out.val = np.tan(a.val)
        a.children.append((1/(np.cos(a.val))**2, out)) # weight = ∂z/∂self = 1/(cos(self))^2
    except AttributeError:
        try:
            out.val = np.tan(a)
        except Exception as e:
            raise TypeError('Tan failed: `input` not an `Node` object or a real number.')
    return out

# 6) Arcsin        
def arcsin(a):
    out = Node()
    try:
        out.val = np.arcsin(a.val)
        a.children.append((1/(1-a.val**2)**0.5, out)) # weight = ∂z/∂self = 1/ sqrt(1-x**2)
    except AttributeError:
        try:
            out.val = np.arcsin(a)
        except Exception as e:
            raise TypeError('Arcsin failed: `input` not an `Node` object or a real number.')
    return out

# 7) Arccos        
def arccos(a):
    out = Node()
    try:
        out.val = np.arccos(a.val)
        a.children.append((-1/(1-a.val**2)**0.5, out)) # weight = ∂z/∂self = -1/sqrt(1 - x^2)
    except AttributeError:
        try:
            out.val = np.arccos(a)
        except Exception as e:
            raise TypeError('Arccos failed: `input` not an `Node` object or a real number.')
    return out

# 8) Arctan        
def arctan(a):
    out = Node()
    try:
        out.val = np.arctan(a.val)
        a.children.append((1/(1+a.val**2), out)) # weight = ∂z/∂self = 1/(1 + x^2)
    except AttributeError:
        try:
            out.val = np.arctan(a)
        except Exception as e:
            raise TypeError('Arctan failed: `input` not an `Node` object or a real number.')
    return out

# 9) sinh        
def sinh(a):
    out = Node()
    try:
        out.val = np.sinh(a.val)
        a.children.append((np.cosh(a.val), out)) # weight = ∂z/∂self = cosh(x)
    except AttributeError:
        try:
            out.val = np.sinh(a)
        except Exception as e:
            raise TypeError('sinh failed: `input` not an `Node` object or a real number.')
    return out

# 10) cosh        
def cosh(a):
    out = Node()
    try:
        out.val = np.cosh(a.val)
        a.children.append((np.sinh(a.val), out)) # weight = ∂z/∂self = sinh(x)
    except AttributeError:
        try:
            out.val = np.cosh(a)
        except Exception as e:
            raise TypeError('cosh failed: `input` not an `Node` object or a real number.')
    return out

# 11) tanh        
def tanh(a):
    out = Node()
    try:
        out.val = np.tanh(a.val)
        a.children.append((1/(np.cosh(a.val))**2, out)) # weight = ∂z/∂self = 1/(cosh^2(x))
    except AttributeError:
        try:
            out.val = np.tanh(a)
        except Exception as e:
            raise TypeError('tanh failed: `input` not an `Node` object or a real number.')
    return out

# 12) Square Root
def sqrt(a):
    out = Node()
    try:
        out.val = a.val**0.5
        a.children.append((1./(2*a.val**0.5), out))
    except AttributeError:
        try:
            out.val = a**0.5
        except Exception as e:
            raise TypeError('Square root failed: `input` not an `Node` object or a real number.')   
    return out

# 13) Logistic Sigmoid 
def expit(a):
    out = Node()
    try:
        out.val = 1/(1+np.exp(-a.val))
        a.children.append((1/(1+np.exp(-a.val)), out))
    except AttributeError:
        try:
            return 1/(1+np.exp(-a))
        except Exception as e:
            raise TypeError('Logistic Sigmoid failed: `input` not an `Node` object or a real number.')
    return out
