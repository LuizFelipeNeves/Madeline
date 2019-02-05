import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from funcoes import *

# http://sonda.ccst.inpe.br/infos/variaveis.html
# http://sonda.ccst.inpe.br/basedados/index.html

# id CPA = 29968

# Otimizar script.
# dispersao de 4 em 4 meses,
# bolinhas pintadas para medias mensais, bolinhas vazias.
# Criar as pastas
# CPA, PTR, NAT, SLZ, SMS

sigla = 'BRB'
ano = 2018
mes = 7

listaunica = 'ListaUnicaCompleta_201606.txt'

x=[]
y=[]

xmensal=[]
ymensal=[]

GLdia=[]
GLir=[]

dia_anual= [*range(1, 367)]
ir_anual_son= 366 * [None]
ir_anual_gl=366 * [None]

# Inicio
def plot_sonda(plotadiario):
    global dadosGL, estacoesin, estacoesout, arquivotxt
    planilha = './DADOS/SONDA/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + 'ED.csv'
    estacoesin = './DADOS/GLESTACAO/' + str(ano) + '/estacao_' + str(ano) + format(mes, '02d') + '.txt'
    estacoesout = './DADOS/OUTPUT/estacao_' + str(ano) + format(mes, '02d') + '.txt'
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    arquivotxt = './DADOS/TXT/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + '.txt'    

    with open(planilha, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')
        global diasmes, media, sonda;

        # Detecta se determinado ano é bissexto
        if anobissexto(ano): diasmes = [31 , 29 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # É
        else: diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # N
        
        # Faz a leitura dos dados do Modelo GL
        GL();
        
        # Plotagem diaria
        sonda = pd.read_csv(planilha, header=None, sep=';', usecols=[*range(6)])
        cabecalho(str(sonda.loc[0, 3]).isdigit())
        
        for dia in range(31):
            diaria(dia+1, plotadiario)

        # Plotagem mensal
        mensal();

        # Plotagem dispersao
        #dispersao();

        # Atualiza Estacoes
        atualizar();

        # Gera os arquivos de Texto com os valores calculados
        gravartexto();
        print('Concluido: ' + str(mes))
        
# Plotagem diaria

def diaria(dia, plotadiario):
    select = sonda.iloc[np.where(sonda[col_dia].values == dia)]
    x = select[col_min].values.tolist()
    y = select[col_irrad].values.tolist()
    
    for i in range(len(y)):
        if(y[i] > 1600) or np.isnan(y[i]): y[i]=None
        x[i] = horamin(x[i])

    if(contarelemento(y) > 1260): # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados, 1440-180=1260

        media = mediadiaria(y)/1440
        ymensal.append(media)
        
        temp_day = diajuliano(dia, mes, ano)
        print(dia, mes, ano, temp_day-1)
        
        ir_anual_son[temp_day-1] = round(media, 3);
        
        plt.figure(dia)
        plt.cla() # Limpa os eixos
        plt.clf() # Limpa a figura
        plt.plot(x,y, 'b-') #b- é azul
        plt.title("Rede Sonda - " + sigla + str(ano)[-2:] + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(dia) + "]")
        plt.ylabel('Irradiância (Wm-2)')
        plt.xlabel('Tempo (Hora UTC)')
        plt.ylim(0, 1600)
        plt.text(0.35, 1400, 'Média: %5.2f' % media, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})

        diretorio = './DADOS/IMAGENS/Sonda/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
        try: os.stat(diretorio)
        except: os.mkdir(diretorio)
        plt.savefig(diretorio + '/' + str(dia) + '.png')

        if(plotadiario < 1): plt.close()
            
    else: ymensal.append(None)

    # Registra o dia
    xmensal.append(dia)

    # Limpa as Variaveis
    x.clear()
    y.clear()


# Plotagem Mensal
def mensal():    
    plt.figure('Mensal')
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    plt.plot(xmensal,ymensal, 'b-') #b- é azul
    plt.plot(GLdia, GLir, 'r-') #r- é vermelho
    plt.title("Rede Sonda - " + sigla + str(ano)[-2:] + format(mes, '02d') + " - Medias Diárias")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1, 31)
    
    # Media
    try: mediamensal = somararray(ymensal)/contarelemento(ymensal)
    except: mediamensal = 0;
    plt.text(3, 400, 'Média Sonda: %5.2f' % mediamensal, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':8})

    # Media GL
    try: mediagl = somararray(GLir)/contarelemento(GLir)
    except: mediagl = 0;
    plt.text(15, 400, 'Média GL: %5.2f' %mediagl, bbox={'facecolor':'red', 'alpha':0.5, 'pad':8})
    plt.savefig('./DADOS/IMAGENS/Sonda/' + str(ano) + '/' + sigla + '/' + format(mes, '02d') + '/Mensal.png')

def gravartexto():
    arquivo = open(arquivotxt, 'w+', encoding="ansi")
    for i in range(len(GLir)):
        string = str(xmensal[i]+1)+ '\t' + str(formatn(ymensal[i]))+ '\t' + str(formatn(GLir[i])) + '\n'
        arquivo.write(string)
    arquivo.close()

    # Limpa as Variaveis
    xmensal.clear()
    ymensal.clear()
    GLdia.clear()
    GLir.clear()

# Define o cabecalho do Cabecalhos
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

def anobissexto(ano):    
    if(ano % 400 == 0 or ano % 4 == 0 and ano % 100 != 0): return True
    else: return False

# Converte minutos em horas
def horamin(x):
    hora = (x/60)
    return (hora)

# Encontra um Elemento em uma Lista
def findElement(elemento, lista):
    for i in range(len(lista)):
        if(elemento == lista[i]):
            return i;
            break;
            
# Retorna o numero de dias de determinado mes            
def numerodiasmes(mes):
    return diasmes[mes-1]

# Formata determinado numero para duas casas.    
def formatn(numero):
    if(numero == None): return -999;
    else: return float("%.2f" % numero)
    
# Atualiza estações
def atualizar():    
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

# Faz a leitura da Estimativa do Modelo GL.
def GL(): 
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

def plotanual():
    global dia_anual, ir_anual_son, ir_anual_gl
    if(contarelemento(ir_anual_son) > 10):
        plt.figure(ano, figsize=(20, 10))
        plt.cla() # Limpa os eixos
        plt.clf() # Limpa a figura
        plt.plot(dia_anual, ir_anual_son, 'b-') #b- é azul
        plt.plot(dia_anual, ir_anual_gl, 'r-') #r- é vermelho
        plt.title("Rede Sonda - " + sigla + '-' + str(ano) + " - Anual")
        plt.ylabel('Irradiância (Wm-2)')
        plt.xlabel('Dia')
        plt.ylim(0, 450)
        plt.xticks(np.arange( 1, 366, 15))
        plt.xlim(1, 366)

        plt.legend(('Sonda', 'GL'), loc='upper right')

        # Media SolRad-Net
        try: mediamensal = somararray(ir_anual_son)/contarelemento(ir_anual_son)
        except: mediamensal = 0;
        plt.text(20, 400, 'Média Sonda: %5.2f' % mediamensal, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':16})

        # Media GL
        try: mediagl = somararray(ir_anual_gl)/contarelemento(ir_anual_gl)
        except: mediagl = 0;
        plt.text(80, 400, 'Média GL: %5.2f' %mediagl, bbox={'facecolor':'red', 'alpha':0.5, 'pad':16})

        diretorio = './DADOS/IMAGENS/Sonda/' + str(ano) + '/' + sigla + '/'
        plt.savefig(diretorio + 'Anual.png', dpi=300, bbox_inches='tight')

    # Limpa as Variaveis
    ir_anual_son= 366 * [None]
    ir_anual_gl= 366 * [None]

select = ['BRB', 'CPA']
for i in range(len(select)):
    select = ['BRB', 'CPA']
    sigla = select[i]
    print(sigla)
    for i in range(12):
       mes = i+1
       try:plot_sonda(0)
       except FileNotFoundError: pass
    plotanual()
    
##for i in range(6):
##    mes = i+1
##    plot_sonda(0);

#plot_sonda(int(input('Digite -> ')))
##plot_sonda(0)
##plt.show();
