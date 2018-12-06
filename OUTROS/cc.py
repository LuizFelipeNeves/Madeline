import pandas as pd
import numpy as np

def cabecalho(x):
    global col_dia, col_min, col_irrad, rede
    if x == True:
        # Sonda Novo
        col_dia = 2
        col_min = 3
        col_irrad = 4
    else:
       # Sonda Antigo 
       col_dia = 2
       col_min = 4
       col_irrad = 5


sigla = 'PTR'
ano = 2017
mes = 3

planilha = './DADOS/SONDA/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + 'ED.csv'

df = pd.read_csv(planilha, header=None, sep=';', usecols=[*range(6)])

cabecalho(str(df.loc[0, 3]).isdigit())
select = df.iloc[np.where(df[col_dia].values == 90)]

x = select[col_min].values.tolist()
y = select[col_irrad].values.tolist()

for i in range(len(y)):
    if(y[i] > 1300): y[i]=np.nan
        
#if(np.isnan(IR)): print(IR)
#select = df.loc[df[col_dia] == 90]
        
# Versao do Cabecalho,
# Identificar valores acima de 1600, Nan
# Passar esses valores para uma lista/array
# Salvar figura apenas caso gere o grafico.



