import numpy as np
from AD_Derivators.functions.tensor import Tensor
from AD_Derivators.helper_functions.ad_utils import check_array, check_number, check_list, check_list_shape
class AD:
    def __init__(self,num_functions, num_inputs, vec_dim = 1):
        """ 
        Initializes the AD object with Tensor inputs and AD mode.

        Args:
        ============
        num_functions (int): number of functions
        num_inputs (int)L number of inputs in each function
        vec_dim: the length of each argument of functions

        ATTRIBUTES:
        ============
        self.inputs (list of Tensor): a list of Tensor objects. 
        self.function (function): the list of functions for automatic differentiation
        self.jacobian (np.ndarray): the jacobian matrix of the inputs given self.function
        self.jvp (np.ndarray): the value of automatic differentiation given inputs, 
                            self.functions at a given direction p
        self.num_functions (int): the number of functions
        self.num_inputs (int): the number of inputs for each function. All should be the same.
        self.shape (tuple): （self.num_functions, self.num_inputs, vec_dim). All vector Tensor should have the same length.
        
        """
        self._num_func = num_functions
        self._num_inputs = num_inputs
        self._vec_dim = vec_dim
        self._inputs = None
        self._func = None
        self._jacobian = None
        self._jvp = None

    @property
    def num_functions(self):
        return self._num_func
    
    @property
    def num_inputs(self):
        return self._num_inputs
    

    
    def _prepare_inputs(self, mat_inputs):
        """
        This function helps user to prepare inputs of AD class by
        giving a list 
        Args:
        =======================
        mat_inputs (list or np.ndarray): a. a 2-d (m x n) list for AD class with m functions, each having n inputs
                            b. a 3-d (m x n x v) list for class with m functions, each having n inputs and each input have a Tensor in length of v
        
        Returns:
        ========================
        res: a 2-d (m x n) list of Tensor 

        """
        if isinstance(mat_inputs, list):
            mat_inputs = np.array(mat_inputs)
        
        assert self._check_shape(mat_inputs)
        
        res = []
   
        for m in range(self.num_functions):
            inp = []
            for n in range(self.num_inputs):
                inp.append(Tensor(mat_inputs[m,n]))
            res.append(inp)
        
        return res

    
    def add_inputs(self, inputs):
        """
        Add inputs for the class. The dimension of inputs should match self.shape.
        Would update self.inputs
        
        Args:
        =================================
        inputs(list or np.ndarray): a 2-d or 3-d array. The dimension should match self.shape.
        
        """

        # always convert list to np.array first
        if isinstance(inputs,list):
            inputs = np.array(inputs)
        # check the dimension
        assert self._check_shape(inputs)
        
        self._inputs = self._prepare_inputs(inputs)
        self._jacobian = None # reset jacobian function



    def build_function(self, input_functions):
        """ Calculates the jacobian matrix given the input functions. 

        !!! No Tensor objects should be used in input_function
        unless it's the input variable

        would update self.functions and self.jacobian and erase self.jvp

        Args
        =========================
        input_functions (list): a list of m functions. each function have n inputs. Each input could
                        be either a scaler or a vector. Each function should have a return vector or scalar with the 
                        same dimension as each input of the functions.

        """
        # check list and length
        assert isinstance(input_functions, list) and len(input_functions) == self._num_func
        

        # check functions
        if all(callable(f) for f in input_functions):
            self._func = input_functions

        else:
            raise TypeError('the input should be a list of callable function')

        if self._inputs is None:
            raise ValueError('No inputs added to AD class.')
        
       
        self._jacobian = []
        for f, inp in zip(self._func, self._inputs):
            devs = []
            if self._vec_dim == 1:
                const_inp = [t.val[0] for t in inp]
            else:
                const_inp = [t.val.tolist() for t in inp]

            for i,t in enumerate(inp):               
                input_values = const_inp.copy()
                input_values[i] = t # only changes the ith element to be Tensor object.
                # calculate partial derivatives
           
                val = f(*input_values)
                

                # check function returns
                if not isinstance(val, Tensor):
                    raise TypeError('The input function should only return a Tensor object')
                
                # if len(tensor) > 1
                if self._vec_dim > 1:
                    devs.append(val.der.tolist())

                # if tensor is a scalar
                else:
                    devs.append(val.der[0])
             
            self._jacobian.append(devs)
        
        # jacobian is an np.ndarray (m x n or m x n x v)
        self._jacobian = np.array(self._jacobian)

        # reset self._jvp
        self._jvp = None
    
    @property
    def inputs(self):
        return self._inputs
    
    def __str__(self):
        """
        Examples
        ================
        ad = autograd.AD(tensor.Tensor(2.0))
        >>> print(ad)
        AD(Tensor([2.0]))
        """
        return f"AD(Tensor({[str(tens) for tens in self._inputs]}))"
    
    def __repr__(self):
        """
        Examples
        ================
        ad = autograd.AD(tensor.Tensor(2.0))
        >>> repr(ad)
        'AD: inputs(Tensor([2.0])), function(None)'       
        """

        return f"AD: inputs({[str(tens) for tens in self._inputs]}), function({str(self._func)})"

    
    @property
    def function(self):
       
        return self._func

    @property
    def jacobian(self):
        """Returns the Jacobian matrix given Tensor inputs and the input functions.
        """
      
        return self._jacobian
        
    @property
    def jvp(self):
        """Returns the dot product between the Jacobian of the given 
           function at the point 
        """
    
        return self._jvp

    def run(self, seed = [[1.0]]):
        """Returns the differentiation results given the mode.
           Right now AD only allows forward mode.
           
           would update self.jvp

        INPUTS
        =======
        seed (list or np.ndarray): shape ==(num_inputs x vec_dim) the direction of differentiation . THE ARRAY HAS TO BE 2D!!!

        RETURNS
        ========
        results (np.ndarray): shape == (num_func x vec_dim)

        """
       
        return self.__forward(seed)
       
    def __forward(self,  seed = [[1.0]]):
        """Returns the differentiation value of the current graph by forward mode.
        
        INPUTS
        =======
        seed (list or np.ndarray): 2-d list or np.ndarray: 
                     a. vec_dim == 1: 1 x num_inputs
                     b. vec_dim > 1: vec_dim x num_inputs
                   

        RETURNS
        ========
        self._jvp (np.ndarray): shape == (num_func x vec_dim)
        """
       
        # always convert list to np.array first
        if isinstance(seed, list):
            seed = np.array(seed)
        if isinstance(seed, np.ndarray) and seed.shape == (self._vec_dim, self.num_inputs):
            pass
        else:
            raise TypeError('seed should be a 2-d (vec_dim x num_inputs) list of numbers ')
    
        self._jvp = self._jacobian@seed.T 
        assert self._jvp.shape == (self._num_func, self._vec_dim)


        return self._jvp
    
    @property
    def shape(self):
        return (self._num_func, self._num_inputs, self._vec_dim)
    
    def get_inputs(self, option = "numpy"):
        """
        option (str): "numpy" or "tensor"

        Returens:
        ===============
        if option == "numpy": returns the np.ndarray format inputs shape: (num_function, num_inputs, vec_dim)
        elif option == "tensor"：returns the same 2d Tensor list as calling self.inputs.
        """
        if option == "tensor":
            return self._inputs

        elif option == "numpy":
            output = []
            for m in range(self.num_functions):
                vec = []
                for n in range(self.num_inputs):
                    vec.append(self._inputs[m][n].val)
                
                output.append(vec)
            return np.array(output)


        else:
            raise IOError("The option should be either numpy or tensor")


    def _check_shape(self, array):
        """
        array(np.ndarray): a 2d or 3d shape np.array

        """
        flag = False
        if isinstance(array, np.ndarray) and len(array.shape) ==2 and array.shape == self.shape[:2]:
            flag = True
        elif isinstance(array, np.ndarray) and len(array.shape) == 3 and array.shape == self.shape:
           flag = True
        
        return flag
    



      
            
    

        





