import numpy as np
import pandas as pd
import optimizer.interfaces.RASPA.launch as launcher
from numpy import matrix as mat

import optimizer.settings as st

def partial_d (params,state,fn,delta):
    # Derivada parcial de primer orden y precisión O(h2)
    # Respecto a param

    derivates = np.zeros((len(params),1)) 
    for i in range(0,len(params)):
        params_up = params.copy()
        params_up[i] += delta/2
        params_down = params.copy()
        params_down[i] -= delta/2

        d_fn_up = fn(params_up,state)
        d_fn_down = fn(params_down,state)
        derivates[i] = (d_fn_up - d_fn_down)/delta
    
    return derivates
    

def jacobian(params,states,fn,delta):
    J = mat(np.zeros((len(states),len(params))))
    for i in range(0,len(states)):
            J[i,:] = partial_d(params,states[i],fn,delta).transpose()
    
    return J


def jacobian2(params,states,delta):
    J = mat(np.zeros((len(states),len(params))))

    for i in range(0,len(params)):
        params_up = params.copy()
        params_up[i] += delta/2
        params_down = params.copy()
        params_down[i] -= delta/2

        launcher.launch_step("derivate_up",0,params_up,states,st.cores)
        d_fn_up = launcher.read_results("derivate_up",0,len(states),"A")
        launcher.clean_tmp("derivate_up",0)
        print(d_fn_up)
        launcher.launch_step("derivate_down",0,params_down,states,st.cores)
        d_fn_down = launcher.read_results("derivate_down",0,len(states),"A")
        launcher.clean_tmp("derivate_down",0)

        for j in range(0,len(states)):
            J[j,i] = (float(d_fn_up[j]) - float(d_fn_down[j]))/delta    
    
    return J