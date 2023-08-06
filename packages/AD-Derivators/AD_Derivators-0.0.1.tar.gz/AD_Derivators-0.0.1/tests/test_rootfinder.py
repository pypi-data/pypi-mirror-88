# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:29:50 2020

@author: Courage
"""

from AD_Derivators import rootfinder
from AD_Derivators.functions import autograd, tensor
import numpy as np
import pytest

x0 = np.array([[0,0],[0,0]])
TOL = 1e-6
MIN_DIFF = 1e-5

def f0(x):
    return x**3+1

def f1(x,y):
    return x+y

def f2(x,y):
    return x- y - 4

def f3(x,y):
    return x**2+y**3

def f4(x,y):
    return x + y**2 -2

def f5(x,y):
    return x**5+y**3-9

def f6(x,y):
    return x**2+y-3

def f7(x,y):
    return tensor.exp(x) + 0*y - 1


def test_x0_type():
    with pytest.raises(AssertionError):
        rootfinder.root('hello',[f1,f2])

def test_f_type():
    with pytest.raises(AssertionError):
        rootfinder.root([1,2], f1)

def test_tol_type():
    with pytest.raises(AssertionError):
        rootfinder.root([1,2], [f1,f2], tolerance=-0.01)
        
def test_maxiter_type():
     with pytest.raises(AssertionError):
        rootfinder.root([1,2], [f1,f2], max_iterations=100.5)
        
def test_method_type():
     with pytest.raises(AssertionError):
        rootfinder.root([1,2], [f1,f2], method=1)
        
def test_variable_number():
    with pytest.raises(IOError):
        rootfinder.root([1,2], [f1, f2, f3])

def test_min_diff():
    x0 = [0]
    func = [f0]
    with pytest.raises(ValueError):
        rootfinder.root(x0, func, min_diff=0.1)

def test_x0_dim():
   x = np.array([[[1,2],[2,3]],[[3,4],[4,5]]]) #len(x)==3
   with pytest.raises(AssertionError):
       rootfinder.root(x, [f1, f2])

def test_root_newton():
    x0 = [1]
    func = [f0]
    res = rootfinder.root(x0, func, method = "newton")
    assert (abs(res['roots'] +1) < TOL).all()

def test_root_broyden1():
    x0 = [0]
    func = [f0]
    res= rootfinder.root(x0, func, method = "broyden1")
    assert(abs(res['roots']  +1) < TOL).all()

def test_root_broyden2():
    x0 = [0]
    func = [f0]
    res= rootfinder.root(x0, func, method = "broyden2")
    assert(abs(res['roots']  +1) < TOL).all()
    
def test_exception_error1():
    x0 = [0]
    func = [f0]
    with pytest.raises(Exception):
        rootfinder.root(x0, func, method = "hello")

def test_exception_error2():
    x0 = np.array([-3])
    x1 = np.array([-3])
    functions = [f0]
    with pytest.raises(Exception):
        rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 100, tolerance=  1e-5, method = "hello", min_diff=  1e-6)

def test_check_root():
    flag1 = rootfinder._check_root(np.array([[2], [-2]]), [f1,f2], 0.01)
    flag2 = rootfinder._check_root(np.array([[2], [-3]]), [f1,f2], 0.01)
    assert flag1 
    assert not flag2

def test_get_fx():
    res1 = rootfinder._get_fx(np.array([[2], [-2]]), [f1,f2])
    assert (res1 == np.array([[0],[0]])).all()

    res2 = rootfinder._get_fx(np.array([[-2], [-3]]), [f1,f2])
    assert (res2 == np.array([[-5],[-3]])).all()

def test_newton_1():
    ad_test = autograd.AD(2,2,1)
    x0 = np.array([0,0])
    x0 = np.repeat([x0], 2, axis = 0)
    
    ad_test.add_inputs(x0)
    ad_test.build_function([f1,f2])

    x, it, case = rootfinder._newton(ad_test, TOL, 100, MIN_DIFF)

    assert (abs(x - np.array([[2], [-2]])) < TOL ).all()

def test_newton_2():
   ad_test = autograd.AD(2,2,1)
   x0 = np.array([1,1])
   x0 = np.repeat([x0], 2, axis = 0)
   
   ad_test.add_inputs(x0)
   ad_test.build_function([f5,f6])

   x, it, case = rootfinder._newton(ad_test, TOL, 100, MIN_DIFF)
   a = x[0,0]
   b = x[1,0]

   assert abs(f5(a,b)) < TOL and abs(f6(a,b)) < TOL 

def test_newton_maxreach():
   ad_test = autograd.AD(2,2,1)
   x0 = np.array([1,1])
   x0 = np.repeat([x0], 2, axis = 0)
   
   ad_test.add_inputs(x0)
   ad_test.build_function([f5,f6])

   x, it, case = rootfinder._newton(ad_test, TOL, 2, MIN_DIFF)
   
   assert case == "[FAIL] maximum iteration reached"

def test_broyden1():
    ad_test = autograd.AD(2,2,1)
    x0 = np.array([0,0])
    x0 = np.repeat([x0], 2, axis = 0)
    
    ad_test.add_inputs(x0)
    ad_test.build_function([f3,f4])

    x, it, case = rootfinder._broyden_good(ad_test, TOL, 100, min_diff = 1e-9)

    assert (abs(x - np.array([[1], [-1]])) < TOL ).all()

def test_broyden1_maxreach():
    ad_test = autograd.AD(2,2,1)
    x0 = np.array([0,0])
    x0 = np.repeat([x0], 2, axis = 0)
    
    ad_test.add_inputs(x0)
    ad_test.build_function([f3,f4])

    x, it, case = rootfinder._broyden_good(ad_test, TOL, 2, min_diff = 1e-9)

    assert case == "[FAIL] maximum iteration reached"
    
def test_broyden2():
   ad_test = autograd.AD(2,2,1)
   x0 = np.array([10,10])
   x0 = np.repeat([x0], 2, axis = 0)
   
   ad_test.add_inputs(x0)
   ad_test.build_function([f1,f7])

   x, it, case = rootfinder._broyden_bad(ad_test, TOL, 100, min_diff= 1e-9)

   assert (abs(x - np.array([[0], [0]])) < TOL ).all()

def test_broyden2_maxreach():
    ad_test = autograd.AD(2,2,1)
    x0 = np.array([0,0])
    x0 = np.repeat([x0], 2, axis = 0)
    
    ad_test.add_inputs(x0)
    ad_test.build_function([f3,f4])

    x, it, case = rootfinder._broyden_bad(ad_test, TOL, 2, min_diff = 1e-9)

    assert case == "[FAIL] maximum iteration reached"
 
def test_bisection_IOerror():
   x0 = np.array([-5, 0])
   x1 = np.array([0, -5])
   functions = [f1, f2]
   with pytest.raises(IOError):
       rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 100, tolerance=  1e-5, method = "bisection", min_diff=  1e-6)

def test_bisection():
   x0 = np.array([-5])
   x1 = np.array([0])
   functions = [f0]
   
   x = rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 100, tolerance=  1e-5, method = "bisection", min_diff=  1e-6)
   assert (abs(x["roots"] - np.array([-1])) < 1e-5 ).all()

def test_bisection_maxreach():
   x0 = np.array([-5])
   x1 = np.array([0])
   functions = [f0]
   
   x = rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 2, tolerance=  1e-5, method = "bisection", min_diff=  1e-6)
   assert x.get('case') == "[FAIL] maximum iteration reached"

def test_secant():
   x0 = np.array([-3])
   x1 = np.array([-3])
   functions = [f0]
   x = rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 100, tolerance=  1e-5, method = "secant", min_diff=  1e-6)
   assert (abs(x["roots"] - np.array([[-1]])) < 1e-3 ).all()

def test_secant_IOerror():
   x0 = np.array([-3, 1])
   x1 = np.array([-3, 1])
   functions = [f1, f2]
   with pytest.raises(IOError):
       rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 100, tolerance=  1e-5, method = "secant", min_diff=  1e-6)

def test_secant_maxreach():
   x0 = np.array([-3])
   x1 = np.array([-3])
   functions = [f0]
   res = rootfinder.root(x0 = x0, x1 = x1, functions = functions,  max_iterations = 2, tolerance=  1e-5, method = "secant", min_diff=  1e-6)
   assert res.get('case') == "[FAIL] maximum iteration reached"

def test_check_zero():
    a = np.array([1, 2, 5, 0, 7, 12, 0]).reshape(-1,1) 
    check_a = rootfinder._check_zero(a)
    assert not (check_a == 0).any()

def test_prepare_bisection():
   funcs = [f0]
   x0 = np.array([1])
   x0 = x0.reshape(len(funcs),-1)
   x0 = np.expand_dims(x0, axis=0)
   x0 = np.repeat(x0, len(funcs), axis = 0 )
   x1 = np.array([-2])
   x1 = x1.reshape(len(funcs),-1)
   x1 = np.expand_dims(x1, axis=0)
   x1 = np.repeat(x1, len(funcs), axis = 0 )
   res1,res2 = rootfinder._prepare_bisection(x0, x1, funcs)

   assert res1 == np.array([[[-2]]]) and res2 == np.array([[[1]]])
   
def test_prepare_bisection_IOerror():
   funcs = [f0]
   x0 = np.array([1])
   x0 = x0.reshape(len(funcs),-1)
   x0 = np.expand_dims(x0, axis=0)
   x0 = np.repeat(x0, len(funcs), axis = 0 )
   x1 = np.array([2])
   x1 = x1.reshape(len(funcs),-1)
   x1 = np.expand_dims(x1, axis=0)
   x1 = np.repeat(x1, len(funcs), axis = 0 )
   with pytest.raises(IOError):
       rootfinder._prepare_bisection(x0, x1, funcs)
