# ROOTFINDER.PY
# This file uses our team's automatic differentiation package to find the roots
# of a given function. 


# THINGS TO DO
# Complete implementation for the root finding methods
# Perhaps include a visualization? 
# Perhaps include some type of automatation for the initial guess that utilizes our derivation package? 
# Double check syntax - tensor vs. AD class
# Consider changing method definitions such that the main class initialization values are set to defaults (this allows the user to change the parameters for each individual numerical method)
# Root counter - count the estimated number of roots over a given domain. Include this? 


# LIBRARIES OF USE
# NOTE THAT THE CHDIR COMMAND SHOULD BE DELETED PRIOR TO FINAL SUBMISSION. IT
# IS HERE SOLELY FOR TESTING PURPOSES
# import os
# os.chdir("C:/Users/DesktopID3412MNY/Desktop/cs107-FinalProject/")
from AD_Derivators.functions import tensor, autograd
import numpy as np
from AD_Derivators.helper_functions import ad_utils
import inspect


# MAIN ROOT FINDER FUNCTION
def root(x0, functions,  x1 = None, tolerance = 1e-9, max_iterations = 100,
               method = "newton", min_diff = None, verbose = 1):
    """
    Args:
    ====================
    x0 (list or np.ndarray): a 1-d or 2-d numpy array matrix for initial guess
         a. 1d: shape == (num_inputs,)
         b. 2d: shape == (num_inputs, vec_dim)
       
    function (list) : A list of callable function with num_inputs inputs for each
        
    tolerance : positive scaler
        How close the estimated root should be to 0. The default is 0.001.
    max_iterations : INT > 0, optional
        Maximum number of iterations the algorithm will be run prior to 
        terminating, which will occur if a value within the tolerance is not 
        found. The default is 100.
    method : STRING, optional
        The name of the root finding algorithm to use. The default is "newton".

    Raises
    ------
    Exception
        An exception is raised if the user enters an algorithm type that is not
        defined in this code base. 

    Returns
    -------
    (dict): {"root": np.ndarray, "iters": int, "case": string}
    """
    
    
    assert isinstance(x0, list) or isinstance(x0, np.ndarray), f"x0 should be a list or np.ndarray"
    assert isinstance(functions, list) and all(callable(f) for f in functions), f"functions should be a list of callable function"
    assert ad_utils.check_number(tolerance) and tolerance > 0, f"Expected tolerance to be a positive number, instead received {type(tolerance)}"
    assert isinstance(max_iterations, int) and max_iterations > 0, f"Expected max_iterations to be a positive integer, instead received {type(max_iterations)}"
    assert isinstance(method, str) 
    assert ad_utils.check_number(min_diff) or (min_diff is None), f"Expected tolerance to be a positive number, instead received {type(min_diff)}"

    if min_diff is None:
        min_diff = tolerance
    elif min_diff > tolerance:
        raise ValueError("Expected the min_diff no less than tolerance")

    method = method.strip().lower()
    
    num_functions = len(functions)
    num_inputs = num_functions #!!!!!
    for f in functions:
        if len(inspect.signature(f).parameters) != num_inputs:
            raise IOError("The number of initialization for each functions should all be same as number of functions")
    # convert x0 to np.array first
    x0 = np.array(x0)
    assert len(x0.shape) < 3, f"we only accept 1 or 2 dimensional input"
    assert x0.shape[0] == num_inputs, f"the dimension of initial guess x0 should match (num_functions,)"
    
    x0 = x0.reshape(num_functions,-1) # expand dimension for 1-dim input
    
    vec_dim = x0.shape[1]

    # expand dim and repeat
    x0 = np.expand_dims(x0, axis=0)
    x0 = np.repeat(x0, num_functions, axis = 0 )
    
    if x1 is None:
        
       
        # build ad class
        ad = autograd.AD(num_functions, num_inputs, vec_dim)
        ad.add_inputs(x0)
        ad.build_function(functions)
        if method == "newton":
            res, iters, case =  _newton(ad, tolerance, max_iterations, min_diff)
        elif method == "broyden1":
            res, iters, case = _broyden_good(ad, tolerance, max_iterations, min_diff)
        elif method == "broyden2":
            res, iters, case = _broyden_bad(ad, tolerance, max_iterations, min_diff)
        
        # elif method == 'steffensen':
        #     res, iters, case = _steffensen(x0, functions, tolerance, max_iterations, min_diff)

        else:
            raise Exception(f"Method \"{method}\" is not a valid solver algorithm when x1 is None")

    else:
        x1 = np.array(x1).reshape(num_functions,-1)
        x1 = np.expand_dims(x1, axis=0)
        x1 = np.repeat(x1, num_functions, axis = 0 )

        assert x1.shape == x0.shape, "the dimension of x0 should match x1"

        if method == "secant":
            
            res, iters, case =  _secant(x0,x1, functions, tolerance, max_iterations, min_diff)
        elif method == "bisection":
            res, iters, case = _bisection(x0,x1, functions,  tolerance, max_iterations, min_diff)
        
        else:
            raise Exception(f"Method \"{method}\" is not a valid solver algorithm when x1 is not None")
    


    if verbose:
        print(f'method: {method}')
        print(f'results: {res}')
        print(f'number of iterations take: {iters}')
        print(case)

    return {'roots': res, 'iters': iters, 'case':case}


def _newton(ad,tolerance, max_iterations, min_diff):
   
    x0 = ad.get_inputs()[0,:,:] # x0 is a np.ndarray (num_inputs, vec_dim)
    case = None
        
    for i in range(max_iterations):

        x = x0 - np.linalg.pinv(ad.jacobian)@_get_fx(x0, ad.function) # x is a np.ndarray (num_inputs, vec_dim)

        if _check_root(x, ad.function, tolerance):
            case = "[PASS] root found"
            return x, i, case
        
        #   converged
        if (np.linalg.norm(x - x0) < min_diff):
            case = "[FAIL] converged"
            return x, i, case

        x0 = x
        
        next_input = np.repeat([x0], ad.num_functions, axis = 0)
        ad.add_inputs(next_input) # update jacobian for next round
        ad.build_function(ad.function) # recalculate jacobian for next step
    case = "[FAIL] maximum iteration reached"
    
    return x, i, case


def _broyden_good(ad, tolerance, max_iterations, min_diff):
    # give the initialization for Jobian inverse
    try:
        J = ad.jacobian
        J_inv = np.linalg.inv(J)
    except: # use identity initialization when jacobian is not invertible
        J_inv = np.eye(ad.num_functions) 

    x0 = ad.get_inputs()[0,:,:] # x0 is a np.ndarray (num_inputs, vec_dim)
    case = None
    f0 = _get_fx(x0, ad.function)
    for i in range(max_iterations):
        
        x = x0 - J_inv@f0

        if _check_root(x, ad.function, tolerance):
            case = "[PASS] root found"
            return x, i, case
        
        #   converged
        if (np.linalg.norm(x - x0)< min_diff):
            case = "[FAIL] converged"
            return x, i, case
        
        delta_x = x - x0
        f = _get_fx(x, ad.function)
        delta_f = f - f0

        # update J_inv, f0, x0
        J_inv = J_inv + np.dot((delta_x - J_inv@delta_f)/np.dot(delta_x.T@J_inv,delta_f), delta_x.T@J_inv)
        f0 = f
        x0 = x

    
    case = "[FAIL] maximum iteration reached"
    
    return x, i, case


def _broyden_bad(ad, tolerance, max_iterations, min_diff):

    #J = ad.jacobian
    try:
        J = ad.jacobian
        J_inv = np.linalg.inv(J)
    except:
        J_inv = np.eye(ad.num_functions) 

    x0 = ad.get_inputs()[0,:,:] # x0 is a np.ndarray (num_inputs, vec_dim)
    case = None
    f0 = _get_fx(x0, ad.function)
        
    for i in range(max_iterations):
        x = x0 - J_inv@f0
        
        if _check_root(x, ad.function, tolerance):
            #print(x,i,case)
            case = "[PASS] root found"
            return x, i, case
        
        #   converged
        if (np.linalg.norm(x - x0) < min_diff):
            case = "[FAIL] converged"
            return x, i, case
        
        delta_x = x - x0
        f = _get_fx(x, ad.function)
        delta_f = f - f0
        J_inv = J_inv + np.dot((delta_x - J_inv@delta_f)/np.power((np.linalg.norm(delta_f)),2), delta_f.T)
        f0 = f
        x0 = x

    
    case = "[FAIL] maximum iteration reached"
    
    return x, i, case


def _check_zero(a):
    """
    make sure no elements in a are 0
    """

    if (a == 0).any():

        a = a.astype(np.float) # convert to float first
    
        for m in range(a.shape[0]):
            for n in range(a.shape[1]):
                if a[m,n] ==0:
                    a[m,n]+= 0.1
                   
    
    return a

    

def _secant(x0,x1, functions,tolerance, max_iterations, min_diff):
    
    if len(functions) > 1:
        raise IOError("The secant method only applys to single function with single variable")
    
    case = None
    x0 = x0.astype(np.float)
    x1 = x1.astype(np.float)
    if x1 == x0:
        x1 = x0 + 0.1
    for i in range(max_iterations):

        # make sure x0 does not equal to x1
        f0 = _get_fx(x0,functions)
        f1 = _get_fx(x1, functions)
        if (f1 - f0 == 0).any():
            case = "[FAIL] Zero division encountered"
            return x1,i,case

        g = (x1-x0)/(f1-f0)

        x = x1 - f1*g

        if _check_root(x, functions, tolerance):
            case = "[PASS] root found"
            return x1,i,case
        
        #   converged
        if (np.linalg.norm(x - x1) < min_diff):
            case = "[FAIL] converged"
            return x1,i,case
        
        x0 = x1
        x1 = x
       
        
    case = "[FAIL] maximum iteration reached"
    
    return x, i, case


def _bisection(x0,x1, functions,tolerance, max_iterations, min_diff):
    """
    Need to make sure x0 < x1 and f(x0)f(x1) <0 
    """
    case = None
    if len(functions) > 1:
        raise IOError("The bisection method only applys to single function with single variable")
    x0 = x0.astype(np.float)
    x1 = x1.astype(np.float)
    x0,x1 = _prepare_bisection(x0,x1,functions)
    
    


    for i in range(max_iterations):
        c= (x0+x1)/2
        if _check_root(c, functions, tolerance):
            case = "[PASS] root found"
            return c, i, case
        
       
        x0,x1 = _update_bisection(x0,x1,c, functions)

        
        #   converged
        if (np.linalg.norm(x1 - x0) < min_diff):
            case = "[FAIL] converged"
            return c, i, case

    case = "[FAIL] maximum iteration reached"
    return c, i, case



def _prepare_bisection(x0,x1, functions):
    """
    make sure all element in x0 < x1 if at the same place
    """

    vec1 = x0[0,:,:]
    vec2 = x1[0,:,:]

    
    res0 = _get_fx(vec1,functions)
    res1 = _get_fx(vec2, functions)

    if (res0*res1 > 0).any():
        raise IOError("For Bisection you need to give inputs that f(x0)f(x1) < 0")


    for m in range(len(vec1)):
        for n in range(len(vec1[0])):
            if vec1[m,n] > vec2[m,n]:
                t = vec1[m,n]
                vec1[m,n] = vec2[m,n]
                vec2[m,n] = t
            
    
    return vec1,vec2 

def _update_bisection(a,b,c, functions):
    """
    a,b,c: num_inputs x vec_dim
    """
    fa = _get_fx(a, functions) # num_functions x vec_dim
    fb = _get_fx(b, functions) # 
    fx = _get_fx(c, functions)

    for m in range(a.shape[0]): 
        for n in range(a.shape[1]):
            
            if fa[m,n]*fx[m,n] > 0: 
        
                a[m,n] = c[m,n]
            elif fb[m,n]*fx[m,n] > 0:
                b[m,n] = c[m,n]
           
        
    return a,b
        
        

def _check_root(x, functions, tolerance):
    """
    x (np.ndarray): a 2-d array, ()
    functions: a list of functions
    tolerance: a positive number
    """
    flag = True
    for f in functions:
        inputs = [x[i] for i in range(len(x))]
        res = f(*inputs) # res is a np.ndarray
        if np.linalg.norm(res) >= tolerance:
            flag = False
            break

    return flag

def _get_fx(x, functions):
    """
    x (np.ndarray): a numpy array ( num_functions, num_inputs, vec_dim)

    """
    output = [] #use list in case the output of root are vectors
    for f in functions:
        inputs = [x[i] for i in range(len(x))]
        res = f(*inputs) # res is a (vec_dim,) np.ndarray
       
        output.append(res) 
       
    return np.array(output) #(num_inputs, vec_dim)

