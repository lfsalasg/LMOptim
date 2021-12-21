import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

__DIR__ = os.getcwd() 


def initialize():
    global jobName
    global delta
    global lamb
    global maxSteps
    global tolerance
    global cores
    global set_dim
    global save

    jobName     = 'Optimization'
    delta       = 0.00002
    lamb        = 1
    maxSteps    = 20 
    tolerance   = 0.01
    cores       = 1
    set_dim     = 1
    save        = {
        "jacobina": False,
        "xy": False,
        "mse": False,
        "log": False
    }
