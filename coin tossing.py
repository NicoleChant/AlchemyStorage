#Simulation of fair coin tossing, i.e., 50% chance to get heads.
#We are simulating the weak law of Big Numbers, i.e., that the sampling mean
#value converges to the actual mean value which is x/2
import random
import math
x=int(input("give a positive integer: "))
S=0
Exp=0

print(x/2)

f=open("results.txt",'w')
f.write("We initialize the random experiment {:d} times.\n".format(x))

for i in range(1,x+1):
    y=random.randint(0,1)
    S+=y
    z=S/i
    f.write("{:1.4f}\n".format(z))
    print("mean value of the sample is equal to: {:1.5f}".format(z))

f.close()


