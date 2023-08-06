import numpy

def check_number(x):
    return not hasattr(x,"__len__")
def check_array(x):
    return isinstance(x, numpy.ndarray)

def check_list(x):
    return isinstance(x, list)

def check_anyzero(x):
    return (x== 0).any()

def isodd(i):
    if (i+1) % 2 == 0:
        return True
    else:
        return False
    
def check_tan(x):
    if check_number(x):
        x = numpy.array([x])
    count = 0
    for i in x:
        if isodd(i /(numpy.pi/2)):
            count += 1
    if count != 0:
        return True
    else:
        return False
    
def check_anyneg(x):
    return (x<=0).any()

def check_lengths(ll, length = None):
    if length:
        len_check = length
    else:
        len_check = len(ll[0])
    return all(len(l) == len_check for l in ll)

def check_list_shape(ll):
    ll_array = numpy.array(ll)
    return ll_array.shape

def check_nontensor_input(x):
    return check_number(x) or check_list(x) or check_array(x)