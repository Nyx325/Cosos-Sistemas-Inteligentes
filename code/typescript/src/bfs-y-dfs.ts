// Podemos representar un nodo como un diccionario, clase o
// lista de listas siempre que podamos guardar un valor y
// ligar de alguna forma con qué nodos tienen conexion, incluso
// podriamos representarlo en una base de datos con tablas cruzadas
// con la parte de foreing keys

import { Queue } from "./containers.js";

// typescript no permite hacer listas de diferentes tipos de datos
// pero en python podria ser algo como
//
// nodo = [valor, [adjacencia1, adjacencia2, adjacencia3]]
// nodo = [1, [nodo2, nodo3, nodo4]]

// o con alguna clase
class NodoString {
  public valor: string; // aquí ponle el tipo que quieras
  public adjacencias: NodoString[];

  // Mausquerramienta que usaremos mas tarde
  public visitado: boolean;

  constructor(valor: string) {
    this.valor = valor;
    this.adjacencias = [];
    this.visitado = false;
  }

  public append(nodo: NodoString) {
    this.adjacencias.push(nodo);
  }
}

// Y puedes crear un nodo
const nodoString = new NodoString("1");

// Y ya manipulas cosas
const nodo_2 = new NodoString("2");
nodoString.adjacencias.push(nodo_2);
const nodo_3 = new NodoString("3");
nodoString.adjacencias.push(nodo_3);

//Para que no cambies muchas cosas o hagas demasiados accesos a
//cosas como las listas en atributos, puedes definir tus propios
//metodos que te acorten escribir y que te faciliten la vida
const nodo_4 = new NodoString("4");
nodoString.append(nodo_4);

// Si es mucho show hacer clases y para rapido, puedes usar diccionarios,
// en python tmb existen, en typescript es un desmadre definir un diccionario
// por cosas del lenguaje pero te juro que en python queda de volada xd

//En python no es necesario esto, defines directamente el atributo y el valor
type Node = {
  valor: number;
  visitado: boolean;
  adjacencias: Node[];
};

const nodo1: Node = { valor: 1, visitado: false, adjacencias: [] };
const nodo2: Node = { valor: 2, visitado: false, adjacencias: [] };
const nodo3: Node = { valor: 3, visitado: false, adjacencias: [] };
const nodo4: Node = { valor: 4, visitado: false, adjacencias: [] };
const nodo5: Node = { valor: 5, visitado: false, adjacencias: [] };

nodo1["adjacencias"] = [nodo2, nodo3, nodo4];
nodo2["adjacencias"] = [nodo3, nodo5];
nodo3["adjacencias"] = [nodo1, nodo2];

const grafo = [nodo1, nodo2, nodo3, nodo4, nodo5];

// BFS y DFS son practicamente iguales, solo cambia la estructura que usan
function bfs(inicio: Node, fin: Node) {
  const vertices_a_chequiar = new Queue<Node>(); //cola pa BFS

  vertices_a_chequiar.enqueue(inicio);
  // Si estás en un grafo, no quieres recorrer nodos que
  // ya recorriste porque se va a ciclar, entonces debes tener
  // un control de cuales ya visitaste, minauro nos enseño poniendole
  // una bandera de visitado, pero puedes llegar a usar una estructura
  // de datos llamada Set que existe en python y que te deja almacenar
  // varios datos sin que se repita ninguno, y es mas facil, pero
  // para este ejemplo no lo haré
  inicio["visitado"] = true;

  while (vertices_a_chequiar.size !== 0) {
    const vertice_actual = vertices_a_chequiar.dequeue();

    // Acá en typescript y seguro en python te puede regresar undefined
    // en typescript o None en python si falla el dequeue porque está vacía,
    //
    // esta validacion
    // es pa que mi editor de codigo no me marque errores pero aunque no
    // lo pusiera tanto en python como en javascript jalaria
    if (vertice_actual === undefined) {
      throw new Error("No debería ser undefined");
    }

    // Manipular tu vertice como quieras, chequear busqueda o lo
    // que sea que debas hacer, por eso en mi codigo lo tenia en
    // una funcion, si necesitas mas variables o valores para esta
    // parte, pasalas como argumento a la funcion general para usarlas
    // acá
    console.log(`${vertice_actual["valor"]}`);

    if (vertice_actual["valor"] === fin["valor"]) {
      console.log(`Encontrado`);
      return;
    }

    // Fin manipulación de vertice actual

    // hacer el for each para recorrido por derecha, si necesitas
    // la parte de por izquierda agregas el codigo para invertir la
    // lista
    for (const adjacencia of vertice_actual["adjacencias"]) {
      //Considerando que fuera un grafo en general, pondriamos
      //condicion de que no estén visitados, si es un arbol, podemos
      //simplemente agregar el vertice sin el if
      if (adjacencia["visitado"] === false) {
        vertices_a_chequiar.enqueue(adjacencia);
      }
    }
  }
}

bfs(nodo1, nodo4);
// Y una vez acabamos el recorrido, considerando que es un grafo y
// que tenemos las banderas de visitado, deberiamos reiniciarlas
for (const adjacencia of grafo) {
  // en javascript todos los objetos son diccionarios, por eso puedo
  // acceder con lo de obj.atributo, pero asi podrias sustituir las cosas
  // en el codigo de arriba si fueran clases, todo queda igual
  adjacencia.visitado = false;
}

// Y ya solo cambiamos Queue por Stack para DFS e invertir la lista
// para izq o derecha, el algoritmo en si no va a cambiar, el unico
// codigo que va a cambiar es el bloque de codigo de la acción
// y los argumentos de la funcion en caso de que debas comparar cosas
//
// Ahí va a estar el reto en el examen, no tanto en el algoritmo
