from math import exp
from math import sqrt
from math import log
import pandas as pd
import numpy as np
from statistics import mean

for tiempo in range(3,41):

    s = 100
    k = 100
    n = tiempo
    t = 20
    vol = 0.2
    dt = t/n
    u = exp(vol*sqrt(dt))
    #u = 1.25
    d = 1/u
    r = log(1.25)
    p = ((exp(r*dt)) - d)/(u - d) # si es con exp el interes es tanto instantaneo
    #p2 = ((1+0.07)**dt - d)/(u - d) Si es con capitalizacion el interes tiene que ser simple
    q = 1-p

    #u = exp*vol*raiz(t/n)
    N_rows = (n * 2) + 1 
    N_cols = n + 1
    arbol_stonks = pd.DataFrame(np.zeros((N_rows, N_cols)))
    arbol_pf = pd.DataFrame(np.zeros((N_rows, N_cols)))

    arbol_stonks.iloc[n,0] = s

    for column in arbol_stonks.columns:
        columnNext = column + 1
        index = 0
        for data in arbol_stonks[column]:
            if data != 0:
                if column != n:
                    arbol_stonks.iloc[index - 1,column + 1] = data * u
                    arbol_stonks.iloc[index + 1,column + 1] = data * d
                    index = index + 1
            else:
                index = index + 1



    #print(arbol_stonks.shape[0]*arbol_stonks.shape[1])
    arbol_stonks = arbol_stonks.replace(0,"") 
    arbol_pf = arbol_pf.replace(0,"")

    index = 0

    for stonks in arbol_stonks[n]:
        #print(stonks)
        #print(type(stonks))
        if stonks != "":
            payoff = stonks - k
            #print(payoff)
            if payoff > 0:
                arbol_pf.iloc[index,n] = payoff
                index = index + 1
            else:
                arbol_pf.iloc[index,n] = 0
                index = index + 1
        else:
            index = index + 1


    for columna in range(n,-1,-1):
        index = 0
        #print("la columna es " + str(columna))
        for payoff in arbol_pf[columna]:
            #print("el payoff es " + str(payoff))
            if payoff != "":
                columnaminus = columna - 1
                #print("columna minus es " +  str(columnaminus))
                #print("el index es " + str(index))
                if columna == 0:
                    columnaminus = 0
                else:
                    columnaminus = columna - 1                
                indexplus = index + 1
                indexplus2 = index + 2
                #print("indexplus " + str(indexplus))
                stop = len(arbol_pf.index) - 2
                if indexplus2 and indexplus <= stop:
                        payoff2 = arbol_pf.iloc[indexplus2, columna]
                        if payoff2 == "":
                            payoff2 = 0
                            #arbol_pf.iloc[indexplus, columnaminus] = (payoff*p + payoff2 * q)/(1+r)**dt
                            arbol_pf.iloc[indexplus, columnaminus] = (payoff*p + payoff2 * q)*exp(-r*dt)
                            index = index + 1
                        else:
                            #arbol_pf.iloc[indexplus, columnaminus] = (payoff*p + payoff2 * q)/(1+r)**dt
                            arbol_pf.iloc[indexplus, columnaminus] = (payoff*p + payoff2 * q)*exp(-r*dt)
                            index = index + 1                        

            else:
                index = index + 1



    print("El precio del call es " + str(arbol_pf.iloc[n,0]) + " y se usaron " + str(n) + " pasos" )
    

print(arbol_stonks)
print(arbol_pf)