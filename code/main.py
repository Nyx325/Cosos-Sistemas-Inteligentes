from typing import Any, Optional

from graph import Graph, WeightedGraph
from nodes import Vertex, WeightedVertex

if __name__ == "__main__":
    v1: Vertex = WeightedVertex(1)
    v2: Vertex = WeightedVertex(2)
    v3: Vertex = WeightedVertex(3)
    v4: Vertex = WeightedVertex(4)
    v5: Vertex = WeightedVertex(5)

    v1.append((v2, 1.0), (v3, 1.0))
    v2.append((v4, 1.0))
    v3.append((v5, 1.0))

    arbol: Graph = WeightedGraph("Arbol Ponderado", [v1, v2, v3, v4, v5])
    arbol.show_adjacencies()

    def equals(vertex: Vertex, vertex2: Optional[Any]) -> tuple[bool, Optional[Any]]:
        if vertex2 is None or not isinstance(vertex2, Vertex):
            raise ValueError("Arg should be a Vertex")

        print(f"  {vertex}")
        if vertex is vertex2:
            return (True, None)
        else:
            return (False, None)

    arbol.explore(
        start=v1,
        algorithm=Graph.Algorithm.BFS,
        direction=Graph.Direction.RIGHT,
    )

    arbol.explore(
        start=v1,
        algorithm=Graph.Algorithm.BFS,
        direction=Graph.Direction.RIGHT,
        action=equals,
        arg=v3,
    )
