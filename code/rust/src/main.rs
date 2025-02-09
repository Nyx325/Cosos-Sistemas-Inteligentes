use data_structs::containers::{Container, Queue, Stack};

pub mod data_structs;
pub mod ds_components;

fn main() {
    let mut container: Box<dyn Container<usize>> = Box::new(Queue::new());

    container.add(1);
    container.add(2);
    println!("{container}");
    container.get();
    container.get();
    container.get();
    println!("{container}");

    container = Box::new(Stack::new());
    container.add(1);
    container.add(2);
    println!("{container}");
    container.get();
    container.get();
    container.get();
    println!("{container}");
}
