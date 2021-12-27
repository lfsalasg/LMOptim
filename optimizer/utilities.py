import numpy as np
import random
import os
import shutil

from datetime import datetime
from matplotlib import pyplot as plt

import optimizer.settings as st

def fetch_data (row,set_dim):
    if len(row) < set_dim + 1:
        raise IOError("Size of the set less than dimension of x-set")
    x_values = [0] *set_dim
    for indx in range(0,set_dim):
        x_values[indx] = float(row[indx])

    y_value = float(row[set_dim])

    return x_values, y_value  

def gen_sample_data(fn,param,filename):
    
    states = np.random.rand(100,2)
    y=[0]*100
    for i in range(0,len(states)):
        y[i] = fn(param,states[i])+random.gauss(0,0.1)
    
    f = open(filename,'a')
    for i in range(0,len(states)):
        x_values=''
        for j in states[i]:
            x_values+=str(j)+' '

        f.write(x_values+' '+str(y[i])+'\n')
    
    plt.plot(states,y)
    plt.show()

def clear_tmp_all():
    folder = st.__DIR__+'/tmp/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    
class Logger:
    # Attributes
    def __init__(self,filename,rewrite):
        self.filename = filename
        self.mode = 'w' if rewrite else 'a'

        f = open(filename,self.mode)
        f.close()
    
    def add(self,step,mse_change,param,more=''):

        f = open(self.filename,'a')
        timestamp = datetime.today()
        f.write("On Step %(step)s: %(timestamp)s  Delta MSE %(mse)s\n" % {'timestamp':timestamp,'step':step,'mse':mse_change})
        f.write("Current value of parameters:\n")
        
        i=0
        for p in param:
            f.write("beta.%(i)s: %(p)s\n"%{'i':i,'p':p})
            i+=1
            
        for line in more:
            f.write(line)
        f.write("\n")
        f.close()
    
    def write(self,content):
        f = open(self.filename,'a')
        timestamp = datetime.today()
        f.write("%(timestamp)s %(content)s\n\n" % {'timestamp':timestamp,'content':content})
        f.close()
    
    def estimates(self,fx,y):
        f = open(self.filename,'a')
        timestamp = datetime.today()
        size = len(fx)

        for i in range(0,size):
            f.write("%(f)s\t%(y)s\n"%{'f':fx[i],'y':y[i]})
        
        f.write("\n")
        f.close()
