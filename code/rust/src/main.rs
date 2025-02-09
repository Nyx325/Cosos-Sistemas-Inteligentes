use data_structs::containers::Stack;

pub mod data_structs;
pub mod ds_components;

fn main() {
    let mut stack = Stack::new();
    stack.push(1);

    for item in stack.iter() {
        println!("{}", item);
    }

    let _items: Vec<i32> = stack.iter().collect();
}
