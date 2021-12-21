import numpy as np
import math
def callable_func (fn,param, state): # La función que se va a ajustar, abc es una matriz que contiene tres parámetros [[a], [b], [c]]
    
    return fn(param,state)


def square_func(param,state):
    a = param[0]
    b = param [1]
    c= param [2]

    return a*state[0]**2+b*state[0]+c

def one_variable(param,state):
    a = param[0]
    b = param[1]
    c = param[2]
    return np.exp(a*state[0]**2+b*state[0]+c)

def two_variables(param,state):
    a = param[0]
    b = param[1]

    return a*state[0]**2+b*math.log(state[1])