#2#Modified single player blackjack or 21

#def Decisions():

def Pouka(S):
    if S<=21:
        return True
    else:
        return False

def Continue(x):
    if x==1:
        return True
    else:
        return False



import random

#defining the 52-card deck
#clubs
whiteclubs=['2cw','3cw','4cw','5cw','6cw','7cw','8cw','9cw','Jcw','Qcw','Kcw','Acw']
blackclubs=['2cb','3cb','4cb','5cb','6cb','7cb','8cb','9cb','Jcb','Qcb','Kcb','Acb']
clubs=whiteclubs+blackclubs

#hearts
whitehearts=['2hw','3hw','4hw','5hw','6hw','7hw','8hw','9hw','Jhw','Qhw','Khw','Ahw']
blackhearts=['2hb','3hb','4hb','5hb','6hb','7hb','8hb','9hb','Jhb','Qhb','Khb','Ahb']
hearts=whitehearts+blackhearts

#diamonds
whitediamonds=['2dw','3dw','4dw','5dw','6dw','7dw','8dw','9dw','Jdw','Qdw','Kdw','Adw']
blackdiamonds=['2db','3db','4db','5db','6db','7db','8db','9db','Jdb','Qdb','Kdb','Adb']
diamonds=whitediamonds+blackdiamonds

#spades
whitespades=['2sw','3sw','4sw','5sw','6sw','7sw','8sw','9sw','Jsw','Qsw','Ksw','Asw']
blackspades=['2sb','3sb','4sb','5sb','6sb','7sb','8sb','9sb','Jsb','Qsb','Ksb','Asb']
spades=whitespades+blackspades

#deck
whites=whiteclubs+whitehearts+whitediamonds+whitespades
blacks=blackclubs+blackhearts+blackdiamonds+blackspades
deck=clubs+hearts+diamonds+spades

#modified deck
deckmod=deck

#thegame

#for i in deckmod:
#        print(i,sep=',',end=' ')
#print("\n")

#initial amount of wealth
wealth = 1000 #euro or some monetary unit
flag=0
j=0
S=0

from random import shuffle
for i in range(1,10):
    random.shuffle(deckmod)

#thehand
mycards=[]
mycards.append(random.choice(deckmod))
deckmod.remove(mycards[0])
try:
    S+=int(mycards[0][0])
except:
    S+=10

print("You have {:d} ".format(S))

while Pouka(S)==True:
    
    x=int(input("To draw another card press 1, otherwise, to stop press 0: "))
    
    if Continue(x)==True:
        mycards.append(random.choice(deckmod))
        deckmod.remove(mycards[0])
        j+=1
        try:
           S+=int(mycards[j][0])
        except:
           S+=10
        print("You have {:d} ".format(S))
    else:
        break

if Pouka(S)==True:
    print("You are out with {:d}.".format(S))
else:
    print("You lost with {:d}.".format(S))

