use crate::ds_components::nodes::Node;
use std::{
    cell::RefCell,
    fmt::Display,
    rc::{Rc, Weak},
};

/// Trait que define las operaciones básicas de un contenedor de elementos.
///
/// # Parámetros de Tipo
/// - `T`: Tipo de los elementos almacenados, que debe implementar `Clone`.
pub trait Container<T>
where
    T: Clone,
{
    /// Devuelve el número de elementos almacenados en el contenedor.
    fn size(&self) -> usize;

    /// Verifica si el contenedor está vacío.
    fn is_empty(&self) -> bool;

    /// Añade un elemento al contenedor.
    fn add(&mut self, value: T);

    /// Remueve y devuelve el siguiente elemento según la semántica del contenedor.
    ///
    /// Por ejemplo, en una pila se remueve el último elemento insertado (LIFO),
    /// mientras que en una cola se remueve el primer elemento insertado (FIFO).
    fn get(&mut self) -> Option<T>;

    /// Devuelve el próximo elemento a salir sin removerlo.
    fn peek(&self) -> Option<T>;

    /// Retorna un iterador que recorre los elementos del contenedor.
    fn iter(&self) -> ContainerIter<T>;
}

impl<T> Display for dyn Container<T>
where
    T: Display + Clone,
{
    /// Implementa la representación en cadena de un contenedor.
    ///
    /// # Formato
    /// Los elementos se imprimen en el orden en que los recorre el iterador del contenedor.
    /// Por ejemplo, para una pila se mostrarán en orden LIFO y para una cola en orden FIFO.
    ///
    /// # Ejemplo
    /// Para una pila:
    /// ```
    /// let mut stack = Stack::new();
    /// stack.push(1);
    /// stack.push(2);
    /// stack.push(3);
    ///
    /// assert_eq!(format!("{}", stack), "[3, 2, 1]");
    /// ```
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut elements = Vec::new();

        // Recorre el contenedor usando su iterador
        for item in self.iter() {
            elements.push(format!("{}", item));
        }

        // Formatea los elementos como una lista separada por comas
        write!(f, "[{}]", elements.join(", "))
    }
}

/// Iterador para contenedores basados en nodos enlazados.
///
/// # Comportamiento
/// - Recorre los elementos en el orden en que están enlazados en el contenedor.
///   Dependiendo de la estructura interna, este orden puede ser LIFO (como en una pila)
///   o FIFO (como en una cola).
/// - No consume el contenedor original.
/// - Clona los valores durante la iteración.
pub struct ContainerIter<T> {
    current: Option<Rc<RefCell<Node<T>>>>,
}

impl<T> Iterator for ContainerIter<T>
where
    T: Clone,
{
    type Item = T;

    fn next(&mut self) -> Option<Self::Item> {
        // Obtiene el nodo actual y avanza el iterador al siguiente nodo
        let current = self.current.take()?;
        let current_ref = current.borrow();
        let value = current_ref.value.clone();
        self.current = current_ref.next.as_ref().map(Rc::clone);
        Some(value)
    }
}

/// Implementación de una pila (LIFO) usando nodos enlazados.
///
/// # Características
/// - Tamaño dinámico.
/// - Inserción y remoción en O(1).
/// - Iteración mediante referencia contada (`Rc`) y mutabilidad interior (`RefCell`).
#[derive(Default, Debug, Clone)]
pub struct Stack<T> {
    /// Número de elementos en la pila.
    size: usize,
    /// Nodo superior de la pila.
    head: Option<Rc<RefCell<Node<T>>>>,
}

impl<T> Stack<T>
where
    T: Clone,
{
    /// Crea una nueva pila vacía.
    ///
    /// # Ejemplo
    /// ```
    /// let stack: Stack<i32> = Stack::new();
    /// ```
    pub fn new() -> Stack<T> {
        Stack {
            size: 0,
            head: None,
        }
    }

    /// Añade un elemento a la parte superior de la pila.
    ///
    /// # Argumentos
    /// - `value`: Valor a almacenar en la pila.
    ///
    /// # Ejemplo
    /// ```
    /// let mut stack = Stack::new();
    /// stack.push(42);
    /// ```
    pub fn push(&mut self, value: T) {
        let new = Node::new(value);

        if let Some(node) = &self.head {
            new.borrow_mut().next = Some(Rc::clone(node));
        }

        self.head = Some(new);
        self.size += 1;
    }

    /// Remueve y devuelve el elemento superior de la pila.
    ///
    /// # Retorno
    /// - `Some(T)` si la pila no está vacía.
    /// - `None` si la pila está vacía.
    ///
    /// # Ejemplo
    /// ```
    /// let mut stack = Stack::new();
    /// stack.push(42);
    /// assert_eq!(stack.pop(), Some(42));
    /// ```
    pub fn pop(&mut self) -> Option<T> {
        let head = self.head.take()?;
        let mut head_ref = head.borrow_mut();

        let value = head_ref.value.clone();
        self.head = head_ref.next.take();
        self.size -= 1;

        Some(value)
    }
}

impl<T: Clone> Container<T> for Stack<T> {
    fn add(&mut self, value: T) {
        self.push(value);
    }

    fn get(&mut self) -> Option<T> {
        self.pop()
    }

    fn peek(&self) -> Option<T> {
        self.head.as_ref().map(|node| node.borrow().value.clone())
    }

    fn size(&self) -> usize {
        self.size
    }

    fn is_empty(&self) -> bool {
        self.size == 0
    }

    fn iter(&self) -> ContainerIter<T> {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}

/// Implementación de `IntoIterator` para la pila.
///
/// Convierte la pila en un iterador que recorre sus elementos en orden LIFO.
/// Dado que los nodos se gestionan mediante `Rc`, se clona la referencia al nodo
/// inicial para crear el iterador.
impl<T> IntoIterator for Stack<T>
where
    T: Clone,
{
    type Item = T;
    type IntoIter = ContainerIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}

/// Estructura que representa una cola FIFO.
///
/// # Campos
/// - `size`: Número de elementos en la cola.
/// - `head`: Referencia al primer elemento de la cola (el siguiente en salir).
/// - `tail`: Referencia débil al último elemento de la cola (el último en entrar).
///
/// # Notas de Implementación
/// - Los nodos se gestionan con `Rc<RefCell<...>>` para permitir mutabilidad compartida.
/// - La derivación de `Clone` realiza una copia superficial, por lo que varias instancias
///   pueden compartir los mismos nodos. Modificar una cola afectará a sus clones.
#[derive(Default, Debug, Clone)]
pub struct Queue<T: Clone> {
    size: usize,
    head: Option<Rc<RefCell<Node<T>>>>,
    tail: Option<Weak<RefCell<Node<T>>>>,
}

impl<T: Clone> Queue<T> {
    /// Crea una nueva cola vacía.
    pub fn new() -> Self {
        Queue {
            size: 0,
            head: None,
            tail: None,
        }
    }

    /// Añade un elemento al final de la cola.
    ///
    /// # Argumentos
    /// - `value`: Valor a añadir.
    ///
    /// # Comportamiento
    /// - Si la cola está vacía, actualiza tanto `head` como `tail`.
    /// - Si no está vacía, enlaza el nodo referenciado por `tail` con el nuevo nodo.
    ///
    /// # Advertencia
    /// - Si la referencia débil (`tail`) no puede actualizarse (por ejemplo, si el nodo
    ///   anterior ya no existe), el enlace al nuevo nodo no se realiza.
    pub fn enqueue(&mut self, value: T) {
        let new_node = Node::new(value);

        match self.tail.take() {
            None => self.head = Some(Rc::clone(&new_node)),
            Some(old_tail_weak) => {
                if let Some(old_tail_rc) = old_tail_weak.upgrade() {
                    old_tail_rc.borrow_mut().next = Some(Rc::clone(&new_node));
                }
            }
        }

        self.tail = Some(Rc::downgrade(&new_node));
        self.size += 1;
    }

    /// Remueve y devuelve el primer elemento de la cola (FIFO).
    ///
    /// # Retorno
    /// - `Some(T)` si la cola no está vacía.
    /// - `None` si la cola está vacía.
    pub fn dequeue(&mut self) -> Option<T> {
        let head = self.head.take()?;
        let mut head_ref = head.borrow_mut();

        let value = head_ref.value.clone();
        self.head = head_ref.next.take();
        if self.head.is_none() {
            self.tail = None;
        }

        self.size -= 1;
        Some(value)
    }
}

impl<T: Clone> Container<T> for Queue<T> {
    fn add(&mut self, value: T) {
        self.enqueue(value);
    }

    fn get(&mut self) -> Option<T> {
        self.dequeue()
    }

    fn peek(&self) -> Option<T> {
        self.head.as_ref().map(|node| node.borrow().value.clone())
    }

    fn size(&self) -> usize {
        self.size
    }

    fn is_empty(&self) -> bool {
        self.size == 0
    }

    fn iter(&self) -> ContainerIter<T> {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}

/// Implementación de `IntoIterator` para la cola.
///
/// Convierte la cola en un iterador que recorre sus elementos en orden FIFO.
/// Se aprovechan las referencias compartidas (`Rc`) para crear el iterador sin modificar
/// la estructura interna de la cola.
impl<T: Clone> IntoIterator for Queue<T> {
    type Item = T;
    type IntoIter = ContainerIter<T>;

    /// Convierte la cola en un iterador FIFO.
    ///
    /// # Ejemplo
    /// ```
    /// let mut queue = Queue::new();
    /// queue.enqueue(1);
    /// queue.enqueue(2);
    ///
    /// let items: Vec<_> = queue.into_iter().collect();
    /// assert_eq!(items, vec![1, 2]);
    /// ```
    fn into_iter(self) -> Self::IntoIter {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}
