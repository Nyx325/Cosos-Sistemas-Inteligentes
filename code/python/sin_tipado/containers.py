from typing import Any

from nodes import Node


class Container:
    """
    "Interfaz" que define el comportamiento
    de una estructura de datos en la que se puede
    almacenar y obtener elementos
    """

    def add(self, value) -> None:
        """
        Agregar un elemento al contenedor
        """
        raise NotImplementedError()

    def get(self) -> Any | None:
        """
        Eliminar un elemento al contenedor, devuelve
        None si está vacío
        """
        raise NotImplementedError()

    def peek(self) -> None:
        """
        Obtener el último valor del contenedor sin
        eliminar, devuelve None si está vacío
        """
        raise NotImplementedError()

    def size(self) -> int:
        """
        Devuelve el número de elementos dentro del
        contenedor
        """
        raise NotImplementedError()

    def empty(self) -> bool:
        """
        Indica si el contenedor está vacío
        """
        raise NotImplementedError()


class Queue(Container):
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

    def add(self, value) -> None:
        """
        Alias de enqueue. Agrega un elemento al final de la cola.
        """
        self.enqueue(value)

    def get(self) -> Any | None:
        """
        Alias de dequeue. Elimina y devuelve el elemento al inicio de la cola.
        """
        return self.dequeue()

    def peek(self) -> Any | None:
        """
        Devuelve el elemento al inicio de la cola sin eliminarlo.

        Returns:
            Any | None: Valor del primer elemento, o None si la cola está vacía.
        """
        return self._head.value if self._head else None


class Stack(Container):
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

    def add(self, value) -> None:
        """
        Alias de push. Agrega un elemento a la cima de la pila.
        """
        self.push(value)

    def get(self) -> Any | None:
        """
        Alias de pop. Elimina y devuelve el elemento en la cima de la pila.
        """
        return self.pop()

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
