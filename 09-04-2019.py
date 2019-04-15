from funcoes import somararray, contarelemento

x1 = list(range(0, 1440))
x2 = [x*2 for x in range(0, 720)]
data = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420, 435, 450, 465, 480]
#print(x)
#print(x2)

def escalatemp(x, fator, intervalo):
    lista= []
    ir = 96 * [None]
    i = int((len(x)/24) * 8)
    n = int(((intervalo-fator)/2) / fator)
    while i < len(x):
        for y in range(-n, n+fator):
            lista.append(x[int(y+i/fator)])
            #print(y, y+i, int(y+i/fator))
            
        ir[int(i/15)] = somararray(lista)/contarelemento(lista)
        lista.clear()
        i+=intervalo

    return ir

#escalatemp(x1, 1, 15)
escalatemp(x2, 2, 15)
