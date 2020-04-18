#MaxEnt
from matplotlib import pyplot as plt
import numpy as np
import random


def pdf(a,n):
    return (1-a)*(a**n)

def loss(a,x):
    return a**(x+1) + (a**(x+2))/(1-a)

def geom(b):
    return np.floor(np.log(random.random())/np.log(1-b))


print("Hello! I'm Carla. What could I do for your business?\n")
print("Uhm, alright. I will try to help you figure out what color of cars you should produce today, just give me some info would you?\n")

Stock=[]
print("Enter the initial warehouse stock to help Carla with her calculations. Press -1 to terminate. \n")
S = int(input())
while S!=-1:
    Stock.append(S)
    S = int(input())

N = len(Stock)

AvgSales=[]

print("Enter the annual average sales of each of {:d} products. \n".format(N))
for i in range(0,N):
           S = float(input())
           AvgSales.append(S)

AddStock = 200
Sum = 0
DecisionLosses=[]
for i in range(0,N):
          for j in range(0,N):
                 b=1/(1+AvgSales[j])
                 a = 1 - b
                 if j!=i:
                       Sum += loss(a,Stock[j])
                 else:
                       Sum += loss(a,Stock[j]+AddStock)
          DecisionLosses.append(Sum)
          Sum = 0


#for i in range(0,len(DecisionLosses)):
#    print("The average loss from decision {:d} is: {1.2f}.\n".format(i+1,DecisionLosses[i]))


Min = min(DecisionLosses)
Spot = DecisionLosses.index(Min) + 1

print("The optimal decision is to create item {:d} with the lowest expected loss of {:1.3f}. \n".format(Spot,Min))

fix = 100
Atoms = [n for n in range(0,fix)]
for j in range(0,N):
          b=1/(1+AvgSales[j])
          a = 1 - b
          Pdf = [ pdf(a,n) for n in range(0,fix)]
          xlocs = plt.xticks
          xlocs = [5*n for n in Atoms]
          plt.xticks(xlocs)
          plt.xlabel('orders')
          plt.ylabel('pdf')
          plt.bar(Atoms,Pdf,width=0.8,color=['green'])
          plt.show()

#simulation of pdf
fix2=100
results=[]
results2=[]
Days=[i for i in range(1,fix2)]
for j in range(0,N):
    b=1/(1+AvgSales[j])
    print(b)
    for i in range(1,fix2):
          results.append(geom(b))
    plt.plot(Days,results)
    results=[]


plt.title("distribution samples")
xlocs = plt.xticks
xlocs = [n*5 for n in Days]
ylocs = plt.yticks
ylocs = [50*n for n in range(1,16)]
plt.xticks(xlocs)
plt.yticks(ylocs)
plt.xlabel('day')
plt.ylabel('number of orders')
plt.legend(['widget {:d}'.format(i) for i in range(1,N+1)])
axes = plt.gca()
axes.set_xlim([0,fix2])
plt.grid(True)
plt.show()


































