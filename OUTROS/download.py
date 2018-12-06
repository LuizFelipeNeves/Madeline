import os
import urllib.request
from urllib.error import URLError, HTTPError

def getsonda(ano, mes, sigla):
    ano = str(ano)
    mes = str(mes)
    base = "http://ftp.cptec.inpe.br/labren/sonda/dados/ambientais/"
    nome = sigla + ano[2:] + mes + "ED.7z"
    url = base + sigla + "/" + ano + "/" + nome
    diretorio = './SONDA/' + ano + '/' + sigla + '/'
    
    try:
        os.stat(diretorio + nome)
        print('Já Existe: ' + mes + '/' + ano)
    except:
        try:
            urllib.request.urlretrieve(url, diretorio + nome)
            print('Concluído: ' + mes + '/' + ano)

        except HTTPError as e:
            if(e.code == 404): 'Nao Existe dado'
            else: print('Error code: ', e.code)

        except URLError as e: print('Reason: ', e.reason)
            
        except FileNotFoundError:
            createdir(ano, mes, sigla)
            urllib.request.urlretrieve(url, diretorio + nome)
            print('Concluído: ' + mes + '/' + ano)


def checkdir(diretorio):
    try: os.stat(diretorio)
    except: os.mkdir(diretorio)

def createdir(ano, mes, sigla):
    diretorio = './SONDA/'
    checkdir(diretorio)
    diretorio += ano + '/'
    checkdir(diretorio)
    diretorio += sigla + '/'
    checkdir(diretorio)

def menu():
    o = int(input('\nPara um ano, digite 1: \nPara um ano e mes específico, digite 2: \nPara um intervalo de tempo, digite 3: '))
    sigla = input('Digite a sigla: ')
    
    if o == 1:
        ano = input('Digite o ano: ')
        for i in range(12): getsonda(ano, format(i+1, '02d'), sigla)
        
    elif o == 2:
        ano = input('Digite o ano: ')
        mes = int(input('Digite o mes: '))
        getsonda(ano, format(mes, '02d'), sigla)

    elif o == 3:
        anoi = int(input('Digite o ano de inicio: '))
        anof = int(input('Digite o ano de fim: '))
        for ano in range(anoi, anof+1):
            for i in range(12): getsonda(ano, format(i+1, '02d'), sigla)

    else:
        print('Opção Invalida!')

menu()
            

