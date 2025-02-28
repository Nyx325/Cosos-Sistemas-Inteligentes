from random import randint, random
from types import NotImplementedType


class Pueblerino:
    def __init__(self, valor, codificacion, fitness) -> None:
        self.valor = valor
        self.codificacion = codificacion
        self.fitness = fitness

    # Equivalente a toString() en java
    def __str__(self) -> str:
        return f"{{ Valor: {self.valor} Codificacion: {self.codificacion} Fitness: {self.fitness} }}"


class AlgoritmosGeneticos:
    @staticmethod
    def generar_poblacion_binaria_aleatoria(
        num_pueblerinos: int,
        bits: int,
    ) -> list[Pueblerino]:
        if bits <= 0 or num_pueblerinos <= 0:
            error = f"Los valores deben ser enteros positivos, se recibió {num_pueblerinos} y {bits}"
            raise Exception(error)

        poblacion: list[Pueblerino] = []
        for _ in range(num_pueblerinos):
            max_num_binario_posible = 2**bits - 1
            codificacion = format(randint(0, max_num_binario_posible), f"0{bits}b")
            valor = int(codificacion, 2)
            fitness = calcular_fitness(valor)
            poblacion.append(Pueblerino(valor, codificacion, fitness))

        return poblacion

    @staticmethod
    def elitismo(poblacion: list[Pueblerino]) -> list[Pueblerino]:
        nueva_poblacion = []

        # Seleccionar al mejor dado el fitness
        # max ya devuelve el objeto
        mejor = max(poblacion, key=lambda p: p.fitness)
        nueva_poblacion.append(mejor)

        # seleccionamos al resto de individuos por torneo
        max_index = len(poblacion) - 1
        for _ in range(max_index):
            ind1 = randint(0, max_index)
            ind2 = randint(0, max_index)

            # ind1 debe ser diferente a ind2
            while ind1 == ind2:
                ind2 = randint(0, max_index)

            # aplicamos torneo determinista
            # elegimos al que tiene mayor fitness
            if poblacion[ind1].fitness > poblacion[ind2].fitness:
                nueva_poblacion.append(poblacion[ind1])
            else:
                nueva_poblacion.append(poblacion[ind2])

        return nueva_poblacion

    @staticmethod
    def rangos(poblacion: list[Pueblerino]) -> list[Pueblerino]:
        nueva_poblacion = []

        # poblacion.sort() altera la lista original
        # sorted() devuelve una copia de la lista
        poblacion_ordenada = sorted(poblacion, key=lambda p: p.fitness)

        l_size = len(poblacion_ordenada)

        # Formula de sumatoria de los primeros "n" numeros naturales
        sumatoria_ranking = (l_size * (l_size + 1)) / 2  # n * (n + 1) / 2

        # Crear los rangos en una lista iniciando por el 0
        rangos: list[float] = [0]

        for i in range(0, l_size):
            # num_elemento / sumatoria
            porcentaje = (i + 1) / sumatoria_ranking

            # Calcular el porcentaje actual mas el anterior
            porcentaje_acumulado = rangos[i] + porcentaje
            rangos.append(round(porcentaje_acumulado, 3))

        # Generar un número aleatorio
        random_num = random()

        # Seleccionar el Pueblerino correspondiente
        for i in range(1, len(rangos)):
            # Seleccionar al valor que esté entre el límite inferior y superior del rango
            if rangos[i - 1] <= random_num < rangos[i]:
                # Seleccionar el Pueblerino correspondiente al rango
                seleccionado = poblacion_ordenada[i - 1]
                nueva_poblacion.append(seleccionado)
                break

        # Solo retorna un valor, ns si eso se deba hacer
        return nueva_poblacion

    @staticmethod
    def cruza(poblacion: list[Pueblerino]) -> list[Pueblerino]:
        nuevaPob = []
        tamanio_poblacion = len(poblacion)
        num_parejas = tamanio_poblacion // 2  # Número de parejas (división entera)

        longitud_codificacion = len(poblacion[0].codificacion)

        for _ in range(num_parejas):
            # Seleccionar dos padres aleatorios
            ind_padre1 = randint(0, tamanio_poblacion - 1)
            ind_padre2 = randint(0, tamanio_poblacion - 1)
            while ind_padre1 == ind_padre2:  # Evitar que sea el mismo padre
                ind_padre2 = randint(0, tamanio_poblacion - 1)

            # Elegir un punto de cruce aleatorio
            puntoCruce = randint(1, longitud_codificacion - 1)

            padre1 = poblacion[ind_padre1]
            padre2 = poblacion[ind_padre2]

            # Realizar la cruza
            codificacion_hijo1 = (
                padre1.codificacion[:puntoCruce] + padre2.codificacion[puntoCruce:]
            )

            codificacion_hijo2 = (
                padre2.codificacion[:puntoCruce] + padre1.codificacion[puntoCruce:]
            )

            # Crear nuevos objetos Pueblerino para los hijos

            # Asumir que está codificado en binario para la decodificacion de la cruza
            valor = int(codificacion_hijo1, 2)
            codificacion = codificacion_hijo1
            fitness = calcular_fitness(valor)
            hijo1 = Pueblerino(valor, codificacion, fitness)

            valor = int(codificacion_hijo2, 2)
            codificacion = codificacion_hijo2
            fitness = calcular_fitness(valor)

            hijo2 = Pueblerino(
                valor=valor,
                codificacion=codificacion,
                fitness=fitness,
            )

            # Agregar los hijos a la nueva población
            nuevaPob.append(hijo1)
            nuevaPob.append(hijo2)

        # Si el tamaño de la población es impar, generar un hijo adicional
        if tamanio_poblacion % 2 != 0:
            ind_padre1 = randint(0, tamanio_poblacion - 1)
            ind_padre2 = randint(0, tamanio_poblacion - 1)
            while ind_padre1 == ind_padre2:
                padre2 = randint(0, tamanio_poblacion - 1)

            puntoCruce = randint(1, longitud_codificacion - 1)

            padre1 = poblacion[ind_padre1]
            padre2 = poblacion[ind_padre2]

            codificacion_hijo = (
                padre1.codificacion[:puntoCruce] + padre2.codificacion[puntoCruce:]
            )

            valor = int(codificacion_hijo, 2)
            codificacion = codificacion_hijo
            fitness = calcular_fitness(valor)
            hijo = Pueblerino(
                valor=valor,
                codificacion=codificacion,
                fitness=fitness,
            )
            nuevaPob.append(hijo)

        return nuevaPob

    @staticmethod
    def muta(
        poblacion: list[Pueblerino],
        probabilidad_muta: float = 0.1,
    ) -> list[Pueblerino]:
        nueva_poblacion = []

        if probabilidad_muta > 1 or probabilidad_muta < 0:
            raise ValueError("La probabilidad de muta debe estar entre 0 y 1")

        for i in range(len(poblacion)):
            pueblerino = poblacion[i]

            codificacion_arr = list(pueblerino.codificacion)

            if random() <= probabilidad_muta:
                alelo = randint(0, len(codificacion_arr) - 1)
                if codificacion_arr[alelo] == "0":
                    codificacion_arr[alelo] = "1"
                else:
                    codificacion_arr[alelo] = "0"

            # Como ahora usamos objetos, si reasignamos
            # la codificacion alteramos la lista anterior,
            # por lo cual toca volver a crear un objeto
            # Además no sé recalculaba el fitness si se
            # daba una mutacion, un errorsote
            codificacion = "".join(codificacion_arr)
            valor = int(codificacion, 2)
            nuevo_pueblerino = Pueblerino(
                codificacion=codificacion,
                valor=valor,
                fitness=calcular_fitness(valor),
            )

            nueva_poblacion.append(nuevo_pueblerino)

        return nueva_poblacion


def calcular_fitness(valor: int):
    return valor**2


def parar(poblacion: list[Pueblerino]):
    for pueblerino in poblacion:
        if pueblerino.fitness == 961:
            return True

    return False


def print_poblacion(poblacion: list):
    print("Poblacion generada: ")
    for p in poblacion:
        print(p)
    print("\n")


poblacion = AlgoritmosGeneticos.generar_poblacion_binaria_aleatoria(
    num_pueblerinos=4,
    bits=5,
)

generacion = 0
while parar(poblacion) != True and generacion <= 30:
    # Seleccionar a los mejores individuos según su fitness,
    # aplicar elitismo para el primer individuo, y torneo
    # determinista para el resto de individuos
    poblacion = AlgoritmosGeneticos.elitismo(poblacion)
    # Cruza de un solo punto, generación de dos hijos por pareja.
    poblacion = AlgoritmosGeneticos.cruza(poblacion)
    poblacion = AlgoritmosGeneticos.muta(poblacion)
    print(f"Generacion {generacion}")
    print_poblacion(poblacion)

    generacion += 1
