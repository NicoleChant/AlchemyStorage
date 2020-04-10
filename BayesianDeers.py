from scipy.special import gamma, factorial
import random
from matplotlib import pyplot as plt
import numpy as np
from operator import itemgetter



def Diri(x,a,b):
    Beta = (gamma(a+b)/(gamma(a)*gamma(b)))*(x**(a-1))*((1-x)**(b-1))
    return Beta

def BayesEstim(a,x,m,A):
    return (a+x)/(m+A)


N = int(input("Enter the number of the available types: \n"))
#print("Enter the supposedly unknown vector parameter: \n")
#p=[]
#flag=1
#for i in range(1,N-1):
#    pi= float(input())
#    while pi >= flag or pi <= 0:
#        pi = float(input())
#    flag -= pi
#    p.append(pi)

#pN=1
#for i in p:
#    pN -= i

#p.append(pN)
#print(p)


print("Enter the initial belief vector parameters: \n")
a=[]
A=0
for i in range(0,N):
    ai = float(input())
    A+=ai
    while ai <= 0:
        ai=float(input())
    a.append(ai)



print("Enter the number of occurences (in increasing order): \n")
x=[]
M=0
for i in range(0,N):
    xi = int(input())
    M+=xi
    while xi <=0:
        xi = int(input())
    x.append(xi)

p = np.linspace(10**(-9), 0.999999999, 200)
Estim=[]
for i in range(0,N):
       K = M + A
       K = K - a[i] - x[i]
       z = Diri(p,a[i]+x[i],K)
       plt.plot(p,z)
       Estim.append(BayesEstim(a[i],x[i],M,A))
       print(Estim[i])

plt.grid()
plt.xlabel('probability parameter')
plt.ylabel('posteriors')
#plt.legend([,])
plt.show()

Atoms = [ 'Bears' , 'Deers' , 'Rabbits']
y=[i*100/M for i in x]
plt.bar(Atoms,y,label = 'sample prevalences' , color=['green','orange','yellow'])
plt.xlabel('animals')
plt.ylabel('sample percentages')
plt.show()

Estim = [i*100 for i in Estim]
plt.bar(Atoms,Estim,label = 'posterior prevalences' , color=['green','orange','yellow'])
plt.xlabel('animals')
plt.ylabel('posterior percentages')
plt.show()
