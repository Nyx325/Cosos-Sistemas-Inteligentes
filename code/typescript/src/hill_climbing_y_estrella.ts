type Node = {
  valor: number;
  adjacencias: Node[];
};

function heuristica(vertice_actual: Node, fin: Node): number {
  // Por el que esté mas cerca del valor del fin o ns, algo
  return fin["valor"] - vertice_actual["valor"];
}

function hill_climbing_o_a_estrella(inicio: Node, fin: Node) {
  // Según yo acá no necesitamos una estructura mas allá de una lista
  let vertices_a_chequiar: Node[] = [];
  vertices_a_chequiar.push(inicio);

  while (vertices_a_chequiar.length !== 0) {
    const vertice_actual = vertices_a_chequiar.pop();

    // validacion para el editor xd
    if (vertice_actual === undefined) throw new Error();

    // Tu codigo que se va a encargar de resolver (aunque no del todo)
    // el ejercicio o buscar el destino e imprimir
    console.log(`${vertice_actual["valor"]}`);
    if (vertice_actual["valor"] == fin["valor"]) return;

    // Codigo para invertir la lista si es necesario
    const adjacencias = vertice_actual.adjacencias;

    if (adjacencias.length !== 0) {
      // nuestras "soluciones" son los nodos vecinos, nosostros
      // debemos establecer una heuristica, esta debe servir como
      // criterio para ordenar, la forma mas facil es definir una
      // funcion que reciba los argumentos necesarios, muchas veces
      // son el vertice actual o el vertice destino y la adjacencia,
      // para obtener un numero, y ordenar la lista en base a ese numero
      //
      // el reto de este algoritmo está en que definas una buena heuristica
      // y que el numero que devuelvas o tu criterio de orden sea correcto
      // para que haga lo que estás esperando, si no, será error de capa 8
      //
      // Te recomiendo investigar el metodo sort de las listas de python,
      // las funciones anónimas (javascript) o apuntadores a funciones (C)
      // o closures (python) y las lambdas (python y creo java), porque
      // los metodos sort nos van a facilitar el que nosotros ordenemos la
      // lista, la neta el typescript no le entiendo a su metodo sort, pero
      // en python es mas facil de entender xd

      // hill_climbing
      vertices_a_chequiar.sort(
        (a, b) => heuristica(a, fin) - heuristica(b, fin),
      );

      // Aquí para A* lo unico que cambia es que aparte de considerar
      // la heuristica haces lo de g + heuristica, puedes hacer dos
      // funciones, una para g y otra para h, y como python permite definir
      // funciones dentro de funciones haces algo como:

      // yo defino g porque no la tengo xd, es una funcion aunque lo defina
      // raro, es pal ejemplo nmas
      //
      const g = (vertice: Node) => vertice.valor; // No tiene sentido pero tu le pones la heuristica que te digan

      // y dentro defines una funcion f, y te aseguras que reciba los argumentos
      // necesarios para g y para la heuristica
      function f(vertice_actual: Node, fin: Node) {
        return g(vertice_actual) + heuristica(vertice_actual, fin);
      }

      // A*
      // vertices_a_chequiar.sort((a, b) => f(a, fin) - f(b, fin));

      // Puede darse el caso donde la heuristica minima la tengan varios, asi
      // que toca separarlos

      // Obtener la heuristica minima, ya sabemos que el primer elemento
      // debe ser el de menor heuristica
      const min_h = heuristica(vertices_a_chequiar[0], fin);

      // Buscar si hay mas soluciones minimas y guardarlas
      const soluciones_minimas = [];
      for (const solucion of vertices_a_chequiar) {
        if (heuristica(solucion, fin) === min_h) {
          soluciones_minimas.push(solucion);
        }
      }

      // Aqui depende de juanpaulo que hacen, si eligen una al azar o algo
      // yo voy a usar la primera

      const eleccion = soluciones_minimas[0];

      // Segun yo en hill climbing dijo Deny que descartas las demas opciones
      vertices_a_chequiar = [eleccion];

      // Para A* (segun Deny) no se descartan, asi que deberia ser algo como
      // vertices_a_chequiar.push(eleccion);
    }
  }
}

const nodo1: Node = { valor: 1, adjacencias: [] };
const nodo2: Node = { valor: 2, adjacencias: [] };
const nodo3: Node = { valor: 3, adjacencias: [] };
const nodo4: Node = { valor: 4, adjacencias: [] };

nodo1["adjacencias"] = [nodo2, nodo3];
nodo2["adjacencias"] = [nodo3, nodo4];
nodo3["adjacencias"] = [nodo1];

hill_climbing_o_a_estrella(nodo1, nodo4);
