from random import randint
from typing import Any

cadena = format(30, f"0{5}b")  # Convertir 30 a una cadena de 5 bits

BITS = 5


def generar_poblacion(cantidad: int, bits: int) -> list[str]:
    poblacion = []
    for _ in range(cantidad):
        pueblerino = {}

        pueblerino["codificacion"] = format(randint(0, 2**bits - 1))
        pueblerino["decodificacion"] = decodificar(pueblerino["codificacion"])
        pueblerino["fitness"] = fitness(pueblerino["decodificacion"])

        poblacion.append(pueblerino)

    return poblacion


def decodificar(pueblerino):
    return int(pueblerino, 2)


# f(x) = x^2
def fitness(pueblerino_decodificado):
    return pueblerino_decodificado**2


def racismo(poblacion: list[dict[str, Any]]):
    pob = poblacion.copy()
    pob.sort(key=lambda pueblerino: pueblerino["fitness"], reverse=True)
    return [pueblerino for pueblerino in pob if pueblerino["fitness"] == max]


def torneo(poblacion: list[dict[str, Any]]):
    pass


poblacion_codificada = generar_poblacion(999999, BITS)

fitness_poblacion = [
    fitness(decodificar(pueblerino)) for pueblerino in poblacion_codificada
]

print(f"Población: {poblacion_codificada}")
print(f"Poblacion decodificada: {fitness_poblacion}")
