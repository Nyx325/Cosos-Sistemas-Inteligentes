from typing import Optional


class Node:
    """
    Representa un nodo en una estructura de datos enlazada.

    Atributos:
        value: El valor almacenado en el nodo.
        _next: Referencia al siguiente nodo en la estructura.
        _prev: Referencia al nodo anterior en la estructura.
    """

    def __init__(self, value, next=None, prev=None) -> None:
        self.value = value
        self._next = next
        self._prev = prev

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del nodo.
        """
        return f"({self.value})"


class Vertex:
    """
    Representa un vértice en un grafo.

    Atributos:
        value: El valor almacenado en el vértice.
        lvl: Nivel del vértice, si aplica.
        visited: Indica si el vértice ha sido visitado.
        adjacencies: Lista de vértices adyacentes.
    """

    def __init__(self, value, lvl=None, adjacencies=None) -> None:
        self.value = value
        self.lvl = lvl
        self.visited = False
        self._adjacencies = adjacencies if adjacencies is not None else []

    def append(self, *adjacencies) -> None:
        """
        Agrega vértices adyacentes a la lista de adyacencias.

        Parámetros:
            *adjacencies: Vértices a agregar como adyacencias.
        """
        self._adjacencies.extend(adjacencies)

    def get(self, index: int) -> Optional["Vertex"]:
        """
        Obtiene el vértice adyacente en la posición indicada.

        Parámetros:
            index: Índice del vértice en la lista de adyacencias.

        Retorna:
            Optional[Vertex]: El vértice en la posición dada, o None si el índice es inválido.
        """
        try:
            return self._adjacencies[index]
        except IndexError:
            return None

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del vértice.
        """
        return f"Vertice: {{ Value: {self.value} lvl: {self.lvl} }}"
