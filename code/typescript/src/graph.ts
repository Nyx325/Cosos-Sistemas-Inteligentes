import { Container, Queue, Stack } from "./containers";
import { NonWeightedVertex, Vertex, WeightedVertex } from "./nodes";

export enum Direction {
  LEFT = "LEFT",
  RIGHT = "RIGHT",
}

export enum Algorithm {
  BFS = "BFS",
  DFS = "DFS",
}

type ExploreAction<T, Adjacency> = (
  vertex: Vertex<T, Adjacency>,
  arg: unknown | undefined,
) => { endExplore: boolean; returnValue?: unknown };

export abstract class Graph<T, Adjacency> {
  protected label: string;
  protected vertexs: Vertex<T, Adjacency>[];

  constructor(
    label: string,
    vertexs: Vertex<T, Adjacency>[] | undefined = undefined,
  ) {
    this.label = label;

    if (vertexs && !vertexs.every((v) => v instanceof Vertex)) {
      throw new Error("All elements in 'vertexs' must be instances of Vertex.");
    }

    this.vertexs = vertexs ? vertexs : [];
  }

  protected abstract vertexFromAdjacency(
    adjacency: Adjacency,
  ): Vertex<T, Adjacency>;

  public showAdjacencies(): void {
    console.log(`Adyacencias de ${this.label}:`);

    for (const vertex of this.vertexs) {
      const adjStr = vertex.adjacencies
        .map((adj) => this.adjStr(adj))
        .join(", ");

      console.log(`${vertex} -> {${adjStr}}`);
    }

    console.log();
  }

  protected adjStr(adjacency: Adjacency): string {
    return String(adjacency);
  }

  public resetVisited(): void {
    for (const vertex of this.vertexs) {
      vertex.visited = false;
    }
  }

  protected printAdjacency(vertex: Vertex<T, Adjacency>): {
    endExplore: boolean;
    returnValue?: unknown;
  } {
    console.log(`  ${vertex.toString()}`);
    return { endExplore: false };
  }

  protected equals(
    vertex: Vertex<T, Adjacency>,
    target?: Vertex<T, Adjacency>,
  ): {
    endExplore: boolean;
    returnValue?: unknown;
  } {
    if (!target || !(target instanceof Vertex)) {
      throw new Error("Argument should be a Vertex");
    }

    this.printAdjacency(vertex);

    return { endExplore: vertex === target };
  }

  public explore({
    start,
    algorithm = Algorithm.BFS,
    arg = undefined,
    direction = Direction.RIGHT,
    action = undefined,
  }: {
    start: Vertex<T, Adjacency>;
    algorithm?: Algorithm;
    arg?: unknown;
    direction?: Direction;
    action?: ExploreAction<T, Adjacency>;
  }): unknown | undefined {
    const vertexToCheck: Container<Vertex<T, Adjacency>> =
      algorithm === Algorithm.DFS ? new Stack() : new Queue();

    const executeAction = action || this.printAdjacency.bind(this);

    vertexToCheck.add(start);
    start.visited = true;

    while (!vertexToCheck.isEmpty) {
      const currV = vertexToCheck.get();
      if (!currV) throw new Error("Unexpected null vertex");

      const { endExplore, returnValue } = executeAction(currV, arg);

      if (endExplore) {
        this.resetVisited();
        return returnValue;
      }

      const adjacencies =
        direction === Direction.RIGHT
          ? currV.adjacencies
          : [...currV.adjacencies].reverse();

      for (const adjacency of adjacencies) {
        const neighbor = this.vertexFromAdjacency(adjacency as Adjacency);
        if (!neighbor.visited) {
          vertexToCheck.add(neighbor);
          neighbor.visited = true;
        }
      }
    }

    this.resetVisited();
    return undefined;
  }

  public search({
    start,
    seek,
    algorithm = Algorithm.BFS,
    direction = Direction.RIGHT,
  }: {
    start: Vertex<T, Adjacency>;
    seek: Vertex<T, Adjacency>;
    algorithm?: Algorithm;
    direction?: Direction;
  }): unknown | undefined {
    return this.explore({
      start,
      algorithm,
      arg: undefined,
      direction,
      action: (v) => this.equals(v, seek),
    });
  }
}

export class NonWeightedGraph<T> extends Graph<T, NonWeightedVertex<T>> {
  protected vertexFromAdjacency(
    adjacency: NonWeightedVertex<T>,
  ): NonWeightedVertex<T> {
    return adjacency;
  }
}

export class WeightedGraph<T> extends Graph<T, [WeightedVertex<T>, number]> {
  protected vertexFromAdjacency(
    adjacency: [WeightedVertex<T>, number],
  ): WeightedVertex<T> {
    const [vertex] = adjacency;
    return vertex;
  }

  protected adjStr(adjacency: [WeightedVertex<T>, number]): string {
    const [vertex, weight] = adjacency;
    return `(${vertex.value}, ${weight})`;
  }
}
