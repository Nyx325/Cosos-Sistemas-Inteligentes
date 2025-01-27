from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Generic, Optional, TypeVar

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

        if vertexs and not all(isinstance(v, Vertex) for v in vertexs):
            raise ValueError("All elements in 'vertexs' must be instances of Vertex.")

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

    def print_adjacency(
        self,
        vertex: Vertex[T, Adjacency],
        _: Optional[Any],
    ) -> tuple[bool, Optional[Any]]:
        print(f"  {vertex}")
        return (False, None)

    def equals(
        self, vertex: Vertex, vertex2: Optional[Any]
    ) -> tuple[bool, Optional[Any]]:
        if vertex2 is None or not isinstance(vertex2, Vertex):
            raise ValueError("Arg should be a Vertex")

        print(f"  {vertex}")

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
                continue

            should_return, value_return = action(curr_v, arg)

            if should_return:
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
        return self.explore(
            start=start,
            algorithm=algorithm,
            direction=direction,
            action=self.equals,
            arg=seek,
        )


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
