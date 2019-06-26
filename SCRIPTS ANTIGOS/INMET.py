# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from funcoes import diames, findElement, diajuliano, jouletowatthora
from module import validar_diaria, GL, plotmensal, plotanual

# Inicio
def plotdiario(opcao):
    diainicial = 1
    diafinal = diames(ano, mes)
    planilha = './DADOS/INMET/' + str(ano) + '/' + sigla + '/' + sigla + '-' + str(ano) + '-' + format(mes, '02d') + '.csv'
    inmet = pd.read_csv(planilha, header=None, sep=',', usecols=[0, 1, 2, 18])
    
    col_dia = 1
    col_hora = 2
    col_ir = 18

    for dia in range(diainicial, diafinal+1):
       textdia = format(dia, '02d') + '/' + format(mes, '02d') + '/' + str(ano)
       select = inmet.iloc[np.where(inmet[col_dia].values == textdia)]

       hora = select[col_hora].values.tolist()
       ir = select[col_ir].values.tolist()

       nhora = [*range(24)]
       nir = [*range(24)]

       for i in range(len(ir)):
           nir[int(hora[i])] = jouletowatthora(float(ir[i])) # Padronizar..

           nhora[int(hora[i])] = hora[i]
           
           #if(ir[i] > 1600 or ir[i] < 0): ir[i]=None # or np.isnan(ir[i])
       validar_diaria(dia, mes, ano, rede, sigla, nir, nhora, opcao);
        
    GL(sigla, listaunica, mes, ano)
    plotmensal(opcao, rede, sigla, mes, ano)

listaunica = 'ListaUnicaCompleta_201606.txt'
rede = 'INMET'
ano= 2018

select = ['A619']

sigla = 'A619'
mes = 3
plotdiario(0)

##for i in range(len(select)):
##    sigla = select[i]
##    for i in range(12):
##       mes = i+1
##       try: plotdiario(0)
##       except FileNotFoundError: pass
##    #plotanual(ano, rede, sigla)

#plt.show();
