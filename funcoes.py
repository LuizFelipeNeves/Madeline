import csv
import math
import pandas as pd
import numpy as np


def selecaolistaunica(id, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, usecols=[4 , 6, 9], encoding="latin-1")
    select = lista.iloc[np.where(lista[4].values == id)]
    select = select.iloc[np.where(select[6].values != '-999')]
    select = select.iloc[np.where(select[9].values == 'Brasil')]
    select = select[6].values.tolist()
    return select

def diames(ano, mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1;
    return diasmes[int(mes)-1]

# Retorna o numero de dias de determinado mes            
def numerodiasmes(mes):
    return diasmes[mes-1]

def diajuliano(dia, mes, ano):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1;
    for i in range(mes-1): dia += diasmes[i]
    return dia


# Encontra um Elemento em uma Lista
def findElement(elemento, lista):
    for i in range(len(lista)):
        if(elemento == lista[i]):
            return i;
            break;
			
# Pega o ID da Estação
def getID(sigla , listaunica):
    with open(listaunica) as lista:
        reader = csv.reader(lista, delimiter='\t')
        for row in reader:
            if(sigla == row[6]): return row[0];

def contarelemento(array):
    count = 0;
    for i in range(len(array)):
        if(array[i] != None): count += 1
    return(count)

# Soma todos os elementos de um array
def somararray(array):
    soma = 0;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
    return soma
	
# Formata determinado numero para duas casas.    
def formatn(numero):
    if(numero == None): return -999;
    else: return float("%.2f" % numero)

# Calcula o desvio padrao
def desviopadrao(array): 
    new=[]
    for i in range(len(array)):
        if(array[i] != None): new.append(array[i])
	
    if(len(new) != 0):
        media = np.sum(new) / len(new)
        for i in range(len(new)):
            new[i] = (new[i] - media)**2
        dp= np.sum(new) / (len(new)-1)
        dp = math.sqrt(dp)
    else: dp = 0;
    return float(round(dp, 3));
	
def erropadrao(dsp, array):
    new=0
    for i in range(len(array)):
        if(array[i] != None): new += 1;
    if(new == 0): new = 1;
    final = float(dsp) / math.sqrt(new)
    return round(final, 3)

def diferenca(a, b):
    final = []
    for i in range(len(a)):
        if(a[i] != None and b[i] != None): final.append(a[i]-b[i])
        else: final.append(None)
    return final

# Media do dia, usando o metodo dos trapezios
def mediadiaria(array):
    menor=0
    maior=0
    somatotal = 0
    abre=[]
    fecha=[]
    chave=False
    for i in range(len(array)):
        if(array[i] is None):
            if chave == False: # Abre
                abre.append(i)
                chave = True;
        else:
            if(chave == True): # Fecha
                fecha.append(i-1)
                chave = False;
            if(menor == 0): menor = array[i] # Menor
            if(array[i] > maior): maior= array[i] # Maior
            somatotal += array[i];

        if((i+1 == len(array)) and chave == True): # Verifica o fim do array
            fecha.append(i)
            chave = False;

    # Calcula os valores
    for i in range(len(abre)):
        intervalo = ((fecha[i]-abre[i])+1)
        if((abre[i]-1 > 0) and (fecha[i]+1 < len(array))): # Apenas entra na condição caso o inicio seja maior que 0, e o fim menor que o limite.
            S = (array[abre[i]-1]+array[fecha[i]+1])*intervalo/2
            somatotal += S/intervalo;
        elif((abre[i]-1 > 0) and(fecha[i]+1 > len(array))):
            S = (array[abre[i]-1])*intervalo/2
            somatotal += S/intervalo;
        elif((abre[i]-1 < 0) and (fecha[i]+1 < len(array))):
            S = (array[fecha[i]+1])*intervalo/2
            somatotal += S;

    return(somatotal)
