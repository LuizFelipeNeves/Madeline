import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# http://sonda.ccst.inpe.br/infos/variaveis.html
# http://sonda.ccst.inpe.br/basedados/index.html

# id CPA = 29968

# Otimizar script.
# dispersao de 4 em 4 meses,
# bolinhas pintadas para medias mensais, bolinhas vazias.

# CPA, PTR, NAT, SLZ, SMS

sigla = 'PTR'
ano = 2017
mes = 4

listaunica = 'ListaUnicaCompleta_201606.txt'

x=[]
y=[]

xmensal=[]
ymensal=[]

GLdia=[]
GLir=[]

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
        global diasmes, diainicial, media, sonda;

        # Detecta se determinado ano é bissexto
        if anobissexto(ano): diasmes = [31 , 29 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # É
        else: diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # N
        
        # Faz a leitura dos dados do Modelo GL
        GL();
        
        # Plotagem diaria
        sonda = pd.read_csv(planilha, header=None, sep=';', usecols=[*range(6)])
        cabecalho(str(sonda.loc[0, 3]).isdigit())

        diainicial = sonda.loc[0, 2]
        for dia in range(31):
            diaria(dia+diainicial, plotadiario)

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
        if(y[i] > 1300) or np.isnan(y[i]): y[i]=None
        x[i] = horamin(x[i]) 

    if(contarelemento(y) > 1260): # Dias com falta de dados durante mais de 180 minutos (3h) sao descartados, 1440-180=1260

        media = mediadiaria(y)/1440
        ymensal.append(media)
        
        plt.figure(dia)
        plt.cla() # Limpa os eixos
        plt.clf() # Limpa a figura
        plt.plot(x,y, 'b-') #b- é azul
        plt.title("Rede Sonda - " + sigla + str(ano)[-2:] + format(mes, '02d') + format(dia-diainicial+1, '02d') + " - Dia [" + str(dia) + "]")
        plt.ylabel('Irradiância (Wm-2)')
        plt.xlabel('Tempo (Hora UTC)')
        plt.ylim(0, 1600)
        plt.text(0.35, 1400, 'Média: %5.2f' % media, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})

        diretorio = './DADOS/IMAGENS/' + sigla + '/' + format(mes, '02d')
        try: os.stat(diretorio)
        except: os.mkdir(diretorio)
        plt.savefig(diretorio + '/' + str(dia) + '.png')

        if(plotadiario < 1): plt.close()
            
    else: ymensal.append(None)

    # Registra o dia
    xmensal.append(dia-diainicial+1)

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
    mediamensal = somararray(ymensal)/contarelemento(ymensal)
    plt.text(3, 400, 'Média Sonda: %5.2f' % mediamensal, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':8})

    # Media GL
    mediagl = somararray(GLir)/contarelemento(GLir)
    plt.text(15, 400, 'Média GL: %5.2f' %mediagl, bbox={'facecolor':'red', 'alpha':0.5, 'pad':8})
    plt.savefig('./DADOS/IMAGENS/' + sigla + '/' + format(mes, '02d') + '/Mensal.png')

def gravartexto():
    arquivo = open(arquivotxt, 'w', encoding="ansi")
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

# Pega o ID da Estação
def getID(sigla):        
    with open(listaunica) as lista:
        reader = csv.reader(lista, delimiter='\t')
        for row in reader:
            if(sigla == row[6]):
                return row[0];
                break;
            
# Retorna o numero de dias de determinado mes            
def numerodiasmes(mes):
    return diasmes[mes-1]

def contarelemento(array):
    count = 0;
    for i in range(len(array)):
        if(array[i] == None): count += 1
    return len(array) - count

def contarelemento3(data):
    data = np.array(data)
    #res = data.size - np.count_nonzero(np.isnan(data))
    return 1440;


# Soma todos os elementos de um array
def somararray(array):
    soma = 0;
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
    return soma

# Formata determinado numero para duas casas.    
def formatn(numero):
    if(numero == None): return -999;
    else: return float("%.2f" % numero)
    
# Atualiza estações
def atualizar():    
    with open(estacoesin, "r") as tsvin, open(estacoesout, "w+") as tsvout:
        reader = csv.reader(tsvin, delimiter=' ')
        output = csv.writer(tsvout, delimiter=' ')
        id = getID(sigla);
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

# Faz a leitura da Estimativa do Modelo GL.
def GL(): 
    with open(dadosGL, "r") as tsvGL:
        reader = csv.reader(tsvGL, delimiter=' ')
        id = getID(sigla);
        for row in reader:
            if(id == row[0]): # Identifica a estação
                for coluna in range(5, 36): # Faz um loop durante as colunas dia.
                    GLdia.append(coluna-4)
                    if(row[coluna] != "-999"): GLir.append(float(row[coluna]))
                    else: GLir.append(None)
                break;

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

#for i in range(12):
#    mes = i+1
#    plot_sonda(1);

plot_sonda(int(input('Digite -> ')))
plt.show();
