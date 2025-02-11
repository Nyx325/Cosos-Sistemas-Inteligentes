use ds_components::vertexs::Vertex;

pub mod data_structs;
pub mod ds_components;

fn main() {
    let vertex = Vertex::new(1);
    let vertex2 = Vertex::new(2);

    vertex.borrow_mut().append(&[vertex2.clone()]);
    vertex2.borrow_mut().append(&[vertex.clone()]);

    for vertex in vertex2.borrow().adjacencies() {
        println!("Valor: {}", vertex.borrow().value)
    }
}
