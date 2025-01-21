from data_structs import *
from nodes import *

if __name__ == "__main__":
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    v6 = Vertex(6)

    v1.append(v2, v3, v4)
    v2.append(v5, v6)
    v3.append(v2)

    arbol = Graph("Arbol", [v1, v2, v3, v5, v6, v4])
    arbol.show_adjacencies()

    arbol.explore(v1, Graph.Algorithm.BFS, direction=Graph.Direction.RIGHT, seek=v4)
    arbol.explore(v1, Graph.Algorithm.DFS, direction=Graph.Direction.RIGHT, seek=v4)
    arbol.explore(v1, Graph.Algorithm.BFS, direction=Graph.Direction.LEFT, seek=v4)
    arbol.explore(v1, Graph.Algorithm.DFS, direction=Graph.Direction.LEFT, seek=v4)
