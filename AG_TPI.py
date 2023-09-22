## Trabajo practico anual

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

cromosoma = []
poblacion = 50  # numero de parques
pobInicial = []  # 0 lugar libre, 1 aerogenerador
nuevaPob = []
segundaPob = []
arregloCiclos = []
resultadoPotencia = []
crossover = 0.75
mutacion = 1 / 20
ciclos = 1500

# funcion para Vestas 172-7.2MW:
densidad = 1.29  # kg/m^3
velocidad = 25  # km/h
diametro = 172  # m
k = 0.25 * math.pi


def creaCromosoma():
    cromosoma.clear()
    for i in range(poblacion):
        if (lugarOcupado(i)):
            cromosoma.append('0')
        else:
            cromosoma.append(str(random.randint(0, 1)))
    return cromosoma


def lugarOcupado(i):
    posicionesOcupadas = [3, 12, 17, 20, 40]
    for j in posicionesOcupadas:
        if (i == j):
            return True
    else:
        return False


def creaPoblacion():
    aux = 0
    while (aux < poblacion):
        nuevoCromosoma = creaCromosoma()
        ##        print(nuevoCromosoma)
        ##        print(filtroCromosoma(nuevoCromosoma))
        if (filtroCromosoma(nuevoCromosoma)):
            lista = nuevoCromosoma.copy()
            pobInicial.append(lista)
            aux = aux + 1


def filtroCromosoma(cromosoma):
    cont = 0
    for i in range(poblacion):
        if (cromosoma[i] == "1"):
            cont += 1
    if (cont <= 25):
        return True
    else:
        return False


def mostrar(pobInicial):
    print("Voy a mostrar el resultado: ")
    cont = 0
    for crom in pobInicial:
        for i in range(len(crom)):
            print(crom[i], end="")
            cont += 1
            if ((cont % 5) == 0):
                print("")
        print()


def potenciaTotal(arreglo):
    global suma
    global cromMax
    global cromMin
    global minimo
    global promedio
    global fitnessTotal
    global arrFitness
    global potenciaMax
    potenciaMax = 0
    suma = 0
    minimo = 99999 ** 2
    fitnessTotal = 0
    arrFitness = []

    for crom in arreglo:
        potenciaTotal = 0
        for i in range(len(crom)):
            potenciaTotal += fdex(crom, i)

        # PotenciaTotal de un parque
        suma += potenciaTotal
        arrFitness.append(potenciaTotal)

        if (potenciaMax <= potenciaTotal):  # Maximo
            potenciaMax = potenciaTotal
            cromMax = crom

        if (minimo >= potenciaTotal):  # Minimo
            minimo = potenciaTotal
            cromMin = crom

    for j in range(len(arrFitness)):
        fitnessTotal += arrFitness[j] / suma

    return potenciaMax


def fdex(crom, pos):  # le pasamos la posicion del cromosoma a la funcion objetivo
    p = dameK(crom, pos) * densidad * (diametro ** 2) * (velocidad ** 3)
    return p


def dameK(crom, pos):  # calcula el valor k con efecto estela
    k = 0.25 * math.pi
    kA = 0
    pos = int(pos)
    if (crom[pos] == "0"):
        return kA
    else:
        if (pos <= 4):
            kA = k
            return kA
        if (crom[pos - 5] == "1"):
            kA = k - (k * 0.1)  # efecto estela aplicado
            return kA
        else:
            return kA


def printeame(poblacion, arrUno, arrDos):
    print("Pos       Fobj    Fitness")
    print("-------------------------")
    for i in range(poblacion):
        print(str(i) + " " + "-- " + str(round(float(arrDos[i]), 5)) + "-- " + str(float(arrDos[i] / suma))[:10])


def dibujaTerreno(cromosoma):
    copia_cromosoma = cromosoma[:]
    for i in range(len(copia_cromosoma)):
        copia_cromosoma[i] = int(copia_cromosoma[i])

    matriz = np.array(copia_cromosoma).reshape(5, 10)
    cmap = ListedColormap(['white', 'green'])

    # Mostrar la matriz con el mapa de colores personalizado
    plt.imshow(matriz, cmap=cmap, interpolation='none', origin='upper')
    plt.xticks(range(1))
    plt.yticks(range(5))
    plt.grid(visible=False)
    plt.show()


def llenaRuleta(pobInicial):
    for i in range(poblacion):
        fitness = 0
        contador = 0
        fitness = (arrFitness[i] / suma) * 100
        for j in range(int(math.ceil(fitness))):
            nuevaPob.append(pobInicial[i])


def ruletaInicial(arreglo):
    segundaPob = random.sample(arreglo, 50)
    return segundaPob


def corte():
    dondeCortar = random.randint(0, 49)
    return dondeCortar


def decide(variante):
    if (random.randint(0, 99) < (variante * 100)):
        return True
    else:
        return False


def nuevaCamada(poblacion, arreglo):
    for i in range(0, poblacion, 2):
        if decide(crossover):
            crossoverDeCorte(arreglo[i], arreglo[i + 1], i, arreglo)

    for j in range(0, poblacion):
        if decide(mutacion):
            corteLocal = corte()
            auxiliar = arreglo[j]
            if auxiliar[corteLocal] == "0":
                auxiliar = list(auxiliar)
                auxiliar[corteLocal] = "1"
                auxiliar = "".join((auxiliar))
            else:
                auxiliar = list(auxiliar)
                auxiliar[corteLocal] = "0"
                auxiliar = "".join((auxiliar))

            arreglo[j] = auxiliar


def crossoverDeCorte(hijoA, hijoB, indice, segundaPob):
    corteLocal = corte()
    auxiliar = hijoA[:corteLocal] + hijoB[corteLocal:50]
    hijoB = hijoB[:corteLocal] + hijoA[corteLocal:50]
    segundaPob[indice] = auxiliar
    segundaPob[indice + 1] = hijoB


# main
creaPoblacion()
# mostrar(pobInicial)
print(potenciaTotal(pobInicial))
##print("Probando: ")
##print("suma: "+str(suma))
##print("CromMax: "+str(cromMax))
##print("CromMin: "+str(cromMin))
##print("Promedio: "+str(suma/poblacion))
##for i in range(len(arrFitness)):
##    print("i: "+ str(i)+ " --> " + str(arrFitness[i]))
##print("Fitnesstotal: "+str(fitnessTotal))
# printeame(poblacion, pobInicial, arrFitness)
llenaRuleta(pobInicial)
ruletaInicial(nuevaPob)
segundaPob = ruletaInicial(nuevaPob)
print("total: " + str(suma) + " --- mayor produccion: " + str(potenciaMax))
resultadoPotencia.append(potenciaMax)
print("***************************************")

for w in range(1, ciclos + 1):
    ultimo = segundaPob[:]
    # cromMaxGuardado = cromMax
    nuevaCamada(poblacion, ultimo)
    potenciaTotal(ultimo)
    # printeame(poblacion, ultimo, arrFitness)
    llenaRuleta(ultimo)
    ruletaInicial(ultimo)
    print("w: " + str(w) + " --- total: " + str(suma) + " --- mayor produccion: " + str(potenciaMax))
    resultadoPotencia.append(potenciaMax)

dibujaTerreno(cromMax)
# dibujaTerreno(cromMaxGuardado)

# The data
for i in range(ciclos + 1):
    arregloCiclos.append(i)

x = arregloCiclos
y1 = resultadoPotencia

# Initialise the figure and axes.
fig, ax = plt.subplots(1, figsize=(8, 6))

# Set the title for the figure
fig.suptitle('Grafica de resultados ' + str(ciclos), fontsize=15)

# Draw all the lines in the same plot, assigning a label for each one to be
# shown in the legend.
ax.plot(x, y1, color="red", label="Max")

# Add a legend, and position it on the lower right (with no box)
plt.legend(loc="lower right", title="Variantes", frameon=False)

plt.show()

input()