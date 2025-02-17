use std::fmt::Display;

use data_structs::graph::{BlindSearch, Direction, Graph};
use ds_components::vertexs::{Adjacency, NonWeightedAdjacency, Vertex, VertexInstance};

pub mod data_structs;
pub mod ds_components;

fn action<T, A, U, R>(
    current: VertexInstance<T, A>,
    seek: VertexInstance<T, A>,
    _arg: &Option<&mut U>,
) -> (bool, Option<R>)
where
    T: Display + Clone + PartialEq,
    A: Adjacency<T>,
{
    // Verificar si el vértice actual es el que estamos buscando
    if current.borrow().value == seek.borrow().value {
        println!("Vértice encontrado: {}", current.borrow().value);
        (true, None) // Terminar la búsqueda y devolver un mensaje de éxito
    } else {
        println!("Visitando vértice: {}", current.borrow().value);
        (false, None) // Continuar la búsqueda
    }
}

fn main() {
    // Crear 50 vértices
    let vertices: Vec<VertexInstance<usize, NonWeightedAdjacency<usize>>> =
        (1..=4).map(|i| Vertex::new(i)).collect();

    // Conectar cada vértice con los siguientes 3 vértices
    for i in 0..vertices.len() {
        let mut adjacencies = Vec::new();
        for j in 1..=3 {
            if i + j < vertices.len() {
                adjacencies.push(NonWeightedAdjacency::new(vertices[i + j].clone()));
            }
        }
        vertices[i].borrow_mut().add_adjacencies(adjacencies);
    }

    let start = vertices.get(0).unwrap().clone();
    let seek = vertices.get(vertices.len() - 1).unwrap().clone();
    let graph = Graph::new("Grafo", &vertices);

    graph.set_lvls(start.clone());

    graph.blind_search::<usize, usize>(
        BlindSearch::BreadthFirstSearch,
        Direction::Left,
        start,
        seek,
        None,
        None,
        true,
        &action,
    );
}
