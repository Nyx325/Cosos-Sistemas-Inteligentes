from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from nodes import DoubleLinkedNode

T = TypeVar("T")


class Container(Generic[T], ABC):
    """
    Generalización de una estructura de datos abstracta que permite almacenar y
    recuperar elementos.

    Esta clase sirve como base para implementar diferentes estructuras de datos
    (como pilas, colas, etc.) y define los métodos abstractos que dichas
    estructuras deben implementar.
    """

    @abstractmethod
    def add(self, value: T) -> None:
        """
        Agrega un elemento al contenedor.

        Args:
            value (Any): El elemento que será agregado al contenedor.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Optional[T]:
        """
        Recupera y elimina un elemento del contenedor.

        Returns:
            Optional[Any]: El elemento recuperado, o None si el contenedor está vacío.

        Raises:
            NotImplementedError: Este método debe ser implementado por una subclase.
        """
        raise NotImplementedError()

    @abstractmethod
    def peek(self) -> Optional[T]:
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


class Queue(Generic[T], Container[T]):
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
        self._head: Optional[DoubleLinkedNode] = None
        self._tail: Optional[DoubleLinkedNode] = None

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

    def enqueue(self, value: T) -> None:
        """
        Agrega un elemento al final de la cola.

        Args:
            value (Any): El elemento que será agregado a la cola.
        """
        new = DoubleLinkedNode(value)
        if self.is_empty():
            self._head = new
            self._tail = new
        else:
            assert self._tail is not None
            self._tail.next = new
            self._tail = new
        self._len += 1

    def dequeue(self) -> Optional[T]:
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
            values.append(str(node.value))
            node = node.next

        return str(values)

    def add(self, value: T) -> None:
        """
        Alias para `enqueue`. Agrega un elemento al final de la cola.

        Args:
            value (Any): El elemento que será agregado a la cola.
        """
        return self.enqueue(value)

    def get(self) -> Optional[T]:
        """
        Alias para `dequeue`. Elimina y devuelve el elemento al inicio de la cola.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la cola está vacía.
        """
        return self.dequeue()

    def peek(self) -> Optional[T]:
        """
        Devuelve el elemento al inicio de la cola sin eliminarlo.

        Returns:
            Optional[Any]: El valor del elemento al inicio, o None si la cola está vacía.
        """
        return self._head.value if self._head else None


class Stack(Generic[T], Container[T]):
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
        self.__head: Optional[DoubleLinkedNode] = None

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

    def push(self, value: T) -> None:
        """
        Agrega un elemento al tope de la pila.

        Args:
            value (Any): El elemento que será agregado a la pila.
        """
        self.__head = DoubleLinkedNode(value, self.__head)
        self.__len += 1

    def pop(self) -> Optional[T]:
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

    def peek(self) -> Optional[T]:
        """
        Devuelve el elemento al tope de la pila sin eliminarlo.

        Returns:
            Optional[Any]: El valor del elemento al tope, o None si la pila está vacía.
        """
        return self.__head.value if self.__head is not None else None

    def add(self, value: T) -> None:
        """
        Alias para `push`. Agrega un elemento al tope de la pila.

        Args:
            value (Any): El elemento que será agregado a la pila.
        """
        return self.push(value)

    def get(self) -> Optional[T]:
        """
        Alias para `pop`. Elimina y devuelve el elemento al tope de la pila.

        Returns:
            Optional[Any]: El valor del elemento eliminado, o None si la pila está vacía.
        """
        return self.pop()

    def __str__(self) -> str:
        """
        Representa la pila como una cadena con los valores almacenados.

        Returns:
            str: Una representación en cadena de los elementos de la cola en orden.
        """
        node = self.__head
        values = []
        while node is not None:
            values.append(str(node.value))
            node = node.next

        return str(values)
