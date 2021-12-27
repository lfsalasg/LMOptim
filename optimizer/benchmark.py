import random
import time
import numpy as np

sum = 0
start_time = time.time()
for i in range(0,400):
    a1 = np.random.rand(90,90)
    a2 = np.random.rand(90,90)
    m1 = np.matrix(a1)
    m2 = np.matrix(a2)

    m3 = m1.T * m2.I
    
print(np.linalg.det(m3))
print("--- %s seconds ---" % (time.time() - start_time))
