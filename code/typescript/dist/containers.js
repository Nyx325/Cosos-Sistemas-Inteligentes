"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Stack = exports.Queue = void 0;
const nodes_1 = require("./nodes");
/**
 * Implementación de cola FIFO (First In First Out)
 * @template T Tipo de elementos almacenados en la cola
 */
class Queue {
    _size;
    head;
    tail;
    /**
     * Crea una nueva cola vacía
     */
    constructor() {
        this._size = 0;
    }
    /**
     * Cantidad actual de elementos en la cola
     */
    get size() {
        return this._size;
    }
    /**
     * Verifica si la cola está vacía
     */
    get isEmpty() {
        return this._size == 0;
    }
    /**
     * Encola un elemento al final de la cola
     * @param value Elemento a encolar
     */
    enqueue(value) {
        const node = new nodes_1.DoubleLinkedNode(value);
        if (this.isEmpty) {
            this.head = node;
            this.tail = node;
        }
        else {
            if (this.tail === undefined) {
                throw new Error("Unexpected behavior");
            }
            this.tail.next = node;
            node.prev = this.tail;
            this.tail = node;
        }
        this._size += 1;
    }
    /**
     * Desencola el primer elemento de la cola
     * @returns Elemento removido o undefined si está vacía
     */
    dequeue() {
        if (this.isEmpty) {
            return undefined;
        }
        if (this.head === undefined) {
            return undefined;
        }
        const value = this.head.value;
        this.head = this.head.next;
        if (this.head !== undefined) {
            this.head.prev = undefined;
        }
        else {
            this.tail = undefined;
        }
        this._size -= 1;
        return value;
    }
    /**
     * Implementación de Container.add: encola un elemento
     * @param value Elemento a añadir
     */
    add(value) {
        this.enqueue(value);
        return undefined;
    }
    /**
     * Implementación de Container.get: desencola un elemento
     * @returns Elemento removido o undefined
     */
    get() {
        return this.dequeue();
    }
    /**
     * Observa el primer elemento de la cola sin removerlo
     * @returns Primer elemento o undefined
     */
    peek() {
        return this.head ? this.head.value : undefined;
    }
}
exports.Queue = Queue;
/**
 * Implementación de pila LIFO (Last In First Out)
 * @template T Tipo de elementos almacenados en la pila
 */
class Stack {
    _size;
    head;
    /**
     * Crea una nueva pila vacía
     */
    constructor() {
        this._size = 0;
        this.head = undefined;
    }
    /**
     * Cantidad actual de elementos en la pila
     */
    get size() {
        return this._size;
    }
    /**
     * Verifica si la pila está vacía
     */
    get isEmpty() {
        return this.size === 0;
    }
    /**
     * Apila un elemento en la cima
     * @param value Elemento a apilar
     */
    push(value) {
        const node = new nodes_1.DoubleLinkedNode(value);
        node.next = this.head;
        this.head = node;
        this._size += 1;
    }
    /**
     * Desapila el elemento de la cima
     * @returns Elemento removido o undefined si está vacía
     */
    pop() {
        if (this.isEmpty || this.head === undefined) {
            return undefined;
        }
        const value = this.head.value;
        this.head = this.head.next;
        if (this.head) {
            this.head.prev = undefined;
        }
        this._size -= 1;
        return value;
    }
    /**
     * Implementación de Container.add: apila un elemento
     * @param value Elemento a añadir
     */
    add(value) {
        this.push(value);
        return undefined;
    }
    /**
     * Implementación de Container.get: desapila un elemento
     * @returns Elemento removido o undefined
     */
    get() {
        return this.pop();
    }
    /**
     * Observa el elemento en la cima sin removerlo
     * @returns Elemento en la cima o undefined
     */
    peek() {
        return this.head ? this.head.value : undefined;
    }
}
exports.Stack = Stack;
