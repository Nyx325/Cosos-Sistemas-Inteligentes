from graph import Graph, WeightedGraph
from nodes import Vertex, WeightedVertex

if __name__ == "__main__":
    v1: Vertex = WeightedVertex(1)
    v2: Vertex = WeightedVertex(2)
    v3: Vertex = WeightedVertex(3)
    v4: Vertex = WeightedVertex(4)
    v5: Vertex = WeightedVertex(5)

    v1.append((v2, 1), (v3, 1))
    v2.append((v4, 1))
    v3.append((v5, 1))

    arbol: Graph = WeightedGraph("Arbol No Ponderado", [v1, v2, v3, v4, v5])
    arbol.show_adjacencies()
    arbol.explore(
        start=v1,
        search_type=Graph.Algorithm.BFS,
        direction=Graph.Direction.RIGHT,
        seek=v5,
    )

    arbol.explore(
        start=v1,
        search_type=Graph.Algorithm.DFS,
        direction=Graph.Direction.RIGHT,
        seek=v5,
    )

    arbol.explore(
        start=v1,
        search_type=Graph.Algorithm.BFS,
        direction=Graph.Direction.LEFT,
        seek=v5,
    )

    arbol.explore(
        start=v1,
        search_type=Graph.Algorithm.DFS,
        direction=Graph.Direction.LEFT,
        seek=v5,
    )
