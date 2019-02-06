import numpy as np
import matplotlib.pyplot as plt
import csv

import time
import timeit

def lista_estacoes():
    lista=[]
    texto = 'ListaUnicaCompleta_201606.txt'
    with open(texto) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            lista.append([row[0] , row[1], row[2], row[3], row[4]]);
    return lista   

def binario(diretorio):
    x = np.fromfile(diretorio, np.int16)
    if(ano  < 2018): x = x.byteswap()
    x = x.reshape(1800, 1800)
    x = x/10
    return x	

def getir(matriz, LAT, LON):
    latfinal = 22-0.04;
    loninicial = -100;
    linha = int(((latfinal - LAT)/.04+0.5))
    coluna = int((LON - loninicial)/.04+0.5)
    try:
        valor = float(matriz[linha , coluna])
        if(valor < 1) : valor=-999
        return(str(valor))
    except: return('-999')

def criarmatriz():
    diretorio = './DADOS/GLGOESbin/' + str(ano) + '/' + format(mes, '02d') + '/'
    estacoes = lista_estacoes()
    FINAL = np.zeros((len(estacoes), 31) , object)
    for dia in range(31):
        try:
            file = 'S11636061_' + str(ano) + format(mes, '02d') + format(dia+1, '02d') + '0000.bin'  
            matriz = binario(diretorio + file)         
            for linha in range(len(estacoes)):
                lat = float(estacoes[linha][1])
                lon = float(estacoes[linha][2])
                ir = getir(matriz, lat, lon)
                FINAL[linha][dia] = ir
        except:
            for linha in range(len(estacoes)): FINAL[linha][dia] = -999
    return FINAL

def gravar(matriz):
    arquivotxt = './DADOS/OUTPUT_GL/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    arquivo = open(arquivotxt, 'w', encoding="ansi")
    espaco = ' '
    header = '%ID Lat Lon Alt Dono 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31'
    arquivo.write(header + espaco + '\n')
    estacoes = lista_estacoes()
    for linha in range(len(estacoes)):
        ir = matriz[linha]
        estacao = estacoes[linha]
        string = ''
        string += estacao[0] + espaco
        string += str(float(estacao[1])) + espaco
        string += str(float(estacao[2])) + espaco
        string += estacao[3] + espaco
        string += estacao[4] + espaco
                   
        for i in range(len(ir)): string += str(ir[i]) + espaco
        arquivo.write(string + '\n')
    arquivo.close()

ano = int(input('Insira o ano:'))
for i in range(1, 13):
    mes = i
    inicio = timeit.default_timer()
    final = criarmatriz()
    gravar(final)
    fim = timeit.default_timer()
    print ('duracao: %.2f segundos' % (fim - inicio))
print('Fim')
