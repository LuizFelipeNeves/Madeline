import matplotlib.pyplot as plt
import math

x=[]
y=[]
So=1357
pi=3.14159

def calculo():
    global menor, maior;
    menor = distancia(1)
    maior = 0
    for dia in range(1, 365): 
        S = distancia(dia)
        x.append(dia)
        y.append(S)

        if(S >= maior): maior = S;
        if(S <= menor): menor = S;
        
def distancia(dia):
    teta = 2 * pi * dia / 365; # teta em graus
    r2sun = 1.00011 + .034221 * math.cos(teta) + .000128 * math.sin(teta);
    S = r2sun * So;
    return S;
    
def diajuliano(dia , mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    diajuliano = 0;
    for m in range(1, mes):
        diajuliano += diasmes[m-1]
    return diajuliano+dia
        
def plot():    
    plt.figure(100)
    plt.plot(x,y, 'b-') #b- é azul
    plt.title("Distancia Terra Sol")
    plt.ylabel('Distancia')
    plt.xlabel('Dia')

    print("Maior: " + str(maior))
    print("Menor: " + str(menor))
    plt.show()
    
calculo();
plot();
