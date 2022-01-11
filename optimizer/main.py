import numpy as np
import random
import math
import subprocess
from numpy import matrix as mat
from matplotlib import pyplot as plt
from datetime import datetime
# From the optimization folder
import optimizer.settings as st
import optimizer.calculus as calc
import optimizer.utilities as ut
import optimizer.callables as cll
import optimizer.interfaces.RASPA.launch as launcher

def main(inf):
    # Initialize parameters
    st.initialize()
    states      = list()
    y           = list()
    testing = False #Set to False in production
    start_fetching = False
    max_steps_reached = True

    with open(inf) as f:
        for line in f:
            tmp = line.split()
            
            if line.startswith('#'):
                continue
            if line == '\n':
                continue
            if tmp[0].replace('.','').isnumeric():
                    start_fetching = True
            if not start_fetching:
                    
                if tmp[0] == 'job-name':
                    st.jobName = tmp[1]
                    
                if tmp[0] == 'x-set-size':
                    st.set_dim = int(tmp[1])
                    
                if tmp[0] == 'init-param':
                    init_param = tmp[1:]
                    
                if tmp[0] == 'derivative-step':
                    st.delta = float(tmp[1])
                    
                if tmp[0] == 'damping-factor':
                    st.lamb = float(tmp[1])
                    
                if tmp[0] == 'max-steps':
                    st.maxSteps = int(tmp[1])
                    
                if tmp[0] == 'tolerance':
                    st.tolerance = float(tmp[1])
                    
                if tmp[0] == 'save-jacobian':
                    st.save["jacobian"] = True
                    
                if tmp[0] == 'save-fx':
                    st.save["fx"] = True
                    
                if tmp[0] == 'save-log':
                    st.save["log"] = True
                if tmp[0] == 'save-mse':
                    st.save["mse"] = True
                    
                if tmp[0] == 'use-cores':
                    st.cores = int(tmp[1])
                continue
            try:
                thisSet = ut.fetch_data(tmp,st.set_dim)
                states.append(thisSet[0])
                y.append(thisSet[1])
            except ValueError as e:
                print("Fatal error: ",e)

    log = ut.Logger("try3.log",True)
    if st.save["jacobian"]:
        logJ = ut.Logger("try3_J.log",True)
    if st.save["fx"]:
        logF = ut.Logger("try3_F.log",True)

    #Initialize the fx vector
    fx = mat (np.zeros ((len(states), 1))) # f (x) 100 * 1 error
    #Initialize the beta_k vector
    beta_k = mat ([float(i) for i in init_param]).T # inicialización de parámetro
    old_mse = 0
    
    log.write("Starting simulation...")
    
    if st.save["fx"]:
        logF.write("Starting simulation...")
    if st.save["jacobian"]:
        logJ.write("Starting simulation...")
    
    start_time = datetime.today()

    ut.clear_tmp_all()

    for step in range(1,st.maxSteps):
        
        mse = 0
        
        launcher.launch_step(st.jobName,step,beta_k,states,st.cores)
 
        estimates = launcher.read_results(st.jobName,step,len(states),"A")
        estimates = [float(i) for i in estimates]
 
        launcher.clean_tmp(st.jobName,step)

        for i in range(0,len(states)):
            fx [i] = estimates[i] - y[i] # Tenga en cuenta que no se puede escribir como y-Func, de lo contrario divergerá    
            mse += fx[i]**2

        J = calc.jacobian2(beta_k,states,st.delta)
        
        H = J.T*J + st.lamb*np.eye(len(beta_k))

        dx = -H.I * J.T * fx 

        beta_k += dx

        log.add(step,abs(mse - old_mse),beta_k)
        if st.save["fx"]:
            logF.estimates(estimates,y)
        print ("step = %d,change mse = %.8f" %(step,abs(mse - old_mse)))  
        if step > 1 and abs(mse -old_mse)/old_mse < st.tolerance:
            max_steps_reached = False
            break
        old_mse = mse

    if max_steps_reached:
        log.write("WARNING Maximum number of steps reached without fulfilling the tolerance. Consider increasing the number of steps or changing the initial values. To restart pass restart-from-file in the input file")
    print (beta_k)

    duration = datetime.today()-start_time
    print("Optimization took %d miliseconds" %(duration.microseconds / 1000))
