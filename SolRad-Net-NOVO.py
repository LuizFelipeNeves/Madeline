import numpy as np
import pandas as pd
from funcoes import getLoc, contarelemento, diames, findElement, selecaolistaunica
from module import integral, binario, getir, regiao, gerarhoras, escalatemp2, validar_diaria, GL, plotmensal, plotanual

#select = selecaolistaunica(14, listaunica)

def plotgeral(mes, ano, estacoes):
    diainicial = 1
    diafinal = diames(ano, mes)
    listaunica = 'ListaUnicaCompleta_201606.txt'
    dataestacoes = []
    
    for i in range(len(estacoes)):
        sigla = estacoes[i]
        posicaoGL = getLoc(sigla , listaunica)
        try: dataestacoes.append([sigla, lermes(diafinal, mes, ano, sigla), posicaoGL])
        except FileNotFoundError: pass

    dataallestacoes = len(dataestacoes) * [diafinal * [24 * [None]]]
    dataallgl = len(dataestacoes) * [diafinal * [24 * [None]]]

    # Para apenas um dia, set dia inicial e final para o dia, aqui!
    for dia in range(diainicial, diafinal+1):
        posicoes = []
        for i in range(len(dataestacoes)):
            posicoes.append(dataestacoes[i][2])
        
        tempgl = GLbinarios(dia, mes, ano, posicoes)[0]
        for i in range(len(dataestacoes)):
            sigla = dataestacoes[i][0]
            dadosestacao = dataestacoes[i][1]
            dadosdiaestacao = formatadia(dia, dadosestacao)
            dataallestacoes[i][dia-1] = dadosdiaestacao
            dataallgl[i][dia-1] = tempgl[0]            
            if(contarelemento(dadosdiaestacao) > 7):
                print('Estação: ' + sigla + ' -- '+ format(dia, '02d') + '/' + format(mes, '02d') + '/' + str(ano)) # plot dia
            
    dataestacoes.clear() # limpa da memoria

    # gerar figura com dados das varias estacoes
    # salvar arquivo

    # load tabela GL. >> plotmensal(opcao, rede, sigla, mes, ano)

 
def GLbinarios(dia, mes, ano, estacoes):
    diretorio = './DADOS/GLGOESbin_horarios/' + str(ano) + format(mes, '02d') + '/'
    minutos = [0, 15, 30, 45]
    final1x= len(estacoes) * [len(minutos) * 24 * [None]]
    final3x= len(estacoes) * [len(minutos) * 24 * [None]]
    final5x= len(estacoes) * [len(minutos) * 24 * [None]]
    for h in range(8, 24):
        for m in range(len(minutos)):
            try:
                file = 'S11636057_' + str(ano) + format(mes, '02d') + format(dia, '02d') + format(h, '02d') + format(minutos[m], '02d') + '.bin'
                matriz = binario(diretorio + file, ano)
                for i in range(len(estacoes)):
                    loc = estacoes[i]
                    lat = loc[0]
                    long = loc[1]
                    p = (h) * len(minutos) + m
                    x1 = getir(matriz, lat, long, 0 , 0)
                    x3 = regiao(matriz, lat , long, 1) # 0, 1 , 2
                    x5 = regiao(matriz, lat , long, 2) # 0, 1 , 2
                    
                    final1x[i][p] = x1
                    final3x[i][p] = x3
                    final5x[i][p] = x5
            except FileNotFoundError: pass
    return [final1x, final3x, final5x]

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
            #media = round(media, 3)
            minutonovo = gerarhoras()
            minutonovo = [i * 60 for i in minutonovo]
            final = escalatemp2([i * 60 for i in minuto], ir)
            
    return final

# é diferente
def lermes(diafinal, mes, ano, sigla):
    diainicial = 1
    rede = 'SolRad-Net'
    planilha = './DADOS/' + rede + '/' + str(ano) + '/' + sigla + '/' + str(ano) + format(mes, '02d') + format(diainicial, '02d')+ '_' + str(ano) + format(mes, '02d') + format(diafinal, '02d') + '_' + sigla + '_py_ALLPOINTS.lev10'
    return pd.read_csv(planilha, sep=',', header=None, skiprows=4, usecols=[0, 1 , 3])
    

# é diferente
def selectdia(dia, data):
    col_dia = 0
    col_min = 1
    col_ir = 3
    select_dia = format(dia, '02d') + ':' + format(mes, '02d') + ':' + str(ano)
    select_ir = data.iloc[np.where(data[col_dia].values == select_dia)]
    ir = select_ir[col_ir].values.tolist()
    minuto = select_ir[col_min].values.tolist()
    minuto = horatomin(minuto)
    for i in range(len(ir)):
        if(ir[i] < 0): ir[i] = None
    return [minuto, ir]

# é diferente
def horatomin(data):
    for i in range(len(data)):
        hora = int(str(data[i])[:2])
        minuto = int(str(data[i])[3:5])
        data[i] = ((hora*30) + (minuto/2)) / 30
        #print(hora, minuto, data[i])
        #((hora*60) + minuto)/60
    return data

ano = 2018
string_estacaoes = ['Alta_Floresta', 'CUIABA-MIRANDA', 'Ji_Parana_SE', 'Rio_Branco']
for i in range(1, 12+1):
    mes = i
    plotgeral(mes, ano, string_estacaoes)       
#plotanual(ano, rede, sigla)

#plt.show()
