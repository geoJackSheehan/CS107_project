"""
Explanation
------------------------------------
Forward and backward auto-differentiation user interface
Items
------------------------------------
AutoDiff: 
    Forward-mode implementation. 
    Internally uses DualNumber objects to track accumulated function value and derivative value. 
    Supports any combination of scalar or vector variables and functions. 
"""

import numpy as np
from bad_package.fad import DualNumber
from bad_package.rad import ReverseMode


class AutoDiff:
    '''
    Explanation
    ------------------------------------
    Class used to implement the forward mode of automatic differentiation. 
    Currently supports scalar and vector instances. 
    Attributes
    ------------------------------------
    f:
        List, ndarray, or single function to implement
    var_list:
        List, ndarray, or single number (argument(s)) to evaluate the function at in forward mode
    len_var_list:
        Number of arguments to calculate (dimensionality)
    trace:
        List of DualNumbers to keep track of the current trace of forward mode
    Methods
    ------------------------------------
    __init__(self, f, var_list)
        Instantiate AutoDiff object
    __repr__(self)
        Easy-to-read object instantiation with memory location
    __str__(self)
        Pretty print of the passed function(s) and variable(s)
    _compute(self)
        Calculate forward mode and get primal and tangent trace
    get_primal(self)
        Return primal trace of forward mode
    get_jacobian(self)
        Return tangent trace of forward mode
    get_var_list(self)
        Getter method of self.var_list
    get_f(self)
        Getter method of self.f
    Raises
    ------------------------------------
    TypeError if f is not callable (a function), list, or ndarray
    TypeError if var_list is not a list, ndarray, int, or float

    Example Driver Script to utilize forward interface
    --------------------------------------------------
    Scalar:
    
    >>> import numpy as np
    >>> from ad_interface import AutoDiff
    >>> def scalar(x):
    >>>     return 4*x + 3
    >>> x = np.array([2])
    >>> ad = AutoDiff(scalar, x)
    >>> print(f'Primal: {ad.get_primal()}')
    Primal: [11]
    >>> print(f'Tangent: {ad.get_jacobian()}')
    Tangent: [[4]]
    Vector:
    
    def vector(x):
        return x[0]**2 + 3*x[1] + 5
    x = np.array([1, 2])
    ad = AutoDiff(vector, x)
    print(f'Primal: {ad.get_primal()}')
    >>> [12]
    print(f'Tangent: {ad.get_jacobian()}')
    >>> [[2, 3]]
    '''
    


    def __init__(self, f, var_list):
        # Flexibility: allow the user to input lists, np.arrays, or single values
        if isinstance(var_list, (list, np.ndarray)):
            var_list = np.array(var_list)
        elif isinstance(var_list, (int, float)):
            var_list = np.array([var_list])
        else:
            raise TypeError(f"Second argument in {print(self)} must be a list or ndarray of integers or float or single integers or floats.")

        if isinstance(f, (list, np.ndarray)):
            f = np.array(f)
        elif callable(f):
            f = np.array([f])
        else:
            raise TypeError(f"First argument in {print(self)} must be a list of ndarray of functions or a single function.")
        
        self.f = f
        self.var_list = var_list
        self.len_var_list = len(var_list)
        self.jacobian = []
        self.primal = []
        
        trace = []
        for variable in var_list:
            trace.append(DualNumber(float(variable), 1))
        self.trace = trace

        # Automatically starts computation, less steps for the user
        self._compute()

    def __repr__(self):
        '''
        Explanation
        ------------------------------------
        Base print of AutoDiff instantiation with passed values and memory location
        Inputs
        ------------------------------------
        None
        ''' 
        return f'AutoDiff({self.f}, {self.var_list}, id: {id(self)})'

    def __str__(self):
        '''
        Explanation
        ------------------------------------
        Pretty print of AutoDiff instantiation with more information
        Inputs
        ------------------------------------
        None
        ''' 
        return f'f: {self.f}, var_list: {self.var_list}'

    def _compute(self):
        '''
        Explanation
        ------------------------------------
        Calculating primal trace and forward tangent trace to store in self.trace
        Inputs
        ------------------------------------
        None
        '''
        # Iterate through all passed functions (same shape)
        for f in self.f:
            if self.len_var_list == 1:
                value = f(self.trace[0])
                self.primal.append(value.real)
                self.jacobian.append(value.dual)
            else:
                value = f(self.trace)
                # Primal trace and tangent trace
                trace, tangent = [], []
                for i in range(self.len_var_list):
                    x = self.trace[i]
                    y = [DualNumber(0, 0)]*self.len_var_list
                    y[i] = x
                    dp = f(y).dual

                    updatedDual = DualNumber(value.real, dp)
                    trace.append(updatedDual)
                    tangent.append(updatedDual.dual)

                # Primal is the function evaluated at the provided point (var_list)
                self.primal.append(value.real)
                # The list of partials for this function added to matrix container
                self.jacobian.append(tangent)

    def get_primal(self):
        '''
        Explanation
        ------------------------------------
        Passed function(s) evaluated at provided coordinates of a given function (primal trace).

        Inputs
        ------------------------------------
        None

        Outputs
        ------------------------------------
        1-D list of shape (# functions, 1)

        Example
        ------------------------------------
        Scalar (1 function passed):

        def scalar(x):
            return x[0]**2 + 3*x[1] + 5
        x = np.array([1, 2])
        ad = AutoDiff(scalar, x)
        print(f'Primal: {ad.get_primal()}')
        >>> [12]

        Vector (2 functions passed):

        def func(x):
            return 4*x + 3
        def func2(x):
            return logBase(x, 2) + exp(x) - e
        x = [2]
        ad = AutoDiff([func, func2])
        print(f'Primal: {ad.get_primal()}')
        >>> [11, 5.67]
        '''
        return self.primal

    def get_jacobian(self):
        '''
        Explanation
        ------------------------------------
        Return  of tangent trace(s) of forward mode. Nested lists correspond to passed function order.
        Values inside the nested lists correspond to the partial derivatives corresponding to passed variable order

        Inputs
        ------------------------------------
        None

        Outputs
        ------------------------------------
        2-D list of shape (# functions, # variables)

        Example
        ------------------------------------
        Scalar (1 function passed):

        def func(x):
            return x[0]**2 + 3*x[1] + 5
        x = np.array([1, 2])
        ad = AutoDiff(func, x)
        print(f'Tangent: {ad.get_jacobian()}')
        >>> [[2,3]]

        Vector (2 functions passed):
        def func(x):
            return x[0]**2 + 3*x[1] + 5
        def func2(x):
            return sin(x[0]) + cos(x[1])
        x = np.array([1, 2])
        f = [func, func2]
        ad = AutoDiff(f, x)
        print(f'Tangent: {ad.get_jacobian()}')
        >>> [[2, 3], [0.54030, -0.90929]]
        '''
        return self.jacobian

    def get_var_list(self):
        '''
        Explanation
        ------------------------------------
        Return var_list passed by user for forward mode

        Inputs
        ------------------------------------
        None

        Outputs
        ------------------------------------
        1-D list of originally passed variables
        '''
        return self.var_list

    def get_f(self):
        '''
        Explanation
        ------------------------------------
        Return function f passed by user for forward mode

        Inputs
        ------------------------------------
        None

        Outputs
        ------------------------------------
        1-D list of originally passed functions
        '''
        return self.f

class ReverseAD:
    
    def __init__(self, f, var_list):
        self.f = f
        self.var_list = var_list
        self.jacobian = []
        self.jacobian_single = 0.0

        try:
            self.len_var_list = len(var_list)
        except TypeError:
            self.len_var_list = 1

        trace = []
        if self.len_var_list > 1:
            for variable in var_list:
                trace.append(ReverseMode(float(variable)))
            self.trace = trace
        self._compute()

    def _compute(self):
        
        #added this
        if isinstance(self.var_list, (int, float)):
            if len(self.f) == 1:
                x = ReverseMode(float(self.var_list))
                z = self.f[0](x)
                z.gradient = 1.0
                self.jacobian_single = x.grad()
                
            else:
                raise TypeError('For multiple functions, variable(s) must be input as numpy array')
                
        elif self.len_var_list == 1:
            for i in range(len(self.f)):
                x = ReverseMode(float(self.var_list[0]))
                z = self.f[i](x)
                z.gradient = 1.0
                self.jacobian.append(x.grad())
                
        elif self.len_var_list > 1:
            for i in range(len(self.f)):
                z = self.f[i](self.trace)
                z.gradient = 1.0
                self.jacobian.append([trace.grad() for trace in self.trace])
                for trace in self.trace:
                    trace.child = []
                    trace.gradient = None
                
        else:
            raise TypeError('Variable list cannot be empty!')

    def get_primal(self):
        raise NotImplementedError('Reverse AutoDiff does not track primal trace.')
        
    def get_jacobian(self):
        if isinstance(self.var_list, (int, float)):
            return self.jacobian_single
        else:
            temp = np.array(self.jacobian)
            self.jacobian = temp.flatten().tolist()
            return self.jacobian
    
    
    
    
    
    