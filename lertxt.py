import numpy as np
import pandas as pd


def selectdia(ano, mes, dia, estacao):
    planilha = './DADOS/TXT/ANOMESDIA/GL12/GL12_' + str(ano) + format(mes, '02d') + format(dia, '02d') + '.txt'
    data = pd.read_csv(planilha, header=None, sep='\t')
    select = data.iloc[np.where(data[0].values == estacao)]

    string = ''
    for i in range(len(select.columns)-1):
        string += str(select.iloc[0, i]) + '\t'
    string += str(select.iloc[0, -1]) + '\n'    
    return string

print(selectdia(2018, 2, 4, 29903))




