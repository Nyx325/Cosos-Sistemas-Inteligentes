use ds_components::vertexs::WVertexBuilder;

pub mod data_structs;
pub mod ds_components;

fn main() {
    let v1 = WVertexBuilder::new().value(1).build();

    let v2 = WVertexBuilder::new()
        .value(2)
        .adjacency(v1.clone(), 1.0)
        .build();

    let _v3 = WVertexBuilder::new()
        .value(3)
        .adjacency(v1.clone(), 2.0)
        .adjacency(v2.clone(), 1.0)
        .build();
}
