from random import randint
from typing import Generic, TypeVar

V = TypeVar("V")
C = TypeVar("C")
F = TypeVar("F")


class Pueblerino(Generic[V, C, F]):
    def __init__(self, valor: V, codificacion: C, fitness: F) -> None:
        self.valor = valor
        self.codificacion = codificacion
        self.fitness = fitness


def calcular_fitness(valor: int):
    return valor**2


def generar_poblacion(num_pueblerinos: int, bits: int):
    if bits <= 0 or num_pueblerinos <= 0:
        raise Exception(
            f"Los valores deben ser enteros positivos, se recibió {num_pueblerinos} y {bits}"
        )

    poblacion: list[Pueblerino[int, str, int]] = []
    for _ in range(num_pueblerinos):
        codificacion = format(randint(0, 2**bits - 1), f"0{bits}b")
        valor = int(codificacion, 2)
        fitness = calcular_fitness(valor)
        poblacion.append(Pueblerino(valor, codificacion, fitness))
