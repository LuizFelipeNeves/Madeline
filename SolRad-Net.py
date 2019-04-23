import numpy as np
import pandas as pd
from funcoes import diames, findElement, selecaolistaunica
from module import validar_diaria, GL, plotmensal, plotanual

def plotdiario(opcao):
    diainicial = 1
    diafinal = diames(ano, mes)
    planilha = './DADOS/' + rede + '/' + str(ano) + '/' + sigla + '/' + str(ano) + format(mes, '02d') + format(diainicial, '02d')+ '_' + str(ano) + format(mes, '02d') + format(diafinal, '02d') + '_' + sigla + '_py_ALLPOINTS.lev10'

    sp = pd.read_csv(planilha, sep=',', header=None, skiprows=4, usecols=[0, 1 , 3])
    for dia in range(diainicial, diafinal+1):
        select_dia = format(dia, '02d') + ':' + format(mes, '02d') + ':' + str(ano)
        select_ir = sp.iloc[np.where(sp[col_dia].values == select_dia)]
        ir = select_ir[col_ir].values.tolist()
        minuto = select_ir[col_min].values.tolist()
        minuto = horatomin(minuto)

        temp = len(minuto) * [None]
        for i in range(len(minuto)):
            if(ir[i] < 0): temp[i]=None
            else: temp[i] = ir[i]
                   
        ir = temp
        validar_diaria(dia, mes, ano, rede, sigla, ir, minuto, opcao)

    GL(sigla, listaunica, mes, ano)
    plotmensal(opcao, rede, sigla, mes, ano)
    
def horatomin(data):
    for i in range(len(data)):
        hora = int(str(data[i])[:2])
        minuto = int(str(data[i])[3:5])
        data[i] = ((hora*30) + (minuto/2)) / 30
        #print(hora, minuto, data[i])
        #((hora*60) + minuto)/60
    
    return data


listaunica = 'ListaUnicaCompleta_201606.txt'
rede = 'SolRad-Net'
ano=2018
col_dia = 0
col_min = 1
col_ir = 3

select = selecaolistaunica(14, listaunica)
for i in range(len(select)):
    sigla = select[i]
    for i in range(12):
       mes = i+1
       try: plotdiario(0)
       except FileNotFoundError: pass
    plotanual(ano, rede, sigla)

##sigla = 'Alta_Floresta'  # Rio_Branco, CUIABA-MIRANDA
##ano=2018
###for i in range(12):
###    mes = i+1
###    plotdiario(0)
##mes = 5
##plotdiario(0)
##plotanual(ano, rede, sigla)

#plt.show()





