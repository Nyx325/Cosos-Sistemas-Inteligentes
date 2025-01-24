from data_structs import *
from nodes import *

if __name__ == "__main__":
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    v6 = Vertex(6)
    v7 = Vertex(7)
    v8 = Vertex(8)
    v9 = Vertex(9)
    v10 = Vertex(10)
    v11 = Vertex(11)
    v12 = Vertex(12)
    v13 = Vertex(13)
    v14 = Vertex(14)
    v15 = Vertex(15)
    v16 = Vertex(16)
    v17 = Vertex(17)
    v18 = Vertex(18)
    v19 = Vertex(19)
    v20 = Vertex(20)

    v1.append(v2, v3, v4)
    v2.append(v5, v6)
    v3.append(v7, v8)
    v4.append(v9, v10)
    v5.append(v11)
    v6.append(v12)
    v7.append(v13)
    v8.append(v14)
    v9.append(v15)
    v10.append(v16)
    v11.append(v17)
    v12.append(v18)
    v13.append(v19)
    v14.append(v20)

    arbol = Graph(
        "Arbol",
        [
            v1,
            v2,
            v3,
            v4,
            v5,
            v6,
            v7,
            v8,
            v9,
            v10,
            v11,
            v12,
            v13,
            v14,
            v15,
            v16,
            v17,
            v18,
            v19,
            v20,
        ],
    )

    # Mostrar las adyacencias
    arbol.show_adjacencies()

    # Explorar el árbol usando DFS
    arbol.explore2(v1, Graph.Algorithm.DFS, max_level=3)
