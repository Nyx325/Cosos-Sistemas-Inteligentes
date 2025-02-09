use data_structs::containers::{Container, Stack};

pub mod data_structs;
pub mod ds_components;

fn main() {
    let mut stack = Stack::new();
    stack.push(1);
    stack.push(3);
    stack.push(5);

    for item in stack.iter() {
        println!("{item}")
    }

    println!("{stack}")
}
