import numpy as np
import matplotlib.pyplot as plt

def teste(diretorio):
    x = np.fromfile(diretorio, np.int16)
    x = x.byteswap()
    x = x.reshape(1800, 1800)
    x = x/10
    return x

d1 = teste('./DADOS/GLGOESbin/2017/01/gc.170103.diarg.bin')
d2 = teste('./DADOS/GLGOESbin/2017/01/gc.170104.diarg.bin')

# Soma
soma = np.zeros((1800, 1800) , float)
soma[d1>0] = soma[d1>0]+d1[d1 > 0]
soma[d2>0] = soma[d2>0]+d2[d2 > 0]

# Contar Dias
dv = np.zeros((1800, 1800) , float)
dv[d1>0] += 1
dv[d2>0] += 1

# Matriz Media
media = np.zeros((1800, 1800) , float)
media[dv > 0] =  soma[dv > 0] / dv[dv > 0]

n1 = (d1 - media)**2
n2 = (d2 - media)**2
soma = (n1+n2)

total = np.zeros((1800, 1800) , float)
total[dv > 0] = soma[dv > 0]/dv[dv > 0]
total = np.sqrt(total)

plt.imshow(total, cmap="jet")
plt.colorbar()
plt.show()
