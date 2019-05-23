# coding: utf-8

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from itertools import cycle
cycol = cycle('bgrcmk')

from mpldatacursor import datacursor
#from unidecode import unidecode

listau = open("ListaComdados.txt",'r')
conteudo = listau.readlines()   

beginLatFig=-38
endLatFig=15
beginLonFig=-80
endLonFig=-28

fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)

map=Basemap(projection='cyl',resolution='i',llcrnrlat=beginLatFig, urcrnrlat=endLatFig,llcrnrlon=beginLonFig,urcrnrlon=endLonFig)

for linha in conteudo:
    if "Lat" not in linha:
        dados = linha.split( )
        idi=dados[0]
        lat=float(dados[1])
        lon=float(dados[2])
        alt=dados[3]
        nome=dados[6]
        dono=dados[10]

        marker = "s"
        R=0
        G=1
        B=1
        A=1
        border=0
        
        map.plot(lon, lat, marker=marker, markeredgecolor='k', c=next(cycol), markersize=5.5, markeredgewidth=border, label=nome + ' (' + dono + ')' )

map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.drawstates()

plt.legend()
plt.title("Mapa de Estações", fontsize=15) 
plt.savefig('mapa.png',format='png', bbox_inches="tight", dpi=200)
datacursor(draggable=True)
plt.show()
