use std::cell::RefCell;
use std::fmt;
use std::rc::{Rc, Weak};

#[derive(Debug, Default, Clone)]
pub struct Node<T> {
    pub value: T,
    pub next: Option<Rc<RefCell<Node<T>>>>,
    pub prev: Option<Weak<RefCell<Node<T>>>>,
}

impl<T: fmt::Display> fmt::Display for Node<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({})", self.value)
    }
}

#[derive(Debug, Clone, Default)]
pub struct NoValue;
#[derive(Debug, Clone, Default)]
pub struct Value<T>(T);

pub struct NodeBuilder<T, V> {
    pub value: V,
    pub next: Option<Rc<RefCell<Node<T>>>>,
    pub prev: Option<Weak<RefCell<Node<T>>>>,
}

impl<T> NodeBuilder<T, NoValue> {
    pub fn new() -> NodeBuilder<T, NoValue> {
        NodeBuilder {
            value: NoValue::default(),
            next: None,
            prev: None,
        }
    }
}

impl<T> NodeBuilder<T, Value<T>> {
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
    pub fn value(self, value: T) -> NodeBuilder<T, Value<T>> {
        NodeBuilder {
            value: Value(value),
            next: self.next,
            prev: self.prev,
        }
    }

    pub fn next(self, next: Rc<RefCell<Node<T>>>) -> NodeBuilder<T, V> {
        NodeBuilder {
            value: self.value,
            next: Some(next),
            prev: self.prev,
        }
    }

    pub fn prev(self, prev: Weak<RefCell<Node<T>>>) -> NodeBuilder<T, V> {
        NodeBuilder {
            value: self.value,
            next: self.next,
            prev: Some(prev),
        }
    }
}
