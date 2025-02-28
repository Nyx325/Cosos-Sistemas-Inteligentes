from random import randint


def generarPoblacion(cantidad):
    poblacion = []
    for i in range(4):
        poblacion.append(format(randint(0, 31), f"{5}b"))
    return poblacion


def evaluarPoblacion(poblacion):
    fitness = []
    # recorro la poblacion
    for ind in poblacion:
        # decodificar y aplicamos la funcion objetivo fx=x^2
        fitness.append(int(ind, 2) ** 2)
    return fitness


def seleccion(poblacion, fitness):
    nuevaPob = []
    # se elige al mejor por elitismo
    indice = fitness.index(max(fitness))
    nuevaPob.append(poblacion[indice])

    for i in range(3):
        ind1 = randint(0, 3)
        ind2 = randint(0, 3)
        while ind1 == ind2:
            ind1 = randint(0, 3)
            ind2 = randint(0, 3)
        # aplicamos torneo determinista
        if fitness[ind1] > fitness[ind2]:
            nuevaPob.append(poblacion[ind1])
        else:
            nuevaPob.append(poblacion[ind2])
    return nuevaPob


# 1.- Generar una población aleatoria de 4 individuos
poblacion = []
poblacion = generarPoblacion(4)

# 2.- Evaluar fitness
fitness = evaluarPoblacion(poblacion)

# 3.- Seleccionar los mejores individuos según su fitness, aplicando elitismo para el primer indice
print(poblacion)
poblacion = seleccion(poblacion, fitness)
print(poblacion)

# Ejemplo de uso de las funciones
iteraciones = 0
paro = False
poblacion = []
