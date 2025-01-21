from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Optional

from nodes import *


class Container(ABC):
    """
    Generalización de una estructura de datos abstracta que permite almacenar y
    recuperar elementos.

    Esta clase sirve como base para implementar diferentes estructuras de datos
    (como pilas, colas, etc.) y define los métodos abstractos que dichas
    estructuras deben implementar.
    """

    @abstractmethod
    def add(self, value: Any) -> None:
        """
        Agrega un elemento al contenedor.

        Args:
            value (Any): El elemento que será agregado al contenedor.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Optional[Any]:
        """
        Recupera y elimina un elemento del contenedor.

        Returns:
            Optional[Any]: El elemento recuperado, o None si el contenedor está vacío.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def peek(self) -> Optional[Any]:
        """
        Recupera un elemento del contenedor sin eliminarlo.

        Returns:
            Optional[Any]: El elemento recuperado, o None si el contenedor está vacío.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def size(self) -> int:
        """
        Obtiene el número de elementos en el contenedor.

        Returns:
            int: El número de elementos almacenados en el contenedor.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Verifica si el contenedor está vacío.

        Returns:
            bool: True si el contenedor está vacío, False en caso contrario.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()


class Queue(Container):
    """
    Implementación de una cola que hereda de la clase abstracta Container.

    La cola permite agregar elementos al final y eliminarlos desde el inicio, manteniendo el orden.

    Attributes:
        _len (int): Número de elementos en la cola.
        _head (Optional[BasicNode]): Nodo que apunta al inicio de la cola.
        _tail (Optional[BasicNode]): Nodo que apunta al final de la cola.
    """

    def __init__(self) -> None:
        """
        Inicializa una cola vacía.
        """
        super().__init__()
        self._len: int = 0
        self._head: Optional[BasicNode] = None
        self._tail: Optional[BasicNode] = None

    def size(self) -> int:
        """
        Obtiene el número de elementos en la cola.

        Returns:
            int: El número de elementos almacenados en la cola.
        """
        return self._len

    def is_empty(self) -> bool:
        """
        Verifica si la cola está vacía.

        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return self.size() == 0

    def enqueue(self, value: Any) -> None:
        """
        Agrega un elemento al final de la cola.

        Args:
            value (Any): El elemento que será agregado a la cola.
        """
        new = BasicNode(value)
        if self.is_empty():
            self._head = new
            self._tail = new
        else:
            assert self._tail is not None
            self._tail.next = new
            self._tail = new
        self._len += 1

    def dequeue(self) -> Optional[Any]:
        """
        Elimina y devuelve el elemento al inicio de la cola.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la cola está vacía.
        """
        if self.is_empty():
            return None

        assert self._head is not None
        value = self._head.value
        self._head = self._head.next

        if self._head is None:
            self._tail = None

        self._len -= 1
        return value

    def __str__(self) -> str:
        """
        Representa la cola como una cadena con los valores almacenados.

        Returns:
            str: Una representación en cadena de los elementos de la cola en orden.
        """
        node = self._head
        values = []
        while node is not None:
            values.append(node.value)
            node = node.next

        return str(values)

    def add(self, value: Any) -> None:
        """
        Alias para `enqueue`. Agrega un elemento al final de la cola.

        Args:
            value (Any): El elemento que será agregado a la cola.
        """
        return self.enqueue(value)

    def get(self) -> Optional[Any]:
        """
        Alias para `dequeue`. Elimina y devuelve el elemento al inicio de la cola.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la cola está vacía.
        """
        return self.dequeue()

    def peek(self) -> Optional[Any]:
        """
        Devuelve el elemento al inicio de la cola sin eliminarlo.

        Returns:
            Optional[Any]: El valor del elemento al inicio, o None si la cola está vacía.
        """
        return self._head.value if self._head else None


class Stack(Container):
    """
    Implementación de una pila que hereda de la clase abstracta Container.

    La pila permite agregar elementos al tope y eliminarlos desde el mismo lugar,
    manteniendo el comportamiento LIFO.

    Attributes:
        __len (int): Número de elementos en la pila.
        __head (Optional[BasicNode]): Nodo que apunta al tope de la pila.
    """

    def __init__(self) -> None:
        """
        Inicializa una pila vacía.
        """
        self.__len: int = 0
        self.__head: Optional[BasicNode] = None

    def size(self) -> int:
        """
        Obtiene el número de elementos en la pila.

        Returns:
            int: El número de elementos almacenados en la pila.
        """
        return self.__len

    def is_empty(self) -> bool:
        """
        Verifica si la pila está vacía.

        Returns:
            bool: True si la pila está vacía, False en caso contrario.
        """
        return self.__len == 0

    def push(self, value: Any) -> None:
        """
        Agrega un elemento al tope de la pila.

        Args:
            value (Any): El elemento que será agregado a la pila.
        """
        self.__head = BasicNode(value, self.__head)
        self.__len += 1

    def pop(self) -> Optional[Any]:
        """
        Elimina y devuelve el elemento al tope de la pila.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la pila está vacía.
        """
        if self.is_empty():
            return None

        assert self.__head is not None  # Garantiza que __head no sea None
        value = self.__head.value
        self.__head = self.__head.next
        self.__len -= 1
        return value

    def peek(self) -> Optional[Any]:
        """
        Devuelve el elemento al tope de la pila sin eliminarlo.

        Returns:
            Optional[Any]: El valor del elemento al tope, o None si la pila está vacía.
        """
        return self.__head.value if self.__head is not None else None

    def add(self, value: Any) -> None:
        """
        Alias para `push`. Agrega un elemento al tope de la pila.

        Args:
            value (Any): El elemento que será agregado a la pila.
        """
        return self.push(value)

    def get(self) -> Optional[Any]:
        """
        Alias para `pop`. Elimina y devuelve el elemento al tope de la pila.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la pila está vacía.
        """
        return self.pop()


class Graph:
    """
    Representa un grafo que contiene vértices y permite explorar sus adyacencias
    utilizando algoritmos de búsqueda (BFS y DFS) y direcciones.

    Inner Classes:
        Direction (Enum): Enumera las direcciones posibles para recorrer los vértices.
            - LEFT: Recorrido en orden inverso.
            - RIGHT: Recorrido en orden normal.

        Algorithm (Enum): Enumera los algoritmos de búsqueda disponibles.
            - BFS: Búsqueda en anchura.
            - DFS: Búsqueda en profundidad.

    Attributes:
        label (str): Etiqueta que identifica al grafo.
        vertexs (list[Vertex]): Lista de vértices que forman el grafo.
    """

    class Direction(Enum):
        """
        Enumera las direcciones posibles para recorrer los vértices.
        """

        LEFT = auto()
        RIGHT = auto()

    class Algorithm(Enum):
        """
        Enumera los algoritmos de búsqueda disponibles.
        """

        BFS = auto()  # Búsqueda en anchura
        DFS = auto()  # Búsqueda en profundidad

    def __init__(self, label: str, vertexs: Optional[list["Vertex"]] = None) -> None:
        """
        Inicializa un grafo con una etiqueta y una lista opcional de vértices.

        Args:
            label (str): Etiqueta que identifica al grafo.
            vertexs (Optional[list[Vertex]]): Lista de vértices que forman el grafo.
                                             Por defecto, es una lista vacía.
        """
        self.label = label
        self.vertexs = vertexs if vertexs else []

    def show_adjacencies(self) -> None:
        """
        Muestra las adyacencias de los vértices del grafo en la consola.
        """
        print(f"Adyacencias del árbol {self.label}:")
        for vertex in self.vertexs:
            print(f"{vertex} {vertex.etiqueta} -> {{")
            for adjacency in vertex.adjacencies:
                print(f"  {adjacency},")
            print("}")
        print()

    def reset_visited(self) -> None:
        """
        Reinicia el estado de visitado de todos los vértices del grafo.
        """
        for vertex in self.vertexs:
            vertex.visited = False

    def explore(
        self,
        start: "Vertex",
        search_type: "Graph.Algorithm",
        seek: Optional["Vertex"] = None,
        direction: "Graph.Direction" = Direction.RIGHT,
    ) -> Optional[int]:
        """
        Explora el grafo utilizando un algoritmo de búsqueda especificado y una dirección.

        Args:
            start (Vertex): Vértice desde donde se inicia la exploración.
            search_type (Graph.Algorithm): Tipo de algoritmo de búsqueda (BFS o DFS).
            seek (Optional[Vertex]): Vértice que se desea buscar. Si es None, realiza
                                      un recorrido completo.
            direction (Graph.Direction): Dirección en la que se recorrerán los adyacentes
                                         (LEFT o RIGHT). Por defecto, RIGHT.

        Returns:
            Optional[int]: Número de pasos para encontrar el vértice buscado, o None si
                           no se encuentra el vértice.
        """
        vertex_to_check: Container = (
            Stack() if search_type == self.Algorithm.DFS else Queue()
        )

        titulo = "Recorrido" if seek is None else f"Búsqueda a {seek}"
        print(
            f"{titulo} {search_type.name} por \n{direction.name} árbol {self.label}: {{"
        )

        steps = 0

        vertex_to_check.add(start)
        start.visited = True

        while not vertex_to_check.is_empty():
            curr_v: Optional[Vertex] = vertex_to_check.get()
            print(f"  {curr_v}")

            steps += 1

            assert curr_v is not None

            if seek is not None and seek == curr_v:
                print("}")
                print(f"Encontrado en: {steps} saltos\n")
                self.reset_visited()
                return steps

            if direction == self.Direction.RIGHT:
                adjacencies = curr_v.adjacencies
            else:
                adjacencies = list(reversed(curr_v.adjacencies))

            assert adjacencies is not None
            for neighbor in adjacencies:
                if not neighbor.visited:
                    vertex_to_check.add(neighbor)
                    neighbor.visited = True
        print("}")
        self.reset_visited()

        if seek is not None:
            print("NO SE ENCONTRÓ EL VÉRTICE\n")

        return None
