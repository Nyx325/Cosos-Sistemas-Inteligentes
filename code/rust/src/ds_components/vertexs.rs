use std::{cell::RefCell, rc::Rc};

pub trait Vertex {
    type Item: Clone;
    type Adjacency;

    fn value(&self) -> Self::Item;
    fn adjacencies(&self) -> impl Iterator<Item = Self::Adjacency> + '_;

    fn append(&mut self, adjacencies: &[Self::Adjacency]);
    fn get(&self, index: usize) -> Option<Self::Adjacency>;
}

pub trait GraphSearchVertex {
    fn visited(&self) -> bool;
    fn lvl(&self) -> usize;
}

pub struct NonWeightedVertex<T>
where
    T: Clone,
{
    pub value: T,
    adjacencies: Vec<Rc<RefCell<NonWeightedVertex<T>>>>,
}

impl<T> NonWeightedVertex<T>
where
    T: Clone,
{
    pub fn new(value: T) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            value,
            adjacencies: Vec::new(),
        }))
    }
}

impl<T> Vertex for NonWeightedVertex<T>
where
    T: Clone,
{
    type Item = T;
    type Adjacency = Rc<RefCell<NonWeightedVertex<T>>>;

    fn value(&self) -> Self::Item {
        self.value.clone()
    }

    fn adjacencies(&self) -> impl Iterator<Item = Self::Adjacency> + '_ {
        self.adjacencies.iter().cloned()
    }

    fn get(&self, index: usize) -> Option<Self::Adjacency> {
        self.adjacencies.get(index).cloned()
    }

    fn append(&mut self, adjacencies: &[Self::Adjacency]) {
        for v in adjacencies {
            if !self.adjacencies.iter().any(|a| Rc::ptr_eq(a, v)) {
                self.adjacencies.push(Rc::clone(v));
            }
        }
    }
}
