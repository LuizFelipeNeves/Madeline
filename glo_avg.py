import matplotlib.pyplot as plt
import csv

# http://sonda.ccst.inpe.br/infos/variaveis.html
# http://sonda.ccst.inpe.br/basedados/index.html

# id CPA = 29968

planilha = './DADOS/SONDA/2017/CPA1709ED.csv'
estacoesin = './DADOS/GLESTACAO/2017/estacao_201709.txt'
estacoesout = './DADOS/OUTPUT/estacao_201709.txt'
dadosGL = './DADOS/GLGOES/2017/TabMGLGLB_Diar.201709.txt'

listaunica = 'ListaUnicaCompleta_201606.txt'

ano = int(planilha[22:24])
mes = int(planilha[24:26])
sigla = planilha[19:22]

x=[]
y=[]

xmensal=[]
ymensal=[]

GLdia=[]
GLir=[]

# Inicio
def plot_sonda():
    with open(planilha, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')
        global diasmes, dia, diainicial, media, soma, total, somamensal, totalmensal
        total = 0
        soma = 0
        somamensal = 0
        totalmensal = 0

        # Detecta se determinado ano é bissexto
        if anobissexto(ano): diasmes = [31 , 29 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # É
        else: diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]; # N
        
        # Detecta a versao do cabecalho
        for row in plots:
            if(row[3].isdigit()): versao(1)
            else: versao(0)
            break;

        diaprint = 0
        
        # Pega o dia inicial
        for row in plots:
            if(row[col_irrad] != "N/A"):     
                dia = row[col_dia]
                diainicial = row[col_dia]
                break;
            else:
                 if(diaprint != row[col_dia]):
                     print(row[col_dia])
                     diaprint = row[col_dia]

             
        # Faz a leitura dos dados do Modelo GL
        GL();
        
        # Plotagem diaria
        for row in plots:
            if(row[col_irrad] != "N/A"):
                #if(float(row[col_irrad]) >= 1600): print(row[col_irrad] + " - Dia: " + row[col_dia])    
                if(dia != row[col_dia]):
                    diaria();

                dia = row[col_dia]    
                x.append(horamin(int(row[col_min])))
                y.append(float(row[col_irrad]))
                soma += float(row[col_irrad])
                total += 1
            
        # Plotagem do ultimo dia, pois não há um próximo dia para realizar a comparação.
        diaria();

        # Plotagem mensal 
        mensal();

        # Plotagem dispersao
        dispersao();

        # Atualiza Estacoes
        atualizar();
        
# Plotagem diaria
def diaria():
    global xmensal, ymensal, dia, diainicial, media, soma, total, somamensal, totalmensal
    plt.figure(dia)
    plt.plot(x,y, 'b-') #b- é azul
    plt.title("Rede Sonda - " + planilha[19:26] +  " - Dia [" + str(dia) + "]")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    plt.ylim(0, 1600)
 
    # Media
    media = soma/total
    plt.text(0.35, 1400, 'Média: %5.2f' % media, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':10})

    xmensal.append(diajuliano(int(dia)))
    ymensal.append(media)

    # Media Mensal
    somamensal += media
    totalmensal += 1

    # Limpa as Variaveis
    x.clear()
    y.clear()   
    soma = 0
    total = 0


# Plotagem Mensal
def mensal():
    plt.figure(1000)
    plt.plot(xmensal,ymensal, 'b-') #b- é azul
    plt.plot(GLdia, GLir, 'r-') #r- é vermelho
    plt.title("Rede Sonda - " + planilha[19:26] +  " - Média Mensal")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.ylim(0, 450)
    plt.xlim(1,numerodiasmes(mes))
    
    # Media
    mediamensal = somamensal/totalmensal
    plt.text(3, 400, 'Média Sonda: %5.2f' % mediamensal, bbox={'facecolor':'blue', 'alpha':0.5, 'pad':8})

    # Media GL
    mediagl = somararray(GLir)/len(GLir)
    
    plt.text(15, 400, 'Média GL: %5.2f' %mediagl, bbox={'facecolor':'red', 'alpha':0.5, 'pad':8})

    # Limpa as Variaveis
    #xmensal.clear()
    #ymensal.clear()   
    #somamensal = 0
    #totalmensal = 0    

def dispersao():
    plt.figure('dispersao')
    plt.title("Rede Sonda - " + planilha[19:26] +  " - Dispersão")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Dia')
    plt.scatter(xmensal,ymensal, c='blue', label='Média Sonda')
    plt.scatter(GLdia, GLir, c='red', label='Média GL')
    plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left', borderaxespad=0.)

# Define a versao do Cabecalhos
def versao(x):
    global col_dia, col_min, col_irrad, rede
    if x == 0: # Sonda Antigo 
       col_dia = 2
       col_min = 4
       col_irrad = 5
            
    elif x == 1: # Sonda Novo
        col_dia = 2
        col_min = 3
        col_irrad = 4

# Converte o dia juliano em dia normal
def diajuliano(var):
    #mes = 1;
    #diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31];
    for m in range(1, 12):
        if(var-diasmes[m-1] >= 1): var -= diasmes[m-1]
        else: break;
        #print(format(dia, '02d') + "/" + format(mes, '02d'))
    return var

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

# Soma todos os elementos de um array
def somararray(array):
    soma = 0;
    for i in range(len(array)): soma += array[i]
    return soma

# Formata determinado numero para duas casas.    
def formatn(numero):
    numero = "%.2f" % numero
    return float(numero)
    
# Atualiza estações
def atualizar():    
    with open(estacoesin, "r") as tsvin, open(estacoesout, "w+") as tsvout:
        reader = csv.reader(tsvin, delimiter=' ')
        output = csv.writer(tsvout, delimiter=' ')
        id = getID(sigla);
        for row in reader:
            if(id == row[0]): # Identifica a estação
                #for coluna in range(xmensal[0]+4, xmensal[-1]+5): # Faz um loop durante as colunas dia.
                for coluna in range(5, 36):
                    if(row[coluna] == "-999"): # Verifica se o dado é Nulo(-999).
                        posicao = findElement(coluna-4, xmensal);
                        if(posicao != None): # Verifica se foi calculado a média para este dia;
                            row[coluna] = str(formatn(ymensal[posicao]));
                                         
            output.writerow(row);

# Faz a leitura da Estimativa do Modelo GL.
def GL():    
    with open(dadosGL, "r") as tsvGL:
        reader = csv.reader(tsvGL, delimiter=' ')
        id = getID(sigla);
        for row in reader:
            if(id == row[0]): # Identifica a estação
                for coluna in range(5, numerodiasmes(mes)+5): # Faz um loop durante as colunas dia.
                    if(row[coluna] != "-999"):
                        GLdia.append(coluna-4)
                        GLir.append(float(row[coluna]))
                        #if float(row[coluna]) <= 0: print(row[coluna])
                break;

plot_sonda();
plt.show();
