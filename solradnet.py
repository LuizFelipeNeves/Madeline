import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import os
from funcoes import *

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

dia_anual= [*range(1, 367)]
ir_anual_sol= 366 * [None]
ir_anual_gl=366 * [None]

def plotdiario(opcao):
    diainicial = 1
    diafinal = diames(ano, mes)
    planilha = './DADOS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + str(ano) + format(mes, '02d') + format(diainicial, '02d')+ '_' + str(ano) + format(mes, '02d') + format(diafinal, '02d') + '_' + sigla + '_py_ALLPOINTS.lev10'

    sonda = pd.read_csv(planilha, sep=',', header=None, skiprows=4, usecols=[0, 1 , 3])
    for dia in range(diainicial, diafinal+1):
        select_dia = format(dia, '02d') + ':' + format(mes, '02d') + ':' + str(ano)
        select_ir = sonda.iloc[np.where(sonda[col_dia].values == select_dia)]
        ir = select_ir[col_ir].values.tolist()
        minuto = select_ir[col_min].values.tolist()
        minuto = horatomin(minuto)
        temp = 720 * [None]
        for i in range(len(minuto)): temp[minuto[i]] = ir[i]
        minuto = [*range(720)]
        for i in range(len(minuto)): minuto[i] = minuto[i]/30
        ir = temp
       
        if(contarelemento(ir) > 630): # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados, 1440-180=1260
            media = mediadiaria(ir)/720
            ymensal[dia-1] = media
            temp_day = diajuliano(dia, mes, ano)
            ir_anual_sol[temp_day-1] = round(media, 3);

            plt.figure(dia)
            plt.cla() # Limpa os eixos
            plt.clf() # Limpa a figura
            plt.plot(minuto, ir, 'b-') #b- é azul
            plt.title("Rede SolRad-Net - " + sigla + str(ano)[-2:] + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(dia) + "]")
            plt.ylabel('Irradiância (Wm-2)')
            plt.xlabel('Tempo (Hora UTC)')
            plt.legend(['Média: %5.2f' %media], loc='upper left')
            plt.ylim(0, 1600)
            plt.xlim(0, 25)
            createdir(ano, mes, sigla)
            diretorio = './DADOS/IMAGENS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
            plt.savefig(diretorio + '/' + str(dia) + '.png')
            if opcao == 0: plt.close()

    GL()
    plotmensal(opcao)

def plotmensal(opcao):
    global xmensal, ymensal

    # Media
    try: mediamensal = somararray(ymensal)/contarelemento(ymensal)
    except: mediamensal = 0;

    # Media GL
    try: mediagl = somararray(GLir)/contarelemento(GLir)
    except: mediagl = 0;

    dp_sol = str(desviopadrao(ymensal))
    err_sol = str(erropadrao(dp_sol, ymensal))
    dp_gl = str(desviopadrao(GLir))
    err_gl = str(erropadrao(dp_gl, GLir))
  
    plt.figure('Mensal')
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    labels = 'Média SRN: %5.2f' % mediamensal + '\n' + 'DP SRN: ' + dp_sol + '\n' + 'EP SRN: ' + err_sol
    plt.plot(xmensal, ymensal, 'b-', label=labels)

    labelgl = 'Média GL: %5.2f' %mediagl + '\n' + 'DP GL: ' + dp_gl + '\n' + 'EP GL: ' + err_gl
    plt.plot(GLdia, GLir, 'r-', label=labelgl)
    
    plt.title("Rede SolRad-Net - " + sigla + str(ano)[-2:] + format(mes, '02d') + " - Medias Diárias")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1, 31)
    plt.legend(loc='upper left', fontsize=6)

    diretorio = './DADOS/IMAGENS/SolRad-Net/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    createdir(ano, mes, sigla)
    plt.savefig(diretorio + '/Mensal.png')

    if opcao == 0: plt.close()
    
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura

    x=[0,350]
    y=[0,350]
    plt.figure('Mensal-D')
    plt.title("Rede SolRad-Net - " + sigla + '-' + str(ano) + str(mes) + " - Dispersão")
    plt.ylabel('Modelo GL')
    plt.xlabel('SolRad-Net')
    plt.ylim(y)
    plt.xlim(x)
    plt.scatter(ymensal, GLir)
    plt.plot(x, y, 'r-')
    #plt.legend(loc='upper left') #bbox_to_anchor=(0.5, 1), loc='upper left', borderaxespad=0.
    plt.savefig(diretorio + '/Dispersao.png', dpi=300, bbox_inches='tight')

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
        id = getID(sigla, listaunica);
        for row in reader:
            if(id == row[0]): # Identifica a estação
                for coluna in range(5, 36): # Faz um loop durante as colunas dia.
                    GLdia.append(coluna-4)
                    if(row[coluna] != "-999"):
                        GLir.append(float(row[coluna]))
                        temp_day = diajuliano(coluna-4, mes, ano)
                        ir_anual_gl[temp_day-1] = round(float(row[coluna]), 3);
                    else: GLir.append(None)
                        
                        
                break;

def GL2():
    id = getID(sigla, listaunica);
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    gl = pd.read_csv(dadosGL, sep=' ', header=None)
    select = gl.iloc[np.where(gl[0].values == id)]
    for coluna in range(5, 36):
        GLdia.append(coluna-4)
        if(str(select[coluna]) != "-999"): GLir.append(float(select[coluna]))
        else: GLir.append(None)

def plotanual():
    global dia_anual, ir_anual_sol, ir_anual_gl
    if(contarelemento(ir_anual_sol) > 10):
        plt.figure(ano, figsize=(20, 10))
        plt.cla() # Limpa os eixos
        plt.clf() # Limpa a figura
        d = diferenca(ir_anual_sol , ir_anual_gl)
        plt.plot(dia_anual, ir_anual_sol, 'b-') #b- é azul
        plt.plot(dia_anual, ir_anual_gl, 'r-') #r- é vermelho
        plt.plot(dia_anual, d, 'g-')
        plt.title("Rede SolRad-Net - " + sigla + '-' + str(ano) + " - Anual")
        plt.ylabel('Irradiância (Wm-2)')
        plt.xlabel('Dia')
        plt.ylim(-200, 450)
        plt.xticks(np.arange( 1, 366, 15))
        plt.xlim(1, 366)

        plt.legend(('SolRad-Net', 'GL'), loc='upper right')

        # Media SolRad-Net
        try: mediamensal = somararray(ir_anual_sol)/contarelemento(ir_anual_sol)
        except: mediamensal = 0;

        # Media GL
        try: mediagl = somararray(ir_anual_gl)/contarelemento(ir_anual_gl)
        except: mediagl = 0;

        plt.legend(('Média SolRad-Net: %5.2f' % mediamensal, 'Média GL: %5.2f' %mediagl), loc='upper left')

        diretorio = './DADOS/IMAGENS/SolRad-Net/' + str(ano) + '/' + sigla + '/'
        plt.savefig(diretorio + 'Anual.png', dpi=300, bbox_inches='tight')

        ## Dispersão
        plt.figure(str(ano)+'D')
        x=[0,450]
        y=[0,450]
        plt.title("Rede SolRad-Net - " + sigla + '-' + str(ano) + " - Dispersão Anual")
        plt.ylabel('Modelo GL')
        plt.xlabel('SolRad-Net')
        plt.xlim(x)
        plt.ylim(y)
        plt.scatter(ir_anual_sol, ir_anual_gl)
        plt.plot(x, y, 'r-')
        plt.savefig(diretorio + '/Anual-Dispersao.png', dpi=300, bbox_inches='tight')

    # Limpa as Variaveis
    ir_anual_sol= 366 * [None]
    ir_anual_gl= 366 * [None]


    
  

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

def horatomin(data):
    for i in range(len(data)):
        hora = int(str(data[i])[:2])
        minuto = int(str(data[i])[3:5]) + 1
        data[i] = int((hora*30) + (minuto/2) - 0.5)
        #((hora*60) + minuto)/60
    return data 


select = selecaolistaunica(14)
for i in range(len(select)):
    sigla = select[i]
    for i in range(12):
       mes = i+1
       try: plotdiario(0)
       except FileNotFoundError: pass
    plotanual()

#xticks
##ano=2018
##sigla = 'Ji_Parana_SE'
##mes = int(input('Insira o mes: '))
##plotdiario(0)

sigla = 'Alta_Floresta'
for i in range(12):
    mes = i+1
    plotdiario(0)
plotanual()

#plotdiario(0)
#plt.show()



