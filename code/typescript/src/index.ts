import { NonWeightedGraph } from "./graph.js";
import { NonWeightedVertex } from "./nodes.js";

const v1 = new NonWeightedVertex({ value: 1 });
const v2 = new NonWeightedVertex({ value: 2 });
const v3 = new NonWeightedVertex({ value: 3 });
const v4 = new NonWeightedVertex({ value: 4 });
const v5 = new NonWeightedVertex({ value: 5 });
const v6 = new NonWeightedVertex({ value: 6 });
const v7 = new NonWeightedVertex({ value: 7 });
const v8 = new NonWeightedVertex({ value: 8 });
const v9 = new NonWeightedVertex({ value: 9 });
const v10 = new NonWeightedVertex({ value: 10 });
const v11 = new NonWeightedVertex({ value: 11 });
const v12 = new NonWeightedVertex({ value: 12 });

v1.append(v2, v3, v4);
v2.append(v5, v6);
v3.append(v7, v8);
v5.append(v9);
v6.append(v10);
v7.append(v11);
v8.append(v12);

const arbol = new NonWeightedGraph("Árbol", [
  v1,
  v2,
  v3,
  v4,
  v5,
  v6,
  v7,
  v8,
  v9,
  v10,
  v11,
  v12,
]);

arbol.hillClimbing({
  start: v1,
  seek: v9,
  heuristic: (adj) => {
    return adj.value;
  },
});
