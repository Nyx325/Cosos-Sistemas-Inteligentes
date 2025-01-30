import { Container, Queue, Stack } from "./containers.js";
import { NonWeightedVertex, Tag, Vertex, WeightedVertex } from "./nodes.js";

/**
 * Enumeración que define la dirección en la que se recorrerán los vértices adyacentes.
 */
export enum Direction {
  /** Recorre los vértices adyacentes en orden inverso. */
  LEFT = "LEFT",
  /** Recorre los vértices adyacentes en orden normal. */
  RIGHT = "RIGHT",
}

/**
 * Enumeración que define el algoritmo de recorrido que se utilizará para explorar el grafo.
 */
export enum Algorithm {
  /** Breadth-First Search (Búsqueda en Anchura). */
  BFS = "BFS",
  /** Depth-First Search (Búsqueda en Profundidad). */
  DFS = "DFS",
}

/**
 * Tipo que define una función que se ejecuta durante la exploración de un vértice.
 * @template T - Tipo de dato almacenado en el vértice.
 * @template Adjacency - Tipo de dato que representa la adyacencia.
 * @param vertex - El vértice que se está explorando.
 * @param arg - Argumento opcional que se puede pasar a la función.
 * @returns Un objeto que indica si la exploración debe terminar y un valor opcional.
 */
type ExploreAction<T, Adjacency> = (
  vertex: Vertex<T, Adjacency>,
  arg?: unknown,
) => { endExplore: boolean; returnValue?: unknown };

/**
 * Clase abstracta que representa un grafo genérico.
 * @template T - Tipo de dato almacenado en los vértices.
 * @template Adjacency - Tipo de dato que representa la adyacencia.
 */
export abstract class Graph<T, Adjacency> {
  /** Etiqueta o nombre del grafo. */
  protected label: string;
  /** Lista de vértices que componen el grafo. */
  protected vertexs: Vertex<T, Adjacency>[];

  /**
   * Constructor de la clase Graph.
   * @param label - Etiqueta o nombre del grafo.
   * @param vertexs - Lista opcional de vértices que componen el grafo.
   * @throws {Error} Si algún elemento en `vertexs` no es una instancia de `Vertex`.
   */
  constructor(label: string, vertexs?: Vertex<T, Adjacency>[]) {
    this.label = label;

    if (vertexs && !vertexs.every((v) => v instanceof Vertex)) {
      throw new Error("All elements in 'vertexs' must be instances of Vertex.");
    }

    this.vertexs = vertexs ? vertexs : [];
  }

  /**
   * Método abstracto que debe ser implementado por las clases derivadas para obtener un vértice a partir de una adyacencia.
   * @param adjacency - La adyacencia de la cual se obtendrá el vértice.
   * @returns El vértice correspondiente a la adyacencia.
   */
  protected abstract vertexFromAdjacency(
    adjacency: Adjacency,
  ): Vertex<T, Adjacency>;

  /**
   * Muestra las adyacencias de todos los vértices del grafo.
   */
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

  /**
   * Convierte una adyacencia en una cadena de texto.
   * @param adjacency - La adyacencia a convertir.
   * @returns La representación en cadena de la adyacencia.
   */
  protected adjStr(adjacency: Adjacency): string {
    return String(adjacency);
  }

  /**
   * Reinicia el estado de visitado de todos los vértices.
   */
  public resetVisited(): void {
    this.vertexs.forEach((vertex) => (vertex.visited = false));
  }

  /**
   * Imprime la información de un vértice.
   * @param vertex - El vértice a imprimir.
   * @returns Un objeto que indica que la exploración no debe terminar.
   */
  protected printAdjacency(vertex: Vertex<T, Adjacency>): {
    endExplore: boolean;
    returnValue?: unknown;
  } {
    console.log(`  ${vertex.toString()}`);
    return { endExplore: false };
  }

  /**
   * Compara dos vértices.
   * @param vertex - El vértice actual.
   * @param target - El vértice objetivo.
   * @returns Un objeto que indica si los vértices son iguales.
   * @throws {Error} Si `target` no es una instancia de `Vertex`.
   */
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

  /**
   * Explora el grafo utilizando un algoritmo específico (BFS o DFS).
   * @param start - El vértice desde el cual comenzar la exploración.
   * @param algorithm - El algoritmo a utilizar (BFS o DFS) por defecto BFS.
   * @param arg - Argumento opcional que se pasa a la función de acción por defecto undefined.
   * @param direction - La dirección en la que se recorrerán los vértices adyacentes por defecto RIGHT.
   * @param action - La función que se ejecutará durante la exploración por defecto undefined.
   * @returns El valor de retorno de la función de acción, si la exploración termina.
   */
  public explore({
    start,
    algorithm = Algorithm.BFS,
    arg = undefined,
    direction = Direction.RIGHT,
    action = undefined,
    lvlLimit = undefined,
    calcLvls = false,
  }: {
    start: Vertex<T, Adjacency>;
    algorithm?: Algorithm;
    lvlLimit?: number;
    calcLvls?: boolean;
    arg?: unknown;
    direction?: Direction;
    action?: ExploreAction<T, Adjacency>;
  }): unknown | undefined {
    if (calcLvls) {
      this.setLvls({ root: start });
    }

    const lvlLimitTitle =
      lvlLimit !== undefined ? `con límite ${lvlLimit}` : "";
    const title = `Recorriendo grafo con método ${algorithm} con dirección ${direction} ${lvlLimitTitle}`;

    console.log(title);

    const vertexToCheck: Container<Vertex<T, Adjacency>> =
      algorithm === Algorithm.DFS ? new Stack() : new Queue();

    const executeAction = action || this.printAdjacency;

    vertexToCheck.add(start);
    start.visited = true;

    while (!vertexToCheck.isEmpty) {
      const currV = vertexToCheck.get();
      if (!currV) throw new Error("Unexpected null vertex");

      const { endExplore, returnValue } = executeAction(currV, arg);

      if (endExplore) {
        console.log();
        this.resetVisited();
        return returnValue;
      }

      const adjacencies =
        direction === Direction.RIGHT
          ? currV.adjacencies
          : [...currV.adjacencies].reverse();

      for (const adjacency of adjacencies) {
        const neighbor = this.vertexFromAdjacency(adjacency as Adjacency);
        const vertexLvl = neighbor.lvl as number;

        const shouldAddVertex =
          !neighbor.visited &&
          (lvlLimit === undefined ||
            (lvlLimit !== undefined && vertexLvl <= lvlLimit));

        if (shouldAddVertex) {
          vertexToCheck.add(neighbor);
          neighbor.visited = true;
        }
      }
    }

    console.log();
    this.resetVisited();
    return undefined;
  }

  /**
   * Busca un vértice específico en el grafo.
   * @param start - El vértice desde el cual comenzar la búsqueda.
   * @param seek - El vértice que se está buscando.
   * @param algorithm - El algoritmo a utilizar (BFS o DFS) por defecto BFS.
   * @param direction - La dirección en la que se recorrerán los vértices adyacentes por defecto RIGHT.
   * @returns El vértice buscado, si se encuentra.
   */
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

  /**
   * Calcula los niveles de los vértices a partir de un vértice raíz.
   * @param root - El vértice raíz desde el cual calcular los niveles.
   * @param direction - La dirección en la que se recorrerán los vértices adyacentes por defecto RIGHT.
   */
  public setLvls({
    root,
    direction = Direction.RIGHT,
  }: {
    root: Vertex<T, Adjacency>;
    direction?: Direction;
  }) {
    const vertexToCheck = new Queue<Vertex<T, Adjacency>>();
    console.log(`Calculando niveles...`);
    vertexToCheck.add(root);
    root.visited = true;
    root.lvl = 1;

    while (!vertexToCheck.isEmpty) {
      const currV = vertexToCheck.get();
      if (!currV || !currV.lvl) throw new Error("Unexpected behavior");

      console.log(`  ${currV.toString()}`);
      const adjacencies =
        direction === Direction.RIGHT
          ? currV.adjacencies
          : [...currV.adjacencies].reverse();

      for (const adj of adjacencies) {
        const vertex = this.vertexFromAdjacency(adj);
        if (!vertex.visited) {
          vertex.visited = true;
          vertex.lvl = currV.lvl + 1;
          vertexToCheck.add(vertex);
        }
      }
    }

    console.log();
    this.resetVisited();
  }
}

/**
 * Clase que representa un grafo no ponderado.
 * @template T - Tipo de dato almacenado en los vértices.
 */
export class NonWeightedGraph<T> extends Graph<T, NonWeightedVertex<T>> {
  /**
   * Devuelve el vértice directamente, ya que no hay pesos involucrados.
   * @param adjacency - La adyacencia de la cual se obtendrá el vértice.
   * @returns El vértice correspondiente a la adyacencia.
   */
  protected vertexFromAdjacency(
    adjacency: NonWeightedVertex<T>,
  ): NonWeightedVertex<T> {
    return adjacency;
  }
}

/**
 * Clase que representa un grafo ponderado.
 * @template T - Tipo de dato almacenado en los vértices.
 */
export class WeightedGraph<T> extends Graph<T, [WeightedVertex<T>, number]> {
  /**
   * Devuelve el vértice de una adyacencia, ignorando el peso.
   * @param adjacency - La adyacencia de la cual se obtendrá el vértice.
   * @returns El vértice correspondiente a la adyacencia.
   */
  protected vertexFromAdjacency(
    adjacency: [WeightedVertex<T>, number],
  ): WeightedVertex<T> {
    const [vertex] = adjacency;
    return vertex;
  }

  /**
   * Calcula el camino más corto desde un vértice dejando una etiqueta en cada vertice
   * del grafo el nodo a seguir para llegar al destino.
   * @param destiny - El vértice destino desde el cual calcular el camino más corto.
   * @param direction - La dirección en la que se recorrerán los vértices adyacentes.
   */
  public shortestPath({
    destiny,
    direction = Direction.RIGHT,
  }: {
    destiny: WeightedVertex<T>;
    direction?: Direction;
  }) {
    const vertexToCheck = new Queue<WeightedVertex<T>>();
    console.log(`Etiquetando...`);
    vertexToCheck.add(destiny);
    destiny.visited = true;
    destiny.tag = {
      vertex: undefined,
      weigth: 0,
    };

    while (!vertexToCheck.isEmpty) {
      const currV = vertexToCheck.get();
      if (!currV || !currV.lvl) throw new Error("Unexpected behavior");

      console.log(`  ${currV.toString()}`);
      const adjacencies =
        direction === Direction.RIGHT
          ? currV.adjacencies
          : [...currV.adjacencies].reverse();

      for (const adj of adjacencies) {
        const [vertex, weigth] = adj;
        const tag = { vertex, weigth };

        if (!vertex.visited) {
          vertex.visited = true;
          vertex.tag = tag;
          vertexToCheck.add(vertex);
        }

        const prevTag = vertex.tag as Tag<T>;
        if (vertex.tag !== undefined && tag.weigth < prevTag.weigth) {
          vertex.tag = tag;
        }
      }
    }

    this.resetVisited();
  }

  /**
   * Convierte una adyacencia en una cadena de texto que incluye el peso.
   * @param adjacency - La adyacencia a convertir.
   * @returns La representación en cadena de la adyacencia.
   */
  protected adjStr(adjacency: [WeightedVertex<T>, number]): string {
    const [vertex, weight] = adjacency;
    return `(${vertex.value}, ${weight})`;
  }
}
