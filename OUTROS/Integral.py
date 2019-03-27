import numpy as np
y = [5, None, 5, None, None, 15, 20, None, 5]
x = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def integral(x, y):
    i = 0
    total = 0
    ant = '-999'
    prox = '-999'
    tant = None
    tprox = None

    while i < len(y):
        if(i+1 < len(y)) :
            if(y[i] == None):
                if(ant == '-999'):  ant = 0
            else: 
                if(ant == '-999'):  ant = y[i]
                else:
                    # faz o calculo
                    prox = y[i]
                    tprox = x[i]
                    b = np.trapz([ant, prox], x=[tant, tprox]) 
                    ant = y[i]
                    total += b
                    #print(b)                 
            tant = x[i]   
        else:
            if(y[i] == None): 
                prox = 0
            else: 
                prox = y[i]
                
            tprox = x[i]
            b = np.trapz([ant, prox], x=[tant, tprox])
            total += b
            #print(b)
        i+=1
    return total 

print(integral(x, y))
