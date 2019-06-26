import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from funcoes import diferenca, contarelemento, somararray

string_estacaoes = ['Alta_Floresta', 'CUIABA-MIRANDA', 'Ji_Parana_SE', 'BRB', 'CPA']
string_redes = ['SOLRADNET', 'SOLRADNET','SOLRADNET', 'SONDA', 'SONDA']
ano = 2018
mes=7
arquivosonda = './DADOS/TXT/7/SPMEDIA201807.txt'
arquivogl = './DADOS/TXT/7/GLMEDIA201807.txt'

dadossonda = pd.read_csv(arquivosonda, header=None, skiprows=1, sep='\t');
dadosgl = pd.read_csv(arquivogl, header=None, skiprows=1, sep='\t');

for i in range(len(dadossonda)):
    plt.figure(i)

    sonda = dadossonda.iloc[i, 4:28].values.tolist()
    GL = dadosgl.iloc[i, 4:28].values.tolist()
    sigla = string_estacaoes[i]
    rede = string_redes[i]
    hora = [*range(24)]
    for i in range(len(sonda)):
        if(sonda[i] > 1600) or sonda[i] == -999: sonda[i]=None
        if(GL[i] > 1600) or GL[i] == -999: GL[i]=None

    dif = diferenca(GL, sonda, 0)
    c1 = contarelemento(GL)
    c2 = contarelemento(sonda)
    
    mediafinal = 0
    if(c1 != 0 and c2 != 0):
        tempgl = somararray(GL)/c1
        tempsonda = somararray(sonda)/c2
        mediafinal =  (tempgl + tempsonda) /2
    
    print(sigla, mediafinal, dif)
    print('--GL-- ')
    print(GL)
    print('--Sonda--')
    print(sonda)
    print()
    
    plt.plot(hora, sonda, 'k-', label='SP') # , label=labelsp preto
    plt.plot(hora, GL, 'r-', label='GL 1x')  # , label=labelgl1x GL vermelho
    plt.plot(hora, dif, 'b-', label='Diferença GL-G') # azul

    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d'))
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    plt.legend(loc='upper left')
    plt.ylim(-200, 1000)
    plt.xlim(9, 23)
    plt.grid()
    plt.show();
    #diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    #plt.savefig(diretorio + '/' + str(dia) + '.png')
    #plt.close() #if opcao == 0: plt.close()
    #plt.cla() # Limpa os eixos
    #plt.clf() # Limpa a figura
        
# Soma todos os elementos de um array
def media(array):
    soma = 0;
    count = 1;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
            count += 1
    return soma/(count-1)
