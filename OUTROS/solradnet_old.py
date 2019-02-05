import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

listaunica = 'ListaUnicaCompleta_201606.txt'
col_dia = 0
col_min = 1
col_ir = 3

sigla = 'CUIABA-MIRANDA'
ano = 2018
mes = 1

GLdia=[]
GLir=[]
xmensal=[*range(1, 32)]
ymensal= 31 * [None]

def plotdiario(opcao):
    diainicial = 1
    diafinal = diames(ano, mes)
    planilha = './DADOS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + str(ano) + format(mes, '02d') + format(diainicial, '02d')+ '_' + str(ano) + format(mes, '02d') + format(diafinal, '02d') + '_' + sigla + '_py_ALLPOINTS.lev10'

    sonda = pd.read_csv(planilha, sep=',', header=None, skiprows=4, usecols=[0, 1 , 3])

    for dia in range(diainicial, diafinal+1):
        select_dia = format(dia, '02d') + ':' + format(mes, '02d') + ':' + str(ano)
        select = sonda.iloc[np.where(sonda[col_dia].values == select_dia)]
        ir = select[col_ir].values.tolist()
        minuto = select[col_min].values.tolist()
        minuto = horatomin(minuto)
        
        if(contarelemento(ir) > 630): # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados, 1440-180=1260
            media = mediadiaria(ir)/720
            ymensal[dia-1] = media

            plt.figure(dia)
            plt.cla() # Limpa os eixos
            plt.clf() # Limpa a figura
            plt.plot(minuto, ir, 'b-') #b- é azul
            plt.title("Rede SolRad-Net - " + sigla + str(ano)[-2:] + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(dia) + "]")
            plt.ylabel('Irradiância (Wm-2)')
            plt.xlabel('Tempo (Hora UTC)')
            plt.text(1.5, 1400, 'Média: %5.2f' % media, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})
            plt.ylim(0, 1600)
            plt.xlim(0, 25)
            createdir(ano, mes, sigla)
            diretorio = './DADOS/IMAGENS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
            plt.savefig(diretorio + '/' + str(dia) + '.png')
            if(opcao == 0): plt.close()

    GL()
    plotmensal(opcao)

def plotmensal(opcao):
    global xmensal, ymensal
    plt.figure('Mensal')
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    plt.plot(xmensal, ymensal, 'b-') #b- é azul
    plt.plot(GLdia, GLir, 'r-') #r- é vermelho
    plt.title("Rede SolRad-Net - " + sigla + str(ano)[-2:] + format(mes, '02d') + " - Medias Diárias")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1, 31)

    # Media
    try: mediamensal = somararray(ymensal)/contarelemento(ymensal)
    except: mediamensal = 0;
    plt.text(3, 400, 'Média SolRad-Net: %5.2f' % mediamensal, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':8})

    print(ymensal)
    print('-')
    print(GLir)

    # Media GL
    try: mediagl = somararray(GLir)/contarelemento(GLir)
    except: mediagl = 0;
    plt.text(18, 400, 'Média GL: %5.2f' %mediagl, bbox={'facecolor':'red', 'alpha':0.5, 'pad':8})

    diretorio = './DADOS/IMAGENS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    createdir(ano, mes, sigla)
    plt.savefig(diretorio + '/Mensal.png')

    if(opcao == 0): plt.close()


    # Limpa as Variaveis
    ymensal.clear()
    ymensal= 31 * [None]

    GLdia.clear()
    GLir.clear()

    for i in range(len(GLir)):
        p = ymensal[i]/100
        d = ymensal[i]-GLir[i]
        print('Dia: ' + str(i+1) + 'P: %5.2f' % (d/p) + '%')

    print('Concluido: ' + str(mes) + ', ' + str(ano) + ', ' + sigla)

# Faz a leitura da Estimativa do Modelo GL.
def GL():
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    with open(dadosGL, "r") as tsvGL:
        reader = csv.reader(tsvGL, delimiter=' ')
        id = getID(sigla);
        for row in reader:
            if(id == row[0]): # Identifica a estação
                for coluna in range(5, 36): # Faz um loop durante as colunas dia.
                    GLdia.append(coluna-4)
                    print(row[coluna])
                    if(row[coluna] != "-999"): GLir.append(float(row[coluna]))
                    else: GLir.append(None)
                break;

def GL2():
    id = getID(sigla);
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    gl = pd.read_csv(dadosGL, sep=' ', header=None)
    select = gl.iloc[np.where(gl[0].values == id)]
    for coluna in range(5, 36):
        GLdia.append(coluna-4)
        if(str(select[coluna]) != "-999"): GLir.append(float(select[coluna]))
        else: GLir.append(None)

def checkdir(diretorio):
    try: os.stat(diretorio)
    except: os.mkdir(diretorio)

def createdir(ano, mes, sigla):
    diretorio = './DADOS/IMAGENS/SolRad-Net/'
    checkdir(diretorio)
    diretorio += str(ano) + '/'
    checkdir(diretorio)
    diretorio += sigla + '/'
    checkdir(diretorio)
    diretorio += format(mes, '02d') + '/'
    checkdir(diretorio)
    

def selecaolistaunica():
    lista = pd.read_csv(listaunica, sep='\t', header=None, usecols=[4 , 6, 9], encoding="latin-1")
    select = lista.iloc[np.where(lista[4].values == 14)]
    select = select.iloc[np.where(select[6].values != '-999')]
    select = select[6].values.tolist()
    return select

def diames(ano, mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1;
    return diasmes[int(mes)-1]

# Pega o ID da Estação
def getID(sigla):
    with open(listaunica) as lista:
        reader = csv.reader(lista, delimiter='\t')
        for row in reader:
            if(sigla == row[6]): return row[0];

def contarelemento(array):
    count = 0;
    for i in range(len(array)):
        if(array[i] != None): count += 1
    return(count)

# Soma todos os elementos de um array
def somararray(array):
    soma = 0;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
    return soma

def horatomin(data):
    for i in range(len(data)):
        hora = int(str(data[i])[:2])
        minuto = int(str(data[i])[3:5]) + 1
        data[i] = ((hora*60) + minuto)/60
    return data

# Media do dia, usando o metodo dos trapezios
def mediadiaria(array):
    menor=0
    maior=0
    somatotal = 0
    abre=[]
    fecha=[]
    chave=False
    for i in range(len(array)):
        if(array[i] is None):
            if chave == False: # Abre
                abre.append(i)
                chave = True;
        else:
            if(chave == True): # Fecha
                fecha.append(i-1)
                chave = False;
            if(menor == 0): menor = array[i] # Menor
            if(array[i] > maior): maior= array[i] # Maior
            somatotal += array[i];

        if((i+1 == len(array)) and chave == True): # Verifica o fim do array
            fecha.append(i)
            chave = False;

    # Calcula os valores
    for i in range(len(abre)):
        intervalo = ((fecha[i]-abre[i])+1)
        if((abre[i]-1 > 0) and (fecha[i]+1 < len(array))): # Apenas entra na condição caso o inicio seja maior que 0, e o fim menor que o limite.
            S = (array[abre[i]-1]+array[fecha[i]+1])*intervalo/2
            somatotal += S/intervalo;
        elif((abre[i]-1 > 0) and(fecha[i]+1 > len(array))):
            S = (array[abre[i]-1])*intervalo/2
            somatotal += S/intervalo;
        elif((abre[i]-1 < 0) and (fecha[i]+1 < len(array))):
            S = (array[fecha[i]+1])*intervalo/2
            somatotal += S;

    return(somatotal)


select = selecaolistaunica()
#'Ji_Parana_SE',
#'Alta_Floresta',
#'Rio_Branco',
#'CUIABA-MIRANDA',
#'Barcelona'
#'Moldova']

for i in range(len(select)):
    sigla = select[i]
    for i in range(12):
       mes = i+1
       try: plotdiario(0)
       except FileNotFoundError: pass

print(len(xmensal))
print(len(ymensal)) 
       
##sigla = 'Alta_Floresta'
##for i in range(12):
##    mes = i+1
##    plotdiario(0)  
 

#plotdiario(0)
#plt.show()
