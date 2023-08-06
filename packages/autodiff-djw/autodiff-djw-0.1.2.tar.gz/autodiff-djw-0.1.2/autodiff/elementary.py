import autodiff.reverse as r
import autodiff.forward as f
import numpy as np
import scipy.special as ss

def elem_call(a, fn_str, *args, **kwargs):
    default = {
        'log':np.log,
        'exp':np.exp,
        'sin':np.sin,
        'cos':np.cos,
        'tan':np.tan,
        'arcsin':np.arcsin,
        'arccos':np.arccos,
        'arctan':np.arctan,
        'sinh':np.sinh,
        'cosh':np.cosh,
        'tanh':np.tanh,
        'sqrt':np.sqrt,
        'expit':ss.expit
    }
    if isinstance(a, r.Node):
        fn = getattr(r, fn_str)
    elif isinstance(a, f.Variable):
        fn = getattr(f, fn_str)
    else:
        fn = default[fn_str]
    return fn(a, *args, **kwargs)

def log(a, *args, **kwargs):
    return elem_call(a, 'log', *args, **kwargs)
    
def exp(a, *args, **kwargs):
    return elem_call(a, 'exp', *args, **kwargs)
  
def sin(a, *args, **kwargs):
    return elem_call(a, 'sin', *args, **kwargs)

def cos(a, *args, **kwargs):
    return elem_call(a, 'cos', *args, **kwargs)

def tan(a, *args, **kwargs):
    return elem_call(a, 'tan', *args, **kwargs)

def arcsin(a, *args, **kwargs):
    return elem_call(a, 'arcsin', *args, **kwargs)

def arccos(a, *args, **kwargs):
    return elem_call(a, 'arccos', *args, **kwargs)

def arctan(a, *args, **kwargs):
    return elem_call(a, 'arctan', *args, **kwargs)
     
def sinh(a, *args, **kwargs):
    return elem_call(a, 'sinh', *args, **kwargs)
      
def cosh(a, *args, **kwargs):
    return elem_call(a, 'cosh', *args, **kwargs)

def tanh(a, *args, **kwargs):
    return elem_call(a, 'tanh', *args, **kwargs)

def sqrt(a, *args, **kwargs):
    return elem_call(a, 'sqrt', *args, **kwargs)

def expit(a, *args, **kwargs):
    return elem_call(a, 'expit', *args, **kwargs)