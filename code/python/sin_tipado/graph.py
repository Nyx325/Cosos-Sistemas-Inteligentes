from enum import Enum, auto
from typing import Any, Optional

from containers import Queue, Stack


class Graph:
    """
    Clase que representa un grafo genérico con tipos parametrizados.

    Atributos:
        label: Etiqueta descriptiva del grafo
        vertexs: Lista de vértices del grafo
    """

    class Direction(Enum):
        """Enumera las direcciones de recorrido posibles"""

        LEFT = auto()  # Recorrido por la izquierda (adyacencias invertidas)
        RIGHT = auto()  # Recorrido por la derecha (orden natural)

    class Algorithm(Enum):
        """Enumera los algoritmos de recorrido disponibles"""

        BFS = auto()  # Breadth-First Search (Anchura)
        DFS = auto()  # Depth-First Search (Profundidad)

    def __init__(self, label, vertexs=None) -> None:
        """
        Inicializa un nuevo grafo.

        Args:
            label: Nombre identificativo del grafo
            vertexs: Lista opcional de vértices iniciales
        """
        self.label = label
        self._vertexs = vertexs if vertexs is not None else []

    def show_adjacencies(self) -> None:
        """Muestra todas las adyacencias del grafo en formato legible."""
        print(f"Adyacencias de {self.label}:")
        for vertex in self._vertexs:
            adj_str = ", ".join(str(adj) for adj in vertex._adjacencies)
            print(f"{vertex} -> {{{adj_str}}}")
        print()

    def reset_visited(self) -> None:
        """Reinicia el estado de visitado de todos los vértices."""
        for vertex in self._vertexs:
            vertex.visited = False

    def set_lvls(self, root, direction=Direction.RIGHT):
        """
        Establece el atributo de lvl a cada uno de los vértices de un grafo
        a partir del nodo inicial que se escoja haciendo uso de recorrido
        en anchura.

        Args:
            root: El nodo que se considerará como nodo inicial
            direction: La dirección en la que hará el recorrido en anchura,
                izquierda o derecha, por defecto derecha
        """
        vertex_to_check = Queue()
        print("Calculando niveles...")
        root.visited = True
        root.lvl = 1
        vertex_to_check.enqueue(root)

        while not vertex_to_check.empty():
            curr_v = vertex_to_check.dequeue()
            assert curr_v is not None
            assert curr_v.lvl is not None

            print(f"  {curr_v}")

            adjacencies = (
                curr_v._adjacencies
                if direction == self.Direction.RIGHT
                else list(reversed(curr_v._adjacencies))
            )

            for vertex in adjacencies:
                if not vertex.visited:
                    vertex.visited = True
                    vertex.lvl = curr_v.lvl + 1
                    vertex_to_check.add(vertex)

        print()
        self.reset_visited()

    def __print_adjacency(
        self,
        vertex,
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

    def explore(
        self,
        start,
        algorithm=Algorithm.BFS,
        direction=Direction.RIGHT,
        set_lvls=False,
        lvl_limit=None,
        iterative=False,
        action=None,
        arg=None,
    ) -> Optional[Any]:
        """
        Realiza un recorrido parametrizado del grafo ejecutando lógica personalizada en cada vértice.

        Parámetros:
            start: Vértice raíz donde inicia el recorrido
            algorithm: Estrategia de recorrido (Algoritmo.BFS o Algoritmo.DFS)
            direction: Orden de procesamiento de adyacencias (LEFT=invertido, RIGHT=natural)
            set_lvls: Ejecutar el método self.set_lvls(start) antes de empezar la exploración
            lvl_limit: Limitar la busqueda a un nivel específico, para esto los vértices deben
                tener el nivel puesto de forma correcta, si no se estableció ningún nivel la función
                soltará una excepción durante el recorrido o si se establecen niveles mal puede ocurrir
                un comportamiento inesperado
            iterative: Recorrer un arbol de forma iterativa (potencial error de ciclado en grafos)
            action: Función callback con firma:
                   (vértice_actual, arg) -> (detener_recorrido: bool, valor_retorno: Any)
                   - Si detener_recorrido = True, se aborta el recorrido y retorna valor_retorno
                   - Si detener_recorrido = False, continúa normalmente
            arg: Argumento opcional que se pasa a la función 'action'

        Retorno:
            - Valor retornado por 'action' si detiene el recorrido
            - None si completa todo el recorrido sin interrupciones
        """
        if set_lvls:
            self.set_lvls(start)

        loop = 1
        vertex_visited = 0
        vertex_before_loop = 0

        vertex_to_check = Stack() if algorithm == self.Algorithm.DFS else Queue()

        if action is None:
            action = self.__print_adjacency

        assert action is not None

        limitTitle = f"con límite {lvl_limit}" if lvl_limit is not None else ""
        print(f"Recorrido {algorithm.name} por {direction.name} {limitTitle}")

        vertex_to_check.add(start)
        vertex_before_loop += 1
        if not iterative:
            start.visited = True

        while not vertex_to_check.empty():
            curr_v = vertex_to_check.get()

            if curr_v is None:
                raise RuntimeError("Vertice actual es None")

            end_explore, value_return = action(curr_v, arg)

            if end_explore:
                print()
                self.reset_visited()
                return value_return

            vertex_visited += 1

            if iterative and vertex_visited == vertex_before_loop:
                loop += 1
                vertex_to_check = (
                    Stack() if algorithm == self.Algorithm.DFS else Queue()
                )
                vertex_to_check.add(start)
                vertex_before_loop += 1
                vertex_visited = 0
                print(f"\nIteración {loop}")
                continue

            adjacencies = (
                curr_v._adjacencies
                if direction == self.Direction.RIGHT
                else list(reversed(curr_v._adjacencies))
            )

            for neighbor in adjacencies:
                if lvl_limit is not None:
                    assert neighbor.lvl
                    should_add = not neighbor.visited and neighbor.lvl <= lvl_limit

                else:
                    should_add = not neighbor.visited

                if should_add:
                    vertex_to_check.add(neighbor)
                    if not iterative:
                        neighbor.visited = True

        print()
        self.reset_visited()
        return None

    def seek(
        self,
        start,
        seek,
        algorithm=Algorithm.BFS,
        direction=Direction.RIGHT,
        lvl_limit=None,
        set_lvls=False,
        iterative=False,
        eval_eq=lambda v1, v2: v1 == v2,
    ) -> Optional[int]:
        """
        Busca un vértice en el grafo mediante recorrido.

        Args:
            start: Vértice inicial de búsqueda
            seek: Vértice objetivo a encontrar
            algorithm: Algoritmo de búsqueda a utilizar
            direction: Dirección de procesamiento de adyacencias
            direction: Orden de procesamiento de adyacencias (LEFT=invertido, RIGHT=natural)
            lvl_limit: Limitar la busqueda a un nivel específico, para esto los vértices deben
                tener el nivel puesto de forma correcta, si no se estableció ningún nivel la función
                soltará una excepción durante el recorrido o si se establecen niveles mal puede ocurrir
                un comportamiento inesperado
            set_lvls: Ejecutar la función self.set_lvls(start) antes de empezar la exploración
            eval_eq: Función o lambda que evalúa si los vértices son iguales, por defecto lambda v1, v2: v1 == v2

        Returns:
            None cuando encuentra el vértice o si no existe
        """
        nodesVisited = [0]

        def action(v, arg) -> tuple[bool, Any]:
            arg[0] += 1

            print(f"  {v}")
            return (eval_eq(v, seek), arg[0])

        print(f"Buscando {seek}")
        return self.explore(
            start=start,
            algorithm=algorithm,
            direction=direction,
            action=action,
            arg=nodesVisited,
            lvl_limit=lvl_limit,
            set_lvls=set_lvls,
            iterative=iterative,
        )
