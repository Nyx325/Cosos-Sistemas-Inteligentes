from random import randint, random
from typing import Any


def generar_poblacion(cantidad: int, bits: int) -> list[dict[str, Any]]:
    poblacion = []
    for _ in range(cantidad):
        pueblerino: dict[str, Any] = {}
        pueblerino["codificacion"] = format(randint(0, 2**bits - 1), f"0{bits}b")
        pueblerino["decodificacion"] = decodificar(pueblerino["codificacion"])
        pueblerino["fitness"] = fitness(pueblerino["decodificacion"])

        poblacion.append(pueblerino)

    return poblacion


def decodificar(pueblerino):
    return int(pueblerino, 2)


# f(x) = x^2
def fitness(pueblerino_decodificado):
    return pueblerino_decodificado**2


# Elitismo
def racismo(poblacion: list[dict[str, Any]]):
    nueva_poblacion: list[dict[str, Any]] = []
    mejor = max(poblacion, key=lambda p: p["fitness"])
    nueva_poblacion.append(mejor)

    max_index = len(poblacion) - 1
    for _ in range(max_index):
        ind1 = randint(0, max_index)
        ind2 = randint(0, max_index)

        while ind2 == ind1:
            ind2 = randint(0, max_index)

        if poblacion[ind1]["fitness"] > poblacion[ind2]["fitness"]:
            nueva_poblacion.append(poblacion[ind1])
        else:
            nueva_poblacion.append(poblacion[ind2])

    return nueva_poblacion


def ordenar_1(poblacion: list[str], fitness: list[int]) -> tuple[list[str], list[int]]:
    poblacion_dict: list[dict[str, Any]] = []

    for i in range(len(poblacion)):
        pueblerino = {"codificacion": poblacion[i], "fitness": fitness[i]}
        poblacion_dict.append(pueblerino)

    poblacion_dict.sort(key=lambda p: p["fitness"])

    poblacion = [p["codificacion"] for p in poblacion_dict]
    fitness = [p["fitness"] for p in poblacion_dict]

    return (poblacion, fitness)


def ordenar_2(poblacion, fitness) -> tuple[list[str], list[int]]:
    poblacion_dict: list[dict[str, Any]] = []

    for i in range(len(poblacion)):
        pueblerino = {"codificacion": poblacion[i], "fitness": fitness[i]}
        poblacion_dict.append(pueblerino)

    poblacion_dict.sort(key=lambda p: p["fitness"])

    poblacion_cpy = []
    for pueblerino in poblacion_dict:
        poblacion_cpy.append(pueblerino["codificacion"])

    fitness_cpy = []
    for pueblerino in poblacion_dict:
        fitness_cpy.append(pueblerino["fitness"])

    return (poblacion_cpy, fitness_cpy)


def rangos(poblacion: list[dict[str, Any]]):
    poblacion_ordenada = list(sorted(poblacion, key=lambda p: p["fitness"]))

    l_size = len(poblacion_ordenada)

    sigma_ranking = (l_size * (l_size + 1)) / 2  # n * (n + 1) / 2

    rangos: list[float] = [0]

    for i in range(0, l_size):
        porcentaje = (i + 1) / sigma_ranking
        rangos.append(rangos[i] + porcentaje)
        print(f"{porcentaje}%")
        poblacion_ordenada[i]["porcentaje"] = porcentaje

    random_num = random()
    for i in range(1, len(rangos)):
        print(f"Entre {rangos[i - 1]} y {rangos[i]}")


poblacion = generar_poblacion(4, 5)
rangos(poblacion)
