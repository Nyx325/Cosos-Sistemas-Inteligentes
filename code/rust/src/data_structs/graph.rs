use std::{cell::RefCell, rc::Rc};

pub enum Direction {
    Left,
    Right,
}

pub enum BlindSearch {
    BreadthFirstSearch,
    DepthFirstSearch,
}

pub enum HeuristicSearch {
    AStar,
    HillClimbing,
}

pub trait Graph<V> {
    fn new(label: impl Into<String>, vertexs: &[Rc<RefCell<V>>]) -> Self;
    fn get(&self, index: usize) -> Option<Rc<RefCell<V>>>;
}
