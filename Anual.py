# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import os
from module import lertexto
from funcoes import diferenca, somararray, contarelemento, diajuliano #, diames, getLoc, formatn , findElement, getID, erropadrao, desviopadrao,  integral

def getanual(ano, rede, sigla):
    GL = [None] * 366
    G = [None] * 366
    for i in range(1, 13):
        data = lertexto(ano, i, sigla)
        for p in range(len(data[0])):
            dia = diajuliano(p, i, ano)            
            GL[dia] = data[0][p]
            G[dia] = data[1][p]
    return G, GL

def plotanual(ano, rede, sigla):  
    dia_anual= [*range(1, 367)]
    data = getanual(ano, rede, sigla)
    print(len(dia_anual))
    G = data[1]
    GL1x = data[0]

    # ir_anual_gl3x = []
    # ir_anual_gl5x = []

    d = diferenca(GL1x, G, 0)
    
    # (a - b)-c
    #d1 = diferenca(GL1x, G , 0)
    #d3 = diferenca(ir_anual_gl3x, G, 0)
    #d5 = diferenca(ir_anual_gl5x, G, 0)

    # Media Terrestre
    try: mediamensal = somararray(G)/contarelemento(G)
    except: mediamensal = 0

    # Media GL
    try: mediagl1x = somararray(GL1x)/contarelemento(GL1x)
    except: mediagl1x = 0

    plt.figure(sigla, figsize=(20, 10))
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    plt.plot(dia_anual, G, 'b-') #b- é azul
    plt.plot(dia_anual, GL1x, 'r-') #r- é vermelho
    plt.plot(dia_anual, d, 'g-')
    plt.plot([0, 360], [0, 0], 'k-')
    
    #plt.plot(dia_anual, d1, 'y-')
    #plt.plot(dia_anual, d3, 'c-')
    #plt.plot(dia_anual, d5, 'm-')

    diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/'
    plt.title('Rede ' + rede + ' - ' + sigla + '-' + str(ano) + " - Anual")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(-200, 450)
    plt.xticks(np.arange( 0, 370, 30))
    plt.xlim(1, 370)
    plt.legend(('Média ' + rede + ': %5.2f' % mediamensal, 'Média GL: %5.2f' %mediagl1x, 'Diferença'), loc='upper left')
    plt.savefig(diretorio + 'Anual.png', dpi=300, bbox_inches='tight')

##    ## Dispersão
##    plt.figure(str(sigla)+'D')
##    x=[0,450]
##    y=[0,450]
##    plt.title('Rede ' + rede + ' - ' + sigla + '-' + str(ano) + " - Dispersão Anual")
##    plt.ylabel('Modelo GL')
##    plt.xlabel(rede)
##    plt.xlim(x)
##    plt.ylim(y)
##    plt.plot(x, y, 'r-')
##    plt.scatter(G, GL1x, c='b', alpha=0.5)
##    plt.savefig(diretorio + '/Anual-Dispersao.png', dpi=300, bbox_inches='tight')


ano = 2018
#estacoes = [ 'Alta_Floresta']

#for sigla in estacoes:
plotanual(ano, 'SOLRADNET', 'Alta_Floresta')
plotanual(ano, 'SOLRADNET', 'CUIABA-MIRANDA')
plotanual(ano, 'SOLRADNET', 'Ji_Parana_SE')
plotanual(ano, 'SOLRADNET', 'Rio_Branco')
plotanual(ano, 'SONDA', 'CPA')
plotanual(ano, 'SONDA', 'BRB')
plt.show()
