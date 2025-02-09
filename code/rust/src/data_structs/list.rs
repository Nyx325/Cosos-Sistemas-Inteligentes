use std::{
    cell::RefCell,
    rc::{Rc, Weak},
};

use crate::ds_components::nodes::Node;

pub struct LinkedList<T> {
    size: usize,
    head: Rc<RefCell<Node<T>>>,
    tail: Weak<RefCell<Node<T>>>,
}
