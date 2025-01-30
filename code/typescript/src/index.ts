import { Algorithm, Direction, WeightedGraph } from "./graph.js";
import { WeightedVertex } from "./nodes.js";

const v1 = new WeightedVertex({ value: 1 });
const v2 = new WeightedVertex({ value: 2 });
const v3 = new WeightedVertex({ value: 3 });
const v4 = new WeightedVertex({ value: 4 });
const v5 = new WeightedVertex({ value: 5 });

v1.append([v2, 1.0], [v3, 1.0]);
v3.append([v4, 1.0]);
v3.append([v5, 1.0]);

const arbol = new WeightedGraph("Arbol ponderado", [v1, v2, v3, v4, v5]);

arbol.showAdjacencies();
arbol.explore({
  start: v1,
  algorithm: Algorithm.BFS,
  direction: Direction.RIGHT,
  calcLvls: true,
  lvlLimit: 2,
});

arbol.explore({
  start: v1,
  algorithm: Algorithm.DFS,
  direction: Direction.RIGHT,
  lvlLimit: 2,
});
