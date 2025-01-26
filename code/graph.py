from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Generic, Optional, TypeVar

from containers import Container, Queue, Stack
from nodes import NonWeightedVertex, Vertex, WeightedVertex

T = TypeVar("T")
Adjacency = TypeVar("Adjacency")


class Graph(Generic[T, Adjacency], ABC):
    """
    Grafo genérico con tipos parametrizados para valores de vértice y adyacencias

    Args:
        T: Tipo del valor almacenado en los vértices
        Adjacency: Tipo de las adyacencias
    """

    class Direction(Enum):
        LEFT = auto()
        RIGHT = auto()

    class Algorithm(Enum):
        BFS = auto()
        DFS = auto()

    def __init__(
        self, label: str, vertexs: Optional[list[Vertex[T, Adjacency]]] = None
    ) -> None:
        self.label = label
        self.vertexs: list[Vertex[T, Adjacency]] = vertexs if vertexs else []

    @abstractmethod
    def vertex_from_adjacency(self, adjacency: Adjacency) -> Vertex[T, Adjacency]:
        pass

    def adj_str(self, adjacency: Adjacency) -> str:
        return str(adjacency)

    def show_adjacencies(self) -> None:
        print(f"Adyacencias de {self.label}:")
        for vertex in self.vertexs:
            adj_str = ", ".join(self.adj_str(adj) for adj in vertex.adjacencies)
            print(f"{vertex} -> {{{adj_str}}}")
        print()

    def reset_visited(self) -> None:
        for vertex in self.vertexs:
            vertex.visited = False

    def explore(
        self,
        start: Vertex[T, Adjacency],
        search_type: Algorithm,
        seek: Optional[Vertex[T, Adjacency]] = None,
        direction: Direction = Direction.RIGHT,
    ) -> Optional[int]:
        vertex_to_check: Container[Vertex[T, Adjacency]] = (
            Stack() if search_type == self.Algorithm.DFS else Queue()
        )

        title = "Recorrido" if seek is None else f"Búsqueda a {seek}"
        print(f"{title} {search_type.name} por {direction.name} de {self.label}: {{")

        steps = 0
        vertex_to_check.add(start)
        start.visited = True
        print(f"Container: {vertex_to_check}")

        while not vertex_to_check.is_empty():
            curr_v = vertex_to_check.get()
            print(f"  {curr_v}")
            steps += 1

            if curr_v is None:
                continue

            if seek is not None and seek == curr_v:
                print("}")
                print(f"Encontrado en {steps} saltos\n")
                self.reset_visited()
                return steps

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

            print(f"Container: {vertex_to_check}")

        print("}")
        self.reset_visited()

        if seek is not None:
            print("NO SE ENCONTRÓ EL VÉRTICE\n")

        return None


class NonWeightedGraph(Graph[T, NonWeightedVertex[T]]):
    def vertex_from_adjacency(
        self, adjacency: NonWeightedVertex[T]
    ) -> NonWeightedVertex[T]:
        return adjacency


class WeightedGraph(Graph[T, tuple[WeightedVertex[T], float]]):
    def vertex_from_adjacency(
        self, adjacency: tuple[WeightedVertex[T], float]
    ) -> WeightedVertex[T]:
        vertex, _ = adjacency
        return vertex

    def adj_str(self, adjacency: tuple[WeightedVertex[T], float]) -> str:
        vertex, weight = adjacency
        return f"({vertex.value}, {weight})"
