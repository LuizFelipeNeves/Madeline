import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import csv

sigla = 'SMS'
ano = 2017

# CPA, PTR, NAT, SLZ, SMS

def dispersao(posicao):
    global silga, ano, mes
    estacoes = [[12, 1, 2], [3, 4, 5], [6, 7, 8 ], [9, 10, 11]]
    cor=['blue', 'red', 'green']
    meses=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    plt.figure(posicao+1)
    plt.title("Rede Sonda - " + sigla + str(ano)[-2:] + " - Dispersão")
    plt.ylabel('Modelo GL')
    plt.xlabel('Sonda')

    for j in range(3):
        mes = estacoes[posicao][j]
        arquivotxt = './DADOS/TXT/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + '.txt'

        try:
            reader = pd.read_csv(arquivotxt, header=None, sep='\t')
            sonda = reader[1].values.tolist()
            GL = reader[2].values.tolist()

            for i in range(len(sonda)):
                if(sonda[i] > 1600) or sonda[i] == -999: sonda[i]=None
                if(GL[i] > 1600) or GL[i] == -999: GL[i]=None

            plt.scatter(sonda, GL, c=cor[j], label=meses[mes-1], alpha=0.5)
            plt.scatter(media(GL), media(GL), marker='s', c=cor[j], alpha=1.0)
            
        except FileNotFoundError: pass
            
    plt.xlim(0, 400)
    plt.ylim(0, 400)
    plt.legend(loc='upper left') #bbox_to_anchor=(0.5, 1), loc='upper left', borderaxespad=0.
    plt.savefig('./DADOS/IMAGENS/' + sigla + '/' + '/Dispersao' + str(posicao+1) + '.png')

# Soma todos os elementos de um array
def media(array):
    soma = 0;
    count = 1;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
            count += 1
    return soma/(count-1)

for posicao in range(4):
    dispersao(posicao)

#dispersao(1)
#dispersao(2)
plt.show();
