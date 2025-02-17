use std::{collections::HashSet, fmt::Debug};

use crate::{
    data_structs::containers::{Container, Queue, Stack},
    ds_components::vertexs::{Adjacency, VertexInstance, VertexWrapper},
};

pub enum Direction {
    Left,
    Right,
}

impl std::fmt::Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Left => write!(f, "Izquierda"),
            Self::Right => write!(f, "Derecha"),
        }
    }
}

pub enum BlindSearch {
    BreadthFirstSearch,
    DepthFirstSearch,
}

impl std::fmt::Display for BlindSearch {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::BreadthFirstSearch => write!(f, "BFS"),
            Self::DepthFirstSearch => write!(f, "DFS"),
        }
    }
}

pub enum HeuristicSearch {
    AStar,
    HillClimbing,
}

impl std::fmt::Display for HeuristicSearch {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::AStar => write!(f, "A*"),
            Self::HillClimbing => write!(f, "HillClimbing"),
        }
    }
}

pub struct Graph<T, A>
where
    T: Clone,
    A: Adjacency<T>,
{
    pub label: String,
    vertexs: Vec<VertexInstance<T, A>>,
}

impl<T, A> Graph<T, A>
where
    T: Clone + Debug,
    A: Adjacency<T> + Debug,
{
    pub fn new(label: impl Into<String>, vertexs: &[VertexInstance<T, A>]) -> Self {
        Self {
            label: label.into(),
            vertexs: vertexs.to_vec(),
        }
    }

    pub fn get(&self, index: usize) -> Option<VertexInstance<T, A>> {
        let r = self.vertexs.get(index).take()?;
        Some(r.clone())
    }

    pub fn blind_search<U, R>(
        &self,
        algorithm: BlindSearch,
        direction: Direction,
        start: VertexInstance<T, A>,
        seek: VertexInstance<T, A>,
        lvl_limit: Option<usize>,
        arg: Option<&mut U>,
        iterative: bool,
        action: &'_ dyn Fn(
            VertexInstance<T, A>,
            VertexInstance<T, A>,
            &Option<&mut U>,
        ) -> (bool, Option<R>),
    ) -> Option<R>
    where
        T: Clone,
        A: Adjacency<T>,
    {
        let mut loops = 1;
        let mut vertex_visited = 0;
        let mut vertex_before_loop = 0;

        let mut visited = HashSet::new();

        let limit_title = match lvl_limit {
            None => String::new(),
            Some(limit) => format!("{limit}"),
        };

        let title = format!(
            "Recorriendo {} con método {} con dirección {} {}",
            self.label, algorithm, direction, limit_title
        );

        println!("{title}");

        let mut agenda: Box<dyn Container<VertexInstance<T, A>>> = match algorithm {
            BlindSearch::BreadthFirstSearch => Box::new(Queue::new()),
            BlindSearch::DepthFirstSearch => Box::new(Stack::new()),
        };

        agenda.add(start.clone());

        if !iterative {
            visited.insert(VertexWrapper::new(start.clone()));
        }

        while let Some(curr_v) = agenda.get() {
            let (end_search, return_value) = action(curr_v.clone(), seek.clone(), &arg);

            if end_search {
                println!();
                return Some(return_value?);
            }

            if iterative && vertex_visited == vertex_before_loop {
                loops += 1;
                vertex_before_loop += 1;
                vertex_visited = 0;

                let mut agenda: Box<dyn Container<VertexInstance<T, A>>> = match algorithm {
                    BlindSearch::BreadthFirstSearch => Box::new(Queue::new()),
                    BlindSearch::DepthFirstSearch => Box::new(Stack::new()),
                };

                agenda.add(start.clone());

                println!("\nIteración {loops}");
                continue;
            }

            let adjacencies = match direction {
                Direction::Right => curr_v.borrow().adjacencies(),
                Direction::Left => curr_v.borrow().adjacencies().into_iter().rev().collect(),
            };

            for adjacency in adjacencies {
                let vertex = adjacency.vertex();

                let should_add_vertex = match lvl_limit {
                    None => !visited.contains(&VertexWrapper::new(vertex.clone())),
                    Some(limit) => {
                        !visited.contains(&VertexWrapper::new(vertex.clone()))
                            && vertex.borrow().level.expect("Vértice sin nivel") <= limit
                    }
                };

                if should_add_vertex {
                    if !iterative {
                        visited.insert(VertexWrapper::new(vertex.clone()));
                    }

                    agenda.add(vertex);
                }
            }
        }

        println!();
        None
    }

    pub fn set_lvls(&self, root: VertexInstance<T, A>) {
        let mut visited = HashSet::new();
        let mut agenda = Queue::new();
        agenda.add(root.clone());
        visited.insert(VertexWrapper::new(root.clone()));
        root.borrow_mut().level = Some(1);

        println!("Agenda: {}", agenda);
        while let Some(curr_v) = agenda.get() {
            for adj in curr_v.borrow().adjacencies() {
                let vertex = adj.vertex();
                let v_hash = VertexWrapper::new(vertex.clone());
                if !visited.contains(&v_hash) {
                    visited.insert(v_hash);
                    vertex.borrow_mut().level = Some(curr_v.borrow().level.unwrap() + 1);
                    agenda.add(vertex.clone());
                    println!("Agenda: {:#?}", agenda);
                }
            }
        }
        println!()
    }
}
