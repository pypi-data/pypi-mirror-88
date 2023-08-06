from autodiff.forward import Variable
from autodiff.reverse import Node
import numpy as np

class AutoDiffBase:
    '''
    Class for automatic auto-differentation of functions.

    Calculates outputs values, directional derivatives and jacobians in a lazy fashion 
    (only when requested).

    Reuses calculations wherever it's possible to make it more efficient. 

    ----------------

    Example:

    vals = [1,2,3]
    ders = [1,1,1] 

    inputs_vals = [1,2,3] 
    seed = [1,1,1]
    f1 = lambda inputs: inputs[0]*inputs[2]**2 
    f2 = lambda inputs: np.sin(inputs[1])
    f = np.array([f1, f2])

    autodiff = AutoDiff(f=f, vals=vals) 
    
    autodiff.inputs
    >> [1,2,3]

    autodiff.outputs
    >> [9, 0.9092974268256817]
    
    autodiff.jacobian
    >> [[ 9.          0.          6.        ]
    [-0.         -0.41614684 -0.        ]]

    autodiff.gradient(fn_idx=0))
    >> [9. 0. 6.]

    autodiff.dir_der(seed=seed)
    >> [15.         -0.41614684]
    '''

    def __init__(self, f, vals):
        '''
        Arguments
        ---------
        f: array_like
            List-like output functions. Order preserving.
        vals: array_like 
            List-like initital values for inputs. All output functions will be evaluated at this values.
        ''' 
        if not hasattr(type(vals), '__iter__'):
            raise TypeError('Expected list-like object for `vals`.')
        if not (isinstance(vals[0],int) | isinstance(vals[0],float)):
            raise TypeError('`vals` element type does not match a numeric type.')

        self.f = f
        self.vals = vals
        self._jacobian = []
        self._inputs = []
        self._outputs = [] 

    @property
    def outputs(self, var_idx=None):
        # Lazy calculation
        if not self._outputs:
            # Assert whether this calculations yilds same values as through Variable method in `dir_der`.
            self._outputs = [f_(self.vals) for f_ in self.f]
        
        if not var_idx:
            return self._outputs
        else:
            # Test if our assertions work right
            if not isinstance(var_idx, int):
                raise TypeError('Expected `integer` type for `var_idx`.')
            if var_idx >= len(self._outputs):
                raise IndexError('`var_idx` out of range.')
            return self._outputs[var_idx]

    @property
    def inputs(self, var_idx=None):
        return self.vals
        if not var_idx:
            return self.vals
        else:
            if not isinstance(var_idx, int):
                raise TypeError('Expected `integer` type for `var_idx`.')
            if var_idx >= len(self._outputs):
                raise IndexError('`var_idx` out of range.')
            return self.vals[var_idx]

    @property
    def jacobian(self):
        if len(self._jacobian) == 0:
            self.jac()
        return self._jacobian
        
    def dir_der(self, seed):
        '''
        Calculates the derivative of each output function in the direction of `dir`=`seed`.
        If the `._jacobian` was already calculated, then use it to calculate the directional derivative.
        
        Forward specific: doesn't need the jacobian to make this calculation, though if it exists it will use it.
        Reverse specific: the reverse mode will require the jacobian to be calculated first.

        Arguments
        ---------
        seed: array-like (M,)
            Represents the direction to calculate the derivative of each output function.
            Must have the same dimension as the number of inputs.
            M: number of inputs
        
        Returns
        -------
        list (N,)
            Derivative of each input function in the direction of `seed` vector.
            N: number of functions    
        
        Example
        -------
        N = 2
        M = 3
        
        seed = [1,0,0]
        autodiff.dir_der(seed)
        >> [df1/d_seed, df2/d_seed]
        
        df1/d_seed: scalar (first element) 
        df2/d_seed: scalar (second element)
        
        '''
        
        raise NotImplementedError('Must implement `dir_der` method.')
    
    def jac(self):
        '''
        Calculates the Jacobian.
        
        Jacobian (NxM):
        [[df1/dx1, df1/x2, df1/x3] 
        [df2/dx1, df2/x2, df2/x3]]
        
        Each row corresponds to a function, each column corresponds to an input.

        First column of the jacobian corresponds to the directional derivative of each 
        output function with respect to the seed [1,0...0], seed is of size M.

        Second column of the jacobian corresponds to the directional derivative of each 
        output function with respect to the seed [0,1...0], seed is of size M.

        ....

        Last column of the jacobian corresponds to the directional derivative of each 
        output function with respect to the seed [0,0...1], seed is of size M.
        
        Reverse specific: this function calls *`gradient` to calculate each row
        Forward specific: this function calls `dir_dev` to calculate each column
        
        Returns
        -------
        np.array (N,M)
            N: number of functions
            M: number of inputs

        Example
        -------
        N = 2
        M = 3
        
        inputs = [x1,x2,x3]
        outputs = [f1(inputs), f2(inputs)]
        '''
        raise NotImplementedError('Must implement `jac` method.')
        
    def gradient(self, fn_idx):
        '''
        Creates or pulls a row of the Jacobian
        
        Calculates the derivative of the output function `fn_index` with respect to each input variable.
        >> This is done automatically in reverse-mode by seeding the output functions with unit seed of size N
        
        Arguments
        --------
        fn_idx: int 
            Index of the output function to calculate the gradient.
        
        Returns
        -------
        list (M,)
            M: number of inputs

        Example
        -------
        N = 2
        M = 3
        
        inputs = [x1,x2,x3]
        outputs = [f1(inputs), f2(inputs)]
        
        autodiff.gradient(0)
        >> [df1/dx1, df1/x2, df1/x3]
        '''
        raise NotImplementedError('Must implement `gradient` method.')

class AutoDiffReverse(AutoDiffBase):
    
    def __init__(self, f, vals):
        super().__init__(f,vals)
        
    def dir_der(self, seed):
        if len(self.vals) != len(seed):
            raise Exception('Length of seed should be the same as length of `self.vals`.')
        # Unlike the forward mode, the reverse mode will require the jacobian to be calculated first
        if not len(self._jacobian) > 0:
            self.jac() 
        
        return np.matmul(self._jacobian, seed)
        
    def jac(self):
        N = len(self.f) # number of output functions
        M = len(self.vals) #number of input values
        jacobian = np.zeros((N,M))
        
        for i in range(N): #number of output functions
            # row `i` of the jacobian is set to the corresponding gradient
            jacobian[i,:] = self.gradient(fn_idx = i)
        self._jacobian = jacobian
        
    def gradient(self, fn_idx):
        if len(self._jacobian) > 0:
            # Will save computation if the jacobian already exists and a function idx is provided
            return self._jacobian[fn_idx,:]
        
        else:
            if fn_idx >= len(self.f):
                raise Exception('fn_idx should be less than the length of `self.f`.')
                
            inputs_vars = [Node(val=val) for val in self.vals]
            f_vars = np.array([f_(inputs_vars) for f_ in self.f]) 
            
            # Seed with .grad_value = 1 only for the function at fn_idx and all all others .grad_value = 0
            for i in range(len(f_vars)):
                if i == fn_idx:
                    f_vars[i].grad_value = 1.0
                else:
                    f_vars[i].grad_value = 0
            
            # Get the partial derivative wrt each input
            der = [inputs_.grad() for inputs_ in inputs_vars]
            return der
        
class AutoDiffForward(AutoDiffBase):
    
    def __init__(self, f, vals):
        super().__init__(f,vals)
    
    def dir_der(self, seed):
        if len(self._jacobian) > 0:
            # Will save computation if the jacobian already exists
            return np.matmul(self._jacobian, seed)
        else:    
            if len(self.vals) != len(seed):
                raise Exception('Length of seed should be the same as length of `self.vals`.')

            inputs_vars = [Variable(val=val, der=der) for val, der in zip(self.vals, seed)] 
            self.f_vars = np.array([f_(inputs_vars) for f_ in self.f]) 
            
            if len(self._outputs) == 0: 
                # Independent of seed, every time you call `dir_der` it's gonna yield the same value
                self._outputs = [f_.val for f_ in self.f_vars]
            der = [f_.der for f_ in self.f_vars]
            return der
            
    def jac(self):
        N = len(self.f) # number of output functions
        M = len(self.vals) #number of input values
        jacobian = np.zeros((N,M))

        seeds = np.diag(np.full([M], 1))
        for i in range(M): 
            # column `i` of the jacobian is set to the corresponding direction derivative
            jacobian[:,i] = self.dir_der(seed=seeds[i,:])
        self._jacobian = jacobian

    def gradient(self, fn_idx):
        # jacobian needs to be generated first
        if not len(self._jacobian)>0:
            self.jac()

        # return row of jacobian array
        return self._jacobian[fn_idx,:]
        
class AutoDiff:
    def __init__(self, f, vals, mode='forward'):
        '''
        Arguments
        ---------
        f: array_like
            List-like output functions. Order preserving.
        vals: array_like 
            List-like initital values for inputs. All output functions will be evaluated at this values.
        mode: string (default=`forward`)
            Either `forward` or `backward` mode.
        ''' 
        
        modes = {'forward': AutoDiffForward, 'reverse': AutoDiffReverse}
        if mode not in modes.keys():
           raise ValueError("Invalid autodifferentiation mode.")
        self.__class__ = modes[mode]
        self.__init__(f, vals)
        