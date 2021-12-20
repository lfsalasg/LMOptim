#import interfaces.RASPA.launch as launcher
import calculus as ca
sname = 'test'
param = [
    47.8562,
    3.47299
]
states = [
    [300,100],
    [300,1000],
    [300,10000],
    [300,20000],
    [300,30000]
]

#launcher.launch_step(sname,0,param,states,4)
#y_values = launcher.read_results(sname,0,len(states),"A")

J = ca.jacobian2(param,states,0.0001)
print(J)