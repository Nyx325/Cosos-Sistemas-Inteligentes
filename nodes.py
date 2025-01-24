from typing import Any, Optional


class Node:
    """
    Representa clase molde de nodo en una estructura de datos,
    como una lista enlazada o un grafo omitiendo las referencias
    o enlaces a otros nodos


    Attributes:
        value (Any): El valor almacenado en el nodo.
    """

    def __init__(self, value: Any) -> None:
        """
        Inicializa un nodo con un valor.

        Args:
            value (Any): El valor que será almacenado en el nodo.
        """
        self.value = value
        self.visited = False

    def __str__(self) -> str:
        """
        Representa el nodo como una cadena.

        Returns:
            str: Una representación en cadena del nodo en el formato "(valor)".
        """
        return f"({self.value})"


from typing import Any, Optional


class BasicNode(Node):
    """
    Representa un nodo con una referencia a un nodo siguiente y
    un nodo anterior.

    Hereda de la clase Node y extiende su funcionalidad para incluir
    referencias al siguiente y al nodo previo en la lista.

    Attributes:
        value (Any): El valor almacenado en el nodo (heredado de Node).
        next (Optional[BasicNode]): Una referencia al siguiente nodo en la lista.
        prev (Optional[BasicNode]): Una referencia al nodo previo en la lista.
    """

    def __init__(
        self,
        value: Any,
        next: Optional["BasicNode"] = None,
        prev: Optional["BasicNode"] = None,
    ) -> None:
        """
        Args:
            value (Any): El valor que será almacenado en el nodo.
            next (Optional[BasicNode]): El siguiente nodo en la lista, o None si no hay uno.
            prev (Optional[BasicNode]): El nodo previo en la lista, o None si no hay uno.
        """
        super().__init__(value)
        self.next: Optional[BasicNode] = next
        self.prev: Optional[BasicNode] = prev


class Vertex(Node):
    """
    Representa un vértice en un grafo.

    Hereda de la clase Node y extiende su funcionalidad para incluir
    una lista de adyacencias, que representa las conexiones a otros vértices.

    Attributes:
        value (Any): El valor almacenado en el vértice (heredado de Node).
        adjacencies (List[Vertex]): Lista de vértices adyacentes (vecinos).
        etiqueta (Any): Una etiqueta opcional para el vértice.
        visited (bool): Indicador de si el vértice ha sido visitado.
    """

    def __init__(
        self,
        value: Any,
        adjacencies: Optional[list["Vertex"]] = None,
    ) -> None:
        """
        Inicializa un vértice con un valor y opcionalmente con una lista de adyacencias.

        Args:
            value (Any): El valor que será almacenado en el vértice.
            adjacencies (list[Vertex]): Una lista de vértices adyacentes,
                o una lista vacía si no se proporciona.
        """
        super().__init__(value)
        self.adjacencies = adjacencies if adjacencies else []

    def append(self, *adjacencies: "Vertex") -> None:
        """
        Agrega uno o más vértices a la lista de adyacencias del vértice actual.

        Args:
            *adjacency (Vertex): Uno o más vértices que se agregarán como adyacentes.
        """
        for vertex in adjacencies:
            self.adjacencies.append(vertex)

    def get(self, index: int) -> Optional["Vertex"]:
        """
        Obtiene un vértice adyacente en la posición especificada.

        Args:
            index (int): El índice del vértice adyacente a obtener.

        Returns:
            Optional[Vertex]: El vértice en la posición especificada, o None
            si el índice está fuera de rango.
        """
        if index < 0 or index >= len(self.adjacencies):
            return None

        return self.adjacencies[index]


class WeightedVertex(Node):
    """
    Representa un vértice en un grafo ponderado con aristas con pesos.

    Hereda de la clase Node y extiende su funcionalidad para incluir
    una lista de adyacencias ponderadas, que representa las conexiones
    a otros vértices junto con los pesos de las aristas.

    Attributes:
        value (Any): El valor almacenado en el vértice (heredado de Node).
        adjacencies (list[tuple[WeightedVertex, float]]): Lista de tuplas que representan
            vértices adyacentes y sus respectivos pesos.
        visited (bool): Indicador de si el vértice ha sido visitado (heredado de Node).
    """

    def __init__(
        self,
        value: Any,
        adjacencies: Optional[list[tuple["WeightedVertex", float]]] = None,
    ) -> None:
        """
        Inicializa un vértice ponderado con un valor y opcionalmente con una lista de adyacencias.

        Args:
            value (Any): El valor que será almacenado en el vértice.
            adjacencies (Optional[list[tuple[WeightedVertex, float]]]): Lista de tuplas
                que representan vértices adyacentes y sus pesos. Si no se proporciona,
                se inicializa como una lista vacía.
        """
        super().__init__(value)
        self.tag: Optional[tuple["WeightedVertex", float]] = None
        self.adjacencies = adjacencies if adjacencies else []

    def append(
        self,
        *adjacencies: tuple["WeightedVertex", float],
    ) -> None:
        """
        Agrega una o más adyacencias ponderadas a la lista del vértice.

        Args:
            *adjacencies (tuple[WeightedVertex, float]): Una o más tuplas que contienen:
                - WeightedVertex: Vértice adyacente
                - float: Peso de la arista hacia ese vértice
        """
        for adjacency in adjacencies:
            self.adjacencies.append(adjacency)

    def get(self, index: int) -> Optional[tuple["WeightedVertex", float]]:
        """
        Obtiene la adyacencia ponderada en la posición especificada.

        Args:
            index (int): Índice de la adyacencia a recuperar (basado en 0)

        Returns:
            Optional[tuple[WeightedVertex, float]]: Tupla con vértice y peso en la posición
            especificada, o None si el índice está fuera de rango
        """
        if index < 0 or index >= len(self.adjacencies):
            return None

        return self.adjacencies[index]
