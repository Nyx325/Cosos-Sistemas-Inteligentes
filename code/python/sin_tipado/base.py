from typing import Any


class Node:
    """
    Representa un nodo en una estructura de datos enlazada.

    Atributos:
        value: El valor almacenado en el nodo.
        _next: Referencia al siguiente nodo en la estructura.
        _prev: Referencia al nodo anterior en la estructura.
    """

    def __init__(self, value, next=None, prev=None, label=None) -> None:
        self.value = value
        self._next = next
        self._prev = prev
        self.label = label

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del nodo.
        """
        return (
            f"({self.value})" if self.label is None else f"({self.label}:{self.value})"
        )


class Queue:
    """
    Implementación de una cola (FIFO) utilizando nodos doblemente enlazados.

    Attributes:
        _len: Número de elementos en la cola.
        _head: Nodo inicial de la cola.
        _tail: Nodo final de la cola.
    """

    def __init__(self) -> None:
        """
        Inicializa una cola vacía.
        """
        self._len = 0
        self._head = None
        self._tail = None

    def size(self) -> int:
        """
        Devuelve el número de elementos en la cola.

        Returns:
            int: Tamaño de la cola.
        """
        return self._len

    def empty(self) -> bool:
        """
        Indica si la cola está vacía.

        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return self.size() == 0

    def enqueue(self, value) -> None:
        """
        Agrega un elemento al final de la cola.

        Args:
            value: Valor a agregar.
        """
        new = Node(value)
        if self.empty():
            self._head = new
            self._tail = new
        else:
            assert self._tail is not None
            self._tail._next = new
            new._prev = self._tail
            self._tail = new
        self._len += 1

    def dequeue(self) -> Any | None:
        """
        Elimina y devuelve el elemento al inicio de la cola.

        Returns:
            Any | None: Valor eliminado, o None si la cola está vacía.
        """
        if self.empty():
            return None

        assert self._head is not None
        value = self._head.value

        self._head = self._head._next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None

        self._len -= 1
        return value

    def __str__(self) -> str:
        """
        Representa la cola como una cadena.

        Returns:
            str: Representación de los elementos de la cola.
        """
        values = []
        current = self._head
        while current:
            values.append(str(current.value))
            current = current._next
        return f"Queue[{', '.join(values)}]"

    def peek(self) -> Any | None:
        """
        Devuelve el elemento al inicio de la cola sin eliminarlo.

        Returns:
            Any | None: Valor del primer elemento, o None si la cola está vacía.
        """
        return self._head.value if self._head else None


class Stack:
    """
    Implementación de una pila (LIFO) utilizando nodos doblemente enlazados.

    Attributes:
        __len: Número de elementos en la pila.
        __head: Nodo en la parte superior de la pila.
    """

    def __init__(self) -> None:
        """
        Inicializa una pila vacía.
        """
        self.__len = 0
        self.__head = None

    def size(self) -> int:
        """
        Devuelve el número de elementos en la pila.

        Returns:
            int: Tamaño de la pila.
        """
        return self.__len

    def empty(self) -> bool:
        """
        Indica si la pila está vacía.

        Returns:
            bool: True si la pila está vacía, False en caso contrario.
        """
        return self.__len == 0

    def push(self, value) -> None:
        """
        Agrega un elemento a la cima de la pila.

        Args:
            value: Valor a agregar.
        """
        new_node = Node(value, self.__head)
        if self.__head:
            self.__head._prev = new_node
        self.__head = new_node
        self.__len += 1

    def pop(self) -> Any | None:
        """
        Elimina y devuelve el elemento en la cima de la pila.

        Returns:
            Any | None: Valor eliminado, o None si la pila está vacía.
        """
        if self.empty():
            return None

        assert self.__head is not None
        value = self.__head.value
        self.__head = self.__head._next
        if self.__head:
            self.__head.prev = None
        self.__len -= 1
        return value

    def peek(self) -> Any | None:
        """
        Devuelve el elemento en la cima de la pila sin eliminarlo.

        Returns:
            Any | None: Valor del elemento superior, o None si la pila está vacía.
        """
        return self.__head.value if self.__head else None

    def __str__(self) -> str:
        """
        Representa la pila como una cadena.

        Returns:
            str: Representación de los elementos de la pila.
        """
        values = []
        current = self.__head
        while current:
            values.append(str(current.value))
            current = current._next
        return f"Stack[{', '.join(values)}]"
