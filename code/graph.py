from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Generic, Optional, TypeVar

from containers import Container, Queue, Stack
from nodes import Vertex, WeightedVertex

Adjacency = TypeVar("Adjacency")


class Graph(Generic[Adjacency], ABC):
    """
    Representa un grafo que contiene vértices y permite explorar sus adyacencias
    utilizando algoritmos de búsqueda (BFS y DFS) y direcciones.

    Inner Classes:
        Direction (Enum): Enumera las direcciones posibles para recorrer los vértices.
            - LEFT: Recorrido en orden inverso.
            - RIGHT: Recorrido en orden normal.

        Algorithm (Enum): Enumera los algoritmos de búsqueda disponibles.
            - BFS: Búsqueda en anchura.
            - DFS: Búsqueda en profundidad.

    Attributes:
        label (str): Etiqueta que identifica al grafo.
    """

    class Direction(Enum):
        """
        Enumera las direcciones posibles para recorrer los vértices.
        """

        LEFT = auto()
        RIGHT = auto()

    class Algorithm(Enum):
        """
        Enumera los algoritmos de búsqueda disponibles.
        """

        BFS = auto()  # Búsqueda en anchura
        DFS = auto()  # Búsqueda en profundidad

    def __init__(self, label: str, vertexs: Optional[list[Vertex]] = None) -> None:
        """
        Inicializa un grafo con una etiqueta y una lista opcional de vértices.

        Args:
            label (str): Etiqueta que identifica al grafo.
        """
        self.label = label
        self.vertexs = vertexs if vertexs else []

    def show_adjacencies(self) -> None:
        """
        Muestra las adyacencias de los vértices del grafo en la consola.
        """
        print(f"Adyacencias de {self.label}:")
        for vertex in self.vertexs:
            adjacencies_str = ", ".join(str(adj) for adj in vertex.adjacencies)
            print(f"{vertex} -> {{{adjacencies_str}}}")
        print()

    def reset_visited(self):
        for vertex in self.vertexs:
            vertex.visited = False

    def explore(
        self,
        start: Vertex,
        search_type: Algorithm,
        seek: Optional[Vertex] = None,
        direction: Direction = Direction.RIGHT,
    ) -> Optional[int]:
        """
        Explora el grafo utilizando un algoritmo de búsqueda especificado y una dirección.

        Args:
            start (Vertex): Vértice desde donde se inicia la exploración.
            search_type (Graph.Algorithm): Tipo de algoritmo de búsqueda (BFS o DFS).
            seek (Optional[Vertex]): Vértice que se desea buscar. Si es None, realiza
                                      un recorrido completo.
            direction (Graph.Direction): Dirección en la que se recorrerán los adyacentes
                                         (LEFT o RIGHT). Por defecto, RIGHT.

        Returns:
            Optional[int]: Número de pasos para encontrar el vértice buscado, o None si
                           no se encuentra el vértice.
        """
        vertex_to_check: Container = (
            Stack() if search_type == self.Algorithm.DFS else Queue()
        )

        titulo = "Recorrido" if seek is None else f"Búsqueda a {seek}"
        print(f"{titulo} {search_type.name} por \n{direction.name} de {self.label}: {{")

        steps = 0

        vertex_to_check.add(start)
        start.visited = True
        print(f"Container: {vertex_to_check}")

        while not vertex_to_check.is_empty():
            curr_v: Optional[Vertex] = vertex_to_check.get()
            print(f"  {curr_v}")

            steps += 1

            assert curr_v is not None

            if seek is not None and seek == curr_v:
                print("}")
                print(f"Encontrado en: {steps} saltos\n")
                self.reset_visited()
                return steps

            if direction == self.Direction.RIGHT:
                adjacencies = curr_v.adjacencies
            else:
                adjacencies = list(reversed(curr_v.adjacencies))

            assert adjacencies is not None
            for adjacencies in adjacencies:
                neighbor = self.vertex_from_adjacency(adjacencies)
                if not neighbor.visited:
                    vertex_to_check.add(neighbor)
                    neighbor.visited = True

            print(f"Container: {vertex_to_check}")
        print("}")
        self.reset_visited()

        if seek is not None:
            print("NO SE ENCONTRÓ EL VÉRTICE\n")

        return None

    @abstractmethod
    def vertex_from_adjacency(adjacency: Adjacency) -> Vertex[Adjacency]:
        pass


class NonWeightedGraph(Graph):
    def __init__(
        self,
        label: str,
        vertexs: Optional[list[Vertex]] = None,
    ) -> None:
        """
        Inicializa un grafo con una etiqueta y una lista opcional de vértices.

        Args:
            label (str): Etiqueta que identifica al grafo.
            vertexs (Optional[list[Vertex]]): Lista de vértices que forman el grafo.
                                             Por defecto, es una lista vacía.
        """
        self.label = label
        self.vertexs = vertexs if vertexs else []


class WeightedGraph(Graph):
    def __init__(
        self,
        label: str,
        vertexs: Optional[list[WeightedVertex]],
    ) -> None:
        self.label = label
        self.vertexs = vertexs if vertexs else []
