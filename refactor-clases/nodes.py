from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar


class Node(ABC):
    """
    Clase base abstracta para nodos en estructuras de datos.

    Proporciona la funcionalidad básica común a diferentes tipos de nodos,
    incluyendo grafos y árboles.

    Attributes:
        value (Any): Valor almacenado en el nodo
        visited (bool): Indicador de visita para algoritmos de recorrido
            (valor por defecto: False)
    """

    def __init__(self, value: Any) -> None:
        """
        Inicializa un nodo con valor y estado no visitado.

        Args:
            value (Any): Valor a almacenar en el nodo
        """
        super().__init__()
        self.value = value
        self.visited = False

    def __str__(self) -> str:
        """
        Representación en cadena del nodo.

        Returns:
            str: Cadena en formato '(valor)' donde valor es el contenido del nodo
        """
        return f"({self.value})"


Adjacency = TypeVar("Adjacency")


class Vertex(Node, Generic[Adjacency], ABC):
    """
    Clase abstracta base para vértices en grafos con sistema de adyacencias tipado.

    Define la interfaz común para vértices en diferentes tipos de grafos mediante
    el uso de tipos genéricos para las adyacencias.

    Attributes:
        adjacencies (list[Adjacency]): Lista de elementos de adyacencia cuyo tipo
            concreto se define en las subclases

    Type Parameters:
        Adjacency (TypeVar): Tipo genérico que debe ser subtipo de Vertex.
            Define el tipo de elementos en la lista de adyacencias.
    """

    def __init__(
        self, value: Any, adjacencies: Optional[list[Adjacency]] = None
    ) -> None:
        """
        Inicializa un vértice con valor y adyacencias opcionales.

        Args:
            value (Any): Valor identificador del vértice
            adjacencies (Optional[list[Adjacency]]): Lista inicial de elementos
                de adyacencia (por defecto: lista vacía)
        """
        super().__init__(value)
        self.adjacencies: list[Adjacency] = adjacencies if adjacencies else []

    @abstractmethod
    def append(self, *adjacencies: Adjacency) -> None:
        """
        Método abstracto para añadir elementos a las adyacencias.

        Args:
            *adjacencies (Adjacency): Uno o más elementos de adyacencia a agregar

        Raises:
            NotImplementedError: Si no se implementa en subclase concreta
        """
        for vertex in adjacencies:
            self.adjacencies.append(vertex)

    @abstractmethod
    def get(self, index: int) -> Optional[Adjacency]:
        """
        Método abstracto para obtener un elemento de adyacencia por índice.

        Args:
            index (int): Posición en la lista de adyacencias (basado en 0)

        Returns:
            Optional[Adjacency]: Elemento en la posición solicitada o None si
            el índice es inválido

        Raises:
            NotImplementedError: Si no se implementa en subclase concreta
        """
        if index < 0 or index >= len(self.adjacencies):
            return None

        return self.adjacencies[index]

    # Ejemplo de documentación para implementaciones concretas
    class ExampleUsage:
        """
        Ejemplos de implementación para diferentes tipos de grafos:

        1. Grafo no ponderado:
        ```python
        class Vertex(Vertex['Vertex']):
            def append(self, *adjacencies: 'Vertex') -> None:
                self.adjacencies.extend(adjacencies)

            def get(self, index: int) -> Optional['Vertex']:
                try:
                    return self.adjacencies[index]
                except IndexError:
                    return None
        ```

        2. Grafo ponderado:
        ```python
        class WeightedVertex(Vertex[tuple['WeightedVertex', float]]):
            def append(self, *adjacencies: tuple['WeightedVertex', float]) -> None:
                self.adjacencies.extend(adjacencies)

            def get(self, index: int) -> Optional[tuple['WeightedVertex', float]]:
                try:
                    return self.adjacencies[index]
                except IndexError:
                    return None
        ```
        """


class DoubleLinkedNode(Node):
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
        next: Optional["DoubleLinkedNode"] = None,
        prev: Optional["DoubleLinkedNode"] = None,
    ) -> None:
        """
        Args:
            value (Any): El valor que será almacenado en el nodo.
            next (Optional[BasicNode]): El siguiente nodo en la lista, o None si no hay uno.
            prev (Optional[BasicNode]): El nodo previo en la lista, o None si no hay uno.
        """
        super().__init__(value)
        self.next: Optional[DoubleLinkedNode] = next
        self.prev: Optional[DoubleLinkedNode] = prev


class NonWeightedVertex(Vertex["NonWeightedVertex"]):
    """
    Implementación concreta de vértice para grafos no ponderados.

    Hereda de Vertex especificando que las adyacencias son otros vértices del mismo tipo
    sin pesos asociados.

    Attributes:
        value (Any): Valor almacenado en el vértice (heredado de Node)
        adjacencies (list[NonWeightedVertex]): Lista de vértices adyacentes directos
        visited (bool): Estado de visita (heredado de Node)
    """

    def __init__(
        self,
        value: Any,
        adjacencies: Optional[list["NonWeightedVertex"]] = None,
    ) -> None:
        """
        Inicializa un vértice no ponderado con valor y adyacencias opcionales.

        Args:
            value (Any): Identificador único del vértice
            adjacencies (Optional[list[NonWeightedVertex]]): Lista inicial de
                vértices adyacentes (por defecto: lista vacía)
        """
        super().__init__(value, adjacencies)

    def append(self, *adjacencies: "NonWeightedVertex") -> None:
        """
        Añade uno o más vértices a las adyacencias.

        Args:
            *adjacencies (NonWeightedVertex): Vértices a agregar como adyacentes

        Raises:
            TypeError: Si se intenta agregar un tipo que no es NonWeightedVertex
        """
        return super().append(*adjacencies)

    def get(self, index: int) -> Optional["NonWeightedVertex"]:
        """
        Recupera un vértice adyacente por posición en la lista.

        Args:
            index (int): Posición en la lista de adyacencias (basado en 0)

        Returns:
            Optional[NonWeightedVertex]: Vértice en la posición solicitada o
            None si el índice es inválido
        """
        return super().get(index)


class WeightedVertex(Vertex[tuple["WeightedVertex", float]]):
    """
    Implementación concreta de vértice para grafos ponderados.

    Hereda de Vertex especificando que las adyacencias son tuplas que contienen:
    (vértice adyacente, peso de la arista).

    Attributes:
        value (Any): Valor almacenado en el vértice (heredado de Node)
        adjacencies (list[tuple[WeightedVertex, float]]): Lista de adyacencias
            con pesos en formato (vértice, peso)
        visited (bool): Estado de visita (heredado de Node)
    """

    def __init__(
        self,
        value: Any,
        adjacencies: Optional[list[tuple["WeightedVertex", float]]] = None,
    ) -> None:
        """
        Inicializa un vértice ponderado con valor y adyacencias opcionales.

        Args:
            value (Any): Identificador único del vértice
            adjacencies (Optional[list[tuple[WeightedVertex, float]]]): Lista
                inicial de adyacencias con pesos (por defecto: lista vacía)
        """
        super().__init__(value, adjacencies)

    def append(
        self,
        *adjacencies: tuple["WeightedVertex", float],
    ) -> None:
        """
        Añade una o más adyacencias con peso.

        Args:
            *adjacencies (tuple[WeightedVertex, float]): Tuplas conteniendo:
                - WeightedVertex: Vértice adyacente
                - float: Peso de la conexión

        Raises:
            TypeError: Si algún elemento no es una tupla válida
        """
        return super().append(*adjacencies)

    def get(self, index: int) -> Optional[tuple["WeightedVertex", float]]:
        """
        Recupera una adyacencia ponderada por posición en la lista.

        Args:
            index (int): Posición en la lista de adyacencias (basado en 0)

        Returns:
            Optional[tuple[WeightedVertex, float]]: Tupla (vértice, peso) en
            la posición solicitada o None si el índice es inválido
        """
        return super().get(index)
