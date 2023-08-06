# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:58:22 2020
@author: Courage and Ethan
"""
import numpy as np
from AD_Derivators.helper_functions.ad_utils import check_number, check_array, check_list, check_anyzero, check_tan, check_anyneg, check_nontensor_input
"""
tensor.py
derivative rules for elementary operations.
"""

def sin(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """

    if check_nontensor_input(t):
        return np.sin(t)
    elif isinstance(t,Tensor):
        pass
    else: 
        raise TypeError('The input of tensor.sin can only be a Tensor/list/np.array/number.')
    
    ob = Tensor()
    #new func val
    ob._val = np.sin(t._val)
    #chain rule
    ob._der = np.cos(t._val)* t._der
    
    return ob
def cos(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """
    if check_nontensor_input(t):
        return np.cos(t)
    elif isinstance(t,Tensor):
        pass
    else:
        raise TypeError('The input of tensor.cos can only be a Tensor/list/np.array/number.')

    ob = Tensor()
    #new func val
    ob._val = np.cos(t._val)
    #chain rule
    ob._der = -np.sin(t._val)* t._der
    return ob

def tan(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """

    if check_nontensor_input(t):
        if not check_tan(t):
            return np.tan(t)
        else:
            raise ValueError('Tan undefined')
        
    elif isinstance(t,Tensor):
        if check_tan(t._val):
            raise ValueError('Tan undefined')
    else:
        raise TypeError('The input of tensor.tan can only be a Tensor/list/np.array/number.')
    
    ob = Tensor()
    #new func val
    ob._val = np.tan(t._val)
    #chain rule
    ob._der = t._der/(np.cos(t._val)**2)
    
    return ob


def asin(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """

    if check_nontensor_input(t):
        t = np.array(t)
        if (t > 1).any() or (t < -1).any():
            raise ValueError('The value of asin is undefined outside of 1 or -1')    
        else:
            return np.arcsin(t)

    elif isinstance(t,Tensor):
        if (t._val == 1).any() or (t._val == -1).any():
            raise ValueError('The derivative of asin is undefined at 1 or -1')
    
        elif (t._val > 1).any() or (t._val < -1).any():
            raise ValueError('The value of asin is undefined outside of 1 or -1')    

        else:
            ob = Tensor()
            #new func val
            ob._val = np.arcsin(t._val)
            #chain rule
            ob._der = 1/(np.sqrt(1 - t._val**2))* t._der
            
            return ob    
                

    else:
        raise TypeError('The input of tensor.asin can only be a Tensor/numpy/list/scaler object.')


    
    

def sinh(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """
    if check_nontensor_input(t):
        t = np.array(t)
        return np.sinh(t)
    elif isinstance(t,Tensor):
        ob = Tensor()
        #new func val
        ob._val = np.sinh(t._val)
        #chain rule
        ob._der = np.cosh(t._val)* t._der
        
        return ob 

    else:
        raise TypeError('The input of tensor.sinh can only be a Tensor/numpy/list/scaler object.')
    
    

def acos(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """

    if check_nontensor_input(t):
        t = np.array(t)
        if (t > 1).any() or (t < -1).any():
            raise ValueError('The value of acos is undefined outside of 1 or -1')    
        else:
            return np.arccos(t)

    elif isinstance(t,Tensor):
        if (t._val == 1).any() or (t._val == -1).any():
            raise ValueError('The derivative of acos is undefined at 1 or -1')
    
        elif (t._val > 1).any() or (t._val < -1).any():
            raise ValueError('The value of acos is undefined outside of 1 or -1')    

        else:
            ob = Tensor()
            #new func val
            ob._val = np.arccos(t._val)
            #chain rule
            ob._der = -1/(np.sqrt(1 - t._val**2))* t._der
            
            return ob
                
    else:
        raise TypeError('The input of tensor.acos can only be a Tensor/numpy/list/scaler object.')



def cosh(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """
    if check_nontensor_input(t):
        t = np.array(t)
        return np.cosh(t)
    elif isinstance(t,Tensor):
        ob = Tensor()
        #new func val
        ob._val = np.cosh(t._val)
        #chain rule
        ob._der = np.sinh(t._val)* t._der
        
        return ob 

    else:
        raise TypeError('The input of tensor.cosh can only be a Tensor/numpy/list/scaler object.')

    

def atan(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """
    if check_nontensor_input(t):
        t = np.array(t)
        return np.arctanh(t)
    elif isinstance(t,Tensor):

        ob = Tensor()
        #new func val
        ob._val = np.arctan(t._val)
        #chain rule
        ob._der = t._der/(1 + t._val**2)
        
        return ob
    else:
        raise TypeError('The input of tensor.atah can only be a Tensor/numpy/list/scaler object.')


def tanh(t):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    """
    if check_nontensor_input(t):
        t = np.array(t)
        return np.tanh(t)
    elif isinstance(t,Tensor):
        ob = Tensor()
        #new func val
        ob._val = np.tanh(t._val)
        #chain rule
        ob._der = t._der* (1/np.cosh(t._val))**2
        
        return ob 

    else:
        raise TypeError('The input of tensor.tanh can only be a Tensor/numpy/list/scaler object.')




def exp(t, base = np.e):
    """
    Input
    =========
    t (tensor.Tensor/numpy/list/scaler)
    base (scaler)
    """
    
    if not check_number(base):
        raise TypeError('The base must be a scaler.')

    if check_nontensor_input(t): # no need to worry if base nonpositive
        return np.power(base,t)

    elif isinstance(t,Tensor):
        if base <=0:
            raise ValueError('The base must be positive, otherwise derivation undefined')
    else:
        raise TypeError('The input of tensor.exp can only be a Tensor/list/np.array/number.')

    ob = Tensor()
    #new func val
    ob._val = np.power(base,t._val)
    #chain rule
    ob._der = np.power(base,t._val) * t._der * np.log(base)
    
    return ob

def log(t, a = np.e):
    """
    Input
    =========
    t (tensor.Tensor)
    """
    if not check_number(a):
        raise TypeError('The base should be a scaler')

    if a <= 0:
        raise ValueError('The base must be positive')

    if check_nontensor_input(t):
        t = np.array(t)
        if (t <= 0).any():
            raise ValueError('log undefined')
        else:
            return np.log(t)

    elif isinstance(t,Tensor):
        if check_anyneg(t._val):
            raise ValueError('Log undefined')
        else:
            #create object for output and derivative
            ob = Tensor()
            #new func val
            ob._val = np.log(t._val)/np.log(a)
            #chain rule
            ob._der = (1/(t._val*np.log(a)))*t._der
            
            return ob
    else:
        raise TypeError('The input of tensor.log can only be a Tensor/list/np.array/number.')



def sigmoid(t, t0 = 0, L = 1, k = 1):
    """
    A logistic function or logistic curve is a common S-shaped curve (sigmoid curve) with equation
    f(t) = L/(1+exp(-k(t-t0)))
    Input
    =========
    t needs to be a tensor.Tensor object
    t0 is the x value of the sigmoid's midpoint. The default value is 0.
    L is the curve's maximum value.
    k is the logistic growth rate or steepness of the curve.
    """
    if not isinstance(t,Tensor):
        raise TypeError('The input of tensor.sigmoid can only be a Tensor object.')
    if not check_number(t0):
        raise TypeError('t0 must be either an int or float')
    if not check_number(L):
        raise TypeError('L must be either an int or float')
    if not check_number(k):
        raise TypeError('k must be either an int or float')
        
    #create object for output and derivative
    ob = Tensor()
    #new func val
    ob._val = L / (1+np.exp(-k * (t._val - t0)))
    #chain rule
    ob._der = t._der * (L * k * np.exp(-k * (t._val - t0))) / (1 + np.exp(-k * (t._val - t0)))**2
    
    return ob

def sqrt(t):
    """
    The function used to calculate the square root of a non-negative variable.
    Input
    ============
    t needs to be a tensor.Tensor object. All the elements must be non-negative.
    """

    if check_nontensor_input(t):
        t = np.array(t)
        if (t < 0).any():
            raise ValueError('The constant input must be all nonnegative value, no complex number allowed')
        else:
            return np.sqrt(t)
        
    elif isinstance(t,Tensor):
        
        if check_anyneg(t):
            raise ValueError('The input must be all positive value, no complex number allowed')
        else:
            ob = Tensor()
            ob._val = t._val**(0.5)
            ob._der = 0.5* t._val**(-0.5) * t._der
            
            return ob
    
    else:
        raise TypeError('The input of tensor.sqrt can only be a Tensor/list/number/np.ndarray object.')
        
    


    

class Tensor:
    def __init__ (self, val = np.array([1.0])):
        """
        Initialize Tensor object.
        val (scalar/list/np.ndarray)
        Attributes:
        =============
        self.val (number): the value of the Tensor
        self.der (number): the derivative of the Tensor
        Example
        =============
        >>> a = Tensor(2.0)
        >>> print(a.val)
        2.0
        >>> print(a.der)
        1.0
        >>> a.der = 2
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        AttributeError: can't set attribute
    
        """

        #check inputs
        if check_number(val):
            self._val = np.array([val])
        elif check_list(val):
            self._val = np.array(val)
        elif check_array(val):
            self._val = val
        else:
            raise TypeError('The input of val should be a number, a list or a numpy array.')
        #self._flag = False
        self._der = np.ones(len(self._val)) 
    
    @property
    def val(self):
        return self._val
      

    @property
    def der(self):
        return self._der
        
    
    def __add__ (self, other):
        """
        Overload the addition
        EXAMPLES
        ==========
        >>> f = Tensor(2.0) + 3.0
        >>> (f.val, f.der)
        (5.0, 1.0)
        """
        x = Tensor()
        if isinstance(other, Tensor):
            x._val = self._val + other.val 
            x._der = self._der + other.der
            return x
        elif check_number(other) or check_array(other):
                x._val = self._val + other
                x._der = self._der
                return x
        else:
            raise TypeError('Tensor object can only add a number or a Tensor object')
            
    
    def __radd__ (self, other):
        """
        Overload the addition and make it commutable
        EXAMPLES
        ==========
        >>> f = 3.0 + Tensor(2.0)
        >>> (f.val, f.der)
        (5.0, 1.0)
        """
        return self.__add__(other)
    
    def __sub__ (self, other):
        """
        Overload the substraction
        EXAMPLES
        ==========
        >>> f = Tensor(2.0) - 3.0
        >>> (f.val, f.der)
        (-1.0, 1.0)
        """
        x = Tensor()
        try:
            x._val = self._val - other.val
            x._der = self._der- other.der
            return x
        except:
            if check_number(other) or check_array(other):
                x._val = self._val - other
                x._der = self._der
                return x
            else:
                raise TypeError('Tensor object can only multiply with Tensor or number')

        
    def __rsub__ (self, other):
        """
        Overload the substraction and make it commutable
        EXAMPLES
        ==========
        >>> f = 3.0 - Tensor(2.0)
        >>> (f.val, f.der)
        (1.0, -1.0)
        """
        return - self.__sub__(other)
    
    def __mul__ (self, other):
        """
        Overload the multiplication
        EXAMPLES
        ==========
        >>> f = Tensor(2.0) * 3.0
        >>> (f.val, f.der)
        (6.0, 3.0)
        """
        x =Tensor()
        if isinstance(other, Tensor):
            x._val = self._val * other.val
            x._der = self._der * other.val + self._val * other.der
            return x
        elif check_number(other) or check_array(other):
                x._val = self._val * other
                x._der = self._der * other
                return x
        else:
            raise TypeError('Tensor object can only multiply with Tensor or number')
    
    def __rmul__ (self, other):
        """
        Overload the multiplication and make it commutable
        EXAMPLES
        ==========
        >>> f = 3.0 * Tensor(2.0)
        >>> (f.val, f.der)
        (6.0, 3.0)
        """
        
        return self.__mul__(other)
    
    def __truediv__ (self, other):
        """
        Overload the division, input denominator cannot include zero. Otherwise raise ValueError.
        EXAMPLES
        ==========
        >>> f = Tensor(2.0)/2.0
        >>> (f.val, f.der)
        (1.0, 0.5)
        """
        x = Tensor()
        if (check_number(other) and other == 0) or\
            (isinstance(other, Tensor) and check_anyzero(other.val)) or \
                (check_array(other) and check_anyzero(other)):
            raise ZeroDivisionError('The Tensor is divided by 0')

        if isinstance(other, Tensor):
            x._val = self._val/ other.val
            x._der = (self._der*other.val - self._val*other.der)/(other.val*other.val)
            return x
        elif check_number(other) or check_array(other):
                x._val = self._val / other
                x._der = self._der / other
                return x
    
        else:
            raise TypeError('Tensor can only be divided by a number or a Tensor object')
            
    def __rtruediv__ (self, other):
        """
        Overload the division, and make it commutable. Input denominator cannot include zero, otherwise raise ValueError.
        EXAMPLES
        ==========
        >>> f = 2.0/Tensor(2.0)
        >>> (f.val, f.der)
        (1.0, -0.5)
        """
        x = Tensor() 
        if check_anyzero(self._val):# a/tensor(0)
            raise ZeroDivisionError('The Tensor object in denominator should not be zero.')
        # if isinstance(other, Tensor):
        #     x._val = other.val/ self._val
        #     x._der = (self._val*other.der - self._der*other.val)/(self._val*self._val)
        #     return x
        if check_number(other) or check_array(other):
            x._val = other / self._val
            x._der = -other * self._der / (self._val * self._val)
            return x
        else:
            raise TypeError('Only an numpy array or number can be divided by Tensor.')
        
                 
                
        
    def __pow__ (self, other):
        """
        Overload the power method
        EXAMPLES
        ==========
        >>> f = Tensor(2.0)**3
        >>> (f.val, f.der)
        (8.0, 12.0)
        """
        x = Tensor()

        if isinstance(other, Tensor): # x**a -> a*x**(a-1)
            if (other.val > 0).all():
                x._val = self._val ** other.val
                x._der = (self._val ** other.val) * (other.der * np.log (self._val) + other.val * self._der/ self._val)
                return x
            # elif (self._val == 0 and other.val <1).any():
            #     raise ZeroDivisionError('the base cannot be 0 when power is negative')
            else:
                raise ValueError('log function undefined for exponent <= 0')
        elif check_number(other) or (check_array(other) and len(other) == 1):
            if other == 0:
                x._val = 1
                x._der = 0
                return x
            elif (self._val == 0).any() and other <1:
                raise ZeroDivisionError('the base cannot be 0 when power is negative')

            else:
                other = float(other) #convert to float first
                x._val  = self._val** other
                x._der = other * self._val ** (other - 1) * self._der
                return x

        else:
            raise TypeError('Tensor base can only be operated with a Tensor object or a number/np.ndarray')
       
        
    def __rpow__ (self, other):
        """
        Overload the power method and make it commutable.
        EXAMPLES
        ==========
        >>> f = 3**Tensor(2.0)
        >>> (f.val, f.der)
        (9.0, 9.887510598012987)
        """
        x = Tensor()


        if check_number(other) or (check_array(other) and len(other) == 1): 
            if other <= 0:
                raise ValueError('log function undefined for exponent <= 0')
            else:
                x._val  = other ** self._val
                x._der = (other ** self._val) * (self._der * np.log(other))
                return x

        else:
            raise TypeError('Tensor base can only be operated with a Tensor object or a number/np.ndarray')


    
    def __neg__ (self):
        """
        Overload the negation method.
        EXAMPLES
        ==========
        >>> f = -Tensor(2.0)
        >>> (f.val, f.der)
        (-2.0, -1.0)
        """
        x = Tensor()
        x._val = -self._val
        x._der = -self._der
        return x
    
    # Alice added functions
    
    def __lt__(self, other):
        try:
            return self._val < other.val 
        except: # other is a scaler
            return self._val < other
    def __le__(self, other):
        try:
            return self._val <= other.val 
        except: # other is a scaler
            return self._val <= other
    def __gt__(self, other): 
        try:
            return self._val > other.val 
        except: # other is a scaler
            return self._val > other
    def __ge__(self, other):
        try:
            return self._val >= other.val 
        except: # other is a scaler
            return self._val >= other
    
    def __eq__(self, other):
        if not isinstance(other, Tensor):
            raise TypeError('Tensor object can only be compared with Tensor object')
        return (self._val == other.val).all()
    
    def __ne__(self, other):
        return not self.__eq__(other).all()
    
    def __abs__(self):
        # only used for calculation
        return abs(self._val)
    
   
    
    def __str__(self):
        """
        Examples
        ================
        >>> c = tensor.Tensor(3.0)
        >>> print(c)
        Tensor(3.0) 
        """
        return f"Tensor({self._val.tolist()})"
    
    def __repr__(self):
        """
        Examples
        ================
        >>> c = tensor.Tensor(3.0)
        >>> repr(c)
        'Tensor: val(3.0), der(1.0)'    
        """
        return f"Tensor: val({self._val.tolist()}), der({self._der.tolist()})"
    
    def __len__(self):
        return len(self._val)