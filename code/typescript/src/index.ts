import { WeightedGraph } from "./graph.js";
import { WeightedVertex } from "./nodes.js";

const v1 = new WeightedVertex({ value: 1, lvl: 1 });
const v2 = new WeightedVertex({ value: 2, lvl: 2 });
const v3 = new WeightedVertex({ value: 3, lvl: 2 });
const v4 = new WeightedVertex({ value: 4, lvl: 3 });
const v5 = new WeightedVertex({ value: 5, lvl: 3 });

v1.append([v2, 1.0], [v3, 1.0]);
v3.append([v4, 1.0]);
v3.append([v5, 1.0]);

const arbol = new WeightedGraph("Arbol ponderado", [v1, v2, v3, v4, v5]);
arbol.showAdjacencies();

arbol.explore({
  start: v1,
  arg: 2,
  action: (vertex, arg) => {
    if (vertex.lvl === undefined) {
      throw new Error("Unexpected behavior");
    }

    const lvlLimit = arg as number;

    if (lvlLimit < vertex.lvl) return { endExplore: true };

    console.log(`${vertex.toString()}:${vertex.lvl}`);

    return { endExplore: false };
  },
});
