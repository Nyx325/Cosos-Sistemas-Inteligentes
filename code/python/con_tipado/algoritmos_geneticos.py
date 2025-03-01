from enum import Enum, auto
from random import randint, random
from typing import Callable, Generic, Optional, TypeVar

V = TypeVar("V")
C = TypeVar("C")


class Pueblerino(Generic[V, C]):
    def __init__(self, valor: V, codificacion: C, fitness: float) -> None:
        self.valor = valor
        self.codificacion = codificacion
        self.fitness = fitness

    def __str__(self) -> str:
        return f"{{ Valor: {self.valor} Codificacion: {self.codificacion} Fitness: {self.fitness} }}"


class AlgoritmoGenetico(Generic[V, C]):
    class ModoSeleccion(Enum):
        ELITISMO = auto()
        RANGOS = auto()
        RULETA = auto()

    def __init__(
        self,
        # Funcion para realizar la cruza
        cruza: Callable[[list[Pueblerino[V, C]]], list[Pueblerino[V, C]]],
        # Funcion para mutar la poblacion
        muta: Callable[[list[Pueblerino[V, C]]], list[Pueblerino[V, C]]],
        # Funcion para determinar si se llegó al objetivo
        paro: Callable[[list[Pueblerino[V, C]]], bool],
    ) -> None:
        self.cruza = cruza
        self.muta = muta
        self.paro = paro

    def elitismo(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        mejor = max(poblacion, key=lambda p: p.fitness)
        nueva_poblacion.append(mejor)

        max_index = len(poblacion) - 1
        for _ in range(max_index):
            ind1 = randint(0, max_index)
            ind2 = randint(0, max_index)
            while ind1 == ind2:
                ind2 = randint(0, max_index)

            if poblacion[ind1].fitness > poblacion[ind2].fitness:
                nueva_poblacion.append(poblacion[ind1])
            else:
                nueva_poblacion.append(poblacion[ind2])

        return nueva_poblacion

    def rangos(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        poblacion_ordenada = sorted(poblacion, key=lambda p: p.fitness)

        size = len(poblacion)

        # Formula de los primeros n numeros naturales
        sumatoria_ranking = size * (size + 1) / 2

        rangos = [0.0]
        for i in range(size):
            porcentaje = (i + 1) / sumatoria_ranking
            porcentaje_acumulado = rangos[i] + porcentaje
            redondeo = round(porcentaje_acumulado, 3)
            rangos.append(redondeo)

        for _ in range(size):
            random_num = random()

            for i in range(len(rangos)):
                if rangos[i - 1] <= random_num < rangos[i]:
                    seleccion = poblacion_ordenada[i - 1]
                    nueva_poblacion.append(seleccion)
                    break

        return nueva_poblacion

    def ruleta(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        poblacion_ordenada = sorted(poblacion, key=lambda p: p.fitness, reverse=True)
        aptitud_total = sum(p.fitness for p in poblacion_ordenada)

        size = len(poblacion)
        rangos = [0.0]

        for i in range(size):
            p = poblacion_ordenada[i]
            porcentaje = p.fitness / aptitud_total
            porcentaje_acumulado = rangos[i] + porcentaje
            rangos.append(round(porcentaje_acumulado, 3))

        for _ in range(size):
            random_num = random()

            for i in range(len(rangos)):
                if rangos[i - 1] <= random_num < rangos[i]:
                    seleccionado = poblacion_ordenada[i - 1]
                    nueva_poblacion.append(seleccionado)
                    break

        return nueva_poblacion

    def ejecutar_algoritmo(
        self,
        poblacion: list[Pueblerino[V, C]],
        seleccion: ModoSeleccion,
        lim_generaciones: Optional[int],
    ):
        generacion = 0
        poblacion_cpy = poblacion.copy()

        seleccionMatcher = {
            self.ModoSeleccion.ELITISMO: self.elitismo,
            self.ModoSeleccion.RULETA: self.ruleta,
            self.ModoSeleccion.RANGOS: self.rangos,
        }

        while self.paro(poblacion_cpy) and (
            lim_generaciones == None or generacion <= lim_generaciones
        ):
            poblacion_cpy = seleccionMatcher[seleccion](poblacion_cpy)
            poblacion_cpy = self.cruza(poblacion_cpy)
            poblacion_cpy = self.muta(poblacion_cpy)

            print(f"Generacion {generacion}")
            print(poblacion_cpy)

            generacion += 1
