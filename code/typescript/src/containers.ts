import { DoubleLinkedNode } from "./nodes.js";

/**
 * Interfaz base para contenedores de elementos
 * @template T Tipo de elementos almacenados en el contenedor
 */
export interface Container<T> {
  /**
   * Añade un elemento al contenedor
   * @param value Elemento a añadir
   */
  add(value: T): undefined;

  /**
   * Obtiene y remueve un elemento del contenedor
   * @returns Elemento removido o undefined si está vacío
   */
  get(): T | undefined;

  /**
   * Observa el próximo elemento sin removerlo
   * @returns Próximo elemento o undefined si está vacío
   */
  peek(): T | undefined;

  /**
   * Cantidad de elementos en el contenedor
   */
  get size(): number;

  /**
   * Indica si el contenedor está vacío
   */
  get isEmpty(): boolean;
}

/**
 * Implementación de cola FIFO (First In First Out)
 * @template T Tipo de elementos almacenados en la cola
 */
export class Queue<T> implements Container<T> {
  private _size: number;
  private head: DoubleLinkedNode<T> | undefined;
  private tail: DoubleLinkedNode<T> | undefined;

  /**
   * Crea una nueva cola vacía
   */
  public constructor() {
    this._size = 0;
  }

  /**
   * Cantidad actual de elementos en la cola
   */
  public get size(): number {
    return this._size;
  }

  /**
   * Verifica si la cola está vacía
   */
  public get isEmpty(): boolean {
    return this._size == 0;
  }

  /**
   * Encola un elemento al final de la cola
   * @param value Elemento a encolar
   */
  public enqueue(value: T) {
    const node = new DoubleLinkedNode<T>(value);

    if (this.isEmpty) {
      this.head = node;
      this.tail = node;
    } else {
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
  public dequeue(): T | undefined {
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
    } else {
      this.tail = undefined;
    }

    this._size -= 1;
    return value;
  }

  /**
   * Implementación de Container.add: encola un elemento
   * @param value Elemento a añadir
   */
  public add(value: T): undefined {
    this.enqueue(value);
    return undefined;
  }

  /**
   * Implementación de Container.get: desencola un elemento
   * @returns Elemento removido o undefined
   */
  public get(): T | undefined {
    return this.dequeue();
  }

  /**
   * Observa el primer elemento de la cola sin removerlo
   * @returns Primer elemento o undefined
   */
  public peek(): T | undefined {
    return this.head ? this.head.value : undefined;
  }
}

/**
 * Implementación de pila LIFO (Last In First Out)
 * @template T Tipo de elementos almacenados en la pila
 */
export class Stack<T> implements Container<T> {
  private _size: number;
  private head: DoubleLinkedNode<T> | undefined;

  /**
   * Crea una nueva pila vacía
   */
  public constructor() {
    this._size = 0;
    this.head = undefined;
  }

  /**
   * Cantidad actual de elementos en la pila
   */
  public get size(): number {
    return this._size;
  }

  /**
   * Verifica si la pila está vacía
   */
  public get isEmpty(): boolean {
    return this.size === 0;
  }

  /**
   * Apila un elemento en la cima
   * @param value Elemento a apilar
   */
  public push(value: T) {
    const node = new DoubleLinkedNode<T>(value);
    node.next = this.head;
    this.head = node;
    this._size += 1;
  }

  /**
   * Desapila el elemento de la cima
   * @returns Elemento removido o undefined si está vacía
   */
  public pop(): T | undefined {
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
  public add(value: T): undefined {
    this.push(value);
    return undefined;
  }

  /**
   * Implementación de Container.get: desapila un elemento
   * @returns Elemento removido o undefined
   */
  public get(): T | undefined {
    return this.pop();
  }

  /**
   * Observa el elemento en la cima sin removerlo
   * @returns Elemento en la cima o undefined
   */
  public peek(): T | undefined {
    return this.head ? this.head.value : undefined;
  }
}
