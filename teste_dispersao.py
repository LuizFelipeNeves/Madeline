import matplotlib.pyplot as plt
import csv

ano = 2018
mes = 3

dir_original = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
dir_gerado = './DADOS/OUTPUT_GL/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'


# Faz a leitura da Estimativa do Modelo GL.
def leia(arquivo): 
    with open(arquivo, "r") as tsvGL:
        reader = csv.reader(tsvGL, delimiter=' ')
        GLir=[]
        for row in reader:
            for coluna in range(5, 36): # Faz um loop durante as colunas dia.
                if(row[coluna] != "-999"): GLir.append(float(row[coluna]))
                else: GLir.append(None)
        return GLir
        

def dispersao(posicao):
    cor=['blue', 'red', 'green']
    meses=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    plt.figure(posicao)
    plt.title("Rede Sonda - " + str(ano)[-2:] + " - Dispersão")
    plt.ylabel('Original')
    plt.xlabel('Gerado')

    gerado = leia(dir_gerado)
    original = leia(dir_original)

    limite = 5
    print('original', 'gerado')
    for i in range(len(gerado)):
        if(gerado[i] != original[i]):
            print(original[i], gerado[i])
            limite -= 1
        if(limite == 0): break

    for i in range(len(gerado)):
        if(gerado[i] != None):
            if(gerado[i] > 1600) or gerado[i] == -999: gerado[i]=None
        if(original[i] != None):
            if(original[i] > 1600) or original[i] == -999: original[i]=None
            
    plt.scatter(gerado, original, c=cor[0], label=meses[mes-1], alpha=0.5)
    plt.scatter(media(gerado), media(original), marker='s', c=cor[1], alpha=1.0)
            
    #plt.xlim(0, 400)
    #plt.ylim(0, 400)
    plt.legend(loc='upper left')
    #plt.savefig('./DADOS/' + '/Dispersao.png')

# Soma todos os elementos de um array
def media(array):
    soma = 0;
    count = 1;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
            count += 1
    return soma/(count-1)

dispersao(1)
plt.show();
