"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const graph_1 = require("./graph");
const nodes_1 = require("./nodes");
const v1 = new nodes_1.WeightedVertex(1);
const v2 = new nodes_1.WeightedVertex(2);
const v3 = new nodes_1.WeightedVertex(3);
const v4 = new nodes_1.WeightedVertex(4);
const v5 = new nodes_1.WeightedVertex(5);
v1.append([v2, 1.0], [v3, 1.0]);
v3.append([v4, 1.0]);
v3.append([v5, 1.0]);
const arbol = new graph_1.WeightedGraph("Arbol ponderado", [v1, v2, v3, v4, v5]);
arbol.showAdjacencies();
let explore = [];
const action = (vertex, arg) => {
    const explore = arg;
    console.log(`  ${vertex.toString()}`);
    explore.push(vertex.toString());
    return { endExplore: false };
};
arbol.explore({
    start: v1,
    arg: explore,
    algorithm: graph_1.Algorithm.BFS,
    direction: graph_1.Direction.RIGHT,
    action,
});
console.log(`Recorrido BFS derecha: ${explore}`);
explore = [];
arbol.explore({
    start: v1,
    arg: explore,
    algorithm: graph_1.Algorithm.BFS,
    direction: graph_1.Direction.LEFT,
    action,
});
console.log(`Recorrido BFS izquierda: ${explore}`);
explore = [];
arbol.explore({
    start: v1,
    arg: explore,
    algorithm: graph_1.Algorithm.DFS,
    direction: graph_1.Direction.RIGHT,
    action,
});
console.log(`Recorrido DFS derecha: ${explore}`);
explore = [];
arbol.explore({
    start: v1,
    arg: explore,
    algorithm: graph_1.Algorithm.DFS,
    direction: graph_1.Direction.LEFT,
    action,
});
console.log(`Recorrido DFS izquierda: ${explore}`);
