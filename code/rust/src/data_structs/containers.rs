//! Módulo para implementar una pila (LIFO) con iteradores seguros usando Rc y RefCell

use crate::ds_components::nodes::{Node, NodeBuilder};
use std::{cell::RefCell, fmt::Display, rc::Rc};

/// Trait que define las operaciones básicas de un contenedor de elementos
///
/// # Type Parameters
/// - `T`: Tipo de elementos almacenados, debe implementar Clone
pub trait Container<T: Clone>: IntoIterator {
    /// Tipo del iterador asociado al contenedor
    type Iter: Iterator<Item = T>;

    /// Devuelve el número de elementos en el contenedor
    fn size(&self) -> usize;

    /// Verifica si el contenedor está vacío
    fn is_empty(&self) -> bool;

    /// Añade un elemento al contenedor
    fn add(&mut self, value: T);

    /// Remueve y devuelve un elemento del contenedor
    fn get(&mut self) -> Option<T>;

    /// Observa el próximo elemento a salir sin removerlo
    fn peek(&self) -> Option<T>;

    /// Devuelve un iterador Iterator<Item = T>
    fn iter(&self) -> Self::Iter;
}

/// Iterador para contenedores basados en nodos enlazados
///
/// # Comportamiento
/// - Recorre los elementos en orden LIFO (último en entrar, primero en salir)
/// - No consume el contenedor original
/// - Clona los valores durante la iteración
pub struct ContainerIter<T> {
    current: Option<Rc<RefCell<Node<T>>>>,
}

impl<T: Clone> Iterator for ContainerIter<T> {
    type Item = T;

    fn next(&mut self) -> Option<Self::Item> {
        // Obtener el nodo actual y mover el iterador al siguiente
        let current = self.current.take()?;
        let current_ref = current.borrow();
        let value = current_ref.value.clone();
        self.current = current_ref.next.as_ref().map(Rc::clone);
        Some(value)
    }
}

/// Implementación de pila (LIFO) usando nodos enlazados
///
/// # Características
/// - Tamaño dinámico
/// - Inserción y remoción en O(1)
/// - Iteración segura usando referencia contada (Rc) y mutabilidad interior (RefCell)
#[derive(Default, Debug, Clone)]
pub struct Stack<T> {
    /// Número de elementos en la pila
    size: usize,
    /// Nodo superior de la pila
    head: Option<Rc<RefCell<Node<T>>>>,
}

impl<T: Clone> Stack<T> {
    /// Crea una nueva pila vacía
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

    /// Añade un elemento a la parte superior de la pila
    ///
    /// # Argumentos
    /// - `value`: Valor a almacenar en la pila
    ///
    /// # Ejemplo
    /// ```
    /// let mut stack = Stack::new();
    /// stack.push(42);
    /// ```
    pub fn push(&mut self, value: T) {
        let new = NodeBuilder::new().value(value);

        let new = match &self.head {
            None => new,
            Some(node) => new.next(node.clone()),
        };

        self.head = Some(new.build());
        self.size += 1;
    }

    /// Remueve y devuelve el elemento superior de la pila
    ///
    /// # Retorno
    /// `Option<T>` - Some(value) si la pila no está vacía, None en caso contrario
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
    type Iter = ContainerIter<T>;

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

    fn iter(&self) -> Self::IntoIter {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}

/// Implementación de IntoIterator para conversión a iterador
///
/// # Comportamiento
/// - Consume la pila (move semantics)
/// - Mantiene los elementos originales a través de Rc
impl<T: Clone> IntoIterator for Stack<T> {
    type Item = T;
    type IntoIter = ContainerIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        ContainerIter {
            current: self.head.as_ref().map(Rc::clone),
        }
    }
}

impl<T: Display + Clone> Display for Stack<T> {
    /// Implementa la representación en cadena de la pila
    ///
    /// # Formato
    /// Los elementos se imprimen en orden LIFO (último en entrar, primero en salir),
    /// separados por comas y encerrados entre corchetes.
    ///
    /// # Ejemplo
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

        // Recorre la pila usando el iterador no consumidor
        for item in self.iter() {
            elements.push(format!("{}", item));
        }

        // Formatea los elementos como una lista separada por comas
        write!(f, "[{}]", elements.join(", "))
    }
}
