import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from funcoes import diajuliano, formatn, diferenca, desviopadrao, erropadrao, getLoc, contarelemento, diames#, findElement, selecaolistaunica
from module import integral, binario, getir, regiao, gerarhoras, escalatemp2#, validar_diaria, GL, plotmensal, plotanual

#select = selecaolistaunica(14, listaunica)

# TODO: rede, plotmensal, plotanual, save files

def plotgeral(mes, ano):
    diainicial = 1
    diafinal = diames(ano, mes)
    opcao = 0
    listaunica = 'ListaUnicaCompleta_201606.txt'
    dataestacoes = []
    posicoes = []

    NE = 4
    matrizdiariaGL0 = np.zeros((NE, 27))
    matrizposicoes = np.zeros((NE, 3))

    matrizdiariaGL0[0, :3] = [29903, -9.871, -56.104]
    matrizdiariaGL0[1, :3] = [29907, -15.729, -56.021]
    matrizdiariaGL0[2, :3] = [29902, -10.934, -62.852]
    matrizdiariaGL0[3, :3] = [29905, -9.957, 67.869]


    latfinal = 22-0.04
    loninicial = -100
    for i in range(NE):
        LAT = matrizdiariaGL0[i, 1]
        LON = matrizdiariaGL0[i, 2]
        IDD = matrizdiariaGL0[i, 0]
        linha = int(((latfinal - LAT)/.04+0.5))
        coluna = int((LON - loninicial)/.04+0.5)
        matrizposicoes[i, :3] = [IDD, linha, coluna]
    

    
    #dataallestacoes = len(dataestacoes) * [diafinal * [24 * [None]]]
    #dataallgl1x = len(dataestacoes) * [diafinal * [24 * [None]]]
    #dataallgl3x = len(dataestacoes) * [diafinal * [24 * [None]]]
    #dataallgl5x = len(dataestacoes) * [diafinal * [24 * [None]]]

    for dia in range(diainicial, diafinal+1):        
        minutonovo = gerarhoras()
        minutonovo = [i * 60 for i in minutonovo]

        # DATA
        anomesdia = ano * 10000 + mes * 100 + dia
        datagl = GLbinarios(anomesdia, matrizposicoes, matrizdiariaGL0)        
        
        for i in range(len(dataestacoes)):
            #sigla = dataestacoes[i][0]
            #dadosdiaestacao = formatadia(dia, dataestacoes[i][1])

            # datagl[0][estacao]
            gl1x = datagl[0][i, :] 
            gl3x = datagl[1][i, :]
            gl5x = datagl[2][i, :]
          
            
            #csp = contarelemento(dadosdiaestacao)
            cgl1x = contarelemento(gl1x)
            cgl3x = contarelemento(gl3x)
            cgl5x = contarelemento(gl5x)
            
            if(cgl1x < 7): gl1x = len(gl1x) * [None]
            if(cgl3x < 7): gl3x = len(gl1x) * [None]
            if(cgl5x < 7): gl5x = len(gl1x) * [None]

            dataallgl1x[i][dia-1] = gl1x
            dataallgl3x[i][dia-1] = gl3x
            dataallgl5x[i][dia-1] = gl5x

            hora = [*range(24)]
            mediasp = integral(hora, dadosdiaestacao, len(dadosdiaestacao))
            mediagl1x = integral(hora, gl1x, len(gl1x))
            mediagl3x = integral(hora, gl3x, len(gl3x))
            mediagl5x = integral(hora, gl5x, len(gl5x))
            
            if(csp > 7):
                dataallestacoes[i][dia-1] = dadosdiaestacao


    # load tabela GL. >> plotmensal(opcao, rede, sigla, mes, ano)
    dataestacoes.clear() # limpa da memoria
    print('Concluido: ' + format(mes, '02d') + '-' + str(ano))

def checkdir(diretorio):
    try: os.stat(diretorio)
    except: os.mkdir(diretorio)

def createdir(ano, mes, sigla, rede):
    diretorio = './DADOS/IMAGENS/' + rede + '/'
    checkdir(diretorio)
    diretorio += str(ano) + '/'
    checkdir(diretorio)
    diretorio += sigla + '/'
    checkdir(diretorio)
    diretorio += format(mes, '02d') + '/'
    checkdir(diretorio)    
 
def GLbinarios(anomesdia, matrizposicoes, matrizdiariaGL0):
    anomes = int(anomesdia/100)
    diretorio = './DADOS/GLGOESbin_horarios/' + str(anomes) + '/'
    minutos = [0, 15, 30, 45]


    NE = len(matrizposicoes[:, 1])
    final1x = np.zeros((NE, 4* 24))
    final3x = np.zeros((NE, 4 * 24))
    final5x = np.zeros((NE, 4 * 24))
    
    for h in range(8, 24):
        for m in range(len(minutos)):
            try:
                file = 'S11636057_' + str(anomesdia) + format(h, '02d') + format(minutos[m], '02d') + '.bin'
                matriz = binario(diretorio + file, 2018)
                for i in range(NE):
                    linha = matrizposicoes[i, 1]
                    coluna = matrizposicoes[i , 2]
                    p = (h) * len(minutos) + m
                    x1 = getir(matriz, linha, coluna, 0, 0)
                    #x3 = regiao(matriz, lat , long, 1)
                    #x5 = regiao(matriz, lat , long, 2)

                    final1x[i, p] = x1
                    #final3x[i, p] = x3
                    #final5x[i, p] = x5
            except FileNotFoundError: pass


    ## Escala
    minuto = gerarhoras()
    matrizdiariaGL = matrizdiariaGL0
    for i in range(NE):
        matrizdiariaGL[i , 3:27] = escalatemp2([i * 60 for i in minuto], final1x[i, :])
            

    ## GRAVAR TEXTO
    diretorio = './DADOS/TXT/ANOMESDIA/GL12'
    #checkdir(diretorio)
    arquivotxt = diretorio + '/GL12_'  + str(anomesdia) + '.txt'
    
    with open(arquivotxt,'wb') as f:
        for line in matrizdiariaGL:
            np.savetxt(f, line, fmt='%.2f')
    
    return [final1x, final3x, final5x] # data[0][estacaomatriz]

def formatadia(dia, data):
    temp = selectdia(dia, data)
    minuto = temp[0]
    ir = temp[1]
    final = 24 * [None]
    if(contarelemento(ir) > (len(ir)/ 24) * 8):
        minutonovo = [i * 60 for i in minuto]
        m = minutonovo[1]-minutonovo[0]
        media = integral(minutonovo, ir, 1440/m)
        if(media != None):
            minutonovo = gerarhoras()
            minutonovo = [i * 60 for i in minutonovo]
            final = escalatemp2([i * 60 for i in minuto], ir)
            
    return final

ano = 2018
mes = 5
plotgeral(mes, ano) 

##for i in range(1, 12+1):
##    mes = i
##    plotgeral(mes, ano)       
#plotanual(ano, , sigla)
#plt.show()
