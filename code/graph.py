from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar

from containers import Container, Queue, Stack
from nodes import NonWeightedVertex, Vertex, WeightedVertex

T = TypeVar("T")
Adjacency = TypeVar("Adjacency")


class Graph(Generic[T, Adjacency], ABC):
    """
    Clase abstracta que representa un grafo genérico con tipos parametrizados.

    Atributos:
        label (str): Etiqueta descriptiva del grafo
        vertexs (list[Vertex[T, Adjacency]]): Lista de vértices del grafo

    Args:
        T: Tipo de dato almacenado en los vértices
        Adjacency: Tipo de las relaciones de adyacencia

    Raises:
        ValueError: Si se proporcionan vértices que no son instancias de Vertex
    """

    class Direction(Enum):
        """Enumera las direcciones de recorrido posibles"""

        LEFT = auto()  # Recorrido por la izquierda (adyacencias invertidas)
        RIGHT = auto()  # Recorrido por la derecha (orden natural)

    class Algorithm(Enum):
        """Enumera los algoritmos de recorrido disponibles"""

        BFS = auto()  # Breadth-First Search
        DFS = auto()  # Depth-First Search

    def __init__(
        self, label: str, vertexs: Optional[list[Vertex[T, Adjacency]]] = None
    ) -> None:
        """
        Inicializa un nuevo grafo.

        Args:
            label: Nombre identificativo del grafo
            vertexs: Lista opcional de vértices iniciales
        """
        self.label = label

        if vertexs and not all(isinstance(v, Vertex) for v in vertexs):
            raise ValueError("All elements in 'vertexs' must be instances of Vertex.")

        self.vertexs: list[Vertex[T, Adjacency]] = vertexs if vertexs else []

    @abstractmethod
    def vertex_from_adjacency(self, adjacency: Adjacency) -> Vertex[T, Adjacency]:
        """
        Método abstracto para obtener el vértice destino desde una adyacencia.

        Args:
            adjacency: Relación de adyacencia a convertir

        Returns:
            Vértice correspondiente a la adyacencia
        """
        pass

    def adj_str(self, adjacency: Adjacency) -> str:
        """
        Formatea una adyacencia para representación como cadena.

        Args:
            adjacency: Relación de adyacencia a formatear

        Returns:
            Representación en cadena de la adyacencia
        """
        return str(adjacency)

    def show_adjacencies(self) -> None:
        """Muestra todas las adyacencias del grafo en formato legible."""
        print(f"Adyacencias de {self.label}:")
        for vertex in self.vertexs:
            adj_str = ", ".join(self.adj_str(adj) for adj in vertex.adjacencies)
            print(f"{vertex} -> {{{adj_str}}}")
        print()

    def reset_visited(self) -> None:
        """Reinicia el estado de visitado de todos los vértices."""
        for vertex in self.vertexs:
            vertex.visited = False

    def print_adjacency(
        self,
        vertex: Vertex[T, Adjacency],
        _: Optional[Any],
    ) -> tuple[bool, Optional[Any]]:
        """
        Acción por defecto para imprimir vértices durante el recorrido.

        Args:
            vertex: Vértice actual siendo visitado
            _: Argumento adicional no utilizado

        Returns:
            Tupla (False, None) para continuar el recorrido
        """
        print(f"  {vertex}")
        return (False, None)

    def equals(
        self, vertex: Vertex, vertex2: Optional[Any]
    ) -> tuple[bool, Optional[Any]]:
        """
        Compara dos vértices para búsqueda.

        Args:
            vertex: Vértice actual siendo visitado
            vertex2: Vértice buscado como objetivo

        Returns:
            Tupla (True, None) si coinciden, (False, None) en caso contrario

        Raises:
            ValueError: Si vertex2 no es una instancia de Vertex
        """
        if vertex2 is None or not isinstance(vertex2, Vertex):
            raise ValueError("Arg should be a Vertex")

        self.print_adjacency(vertex, None)

        return (True, None) if vertex is vertex2 else (False, None)

    def explore(
        self,
        start: Vertex[T, Adjacency],
        algorithm: Algorithm,
        action: Optional[
            Callable[[Vertex[T, Adjacency], Optional[Any]], tuple[bool, Optional[Any]]]
        ] = None,
        arg: Optional[Any] = None,
        direction: Direction = Direction.RIGHT,
    ) -> Optional[Any]:
        """
        La verdad la documentación la hice con ChatGPT pero la intención es proporcionar
        un método que haga los recorridos cambiando algritmo y dirección, además de poder
        recibir una función anónima que puede recibir el vertice actual y un objeto Any
        y devolver un retorno y controlar si se sigue o no ejecutando la función con
        el retorno de la tupla (bool, Any) en el retorno de la acción

        Documentación hecha con deepseek:
        Realiza un recorrido parametrizado del grafo ejecutando lógica personalizada en cada vértice.

        Diseño clave:
        - Implementa un patrón de iteración flexible (Template Method)
        - Permite inyectar comportamiento personalizado durante el recorrido
        - Provee control de flujo mediante valores de retorno
        - Soporta diferentes algoritmos (BFS/DFS) y direcciones de recorrido

        Flujo de control:
        1. Visita un vértice
        2. Ejecuta la función 'action' con el vértice actual
        3. Si 'action' devuelve True -> Detiene el recorrido y retorna valor
        4. Si devuelve False -> Continúa procesando adyacencias

        Parámetros:
            start: Vértice raíz donde inicia el recorrido
            algorithm: Estrategia de recorrido (Algoritmo.BFS o Algoritmo.DFS)
            action: Función callback con firma:
                   (vértice_actual, arg) -> (detener_recorrido: bool, valor_retorno: Any)
                   - Si detener_recorrido = True, se aborta el recorrido y retorna valor_retorno
                   - Si detener_recorrido = False, continúa normalmente
            arg: Argumento opcional que se pasa a la función 'action'
            direction: Orden de procesamiento de adyacencias (LEFT=invertido, RIGHT=natural)

        Retorno:
            - Valor retornado por 'action' si detiene el recorrido
            - None si completa todo el recorrido sin interrupciones

        Ejemplos de uso:
            1. Búsqueda de vértice:
               action = lambda v, target: (v == target, None)

            2. Recopilar información:
               def collect_vertices(v, acc):
                   acc.append(v)
                   return (False, acc)

            3. Búsqueda con retorno temprano:
               def find_special(v, _):
                   if v.is_special:
                       return (True, v)
                   return (False, None)

        Comportamiento por defecto:
            Si no se provee 'action', se usa print_adjacency que:
            - Imprime cada vértice visitado
            - Nunca detiene el recorrido (siempre retorna False)

        Notas importantes:
            - Auto-resetea estados 'visited' al finalizar
            - La dirección LEFT invierte el orden de procesamiento de adyacencias
            - Usa el patrón Strategy para algoritmos (BFS/DFS)
            - 'arg' permite implementar closures/acumuladores en 'action'
        """
        vertex_to_check: Container[Vertex[T, Adjacency]] = (
            Stack() if algorithm == self.Algorithm.DFS else Queue()
        )

        if action is None:
            action = self.print_adjacency
        assert action is not None

        print(f"Recorrido {algorithm.name} por {direction.name} de {self.label}: {{")
        vertex_to_check.add(start)
        start.visited = True

        while not vertex_to_check.is_empty():
            curr_v = vertex_to_check.get()

            if curr_v is None:
                raise RuntimeError("Vertice actual es None")

            end_explore, value_return = action(curr_v, arg)

            if end_explore:
                print("}")
                self.reset_visited()
                return value_return

            adjacencies = (
                curr_v.adjacencies
                if direction == self.Direction.RIGHT
                else list(reversed(curr_v.adjacencies))
            )

            for adjacency in adjacencies:
                neighbor = self.vertex_from_adjacency(adjacency)
                if not neighbor.visited:
                    vertex_to_check.add(neighbor)
                    neighbor.visited = True

        print("}")

        self.reset_visited()
        return None

    def search(
        self,
        start: Vertex[T, Adjacency],
        seek: Vertex[T, Adjacency],
        algorithm: Algorithm = Algorithm.BFS,
        direction: Direction = Direction.RIGHT,
    ) -> Optional[Any]:
        """
        Busca un vértice en el grafo mediante recorrido.

        Args:
            start: Vértice inicial de búsqueda
            seek: Vértice objetivo a encontrar
            algorithm: Algoritmo de búsqueda a utilizar
            direction: Dirección de procesamiento de adyacencias

        Returns:
            None cuando encuentra el vértice o si no existe
        """
        return self.explore(
            start=start,
            algorithm=algorithm,
            direction=direction,
            action=self.equals,
            arg=seek,
        )


class NonWeightedGraph(Graph[T, NonWeightedVertex[T]]):
    """
    Grafo no ponderado donde las adyacencias son vértices directamente.

    Hereda de:
        Graph[T, NonWeightedVertex[T]]
    """

    def vertex_from_adjacency(
        self, adjacency: NonWeightedVertex[T]
    ) -> NonWeightedVertex[T]:
        """
        Obtiene el vértice destino desde una adyacencia no ponderada.

        Args:
            adjacency: Vértice adyacente directo

        Returns:
            El mismo vértice de la adyacencia
        """
        return adjacency


class WeightedGraph(Graph[T, tuple[WeightedVertex[T], float]]):
    """
    Grafo ponderado donde las adyacencias son tuplas (vértice, peso).

    Hereda de:
        Graph[T, tuple[WeightedVertex[T], float]]
    """

    def vertex_from_adjacency(
        self, adjacency: tuple[WeightedVertex[T], float]
    ) -> WeightedVertex[T]:
        """
        Obtiene el vértice destino desde una adyacencia ponderada.

        Args:
            adjacency: Tupla (vértice adyacente, peso)

        Returns:
            Componente vértice de la tupla de adyacencia
        """
        vertex, _ = adjacency
        return vertex

    def adj_str(self, adjacency: tuple[WeightedVertex[T], float]) -> str:
        """
        Formatea una adyacencia ponderada como '(valor, peso)'.

        Args:
            adjacency: Tupla (vértice, peso) a formatear

        Returns:
            Cadena formateada con valor del vértice y peso
        """
        vertex, weight = adjacency
        return f"({vertex.value}, {weight})"
