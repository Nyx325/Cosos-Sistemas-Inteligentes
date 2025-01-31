from graph import Graph, NonWeightedGraph
from nodes import NonWeightedVertex

if __name__ == "__main__":
    v1 = NonWeightedVertex(1)
    v2 = NonWeightedVertex(2)
    v3 = NonWeightedVertex(3)
    v4 = NonWeightedVertex(4)
    v5 = NonWeightedVertex(5)

    v1.append(v2, v3)
    v2.append(v4)
    v3.append(v5)

    arbol = NonWeightedGraph("Arbol Ponderado", [v1, v2, v3, v4, v5])
    arbol.show_adjacencies()
    arbol.search(
        start=v1,
        seek=v4,
        set_lvls=True,
        algorithm=Graph.Algorithm.BFS,
        lvl_limit=2,
    )

    arbol.search(
        start=v1,
        seek=v4,
        algorithm=Graph.Algorithm.BFS,
        lvl_limit=3,
    )
