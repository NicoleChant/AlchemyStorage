from scipy.special import gamma, factorial
import matplotlib.pyplot as plt
import random
import numpy as np


#prior parameter distribution: θ
#beta distribution with parameters a and b
def beta(x,a,b):
     z = (x**(a - 1))*((1 - x )**(b - 1 ))*gamma(a+b)/(gamma(a)*gamma(b))
     return z

#average estimation
def avg(count,N,a,b):
    z = ( a + count )/(a + b + N )
    return z

#def flip(a,b):
    #if random.random()<=np.random.beta(a, b):
def flip(p):
    if random.random()<=p: #assumingly, we ignore the generating parameter p
        return 1
    else:
        return 0

#a, b are merely initial beliefs which they will "adapt" to the new data
p = float(input("Enter the supposedly unknown parameter that we want to estimate: "))
a = float(input("Enter alpha parameter: "))
b = float(input("Enter beta parameter: "))

#Number of available data
N = int(input("Enter the number of trials: "))
count=0 #counts number of heads

#experimental data generator
for i in range(1,N+1):
    #if flip(a,b)==1:
    if flip(p)==1:
         count+=1

print(count)
events = [ 'Heads' , 'Tails' ]
numb = [ count , N - count ]

z=avg(count,N,a,b)
print("Our data is {:d} Heads out of {:d} trials.\n".format(count,N))
print("We estimate that the parameter is equal to {:1.3f}.\n".format(z))
print("Actual absolute error: {:1.3f}.\n".format(abs(z-p)))

#graphs of priors and posteriors
x=np.linspace(0.00000001, 0.999999999, 200)
y=beta(x,a,b)
z=beta(x, a + count, b + N - count)
plt.plot(x, y)
plt.plot(x, z)
plt.grid()
plt.xlabel('p')
plt.ylabel('y and z')
plt.legend(['prior', 'posterior'])
plt.show()

plt.bar(events, numb , label='coin fliping', color=['blue','orange'])
plt.xlabel('events')
plt.ylabel('occurences')
plt.show()
