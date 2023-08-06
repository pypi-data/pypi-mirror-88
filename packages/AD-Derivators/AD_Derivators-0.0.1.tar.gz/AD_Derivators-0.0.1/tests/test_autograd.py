import numpy as np
from AD_Derivators.functions import autograd, tensor


import pytest

TOL = 1e-9

def input_function1(x):
    return x**2+tensor.log(x)- tensor.exp(x)
def input_function2(x,y):
    return x**3+tensor.sin(y)*x
def input_function3(x,y):
    return x**2+tensor.log(y)- tensor.exp(x)

def input_function4(x,y,z):
    return x+y+z-2

def input_function5(x,y,z):
    return x*y*z 



input1= tensor.Tensor(2)
input2= tensor.Tensor([-1])
input3= tensor.Tensor(np.array([3,1,2]))

ad1 = autograd.AD(2,2,1)
ad2 = autograd.AD(2,3,1)
ad3 = autograd.AD(1,2,3)

def test_build_AD_obj():
    ad1 = autograd.AD(1,2,3)
    assert ad1.num_functions == 1
    assert ad1.num_inputs == 2
    assert ad1.shape == (1,2,3)
    assert ad1.function is None
    assert ad1.jacobian is None
    assert ad1.jvp is None

    ad2 = autograd.AD(2,2)
    assert ad2.num_functions == 2
    assert ad2.num_inputs == 2
    assert ad2.shape == (2,2,1)
    

def test_prepare_inputs():
    
    mat_inputs1 = [[1,2],[3,4]]
    mat_inputs2 = np.random.rand(2,3)
    mat_inputs3 = np.random.rand(1,2,3)
    ad1.add_inputs(mat_inputs1)
    ad2.add_inputs(mat_inputs2)
    ad3.add_inputs(mat_inputs3)
    assert ad1.inputs== [[tensor.Tensor(1),tensor.Tensor(2)],\
    [tensor.Tensor(3),tensor.Tensor(4)]]

    assert ad2.inputs == [[tensor.Tensor(mat_inputs2[0,0]),tensor.Tensor(mat_inputs2[0,1]),tensor.Tensor(mat_inputs2[0,2])],\
                    [tensor.Tensor(mat_inputs2[1,0]),tensor.Tensor(mat_inputs2[1,1]),tensor.Tensor(mat_inputs2[1,2])]]
    
    assert ad3.inputs == [[tensor.Tensor(mat_inputs3[0,0,:]),tensor.Tensor(mat_inputs3[0,1,:])]]



def test_build_function():
    ad1.build_function([input_function2, input_function3])
    ad2.build_function([input_function4, input_function5])
    a1 = ad1.inputs
    x1 = a1[0][0].val[0]
    y1 = a1[0][1].val[0]
    z1 = a1[1][0].val[0]
    h1 = a1[1][1].val[0]

    assert (abs(ad1.jacobian - np.array([[3*x1**2+np.sin(y1), x1*np.cos(y1)],[2*z1-np.exp(z1), 1/h1]])) < TOL).all()


def test_build_function_1():
    with pytest.raises(TypeError):
        ad1.build_function(input_function2, input_function3)

def test_build_function_2():
    with pytest.raises(AssertionError):
        ad1 = autograd.AD(0,0,0)
        ad1.build_function([input_function2, input_function3])

def test_build_function_3():
    with pytest.raises(ValueError):
        ad1 = autograd.AD(2,2,1)
        ad1.build_function([input_function2, input_function3])

def test_run():
    seed1 = [[0.2,0.8]]
    seed2 = np.array([[1,1]])

    res1 = ad1.run(seed1)
    assert (res1 == ad1.jvp).all()
    assert (res1 == ad1.jacobian@np.array(seed1).T).all()

    res2 = ad1.run(seed2)
    assert (res2 == ad1.jvp).all()
    assert (res2 == ad1.jacobian@seed2.T).all()

