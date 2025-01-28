import { WeightedGraph, Algorithm, Direction } from "./graph.js";
import { WeightedVertex } from "./nodes.js";

const v1 = new WeightedVertex(1);
const v2 = new WeightedVertex(2);
const v3 = new WeightedVertex(3);
const v4 = new WeightedVertex(4);
const v5 = new WeightedVertex(5);

v1.append([v2, 1.0], [v3, 1.0]);
v3.append([v4, 1.0]);
v3.append([v5, 1.0]);

const arbol = new WeightedGraph("Arbol ponderado", [v1, v2, v3, v4, v5]);
arbol.showAdjacencies();

let explore: string[] = [];

const action = (vertex: WeightedVertex<number>, arg: unknown) => {
  const explore = arg as string[];
  explore.push(vertex.toString());
  return { endExplore: false };
};

arbol.explore({
  start: v1,
  arg: explore,
  action,
});
console.log(`Recorrido BFS derecha: ${explore}`);

explore = [];
arbol.explore({
  start: v1,
  arg: explore,
  algorithm: Algorithm.BFS,
  direction: Direction.LEFT,
  action,
});
console.log(`Recorrido BFS izquierda: ${explore}`);

explore = [];
arbol.explore({
  start: v1,
  arg: explore,
  algorithm: Algorithm.DFS,
  direction: Direction.RIGHT,
  action,
});
console.log(`Recorrido DFS derecha: ${explore}`);

explore = [];
arbol.explore({
  start: v1,
  arg: explore,
  algorithm: Algorithm.DFS,
  direction: Direction.LEFT,
  action,
});
console.log(`Recorrido DFS izquierda: ${explore}`);
