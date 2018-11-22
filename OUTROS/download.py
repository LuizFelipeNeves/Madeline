import urllib.request
import requests
import patoolib
from pyunpack import Archive

def getsonda(ano, mes, sigla):
    ano = str(ano)
    mes = str(mes)
    base = "http://ftp.cptec.inpe.br/labren/sonda/dados/ambientais/s"
    nome = sigla + ano[2:] + mes + "ED.7z"
    url = base + sigla + "/" + ano + "/" + nome

    try: urllib.request.urlretrieve(url, "./SONDA/" + nome)
    except: print(url)
    
for i in range(12):
    getsonda(2017, format(i+1, '02d'), "PTR")
    
