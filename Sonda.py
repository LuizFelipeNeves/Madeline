import numpy as np
import pandas as pd
from funcoes import diames, findElement, diajuliano
from module import validar_diaria, GL, plotmensal, plotanual

# Inicio
def plotdiario(opcao):
	diainicial = 1
	diafinal = diames(ano, mes)
	planilha = './DADOS/SONDA/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + 'ED.csv'
	sonda = pd.read_csv(planilha, header=None, sep=';', usecols=[*range(6)])
	cabecalho(str(sonda.loc[0, 3]).isdigit())

	for dia in range(diainicial, diafinal+1):
		select = sonda.iloc[np.where(sonda[col_dia].values == diajuliano(dia, mes, ano))]
		minuto = select[col_min].values.tolist()
		ir = select[col_ir].values.tolist()

		for i in range(len(ir)):
			if(ir[i] > 1600 or ir[i] < 0 or np.isnan(ir[i])): ir[i]=None
			minuto[i] = horamin(minuto[i])

		validar_diaria(dia, mes, ano, rede, sigla, ir, minuto, opcao)
	GL(sigla, listaunica, mes, ano)
	plotmensal(opcao, rede, sigla, mes, ano)

# Define o cabecalho do Cabecalhos
def cabecalho(x):
	global col_dia, col_min, col_ir
	if x == True:
		# Sonda Novo
		col_dia = 2
		col_min = 3
		col_ir = 4
	else:
	   # Sonda Antigo
	   col_dia = 2
	   col_min = 4
	   col_ir = 5

# Converte minutos em horas
def horamin(x):
	hora = (x/60)
	return (hora)

listaunica = 'ListaUnicaCompleta_201606.txt'
rede = 'Sonda'
ano= 2018

select = ['CPA'] #'BRB', 
for i in range(len(select)):
	sigla = select[i]
	for i in range(12):
	   mes = i+1
	   try: plotdiario(0)
	   except FileNotFoundError: pass
	plotanual(ano, rede, sigla)

##plt.show();
