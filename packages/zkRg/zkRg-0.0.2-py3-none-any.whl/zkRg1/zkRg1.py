import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit as cvf

hh = open("file.out","r")

arr = hh.readlines()
arr = np.array(arr)

nrow = len(arr)
nrow2 = int((nrow-3)/2)

values = np.zeros([nrow2,2])

i = 0
index = 0
for row in arr:

    if i>2 and i%2==1:
        values[i-3+index][0] = row.split()[0]
        index-=1
        
    elif i>2 and i%2==0:
        values[i-3+index][1] = row.split()[1]
        
    i+=1
    
times = []
vals = []
both = []
for r in values:
    if r[0]%(10**5)==0:
        times.append(r[0])
        vals.append(r[1])
        both.append(r)
        
times = np.array(times)
vals = np.array(vals)
both = np.array(both)


def func(x, a, b,c ,d):
    return a*x**4+b*x**3+d*x**2+c

popt,pcov = cvf(func,times,vals, p0 = [0,0,0,0] ,maxfev = 1000000)
value_fit = func(times,*popt)


plt.plot(times,vals,"r-")
plt.plot(times,value_fit,"b-")
plt.show()

