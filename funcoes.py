# -*- coding: utf-8 -*-

import csv
import math
import pandas as pd
import numpy as np


def jouletowatthora(valor):
    return ((valor * (10**3))/3600)

def selecaolistaunica(id, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, usecols=[4 , 6, 9], encoding="latin-1")
    select = lista.iloc[np.where(lista[4].values == id)]
    select = select.iloc[np.where(select[6].values != '-999')]
    select = select.iloc[np.where(select[9].values == 'Brasil')]
    select = select[6].values.tolist()
    return select

def diames(ano, mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1
    return diasmes[int(mes)-1]

# Retorna o numero de dias de determinado mes            
def numerodiasmes(mes):
    return diasmes[mes-1]

def diajuliano(dia, mes, ano):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1
    for i in range(mes-1): dia += diasmes[i]
    return dia


# Encontra um Elemento em uma Lista
def findElement(elemento, lista):
    for i in range(len(lista)):
        if(elemento == lista[i]):
            return i

# Pega o ID da Estacao	
def getID(sigla, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, encoding="latin-1")
    select = lista.iloc[np.where(lista[6].values == sigla)]
    select = select[0].values.tolist()
    return select[0]

# Pega a localizacao da Estacao
def getLoc(sigla, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, encoding="latin-1")
    select = lista.iloc[np.where(lista[6].values == sigla)]
    idd = select[0].values[0]
    lat = select[1].values[0]
    long = select[2].values[0]
    rede = select[10].values[0]
    return [idd, lat, long, rede]

def contarelemento(array):
    count = 0
    for i in range(len(array)):
        if(array[i] != None): count += 1
    return(count)

# Soma todos os elementos de um array
def somararray(array):
    soma = 0
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
    return soma



# Formata determinado numero para duas casas.    
def formatn(numero):
    if(numero == None): return -999
    if(float(numero).is_integer()): return numero
    return float("%.1f" % numero) # 2f

# Calcula o desvio padrao
def desviopadrao(array): 
    new=[]
    for i in range(len(array)):
        if(array[i] != None): new.append(array[i])

    if(len(new) != 0):
        media = np.sum(new) / len(new)
        for i in range(len(new)):
            new[i] = (new[i] - media)**2

        t = (len(new)-1)
        if(t < 1): t=1
        dp= np.sum(new) / t
        dp = math.sqrt(dp)
    else: dp = 0
    return float(round(dp, 3))

def erropadrao(dsp, array):
    new=0
    for i in range(len(array)):
        if(array[i] != None): new += 1
    if(new == 0): new = 1
    final = float(dsp) / math.sqrt(new)
    return round(final, 3)

def diferenca(a, b, c):
    final = []
    for i in range(len(a)):
        if(a[i] != None and b[i] != None): final.append((a[i]-b[i])-c)
        else: final.append(None)
    return final

# Media do dia, usando o metodo dos trapezios

def integral(x, y, fator):
    total = 0
    dxi = x[1]-x[0]
    c = contarelemento(y)

    if(c*dxi > (fator/24 * 7)):
        for i in range(len(y)):
            if(y[i] != None):
                if(y[i] < 0): y[i] = None
            
        for i in range(len(y)-2):
            pa= i
            pp = i+1

            if(y[i]) != None:
              while y[pp] == None:
                if(pp < (len(y)-1)):  break
                else: pp += 1
            else:
              while y[pa] == None:
                if(pa-1 < 0): break
                else: pa -= 1

            ant=y[pa]
            tant=x[pa]
            prox=y[pp]
            tprox=x[pp]

            if prox != None and ant != None:
              if((fator/24 * 13) >= tprox-tant): # 24 * 3
                t = np.trapz([ant, prox], [tant, tprox], dx=dxi) #, [tant, tprox], dx=dxi
                total += t/dxi
              else:
                  print('Intervalo Grande', tprox-tant, (fator/24 * 17))
                  return None


        if(total/fator > 0): return round(total/fator, 3)
        else:
            print('Negativo')
            return None
    else: return None


def integral2(x, y):
    i = 0
    total = 0
    ant = '-999'
    prox = '-999'
    tant = '-999'
    tprox = '-999'

    while i < len(y):
        if(i+1 < len(y)) :
            if(y[i] == None):
                if(ant == '-999'):  
                    ant = 0
                    tant = int(x[i])
            else: 
                if(ant == '-999'):  
                    ant = y[i]
                    tant = int(x[i])
                else:
                    # faz o calculo
                    prox = y[i]
                    tprox = int(x[i])

                    #print(ant, prox, tant, tprox)
                    intervalo = tprox - tant
                    
                    if(intervalo == 0):
                        intervalo=1
                        print(ant, prox, tant, tprox)
                    S = (ant+prox) * intervalo / 2
                    S = S/intervalo

                    
                    b = np.trapz([ant, prox], x=[tant, tprox])

                    #print(S, b)
                    ant = y[i]
                    tant = int(x[i])
                    total += S
                    #print(b)                 
        else:
            if(y[i] != None): 
                prox = y[i]
                tprox = int(x[i])
                print(ant, prox, tant, tprox)
                b = np.trapz([ant, prox], x=[tant, tprox])
                total += S
            #print(b)
        i+=1
    return (total)
