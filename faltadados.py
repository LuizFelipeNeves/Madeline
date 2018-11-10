def faltadados(array):
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

    # Onde começa a falta de dados
    for i in range(len(abre)): print(abre[i])
    print('-----------')

    # Onde termina a falta de dados
    for i in range(len(fecha)): print(fecha[i])
    print('-----------')

    # Imprime o Intervalo onde falta dados.
    for i in range(len(abre)):
        intervalo = ((fecha[i]-abre[i])+1)
        print(intervalo)
    print('-----------')

    # Calcula os valores
    for i in range(len(abre)):
        intervalo = ((fecha[i]-abre[i])+1)
        for m in range(intervalo):
            if((abre[i]-1 > 0) and (fecha[i]+1 < len(array))): # Apenas entra na condição caso o inicio seja maior que 0, e o fim menor que o limite.
                S = (array[abre[i]-1]+array[fecha[i]+1])*intervalo/2
            # Duvida!!!
            elif((abre[i]-1 < 0)):
                S = (array[fecha[i]+1])*intervalo/2
            elif((fecha[i]+1 > len(array))):
                S = (array[abre[i]-1])*intervalo/2

            somatotal += S/intervalo;    
            #array[abre[i]+m] = S; # Atualiza o valor       
                 
    return(somatotal)
        
array = [None, 29 , None , 30 , 31, None, None, 30, None, 30, 35, 31, 30, 31,30, 31, None, 30, None];        
print(faltadados(array));
