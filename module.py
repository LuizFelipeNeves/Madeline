import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from funcoes import *

GLdia=[]
GLir=[]
xmensal=[*range(1, 32)]
ymensal= 31 * [None]

dia_anual= [*range(1, 367)]
ir_anual_sp= 366 * [None]
ir_anual_gl=366 * [None]

def validar_diaria(dia, mes, ano, rede, sigla, ir, minuto, opcao):
    # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados.
    elementos = len(ir)/24 * (10-3) # 210, quantidade de elementos validos.
    if(contarelemento(ir) > elementos):
        media = mediadiaria(ir)/len(ir)
        ymensal[dia-1] = media
        temp_day = diajuliano(dia, mes, ano)
        ir_anual_sp[temp_day-1] = round(media, 3);
        figuradiaria(dia, rede, sigla, ano, mes, opcao, minuto, ir, media)
    else:
        ymensal[dia-1] = None
        temp_day = diajuliano(dia, mes, ano)
        ir_anual_sp[temp_day-1] = None;

def figuradiaria(dia, rede, sigla, ano, mes, opcao, minuto, ir, media):
    plt.figure(dia)
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    plt.plot(minuto, ir, 'b-') #b- é azul
    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(dia) + "]")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    plt.legend(['Média: %5.2f' %media], loc='upper left')
    plt.ylim(0, 1600)
    plt.xlim(0, 25)
    createdir(ano, mes, sigla, rede)
    diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    plt.savefig(diretorio + '/' + str(dia) + '.png')
    if opcao == 0: plt.close()

def plotmensal(opcao, rede, sigla, mes, ano):
    global xmensal, ymensal

    # Media
    try: mediamensal = somararray(ymensal)/contarelemento(ymensal)
    except: mediamensal = 0;

    # Media GL
    try: mediagl = somararray(GLir)/contarelemento(GLir)
    except: mediagl = 0;

    dp_sp = str(desviopadrao(ymensal))
    err_sp = str(erropadrao(dp_sp, ymensal))
    dp_gl = str(desviopadrao(GLir))
    err_gl = str(erropadrao(dp_gl, GLir))
  
    plt.figure('Mensal')
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    labels = 'Média SRN: %5.2f' % mediamensal + '\n' + 'DP SRN: ' + dp_sp + '\n' + 'EP SRN: ' + err_sp
    plt.plot(xmensal, ymensal, 'b-', label=labels)

    labelgl = 'Média GL: %5.2f' %mediagl + '\n' + 'DP GL: ' + dp_gl + '\n' + 'EP GL: ' + err_gl
    plt.plot(GLdia, GLir, 'r-', label=labelgl)
    
    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d') + " - Medias Diárias")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1, 31)
    plt.legend(loc='upper left', fontsize=6)

    diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    createdir(ano, mes, sigla, rede)
    plt.savefig(diretorio + '/Mensal.png')

    if opcao == 0: plt.close()
    
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura

    x=[0,350]
    y=[0,350]
    plt.figure('Mensal-D')
    plt.title('Rede ' + rede + ' - ' + sigla + '-' + str(ano) + str(mes) + " - Dispersão")
    plt.ylabel('Modelo GL')
    plt.xlabel(rede)
    plt.ylim(y)
    plt.xlim(x)
    plt.scatter(ymensal, GLir, c='b', alpha=0.5)
    plt.plot(x, y, 'r-')
    #plt.legend(loc='upper left') #bbox_to_anchor=(0.5, 1), loc='upper left', borderaxespad=0.
    plt.savefig(diretorio + '/Dispersao.png', dpi=300, bbox_inches='tight')

    atualizar(ano, mes); # Atualiza Estacoes
    gravartexto(ano, mes, sigla); # Gera os arquivos de Texto com os valores calculados

    # Limpa as Variaveis
    ymensal.clear()
    ymensal= 31 * [None]

    GLdia.clear()
    GLir.clear()
    print('Concluido: ' + str(mes) + ', ' + str(ano) + ', ' + sigla)

# Faz a leitura da Estimativa do Modelo GL.
def GL(sigla, listaunica, mes, ano):
    id = getID(sigla, listaunica);
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    gl = pd.read_csv(dadosGL, sep=' ', header=None)
    select = gl.iloc[np.where(gl[0].values == id)]
    for coluna in range(5, 36):
        read = round(float(select[coluna]), 3)
        if(read < 0): read=None
        GLdia.append(coluna-4)
        GLir.append(read)
        temp_day = diajuliano(coluna-4, mes, ano)
        ir_anual_gl[temp_day-1] = read;

def plotanual(ano, rede, sigla):
    global dia_anual, ir_anual_sp, ir_anual_gl
    if(contarelemento(ir_anual_sp) > 10):
        plt.figure(ano, figsize=(20, 10))
        plt.cla() # Limpa os eixos
        plt.clf() # Limpa a figura
        d = diferenca(ir_anual_sp , ir_anual_gl)
        plt.plot(dia_anual, ir_anual_sp, 'b-') #b- é azul
        plt.plot(dia_anual, ir_anual_gl, 'r-') #r- é vermelho
        plt.plot(dia_anual, d, 'g-')
        plt.title('Rede ' + rede + ' - ' + sigla + '-' + str(ano) + " - Anual")
        plt.ylabel('Irradiância (Wm-2)')
        plt.xlabel('Dia')
        plt.ylim(-200, 450)
        plt.xticks(np.arange( 1, 366, 15))
        plt.xlim(1, 366)

        # Media Terrestr8e
        try: mediamensal = somararray(ir_anual_sp)/contarelemento(ir_anual_sp)
        except: mediamensal = 0;

        # Media GL
        try: mediagl = somararray(ir_anual_gl)/contarelemento(ir_anual_gl)
        except: mediagl = 0;

        plt.legend(('Média ' + rede + ': %5.2f' % mediamensal, 'Média GL: %5.2f' %mediagl, 'Diferença'), loc='upper left')

        diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/'
        plt.savefig(diretorio + 'Anual.png', dpi=300, bbox_inches='tight')

        ## Dispersão
        plt.figure(str(ano)+'D')
        x=[0,450]
        y=[0,450]
        plt.title('Rede ' + rede + ' - ' + sigla + '-' + str(ano) + " - Dispersão Anual")
        plt.ylabel('Modelo GL')
        plt.xlabel(rede)
        plt.xlim(x)
        plt.ylim(y)
        plt.plot(x, y, 'r-')
        plt.scatter(ir_anual_sp, ir_anual_gl, c='b', alpha=0.5)
        plt.savefig(diretorio + '/Anual-Dispersao.png', dpi=300, bbox_inches='tight')

    # Limpa as Variaveis
    ir_anual_sp= 366 * [None]
    ir_anual_gl= 366 * [None]

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
	
#
def gravartexto(ano, mes, sigla):
    diretorio = './DADOS/TXT/' + str(ano) + '/' + sigla
    checkdir(diretorio)
    arquivotxt = diretorio + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + '.txt' 
    arquivo = open(arquivotxt, 'w+', encoding="ansi")
    for i in range(len(GLir)):
        string = str(xmensal[i]+1)+ '\t' + str(formatn(ymensal[i]))+ '\t' + str(formatn(GLir[i])) + '\n'
        arquivo.write(string)
    arquivo.close()

# Atualiza estações
def atualizar(ano, mes):
    estacoesin = './DADOS/GLESTACAO/' + str(ano) + '/estacao_' + str(ano) + format(mes, '02d') + '.txt'
    estacoesout = './DADOS/OUTPUT/estacao_' + str(ano) + format(mes, '02d') + '.txt'
    try:
        with open(estacoesin, "r") as tsvin, open(estacoesout, "w+") as tsvout:
            reader = csv.reader(tsvin, delimiter=' ')
            output = csv.writer(tsvout, delimiter=' ')
            id = getID(sigla, listaunica);
            for row in reader:
                if(id == row[0]): # Identifica a estação
                    for coluna in range(5, numerodiasmes(mes)+5):
                        if(row[coluna] == "-999"): # Verifica se o dado é Nulo(-999).
                            posicao = findElement(coluna-4, xmensal);
                            # Verifica se foi encontrado dado referente ao dia.
                            if(posicao != None):
                                if(ymensal[posicao] != None):
                                    row[coluna] = str(formatn(ymensal[posicao]));
                                             
                output.writerow(row);
    except: pass
