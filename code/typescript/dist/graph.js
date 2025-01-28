"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WeightedGraph = exports.NonWeightedGraph = exports.Graph = exports.Algorithm = exports.Direction = void 0;
const containers_1 = require("./containers");
const nodes_1 = require("./nodes");
var Direction;
(function (Direction) {
    Direction["LEFT"] = "LEFT";
    Direction["RIGHT"] = "RIGHT";
})(Direction || (exports.Direction = Direction = {}));
var Algorithm;
(function (Algorithm) {
    Algorithm["BFS"] = "BFS";
    Algorithm["DFS"] = "DFS";
})(Algorithm || (exports.Algorithm = Algorithm = {}));
class Graph {
    label;
    vertexs;
    constructor(label, vertexs = undefined) {
        this.label = label;
        if (vertexs && !vertexs.every((v) => v instanceof nodes_1.Vertex)) {
            throw new Error("All elements in 'vertexs' must be instances of Vertex.");
        }
        this.vertexs = vertexs ? vertexs : [];
    }
    showAdjacencies() {
        console.log(`Adyacencias de ${this.label}:`);
        for (const vertex of this.vertexs) {
            const adjStr = vertex.adjacencies
                .map((adj) => this.adjStr(adj))
                .join(", ");
            console.log(`${vertex} -> {${adjStr}}`);
        }
        console.log();
    }
    adjStr(adjacency) {
        return String(adjacency);
    }
    resetVisited() {
        for (const vertex of this.vertexs) {
            vertex.visited = false;
        }
    }
    printAdjacency(vertex) {
        console.log(`  ${vertex.toString()}`);
        return { endExplore: false };
    }
    equals(vertex, target) {
        if (!target || !(target instanceof nodes_1.Vertex)) {
            throw new Error("Argument should be a Vertex");
        }
        this.printAdjacency(vertex);
        return { endExplore: vertex === target };
    }
    explore({ start, algorithm = Algorithm.BFS, arg = undefined, direction = Direction.RIGHT, action = undefined, }) {
        const vertexToCheck = algorithm === Algorithm.DFS ? new containers_1.Stack() : new containers_1.Queue();
        const executeAction = action || this.printAdjacency.bind(this);
        vertexToCheck.add(start);
        start.visited = true;
        while (!vertexToCheck.isEmpty) {
            const currV = vertexToCheck.get();
            if (!currV)
                throw new Error("Unexpected null vertex");
            const { endExplore, returnValue } = executeAction(currV, arg);
            if (endExplore) {
                this.resetVisited();
                return returnValue;
            }
            const adjacencies = direction === Direction.RIGHT
                ? currV.adjacencies
                : [...currV.adjacencies].reverse();
            for (const adjacency of adjacencies) {
                const neighbor = this.vertexFromAdjacency(adjacency);
                if (!neighbor.visited) {
                    vertexToCheck.add(neighbor);
                    neighbor.visited = true;
                }
            }
        }
        this.resetVisited();
        return undefined;
    }
    search(start, seek, algorithm = Algorithm.BFS, direction = Direction.RIGHT) {
        return this.explore({
            start,
            algorithm,
            arg: undefined,
            direction,
            action: (v) => this.equals(v, seek),
        });
    }
}
exports.Graph = Graph;
class NonWeightedGraph extends Graph {
    vertexFromAdjacency(adjacency) {
        return adjacency;
    }
}
exports.NonWeightedGraph = NonWeightedGraph;
class WeightedGraph extends Graph {
    vertexFromAdjacency(adjacency) {
        const [vertex] = adjacency;
        return vertex;
    }
    adjStr(adjacency) {
        const [vertex, weight] = adjacency;
        return `(${vertex.value}, ${weight})`;
    }
}
exports.WeightedGraph = WeightedGraph;
