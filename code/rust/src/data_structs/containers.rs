use std::{cell::RefCell, rc::Rc, usize};

use crate::ds_components::nodes::{Node, NodeBuilder};

pub trait Container<T: Clone> {
    fn size(&self) -> usize;
    fn is_empty(&self) -> bool;
    fn add(&mut self, value: T);
    fn get(&mut self) -> Option<T>;
    fn peek(&self) -> Option<T>;
}

#[derive(Default, Debug, Clone)]
pub struct Stack<T> {
    size: usize,
    head: Option<Rc<RefCell<Node<T>>>>,
}

impl<T: Clone> Stack<T> {
    pub fn new() -> Stack<T> {
        Stack {
            size: 0,
            head: None,
        }
    }

    pub fn push(&mut self, value: T) {
        let new = NodeBuilder::new().value(value);

        let new = match &self.head {
            None => new,
            Some(node) => new.next(node.clone()),
        };

        self.head = Some(new.build());
        self.size += 1
    }

    pub fn pop(&mut self) -> Option<T> {
        let head = self.head.take()?;
        let mut head_ref = head.borrow_mut();

        let value = head_ref.value.clone();
        self.head = head_ref.next.take();
        self.size -= 1;

        Some(value)
    }

    pub fn iter(&self) -> StackIter<T> {
        StackIter {
            current: self.head.as_ref().map(Rc::clone),
        }
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
        match &self.head {
            None => None,
            Some(node) => Some(node.borrow().value.clone()),
        }
    }

    fn size(&self) -> usize {
        self.size
    }

    fn is_empty(&self) -> bool {
        self.size == 0
    }
}

pub struct StackIter<T> {
    current: Option<Rc<RefCell<Node<T>>>>,
}

impl<T: Clone> Iterator for StackIter<T> {
    type Item = T;

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.current.take()?;
        let current_ref = current.borrow();
        let value = current_ref.value.clone();
        self.current = current_ref.next.as_ref().map(Rc::clone);
        Some(value)
    }
}
