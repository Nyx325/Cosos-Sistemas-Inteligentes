/**
 * Clase base abstracta para nodos genéricos.
 * @template T Tipo del valor almacenado en el nodo
 */
export abstract class Node<T> {
  /**
   * Valor almacenado en el nodo
   */
  public value: T;

  /**
   * Crea una instancia de Node
   * @param value Valor inicial del nodo
   */
  constructor(value: T) {
    this.value = value;
  }

  toString(): string {
    return `(${this.value})`;
  }
}

/**
 * Clase base abstracta para vértices de grafos con funcionalidad de adyacencia
 * @template T Tipo del valor almacenado en el vértice
 * @template Adjacency Tipo de las adyacencias para definir un vertice con peso
 * y uno sin peso
 */
export abstract class Vertex<T, Adjacency> extends Node<T> {
  public lvl: number | undefined;
  /**
   * Indica si el vértice ha sido visitado en un recorrido
   */
  public visited: boolean;
  /**
   * Lista de vértices adyacentes
   */
  public adjacencies: Adjacency[];

  /**
   * Crea una instancia de Vertex
   * @param value Valor del vértice
   * @param lvl Nivel
   * @param adjacencies Lista inicial de adyacencias
   */
  public constructor({
    value,
    lvl = undefined,
    adjacencies = undefined,
  }: {
    value: T;
    lvl?: number;
    adjacencies?: Adjacency[];
  }) {
    super(value);
    this.lvl = lvl;
    this.adjacencies = adjacencies ? adjacencies : [];
    this.visited = false;
  }

  /**
   * Añade una o más adyacencias al vértice
   * @param adjacencies Adyacencias a añadir
   */
  public append(...adjacencies: Adjacency[]) {
    adjacencies.forEach((adjacency) => {
      this.adjacencies.push(adjacency);
    });
  }

  /**
   * Obtiene una adyacencia por índice
   * @param index Posición en la lista de adyacencias
   * @returns Adyacencia en la posición solicitada o undefined
   */
  public get(index: number): Adjacency | undefined {
    return this.adjacencies[index];
  }
}

/**
 * Nodo para listas doblemente enlazadas
 * @template T Tipo del valor almacenado en el nodo
 */
export class DoubleLinkedNode<T> extends Node<T> {
  /**
   * Referencia al siguiente nodo en la lista
   */
  public next: DoubleLinkedNode<T> | undefined;
  /**
   * Referencia al nodo anterior en la lista
   */
  public prev: DoubleLinkedNode<T> | undefined;

  /**
   * Crea una instancia de DoubleLinkedNode
   * @param value Valor del nodo
   * @param next Referencia al siguiente nodo (opcional)
   * @param prev Referencia al nodo anterior (opcional)
   */
  public constructor(
    value: T,
    next: DoubleLinkedNode<T> | undefined = undefined,
    prev: DoubleLinkedNode<T> | undefined = undefined,
  ) {
    super(value);
    this.next = next;
    this.prev = prev;
  }
}

/**
 * Vértice para grafos no ponderados
 * @template T Tipo del valor almacenado en el vértice
 */
export class NonWeightedVertex<T> extends Vertex<T, NonWeightedVertex<T>> {
  /**
   * Crea una instancia de NonWeightedVertex
   * @param value Valor del vértice
   * @param lvl Nivel
   * @param adjacencies Lista inicial de vértices adyacentes
   */
  public constructor({
    value,
    lvl = undefined,
    adjacencies = undefined,
  }: {
    value: T;
    lvl?: number;
    adjacencies?: NonWeightedVertex<T>[];
  }) {
    super({ value, lvl, adjacencies });
  }
}

/**
 * Vértice para grafos ponderados
 * @template T Tipo del valor almacenado en el vértice
 */
export class WeightedVertex<T> extends Vertex<T, [WeightedVertex<T>, number]> {
  /**
   * Crea una instancia de WeightedVertex
   * @param value Valor del vértice
   * @param lvl Nivel
   * @param adjacencies Lista inicial de adyacencias ponderadas
   */
  public constructor({
    value,
    lvl = undefined,
    adjacencies = undefined,
  }: {
    value: T;
    lvl?: number;
    adjacencies?: [WeightedVertex<T>, number][];
  }) {
    super({ value, lvl, adjacencies });
  }
}
