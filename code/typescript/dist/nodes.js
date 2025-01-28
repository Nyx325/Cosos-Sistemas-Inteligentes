"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WeightedVertex = exports.NonWeightedVertex = exports.DoubleLinkedNode = exports.Vertex = exports.Node = void 0;
/**
 * Clase base abstracta para nodos genéricos.
 * @template T Tipo del valor almacenado en el nodo
 */
class Node {
    /**
     * Valor almacenado en el nodo
     */
    value;
    /**
     * Crea una instancia de Node
     * @param value Valor inicial del nodo
     */
    constructor(value) {
        this.value = value;
    }
    toString() {
        return `(${this.value})`;
    }
}
exports.Node = Node;
/**
 * Clase base abstracta para vértices de grafos con funcionalidad de adyacencia
 * @template T Tipo del valor almacenado en el vértice
 * @template Adjacency Tipo de las adyacencias para definir un vertice con peso
 * y uno sin peso
 */
class Vertex extends Node {
    _lvl;
    /**
     * Indica si el vértice ha sido visitado en un recorrido
     */
    visited;
    /**
     * Lista de vértices adyacentes
     */
    adjacencies;
    /**
     * Crea una instancia de Vertex
     * @param value Valor del vértice
     * @param lvl Nivel
     * @param adjacencies Lista inicial de adyacencias
     */
    constructor(value, lvl = undefined, adjacencies = undefined) {
        super(value);
        this._lvl = lvl;
        this.adjacencies = adjacencies ? adjacencies : [];
        this.visited = false;
    }
    /**
     * Obtiene el nivel actual del vértice
     */
    get lvl() {
        return this._lvl;
    }
    /**
     * Añade una o más adyacencias al vértice
     * @param adjacencies Adyacencias a añadir
     */
    append(...adjacencies) {
        adjacencies.forEach((adjacency) => {
            this.adjacencies.push(adjacency);
        });
    }
    /**
     * Obtiene una adyacencia por índice
     * @param index Posición en la lista de adyacencias
     * @returns Adyacencia en la posición solicitada o undefined
     */
    get(index) {
        return this.adjacencies[index];
    }
}
exports.Vertex = Vertex;
/**
 * Nodo para listas doblemente enlazadas
 * @template T Tipo del valor almacenado en el nodo
 */
class DoubleLinkedNode extends Node {
    /**
     * Referencia al siguiente nodo en la lista
     */
    next;
    /**
     * Referencia al nodo anterior en la lista
     */
    prev;
    /**
     * Crea una instancia de DoubleLinkedNode
     * @param value Valor del nodo
     * @param next Referencia al siguiente nodo (opcional)
     * @param prev Referencia al nodo anterior (opcional)
     */
    constructor(value, next = undefined, prev = undefined) {
        super(value);
        this.next = next;
        this.prev = prev;
    }
}
exports.DoubleLinkedNode = DoubleLinkedNode;
/**
 * Vértice para grafos no ponderados
 * @template T Tipo del valor almacenado en el vértice
 */
class NonWeightedVertex extends Vertex {
    /**
     * Crea una instancia de NonWeightedVertex
     * @param value Valor del vértice
     * @param lvl Nivel
     * @param adjacencies Lista inicial de vértices adyacentes
     */
    constructor(value, lvl = undefined, adjacencies = undefined) {
        super(value, lvl, adjacencies);
    }
}
exports.NonWeightedVertex = NonWeightedVertex;
/**
 * Vértice para grafos ponderados
 * @template T Tipo del valor almacenado en el vértice
 */
class WeightedVertex extends Vertex {
    /**
     * Crea una instancia de WeightedVertex
     * @param value Valor del vértice
     * @param lvl Nivel
     * @param adjacencies Lista inicial de adyacencias ponderadas
     */
    constructor(value, lvl = undefined, adjacencies = undefined) {
        super(value, lvl, adjacencies);
    }
}
exports.WeightedVertex = WeightedVertex;
