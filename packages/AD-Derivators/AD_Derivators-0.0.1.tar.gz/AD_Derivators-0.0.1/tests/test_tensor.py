# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:41:11 2020
@author: Courage
"""

import numpy as np
#import tensor
from AD_Derivators.helper_functions.ad_utils import check_number, check_array, check_list, check_anyzero, check_tan, check_anyneg, isodd
from AD_Derivators.functions import tensor
import pytest

alpha = 2.0
beta = 3.0
a = 2.0
s = "hello"

v1 = tensor.Tensor(val = np.array([0,0,0]))   
v2 = tensor.Tensor(val = np.array([np.pi/2,np.pi/2,np.pi/2]))
v3 = tensor.Tensor(val = np.array([1,1,1]))  
v4 = tensor.Tensor(val = 1)
v5 = tensor.Tensor(val = np.array([-2]))
v6 = tensor.Tensor(val = np.array([np.pi]))
v7 = tensor.Tensor(val = np.array([1,2,3,4]))
v8 = tensor.Tensor(val = np.array([2,3]))

def test_sin_type_error():
    with pytest.raises(TypeError):
        tensor.sin(s)
def test_cos_type_error():
    with pytest.raises(TypeError):
        tensor.cos(s)
def test_tan_type_error():
    with pytest.raises(TypeError):
        tensor.tan(s)
    
def test_sin_result_1():
    val = tensor.sin(v1).val
    der = tensor.sin(v1).der
    v_check = [np.sin(0),np.sin(0),np.sin(0)]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_sin_result_2():
    val = tensor.sin(v6).val
    der = tensor.sin(v6).der
    v_check = [np.sin(np.pi)]
    der_check = [-1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_sin_result_3():
    val = tensor.sin([alpha,beta])
    v_check = np.sin([alpha,beta])
    assert  np.array_equal(val,v_check)
    
    
def test_cos_result():
    val = tensor.cos(v1).val
    der = tensor.cos(v1).der
    v_check = [np.cos(0),np.cos(0),np.cos(0)]
    der_check = [0,0,0]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_cos_result_1():
    val = tensor.cos([alpha,beta])
    v_check = np.cos([alpha,beta])
    assert  np.array_equal(val,v_check)
    
    
def test_tan_result():
    val = tensor.tan(v1).val
    der = tensor.tan(v1).der
    v_check = [np.tan(0),np.tan(0),np.tan(0)] 
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_tan_result_1():

    val = tensor.tan([0,0])
    v_check = np.tan([0,0])
    assert  np.array_equal(val,v_check)

def test_tan_undefined():
    with pytest.raises(ValueError):
        tensor.tan(v2)

def test_tan_undefined_1():
    with pytest.raises(ValueError):
        tensor.tan([np.pi/2,np.pi/2])


def test_asin_type_error():
    with pytest.raises(TypeError):
        tensor.asin(s)
def test_acos_type_error():
    with pytest.raises(TypeError):
        tensor.acos(s)
def test_atan_type_error():
    with pytest.raises(TypeError):
        tensor.atan(s)
        
def test_sinh_type_error():
    with pytest.raises(TypeError):
        tensor.sinh(s)
def test_cosh_type_error():
    with pytest.raises(TypeError):
        tensor.cosh(s)
def test_tanh_type_error():
    with pytest.raises(TypeError):
        tensor.tanh(s)


def test_asin_result_1():
    val = tensor.asin(v1).val
    der = tensor.asin(v1).der
    v_check = [0,0,0]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_asin_result_2():
    with pytest.raises(ValueError):
        tensor.asin(v3)
    
def test_asin_result_3():
    with pytest.raises(ValueError):
        tensor.asin(v8)
        
def test_asin_result_4():
    with pytest.raises(ValueError):
        tensor.asin(alpha)

def test_asin_result_5():
    val = tensor.asin([0,0,0])
    v_check = [0,0,0]
    assert  np.array_equal(val,v_check)

def test_sinh_result():
    val = tensor.sinh(v1).val
    der = tensor.sinh(v1).der
    v_check = [0,0,0]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_sinh_result_1():
    val = tensor.sinh([0,0,0])
    v_check = [0,0,0]
    assert  np.array_equal(val,v_check)

def test_acos_result_1():
    val = tensor.acos(v1).val
    der = tensor.acos(v1).der
    v_check = [np.pi/2,np.pi/2,np.pi/2]
    der_check = [-1, -1, -1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_acos_result_2():
    with pytest.raises(ValueError):
        tensor.acos(v3)
    
def test_acos_result_3():
    with pytest.raises(ValueError):
        tensor.acos(v8)
        
def test_acos_result_4():
    with pytest.raises(ValueError):
        tensor.acos(alpha)
        
def test_acos_result_5():
    val = tensor.acos([0,0,0])
    v_check = [np.pi/2,np.pi/2,np.pi/2]
    assert  np.array_equal(val,v_check)
        
def test_cosh_result():
    val = tensor.cosh(v1).val
    der = tensor.cosh(v1).der
    v_check = [1,1,1]
    der_check = [0,0,0]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_cosh_result_1():
    val = tensor.cosh([0,0,0])
    v_check = [1,1,1]
    assert  np.array_equal(val,v_check)

def test_atan_result():
    val = tensor.atan(v1).val
    der = tensor.atan(v1).der
    v_check = [0,0,0]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_atan_result_1():
    val = tensor.atan([0,0,0])
    v_check = [0,0,0]
    assert  np.array_equal(val,v_check)

def test_tanh_result():
    val = tensor.tanh(v1).val
    der = tensor.tanh(v1).der
    v_check = [0,0,0]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_tanh_result_1():
    val = tensor.tanh([0,0,0])
    v_check = [0,0,0]
    assert  np.array_equal(val,v_check)

def test_exp_result():
    val = tensor.exp(v1).val
    der = tensor.exp(v1).der
    v_check = [1,1,1]
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_exp_result_1():
    val = tensor.exp([0,0,0])
    v_check = [1,1,1]
    assert  np.array_equal(val,v_check)

def test_exp_base_type():
    with pytest.raises(TypeError):
        tensor.exp(v1, s)
        
def test_exp_base_value():
    with pytest.raises(ValueError):
        tensor.exp(v1, -2)
        
def test_exp_type_error():
    with pytest.raises(TypeError):
        tensor.exp(s)
    
def test_log_result():
    val = tensor.log(v3).val
    der = tensor.log(v3).der
    v_check = [0,0,0] 
    der_check = [1,1,1]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_log_result_1():
    val = tensor.log([1,1,1])
    v_check = [0,0,0] 
    assert  np.array_equal(val,v_check)

def test_log_base_type():
    with pytest.raises(TypeError):
        tensor.log(v3, s)
        
def test_log_base_value():
    with pytest.raises(ValueError):
        tensor.log(v3, -2)

def test_log_type_error():
    with pytest.raises(TypeError):
        tensor.log(s)

def test_log_zero():
    with pytest.raises(ValueError):
        tensor.log(v1)
        
def test_log_zero_1():
    with pytest.raises(ValueError):
        tensor.log(0)

def test_log_neg():
    with pytest.raises(ValueError):
        tensor.log(v5)

def test_log_neg_1():
    with pytest.raises(ValueError):
        tensor.log(-1)
        
def test_sigmoid_result():
    val = tensor.sigmoid(v8).val
    der = tensor.sigmoid(v8).der
    v_check = np.array([1/(1+np.e**(-2)), 1/(1+np.e**(-3))])
    der_check = np.array([np.e**(-2)/(1+np.e**(-2))**2, np.e**(-3)/(1+np.e**(-3))**2])

    assert  np.allclose(val,v_check) and np.allclose(der,der_check)

def test_sigmoid_result1():
    with pytest.raises(TypeError):
        tensor.sigmoid(s)
        
def test_sigmoid_result2():
    with pytest.raises(TypeError):
        tensor.sigmoid(v8, t0 = s)  
        
def test_sigmoid_result3():
    with pytest.raises(TypeError):
        tensor.sigmoid(v8, L = s)  
        
def test_sigmoid_result4():
    with pytest.raises(TypeError):
        tensor.sigmoid(v8, k = s)    
        
def test_datatype():
    with pytest.raises(TypeError):
        tensor.Tensor(s)
        
def test_sqrt_result():
    val = tensor.sqrt(v3).val
    der = tensor.sqrt(v3).der
    v_check = [1,1,1] 
    der_check = [0.5,0.5,0.5]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_sqrt_result_1():
    val = tensor.sqrt([1,1,1])
    v_check = [1,1,1]
    assert  np.array_equal(val,v_check)
        
def test_sqrt_result1():
    with pytest.raises(TypeError):
        tensor.sqrt(s)
        
def test_sqrt_result2():
    with pytest.raises(ValueError):
        tensor.sqrt(v5)
        
def test_sqrt_result3():
    with pytest.raises(ValueError):
        tensor.sqrt(v1)
        
def test_sqrt_result4():
    with pytest.raises(ValueError):
        tensor.sqrt(-1)
        
def test_add_result():
    f = v3 + v3
    val = f.val
    der = f.der
    v_check = [2,2,2] 
    der_check = [2,2,2] 
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_add_typeerror():
    with pytest.raises(TypeError):
        v3 + s

def test_radd_result():
    f = v7 + v7
    val = f.val
    der = f.der
    v_check = [2,4,6,8]
    der_check = [2,2,2,2] 
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_radd_typeerror():
    with pytest.raises(TypeError):
        s + v3

def test_sub_result():
    f = v3 - v3 
    val = f.val
    der = f.der
    v_check = [0,0,0]
    der_check = [0,0,0]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_sub_typeerror():
    with pytest.raises(TypeError):
        v3 - s
 
def test_rsub_result():
    f = v4 - v4
    val = f.val
    der = f.der
    v_check = [0]
    der_check = [0]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_rsub_typeerror():
    with pytest.raises(TypeError):
        s - v3

def test_mul_result():
    f = v3 * v3
    val = f.val
    der = f.der
    v_check = [1,1,1] 
    der_check = [2,2,2]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    
def test_mul_typeerror():
    with pytest.raises(TypeError):
        v3 * s

def test_rmul_result():
    f = v3 * v3
    val = f.val
    der = f.der
    v_check = [1,1,1] 
    der_check = [2,2,2]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)

def test_rmul_typeerror():
    with pytest.raises(TypeError):
        s * v3

def test_div_result():
    f = v3 / v3
    val = f.val
    der = f.der
    v_check = [1,1,1] 
    der_check = [0,0,0]
    assert  np.array_equal(val,v_check) and np.array_equal(der,der_check)
    

def test_div_typeerror():
    with pytest.raises(TypeError):
        v3 / s

def test_div_zero():
    with pytest.raises(ZeroDivisionError):
        v3 / v1
    
def test_rdiv_typeerror():
    with pytest.raises(TypeError):
        s / v3

def test_pow_posnum_result():
    x = tensor.Tensor(a)
    f = x**alpha
    assert f.val == 4.0 and f.der == 4.0
    
def test_pow_negnum_result():
    x = tensor.Tensor(1)
    f = x**(-2)
    assert f.val == 1.0 and f.der == -2.0

def test_pow_array_result():
    f = v7 ** 2
    val = f.val
    der = f.der
    v_check = [1, 4, 9, 16]
    der_check = [2, 4, 6, 8]
    assert np.array_equal(val,v_check) and np.array_equal(der, der_check)

def test_pow_result():
    x = tensor.Tensor(a)
    f = x**x
    assert f.val == 4.0 and f.der == 6.772588722239782

def test_pow_typeerror():
    with pytest.raises(TypeError):
        (tensor.Tensor(a))**s
        
def test_pow_zero_valueerror():
    with pytest.raises(ValueError):
        x = tensor.Tensor(np.array([0]))
        x**x
        
def test_pow_neg_valueerror():
    with pytest.raises(ValueError):
        v5**v5

def test_pow_zeroerror():
    with pytest.raises(ZeroDivisionError):
        v1**(-2)

def test_pow_zerovalue():
    x = tensor.Tensor(0)
    f = x**0
    assert f.val == 1 and f.der == 0

def test_rpow_num_result():
    x = tensor.Tensor(a)
    f = alpha**x
    assert f.val == 4.0 and f.der == 4 * np.log(2)
    
def test_rpow_array_result():
    f = 3**v8
    val = f.val
    der = f.der
    v_check = [9, 27]
    der_check = [9.887510598012987, 29.662531794038966]
    assert np.array_equal(val,v_check) and np.array_equal(der, der_check)

def test_rpow_num_valueerror():
    with pytest.raises(ValueError):
        x = tensor.Tensor(a)
        (-3)**x

def test_rpow_array_valueerror():
    with pytest.raises(ValueError):
        (-3)**v8
    
def test_rpow_typeerror():
    with pytest.raises(TypeError):
        s**(tensor.Tensor(a))
        
def test_rpow_valueerror_zero():
    with pytest.raises(ValueError):
        x = tensor.Tensor(np.array([0]))
        x**x

def test_neg__num_result():
    x = tensor.Tensor(2)
    f = -x
    assert f.val == -2.0 and f.der == -1.0
    
def test_neg_array_result():
    f = -v7
    val = f.val
    der = f.der
    v_check = [-1, -2, -3, -4]
    der_check = [-1, -1, -1, -1]
    assert np.array_equal(val,v_check) and np.array_equal(der, der_check)
    
def test_lt_result():
    assert (v1 < v3).all()
    
def test_le_result():
    assert (v1 <= v3).all()
    assert (v1 <= v1).all()
    
def test_gt_result():
    assert (v3 > v1).all()
    
def test_ge_result():
    assert (v3 >= v1).all()
    assert (v3 >= v3).all()
    
def test_eq_result():
    assert v3 == v3

def test_ne_result():
    assert v3 != v1