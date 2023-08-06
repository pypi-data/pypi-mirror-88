import numpy as np

class Variable:
    def __init__(self,**kwargs):
        self.val = 0
        self.der = 1    
        
        if 'val' in kwargs:
            self.val = kwargs['val']
        if 'der' in kwargs:
            self.der = kwargs['der']

    def __mul__(self, other):
        out = Variable()
        try:
            out.val = self.val*other.val
            out.der = self.val*other.der + self.der*other.val
        except AttributeError:
            try:
                out.val = self.val*other
                out.der = other*self.der
            except Exception as e:
                # print(e)
                raise TypeError('Multiplication failed: `other` not an `AutoDiffToy` neither a real number.')
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

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
                #print(e)
                raise TypeError('Addition failed: `other` not an `AutoDiffToy` neither a real number.')
        return out
    
    def __radd__(self, other):
        return self.__add__(other)  

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
                # print(e)
                raise TypeError('Subtraction failed: `other` is neither an `AutoDiffToy` nor a real number.')
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
                # print(e)
                raise TypeError('Subtraction failed: `other` is neither an `AutoDiffToy` nor a real number.')
        return out

    def __pow__(self, other):
        out = Variable()
        try:
            out.val = self.val ** other.val
            out.der = (np.log(self.val) + 1) * (self.val ** other.val)
        except Exception as e:
            try:
                out.val = self.val**other
                out.der = other*(self.val**(other-1))*self.der
            except Exception as e:
                raise TypeError('Power raised to the base value failed: `other` is neither an `AutoDiffToy` nor a real number.')
        return out

    def __truediv__(self, other):
        out = Variable()
        try:
            out.val = self.val / other.val
            out.der = (self.der - (self.val / other.val) * other.der) / other.val
        except AttributeError:
            try:
                out.val = self.val / other
                out.der = self.der
            except Exception as e:
                # print(e)
                raise TypeError('Multiplication failed: `other` not an `AutoDiffToy` neither a real number.')
        return out

    def __rtruediv__(self, other):
        out = Variable()
        try:
            out.val = other.val / self.val
            out.der = (other.der - (other.val / self.val) * self.der) / self.val
        except AttributeError:
            try:
                out.val = other / self.val
                out.der = self.der
            except Exception as e:
                # print(e)
                raise TypeError('Multiplication failed: `other` not an `AutoDiffToy` neither a real number.')
        return out

def sin(a):
    out = Variable()
    out.val = np.sin(a.val)
    out.der = np.cos(a.val)*a.der
    return out

def cos(a):
    out = Variable()
    out.val = np.cos(a.val)
    out.der = -np.sin(a.val)*a.der
    return out

def tanh(a):
    out = Variable()
    out.val = np.tanh(a.val)
    out.der = (1 - np.tanh(a.val)**2)*a.der
    return b

def exp(a):
    out = Variable()
    out.val = np.exp(a.val)
    out.der = np.exp(a.val)*a.der
    return out

def log(a, base=None):
    out = Variable()
    out.val = np.log(a.val)
    out.der = (1/a.val)*a.der
    return out
