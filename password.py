import random
from datetime import *
##random password maker
def ranges():
    letter=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    LETTER=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    number=['0','1','2','3','4','5','6','7','8','9']
    symbol=[".",",","!","_"]
    return letter,LETTER,number,symbol
def randomseed():
    seed = int(str(datetime.now())[-6:])
    return seed
def randomindex(length):
    letter,LETTER,number,symbol = ranges()
    seeds = randomseed()
    random.seed(seeds)
    order = []
    while True:
        i = int(random.randint(0,3))
        order.append(i)
        if len(order) > int(length): break
    password=[]
    i = 0
    while True:
        i+=1
        if int(order[i]) == 0: 
            let = random.randint(0,25)
            password.append(letter[let])
        elif int(order[i]) == 1: 
            LET = random.randint(0,25)
            password.append(LETTER[LET])
        elif int(order[i]) == 2:
            num = random.randint(0,9)
            password.append(number[num])
        elif int(order[i]) == 3:
            sym = random.randint(0,3)
            password.append(symbol[sym])
        
        if i >= int(length): break
    return password
def main():
    quantit = 0
    reserve = "nothing"
    length = input("Please input the length of password\n")
    quantity = input("How many passwords do you want?\n")
    while True:
        if quantit >= int(quantity): break
        password = randomindex(length)
        if password == reserve:
            pass
        else:
            quantit+=1
            print("".join(password))
        reserve = password
        
main()
