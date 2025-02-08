//! Módulo para implementar una lista doblemente enlazada usando Rc y RefCell

use std::cell::RefCell;
use std::fmt;
use std::rc::{Rc, Weak};

/// Nodo de una lista doblemente enlazada
///
/// # Campos
/// - `value`: Valor almacenado en el nodo (genérico)
/// - `next`: Referencia al siguiente nodo (fuertemente tipada con Rc)
/// - `prev`: Referencia al nodo anterior (débilmente tipada con Weak)
#[derive(Debug, Default, Clone)]
pub struct Node<T> {
    /// Valor almacenado en el nodo
    pub value: T,

    /// Referencia al siguiente nodo en la lista
    ///
    /// Usa `Rc<RefCell<...>>` para permitir:
    /// - Múltiples propietarios
    /// - Mutabilidad interior
    pub next: Option<Rc<RefCell<Node<T>>>>,

    /// Referencia al nodo anterior en la lista
    ///
    /// Usa `Weak<RefCell<...>>` para:
    /// - Evitar ciclos de referencia
    /// - Permitir la liberación de memoria
    pub prev: Option<Weak<RefCell<Node<T>>>>,
}

impl<T: fmt::Display> fmt::Display for Node<T> {
    /// Implementa la representación en cadena del nodo
    ///
    /// # Ejemplo
    /// ```
    /// let node = Node { value: 42, next: None, prev: None };
    /// assert_eq!(format!("{}", node), "(42)");
    /// ```
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({})", self.value)
    }
}

/// Estado de valor no definido para el patrón Builder
#[derive(Debug, Clone, Default)]
pub struct NoValue;

/// Contenedor para el valor definido del nodo
#[derive(Debug, Clone, Default)]
pub struct Value<T>(T);

/// Builder para crear nodos de forma segura y escalonada
///
/// # Tipos genéricos
/// - `T`: Tipo del valor almacenado en el nodo
/// - `V`: Tipo de estado del valor (NoValue | Value<T>)
///
/// # Patrón de diseño
/// Usa el patrón Builder con tipos fantasma para garantizar:
/// - Asignación obligatoria del valor
/// - Configuración flexible de referencias
pub struct NodeBuilder<T, V> {
    /// Valor del nodo (en estado NoValue o Value<T>)
    pub value: V,

    /// Referencia al siguiente nodo
    pub next: Option<Rc<RefCell<Node<T>>>>,

    /// Referencia al nodo anterior
    pub prev: Option<Weak<RefCell<Node<T>>>>,
}

impl<T> NodeBuilder<T, NoValue> {
    /// Crea un nuevo NodeBuilder en estado inicial (sin valor)
    ///
    /// # Ejemplo
    /// ```
    /// let builder = NodeBuilder::<i32, _>::new();
    /// ```
    pub fn new() -> NodeBuilder<T, NoValue> {
        NodeBuilder {
            value: NoValue::default(),
            next: None,
            prev: None,
        }
    }
}

impl<T> NodeBuilder<T, Value<T>> {
    /// Construye el nodo final consumiendo el Builder
    ///
    /// # Retorno
    /// `Rc<RefCell<Node<T>>>` - Nodo listo para usar en la lista
    ///
    /// # Ejemplo
    /// ```
    /// let node = NodeBuilder::new()
    ///     .value(42)
    ///     .build();
    /// ```
    pub fn build(self) -> Rc<RefCell<Node<T>>> {
        let node = Node {
            value: self.value.0,
            next: self.next,
            prev: self.prev,
        };

        Rc::new(RefCell::new(node))
    }
}

impl<T, V> NodeBuilder<T, V> {
    /// Establece el valor del nodo
    ///
    /// # Argumentos
    /// - `value`: Valor a almacenar en el nodo
    ///
    /// # Ejemplo
    /// ```
    /// let builder = NodeBuilder::new().value(42);
    /// ```
    pub fn value(self, value: T) -> NodeBuilder<T, Value<T>> {
        NodeBuilder {
            value: Value(value),
            next: self.next,
            prev: self.prev,
        }
    }

    /// Establece la referencia al siguiente nodo
    ///
    /// # Argumentos
    /// - `next`: Referencia al siguiente nodo (Rc<RefCell<Node<T>>>)
    ///
    /// # Nota
    /// Esta implementación no actualiza automáticamente la referencia
    /// `prev` del nodo siguiente.
    ///
    /// # Ejemplo
    /// ```
    /// let node1 = NodeBuilder::new().value(1).build();
    /// let node2 = NodeBuilder::new().value(2).next(node1).build();
    /// ```
    pub fn next(self, next: Rc<RefCell<Node<T>>>) -> NodeBuilder<T, V> {
        NodeBuilder {
            value: self.value,
            next: Some(next),
            prev: self.prev,
        }
    }

    /// Establece la referencia al nodo anterior
    ///
    /// # Argumentos
    /// - `prev`: Referencia débil al nodo anterior (Weak<RefCell<Node<T>>>)
    ///
    /// # Ejemplo
    /// ```
    /// let node1 = NodeBuilder::new().value(1).build();
    /// let node2 = NodeBuilder::new()
    ///     .value(2)
    ///     .prev(Rc::downgrade(&node1))
    ///     .build();
    /// ```
    pub fn prev(self, prev: Weak<RefCell<Node<T>>>) -> NodeBuilder<T, V> {
        NodeBuilder {
            value: self.value,
            next: self.next,
            prev: Some(prev),
        }
    }
}

/// Ejemplo básico de uso
///
/// # Nota
/// Esta implementación no mantiene automáticamente la consistencia
/// bidireccional de los enlaces entre nodos.
pub fn example_usage() {
    // Crear nodo base
    let node = NodeBuilder::new().value(1).build();

    // Crear segundo nodo enlazado al primero
    let node2 = NodeBuilder::new().value(2).next(node).build();

    // Crear tercer nodo con referencia al segundo
    let _node3 = NodeBuilder::new().value(3).prev(Rc::downgrade(&node2));
}
