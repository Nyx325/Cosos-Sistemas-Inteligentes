from graph import Graph
from nodes import Vertex

if __name__ == "__main__":
    seek = Vertex([[2, 3, 8], [1, 4, 5], [7, 0, 6]])

    # lvl1
    v1 = Vertex([[2, 3, 8], [1, 0, 4], [7, 6, 5]])

    # lvl2
    v2 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v3 = Vertex([[2, 0, 8], [1, 3, 4], [7, 6, 5]])
    v4 = Vertex([[2, 3, 8], [1, 4, 0], [7, 6, 5]])
    v5 = Vertex([[2, 3, 8], [1, 6, 4], [7, 0, 5]])
    v1.append(v2, v3, v4, v5)

    # lvl3
    v6 = Vertex([[0, 3, 8], [2, 1, 4], [7, 6, 5]])
    v7 = Vertex([[2, 3, 8], [7, 1, 4], [0, 6, 5]])
    v8 = Vertex([[2, 3, 8], [1, 0, 4], [7, 6, 5]])
    v2.append(v6, v7, v8)

    v9 = Vertex([[0, 2, 8], [1, 3, 4], [7, 6, 5]])
    v10 = Vertex([[2, 3, 8], [1, 0, 4], [7, 6, 5]])
    v11 = Vertex([[2, 8, 0], [1, 3, 4], [7, 6, 5]])
    v3.append(v9, v10, v11)

    v12 = Vertex([[2, 3, 0], [1, 4, 8], [7, 6, 5]])
    v13 = Vertex([[2, 3, 8], [1, 4, 5], [7, 6, 0]])
    v14 = Vertex([[2, 3, 8], [1, 0, 4], [7, 6, 5]])
    v4.append(v12, v13, v14)

    v15 = Vertex([[2, 3, 8], [1, 6, 4], [0, 7, 5]])
    v16 = Vertex([[2, 3, 8], [1, 6, 4], [7, 5, 0]])
    v17 = Vertex([[2, 3, 8], [1, 0, 4], [7, 6, 5]])
    v5.append(v15, v16, v17)

    # lvl4
    v18 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v19 = Vertex([[3, 0, 8], [2, 1, 4], [7, 6, 5]])
    v6.append(v18, v19)

    v20 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v21 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v7.append(v20, v21)

    v22 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v23 = Vertex([[2, 0, 8], [1, 3, 4], [7, 6, 5]])
    v24 = Vertex([[2, 3, 8], [1, 4, 0], [7, 6, 5]])
    v25 = Vertex([[2, 3, 8], [1, 6, 4], [7, 0, 5]])
    v8.append(v22, v23, v24, v25)

    v26 = Vertex([[1, 2, 8], [0, 3, 4], [7, 6, 5]])
    v27 = Vertex([[2, 0, 8], [1, 3, 4], [7, 6, 5]])
    v9.append(v26, v27)

    v28 = Vertex([[2, 3, 8], [0, 1, 4], [7, 6, 5]])
    v29 = Vertex([[2, 0, 8], [1, 3, 4], [7, 6, 5]])
    v30 = Vertex([[2, 3, 8], [1, 4, 0], [7, 6, 5]])
    v31 = Vertex([[2, 3, 8], [1, 6, 4], [7, 0, 5]])
    v10.append(v28, v29, v30, v31)

    v32 = Vertex([[2, 0, 8], [1, 3, 4], [7, 6, 5]])
    v33 = Vertex([[2, 8, 4], [1, 3, 0], [7, 6, 5]])
    v11.append(v32, v33)

    v34 = Vertex([[2, 0, 3], [1, 4, 8], [7, 6, 5]])
    v35 = Vertex([[2, 3, 8], [1, 4, 0], [7, 6, 5]])
    v12.append(v34, v35)

    v36 = Vertex([[2, 3, 8], [1, 4, 5], [7, 0, 6]])
    v13.append(v36)

    arbol = Graph(
        "Puzzle",
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
            v21,
            v22,
            v23,
            v24,
            v25,
            v26,
            v27,
            v28,
            v29,
            v30,
            v31,
            v32,
            v33,
            v34,
            v35,
            v36,
        ],
    )

    resultados = {}
    eq = lambda v1, v2: bool(v1.value == v2.value)

    resultados["Anchura derecha"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.BFS,
        direction=Graph.Direction.RIGHT,
        eval_eq=eq,
    )

    resultados["Anchura izquierda"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.BFS,
        direction=Graph.Direction.LEFT,
        eval_eq=eq,
    )

    resultados["Profundidad Izquierda"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.DFS,
        direction=Graph.Direction.LEFT,
        eval_eq=eq,
    )

    limite = 3
    resultados[f"Profundidad con límite {limite}"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.DFS,
        direction=Graph.Direction.RIGHT,
        set_lvls=True,
        lvl_limit=limite,
        eval_eq=eq,
    )

    resultados["Profundidad Derecha"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.DFS,
        direction=Graph.Direction.RIGHT,
        eval_eq=eq,
    )

    resultados["Profundidad Iterativo Derecha"] = arbol.seek(
        start=v1,
        seek=seek,
        algorithm=Graph.Algorithm.DFS,
        direction=Graph.Direction.RIGHT,
        iterative=True,
        eval_eq=eq,
    )

    print()
    for clave, valor in resultados.items():
        if valor is not None:
            print(
                f"Para el método {clave} se recorrieron {valor} nodo(s) antes de encontrar el nodo\n"
            )
        else:
            print(f"Para el método {clave} no se encontró el nodo buscado\n")

    resultados_validos = {k: v for k, v in resultados.items() if v is not None}
    if len(resultados_validos) == 0:
        exit()

    min_nodos = min(resultados_validos.values())

    algoritmos_optimos = [k for k, v in resultados_validos.items() if v == min_nodos]

    print(f"El número mínimo de nodos recorridos fue: {min_nodos}")
    print(f"Los algoritmos que lo lograron son: {', '.join(algoritmos_optimos)}")
