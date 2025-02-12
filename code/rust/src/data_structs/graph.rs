use std::{cell::RefCell, rc::Rc};

use crate::ds_components::vertexs::{Adjacency, Vertex};

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
    fn blind_search<T, A, Arg>(
        &self,
        algorithm: BlindSearch,
        direction: Direction,
        start: Vertex<T, A>,
        lvl_limit: usize,
        arg: Option<&mut Arg>,
        iterative: bool,
    ) where
        T: Clone,
        A: Adjacency<T>,
    {
    }
}
