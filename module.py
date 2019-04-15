import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from funcoes import getLoc, formatn , findElement, diferenca, contarelemento, diajuliano, getID, erropadrao, desviopadrao, somararray, integral

GLdia=[]
GLir=[]

intSP=[]
intGL1x=[]
intDia=[]

xmensal=[*range(1, 32)]
ymensal= 31 * [None]

dia_anual= [*range(1, 367)]
ir_anual_sp= 366 * [None]
ir_anual_gl=366 * [None]

def validar_diaria(dia, mes, ano, rede, sigla, ir, minuto, opcao):
    # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados.
    elementos = (len(ir)/ 24) * 6
    minutonovo = [i * 60 for i in minuto]
    if(contarelemento(ir) > elementos):
        media = integral(minutonovo, ir)/len(ir)
        ymensal[dia-1] = media
        temp_day = diajuliano(dia, mes, ano)
        ir_anual_sp[temp_day-1] = round(media, 3)
        figuradiaria(dia, rede, sigla, ano, mes, opcao, minuto, ir, media)
    else:
        ymensal[dia-1] = None
        temp_day = diajuliano(dia, mes, ano)
        ir_anual_sp[temp_day-1] = None

        intSP.append(None)
        intGL1x.append(None)
        intDia.append(dia)


def figuradiaria(dia, rede, sigla, ano, mes, opcao, minuto, ir, mediasp):
    data = GLbinarios(sigla, 'ListaUnicaCompleta_201606.txt', dia, mes, ano)
    gl1x = data[0]
    gl3x = data[1]
    gl5x = data[2]
    suavizado = escalatemp(ir, 1, 15)

    hour = gerarhoras()
    minutonovo = [i * 60 for i in hour]
    mediasuav = integral(minutonovo, suavizado)/len(suavizado)
    mediagl1x = integral(minutonovo, gl1x)/len(gl1x)
    mediagl3x = integral(minutonovo, gl3x)/len(gl3x)
    mediagl5x = integral(minutonovo, gl5x)/len(gl5x)
    
    if(mediasp != 0.0): intSP.append(formatn(mediasp))
    else: intSP.append(None)

    if(mediagl1x != 0.0): intGL1x.append(formatn(mediagl1x))
    else: intGL1x.append(None)

    intDia.append(dia)

    # Superficie
    dp_sp = str(formatn(desviopadrao(ir)))
    err_sp = str(formatn(erropadrao(dp_sp, ir)))

    # Suavizado
    dp_suav = str(formatn(desviopadrao(suavizado)))
    err_suav = str(formatn(erropadrao(dp_suav, suavizado)))

    
    # GL 1x
    dp_gl1x = str(formatn(desviopadrao(gl1x)))
    err_gl1x = str(formatn(erropadrao(dp_gl1x, gl1x)))

    # GL 3x
    dp_gl3x = str(formatn(desviopadrao(gl3x)))
    err_gl3x = str(formatn(erropadrao(dp_gl3x, gl3x)))

    # GL 5x
    dp_gl5x = str(formatn(desviopadrao(gl5x)))
    err_gl5x = str(formatn(erropadrao(dp_gl5x, gl5x)))

    # Fazer o uso.. dos indices

    plt.figure(dia)
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura

    labelsp = 'Média SP Min: ' + str(formatn(mediasp)) + '\n' + 'DP SP: ' + dp_sp + '\n' + 'EP SP: ' + err_sp
    labelsuav = 'Média SP Suavizado: ' + str(formatn(mediasuav)) + '\n' + 'DP SP: ' + dp_suav + '\n' + 'EP SP: ' + err_suav
    labelgl1x = 'Média GL 1x: ' + str(formatn(mediagl1x)) + '\n' + 'DP GL 1x: ' + dp_gl1x + '\n' + 'EP GL 1x: ' + err_gl1x
    labelgl3x = 'Média GL 3x: ' + str(formatn(mediagl3x)) + '\n' + 'DP GL 3x: ' + dp_gl3x + '\n' + 'EP GL 3x: ' + err_gl3x
    labelgl5x = 'Média GL 5x: ' + str(formatn(mediagl5x)) + '\n' + 'DP GL 5x: ' + dp_gl5x + '\n' + 'EP GL 5x: ' + err_gl5x


    plt.plot(minuto, ir, 'k-') # preto
    plt.plot(hour, suavizado, 'b-') #b- é azul

    plt.plot(hour, gl1x, 'ro', markersize=1.5)  # GL vermelho
    plt.plot(hour, gl3x, 'go', markersize=1.5) # GL 3x verde
    plt.plot(hour, gl5x, 'yo', markersize=1.5) # GL 5x amarelo
    
    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(dia) + "]")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    
    plt.legend([labelsp, labelsuav, labelgl1x, labelgl3x, labelgl5x], loc='upper left')
    plt.ylim(0, 1500)
    plt.xlim(0, 25)
    createdir(ano, mes, sigla, rede)
    diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    plt.savefig(diretorio + '/' + str(dia) + '.png')
    if opcao == 0: plt.close()

def plotmensal(opcao, rede, sigla, mes, ano):
    global xmensal, ymensal

    plt.figure('Mensal')
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura
    
    # Media
    try: mediamensal = somararray(ymensal)/contarelemento(ymensal)
    except: mediamensal = 0


    # Media GL
    try: mediagl1x = somararray(GLir)/contarelemento(GLir)
    except: mediagl1x = 0

    dp_sp = str(desviopadrao(ymensal))
    err_sp = str(erropadrao(dp_sp, ymensal))
    
    dp_gl1x = str(desviopadrao(GLir))
    err_gl1x = str(erropadrao(dp_gl1x, GLir))

    labels = 'Média SP: %5.2f' % mediamensal + '\n' + 'DP SRN: ' + dp_sp + '\n' + 'EP SRN: ' + err_sp
    plt.plot(xmensal, ymensal, 'b-', label=labels)

    labelgl = 'Média GL: %5.2f' %mediagl1x + '\n' + 'DP GL: ' + dp_gl1x + '\n' + 'EP GL: ' + err_gl1x
    plt.plot(GLdia, GLir, 'r-', label=labelgl)

    labelint = 'Integral'
    plt.plot(intDia, intGL1x, 'yo', markersize=5, label=labelint)
    
    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d') + " - Medias Diárias")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1, 32)
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
    if(ano == 2018 and mes == 2): plt.scatter(ymensal[3], GLir[3], c='r', alpha=0.5)
    plt.plot(x, y, 'r-')
    #plt.legend(loc='upper left') #bbox_to_anchor=(0.5, 1), loc='upper left', borderaxespad=0.
    plt.savefig(diretorio + '/Dispersao.png', dpi=300, bbox_inches='tight')

    atualizar(ano, mes) # Atualiza Estacoes
    gravartexto(ano, mes, sigla) # Gera os arquivos de Texto com os valores calculados

    # Limpa as Variaveis
    ymensal.clear()
    ymensal= 31 * [None]

    intGL1x.clear()
    intDia.clear()
    GLdia.clear()
    GLir.clear()
    print('Concluido: ' + str(mes) + ', ' + str(ano) + ', ' + sigla)

# Faz a leitura da Estimativa do Modelo GL.
def GL(sigla, listaunica, mes, ano):
    id = getID(sigla, listaunica)
    dadosGL = './DADOS/GLGOES/' + str(ano) + '/TabMGLGLB_Diar.' + str(ano) + format(mes, '02d') + '.txt'
    gl = pd.read_csv(dadosGL, sep=' ', header=None)
    select = gl.iloc[np.where(gl[0].values == str(id))]
    for coluna in range(5, 36):
        read = round(float(select[coluna]), 3)
        if(read < 0): read=None
        GLdia.append(coluna-4)
        GLir.append(read)
        temp_day = diajuliano(coluna-4, mes, ano)
        ir_anual_gl[temp_day-1] = read

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

        # Media Terrestre
        try: mediamensal = somararray(ir_anual_sp)/contarelemento(ir_anual_sp)
        except: mediamensal = 0

        # Media GL
        try: mediagl1x = somararray(ir_anual_gl)/contarelemento(ir_anual_gl)
        except: mediagl1x = 0

        plt.legend(('Média ' + rede + ': %5.2f' % mediamensal, 'Média GL: %5.2f' %mediagl1x, 'Diferença'), loc='upper left')

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
            id = getID(sigla, listaunica)
            for row in reader:
                if(id == row[0]): # Identifica a estação
                    for coluna in range(5, numerodiasmes(mes)+5):
                        if(row[coluna] == "-999"): # Verifica se o dado é Nulo(-999).
                            posicao = findElement(coluna-4, xmensal)
                            # Verifica se foi encontrado dado referente ao dia.
                            if(posicao != None):
                                if(ymensal[posicao] != None):
                                    row[coluna] = str(formatn(ymensal[posicao]))
                                             
                output.writerow(row)
    except: pass


def binario(diretorio, ano):
    x = np.fromfile(diretorio, np.int16)
    if(ano  < 2018): x = x.byteswap()
    x = x.reshape(1800, 1800)
    x = x/10
    return x	

def getir(matriz, LAT, LON, Lin, Col):
    latfinal = 22-0.04
    loninicial = -100
    linha = int(((latfinal - LAT)/.04+0.5)) + Lin 
    coluna = int((LON - loninicial)/.04+0.5) + Col
    try:
        valor = matriz[linha , coluna]
        if(valor < 1) : valor=None
        return(float(valor))
    except: return(None)

def gerarhoras():
    horas = []
    minutos = [0, 15, 30, 45]
    for h in range(24):
        for m in range(len(minutos)):
            t = ((h*60) + minutos[m]) / 60
            horas.append(t)
    return horas

# Escala de Tempo de 15min
def escalatemp(x, fator, intervalo):
    lista= []
    ir = 96 * [None]
    i = int((len(x)/24) * 8)
    n = int(((intervalo-fator)/2) / fator)
    while i < len(x):
        for y in range(-n, n+fator):
            lista.append(x[int(y+i/fator)])
            #print(y, y+i, int(y+i/fator))

        c = contarelemento(lista)
        if(c == 0): media=0
        else: media= somararray(lista)/c

        ir[int(i/15)] = media 
        lista.clear()
        i+=intervalo

    return ir

def regiao(matriz, lat, long , n):
    lista = []
    for y in range(-n, n+1):
        for x in range(-n, n+1):
            # linha, coluna
            ir = getir(matriz, lat, long, x , y)
            lista.append(ir)

    c = contarelemento(lista)
    if(c != 0):
        s = somararray(lista)
        return s/c
    else: return None

def GLbinarios(sigla, listaunica, dia, mes, ano):
    loc = getLoc(sigla , listaunica)
    lat = loc[0]
    long = loc[1]

    diretorio = './DADOS/GLGOESbin_horarios/' + str(ano) + format(mes, '02d') + '/'
    
    minutos = [0, 15, 30, 45]
    final1x= len(minutos) * 24 * [None]
    final3x= len(minutos) * 24 * [None] 
    final5x= len(minutos) * 24 * [None] 

    for h in range(8, 24):
        for m in range(len(minutos)):
            try:
                file = 'S11636057_' + str(ano) + \
                format(mes, '02d') + \
                format(dia, '02d') + \
                format(h, '02d') + \
                format(minutos[m], '02d') + '.bin'

                matriz = binario(diretorio + file, ano)                
                x1 = getir(matriz, lat, long, 0 , 0)
                x3 = regiao(matriz, lat , long, 1) # 0, 1 , 2
                x5 = regiao(matriz, lat , long, 2) # 0, 1 , 2
                p = (h) * len(minutos) + m
                final1x[p] = x1
                final3x[p] = x3
                final5x[p] = x5
            except FileNotFoundError: pass
    return [final1x, final3x, final5x]
