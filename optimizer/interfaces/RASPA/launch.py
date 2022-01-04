import os
import shutil as sh
from distutils.dir_util import copy_tree
import subprocess
import re
import glob
from pathlib import Path
#Modules from this program
import optimizer.settings as st

def set_param(fdir,param):
    fin = open(fdir,'r')srun inside python
    data = fin.read()
    fin.close()
    i=0
    for p in param:
        data = data.replace('{'+str(i)+'}',str(p.item()))
        i+=1
    
    fout = open(fdir,'w')
    fout.write(data)
    fout.close()

def set_state(fdir,state):
    fin = open(fdir,'r')
    data = fin.read()
    fin.close()
    i=0
    for p in state:
        data = data.replace('&'+str(i),str(float(p)))
        i+=1
    
    fout = open(fdir,'w')
    fout.write(data)
    fout.close()

def launch_step(sname,step,param,states,cores):
    
    tmp_dir = st.__DIR__+'/tmp/'
    workplace_dir = st.__DIR__+'/workplace/'

    name = sname+'_step_'+str(step)
    os.mkdir(tmp_dir+name)
    os.mkdir(tmp_dir+name+'/step_files')
    copy_tree(workplace_dir+'RASPA/',tmp_dir+name+'/step_files')

    set_param(tmp_dir+name+'/step_files'+'/pseudo_atoms.def',param)
    set_param(tmp_dir+name+'/step_files'+'/force_field_mixing_rules.def',param)
    set_param(tmp_dir+name+'/step_files'+'/force_field.def',param)
    set_param(tmp_dir+name+'/step_files'+'/simulation.input',param)

    i=0

    commands = list()

    while i < len(states):
        shuttle = open(tmp_dir+'shuttle.sh','w')
        for core in range(0,cores):
            if i >= len(states):
                break
            print("Launch state "+str(i)+" in core "+str(core))
            os.mkdir(tmp_dir+name+'/point_'+str(i))
            copy_tree(tmp_dir+name+'/step_files',tmp_dir+name+'/point_'+str(i))
            set_state(tmp_dir+name+'/point_'+str(i)+'/simulation.input',states[i])
            
            shuttle.write('cd '+tmp_dir+name+'/point_'+str(i)+'&& taskset --cpu-list '+str(core)+' ./run & cd '+tmp_dir+'\n')

            #commands.append('cd '+tmp_dir+name+'/point_'+str(i)+'&& taskset --cpu-list '+str(core)+' ./run ')
            
            #commands.append('cd '+tmp_dir+name+'/point_'+str(i)+'&& ./run && cd ../../../')
    
            i+=1
        shuttle.write('wait')
        shuttle.close()
        proc = subprocess.Popen('cd '+tmp_dir+' && bash shuttle.sh',shell=True)
        exit_code = proc.wait() 
        #print(commands)
    print("Finalizó :)")

def read_results(sname,step,points,observable):
    root_dir = st.__DIR__+'/tmp/'+sname+'_step_'+str(step)
    results = [0] * points
    for i in range(0,points):
        path=root_dir+'/point_'+str(i)+'/Output/System_0/*.data'
        #print(path)
        for filename in glob.glob(path):
            txt = Path(filename).read_text()
            line = re.findall("Average loading excess \[cm\^3 \(STP\)\/gr(?:(?!<\/?p).)*",txt)
            results[i] = line[0].split()[6]
            break
    
    return results

def clean_tmp(sname,step):
    root_dir = st.__DIR__+'/tmp/'+sname+'_step_'+str(step)
    sh.rmtree(root_dir)
def whereamI():
    cwd = os.getcwd()
    print(cwd)