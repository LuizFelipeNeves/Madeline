import numpy as np
import matplotlib.pyplot as plt
import csv

import time
import timeit

ano = 2018
mes = 3
arquivotxt = './DADOS/OUTPUT_GL/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
diretorio = './DADOS/GLGOESbin/2018/03/'

def lista_estacoes():
    lista=[]
    estacao = 'ListaUnicaCompleta_201606.txt'
    with open(estacao) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            lista.append([row[0] , row[1], row[2], row[3], row[4]]);
    return lista   

def binario(diretorio):
    x = np.fromfile(diretorio, np.int16)
    #x = x.byteswap() // ate 2018
    x = x.reshape(1800, 1800)
    x = x/10
    return x	

def getir(matriz, LAT, LON):
    #latinicial = -50; lonfinal = -28; 
    latfinal = 22;
    loninicial = -100;
    linha = int((latfinal - LAT)/.04)
    coluna = int((LON - loninicial)/.04)
    return matriz[linha, coluna]

def irmensal(LAT, LON):
    ir= []
    for i in range(1, 31):
        try:
            file = 'S11636061_201803' + format(i, '02d') + '0000.bin'
            matriz = binario(diretorio + file)
            value = getir(matriz, LAT, LON)
            ir.append(value)
        except: ir.append(-999)
    return ir


def teste():
    estacoes = lista_estacoes()
    FINAL = np.zeros((len(estacoes), 31) , float)
    for dia in range(31):
        try:
            file = 'S11636061_201803' + format(dia+1, '02d') + '0000.bin'
            matriz = binario(diretorio + file)
            for i in range(1446):
                print(float(estacoes[i][2]))
                ir = getir(matriz, float(estacoes[i][1]), float(estacoes[i][2]))
                FINAL[i][dia] = ir

        except:
            for linha in range(len(estacoes)): matriz[linha][dia] = -999
            
teste()

def gravarGL():
    arquivo = open(arquivotxt, 'w', encoding="ansi")
    string = '%ID Lat Lon Alt Dono 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31'
    espaco = ' '
    estacoes = lista_estacoes()
    for linha in range(len(estacoes)):
            estacao = estacoes[linha]
            ir = irmensal(estacao[1], estacao[2])
            for i in range(len(estacao)-1): string += estacao[i] + espaco
            string += estacao[len(estacao)-1]
            for i in range(len(ir)): string += espaco + str(ir[i])
            print(str(linha+1) + '/1446')
    arquivo.write(string)
    arquivo.close()
    print('Fim')

inicio = timeit.default_timer()
#gravarGL()
fim = timeit.default_timer()
print ('duracao: %.2f segundos' % (fim - inicio))
##dia = binario('./DADOS/GLGOESbin/2018/03/S11636061_201803010000.bin')
##plt.imshow(dia, cmap="jet")
##plt.colorbar()
##plt.show()

######################################################
