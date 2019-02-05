
import os
import pandas as pd
import numpy as np
import urllib.request
from urllib.error import URLError, HTTPError

listaunica = 'ListaUnicaCompleta_201606.txt'

# https://solrad-net.gsfc.nasa.gov/zip_files_flux/
# 20180101_20180131_CUIABA-MIRANDA_flux.zip

# https://solrad-net.gsfc.nasa.gov/zip_files_flux/
# 20180101_20180131_CUIABA-MIRANDA_flux.zip

def getdado(ano, mes, sigla):
    ano = str(ano)
    mes = str(mes)
    diainicial = '01'
    diafinal = format(diames(ano, mes), '02d')
    base = 'https://solrad-net.gsfc.nasa.gov/zip_files_flux/'
    nome =  ano + mes + diainicial + '_' + ano + mes + diafinal + '_' + sigla + '_flux.zip'
    url = base + nome

    diretorio = './SolRad-Net/' + ano + '/' + sigla + '/'

    main = 'https://solrad-net.gsfc.nasa.gov/cgi-bin/print_warning_flux?site='
    main += sigla + '&year=117&month=' + str(int(mes)) + '&day=1&year2=117&month2=' + str(int(mes)) + '&day2=' + str(diafinal) + '&LEV10=1&AVG=10&shef_code=P'

    
    try:
        os.stat(diretorio + nome)
        print('Já Existe: ' + mes + '/' + ano)
    except:
        try:
            urllib.request.urlopen(main)
            urllib.request.urlretrieve(url, diretorio + nome)
            print('Concluído: ' + mes + '/' + ano)

        except HTTPError as e:
            if(e.code == 404):
                print(sigla, mes)
            else: print('Error code: ', e.code)

        except URLError as e: print('Reason: ', e.reason)
            
        except FileNotFoundError:
            createdir(ano, mes, sigla)
            urllib.request.urlopen(main)
            urllib.request.urlretrieve(url, diretorio + nome)
            print('Concluído: ' + mes + '/' + ano)

def diames(ano, mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1;
    return diasmes[int(mes)-1]

def selecaolistaunica():
    lista = pd.read_csv(listaunica, sep='\t', header=None, usecols=[4 , 6, 9], encoding="latin-1")
    select = lista.iloc[np.where(lista[4].values == 14)]
    select = select.iloc[np.where(select[6].values != '-999')]
    select = select[6].values.tolist()
    return select

def checkdir(diretorio):
    try: os.stat(diretorio)
    except: os.mkdir(diretorio)

def createdir(ano, mes, sigla):
    diretorio = './SolRad-Net/'
    checkdir(diretorio)
    diretorio += ano + '/'
    checkdir(diretorio)
    diretorio += sigla + '/'
    checkdir(diretorio)

def menu():

    op = int(input('Para todas as estações, digite 1: \nPara uma específica, digite 2:'))

    if op == 1:
        ano = input('Digite o ano: ')
        select = selecaolistaunica()
        for x in range(len(select)):
            sigla = select[x]
            for i in range(12):
                getdado(ano, format(i+1, '02d'), sigla)
                
    elif op == 2:
        o = int(input('\nPara um ano, digite 1: \nPara um ano e mes específico, digite 2: \nPara um intervalo de tempo, digite 3: '))
        sigla = input('Digite a sigla: ')
    
        if o == 1:
            ano = input('Digite o ano: ')
            for i in range(12):
                getdado(ano, format(i+1, '02d'), sigla)
            
        elif o == 2:
            ano = input('Digite o ano: ')
            mes = int(input('Digite o mes: '))
            getsonda(ano, format(mes, '02d'), sigla)

        elif o == 3:
            anoi = int(input('Digite o ano de inicio: '))
            anof = int(input('Digite o ano de fim: '))
            for ano in range(anoi, anof+1):
                for i in range(12): getdado(ano, format(i+1, '02d'), sigla)

    else:
        print('Opção Invalida!')

menu()
            

