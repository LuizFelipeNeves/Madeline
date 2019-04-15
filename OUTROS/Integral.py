import numpy as np
y = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 95.0, 144.3, 204.2, 264.5, 324.3, 383.2, 440.3, 495.6, 548.5, 598.8, 646.1, 690.2, 730.9, 767.8, 801.0, 830.1, 854.9, 875.6, 891.7, 903.4, 910.6, 913.1, 910.9, 904.3, 893.1, 877.4, 857.2, 840.0, 800.8, 757.1, 717.2, 672.1, 631.3, 588.3, 540.9, 498.3, 434.8, 384.1, 326.6, 263.2, 208.8, 147.6, 84.8, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
x = [0, 1, 2, 3, 60, 61, 62, 63, 120, 121, 122, 122, 180, 181, 182, 183, 240, 241, 242, 243, 300, 301, 302, 303, 360, 361, 362, 363, 420, 421, 422, 423, 480, 481, 482, 483, 540, 541, 542, 543, 600, 601, 602, 603, 660, 661, 662, 663, 720, 721, 722, 723, 780, 781, 782, 783, 840, 841, 842, 843, 900, 901, 902, 903, 960, 961, 962, 963, 1020, 1021, 1022, 1023, 1080, 1081, 1082, 1083, 1140, 1141, 1142, 1143, 1200, 1201, 1202, 1203, 1260, 1261, 1262, 1263, 1320, 1321, 1322, 1323, 1380, 1381, 1382, 1383]
def integral(x, y):
    i = 0
    total = 0
    ant = '-999'
    prox = '-999'
    tant = '-999'
    tprox = '-999'

    while i < len(y):
        if(i+1 < len(y)) :
            if(y[i] == None):
                if(ant == '-999'):  
                    ant = 0
                    tant = int(x[i])
            else: 
                if(ant == '-999'):  
                    ant = y[i]
                    tant = int(x[i])
                else:
                    # faz o calculo
                    prox = y[i]
                    tprox = int(x[i])

                    #print(ant, prox, tant, tprox)
                    intervalo = tprox - tant
                    
                    if(intervalo == 0):
                        intervalo=1
                        print(ant, prox, tant, tprox)
                    S = (ant+prox) * intervalo / 2
                    S = S/intervalo

                    
                    b = np.trapz([ant, prox], x=[tant, tprox])

                    #print(S, b)
                    ant = y[i]
                    tant = int(x[i])
                    total += S
                    #print(b)                 
        else:
            if(y[i] != None): 
                prox = y[i]
                tprox = int(x[i])
                print(ant, prox, tant, tprox)
                b = np.trapz([ant, prox], x=[tant, tprox])
                total += S
            #print(b)
        i+=1
    return (total)

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
                chave = True
        else:
            if(chave == True): # Fecha
                fecha.append(i-1)
                chave = False
            if(menor == 0): menor = array[i] # Menor
            if(array[i] > maior): maior= array[i] # Maior
            somatotal += array[i]

        if((i+1 == len(array)) and chave == True): # Verifica o fim do array
            fecha.append(i)
            chave = False

    # Calcula os valores
    for i in range(len(abre)):
        intervalo = ((fecha[i]-abre[i])+1)
        if((abre[i]-1 > 0) and (fecha[i]+1 < len(array))): # Apenas entra na condiÃ§Ã£o caso o inicio seja maior que 0, e o fim menor que o limite.
            S = (array[abre[i]-1]+array[fecha[i]+1])*intervalo/2
            somatotal += S/intervalo
        elif((abre[i]-1 > 0) and(fecha[i]+1 > len(array))):
            S = (array[abre[i]-1])*intervalo/2
            somatotal += S/intervalo
        elif((abre[i]-1 < 0) and (fecha[i]+1 < len(array))):
            S = (array[fecha[i]+1])*intervalo/2
            somatotal += S

    return(somatotal)

itg = integral(x, y)
print(itg, itg/len(x))
md = mediadiaria(y)
print(md, md/len(y))
