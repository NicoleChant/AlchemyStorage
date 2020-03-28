from scipy.special import gamma, factorial
import matplotlib.pyplot as plt
import random
import numpy as np


#beta distribution with parameters a and b
def beta(x,a,b):
     z = (x**(a - 1))*((1 - x )**(b - 1 ))*gamma(a+b)/(gamma(a)*gamma(b))
     return z

#average estimation
def avg(count,N,a,b):
    z = ( a + count )/(a + b + N )
    return z


def flip(p):
    if random.random()<=p: #assumingly, we ignore the generating parameter p
        return 1
    else:
        return 0

#a, b are merely initial beliefs which they will "adapt" to the new data
p = float(input("Enter the supposedly unknown parameter that we want to estimate: "))
while p <= 0 or p >= 1:
     p = float(input())

a = float(input("Enter alpha parameter: "))
while a <= 0:
     a = float(input())

b = float(input("Enter beta parameter: "))
while b <= 0:
     b = float(input())

#Number of available data
N = int(input("Enter the number of trials (>=3): "))
while N < 3:
     N = int(input())

count=0 #counts number of heads
M=0
#experimental data generator
x=np.linspace(0.00000001, 0.999999999, 200)
y=beta(x,a,b)


events = [ 'Heads', 'Tails' ]

for i in range(1,N+1):
    M+=1
    if flip(p)==1:
         count+=1

    #graphs of two final and the third posterior
    if i > N - 2:
       z=beta(x, a + count, b + M - count)
       plt.plot(x,z)

numb = [ count , N - count ]
esti=avg(count,N,a,b)
print("Our data is {:d} Heads out of {:d} trials.\n".format(count,N))
print("We estimate that the parameter is equal to {:1.3f}.\n".format(esti))
print("Actual absolute error: {:1.3f}.\n".format(abs(esti-p)))

#demonstrating graphs
#prior distribution
plt.plot(x, y)
plt.grid()
plt.xlabel('probability parameter p')
plt.ylabel('posteriors')
plt.legend(['prior', 'posterior'])
plt.show()

plt.bar(events, numb , label='coin fliping', color=['green','orange'])
plt.xlabel('events')
plt.ylabel('occurences')
plt.show()
