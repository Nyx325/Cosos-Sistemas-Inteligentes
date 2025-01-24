# Cosos sistemas inteligentes

Todo el codigo que haga respecto a sistemas inteligentes
como siempre programado de forma rara con tipado porque
odio los errores en runtime por tipado

## TODO

- [ ] Impl busqueda con limite de nivel `BFS`:
  - La idea es tener un contador de el nivel actual y
    los nodos que hay que agregar al contenedor para
    pasar al siguiente nivel. Es decir, dado el nodo
    de inicio, se considera nivel 1, y se agregan los `n`
    nodos hijos al contenedor, y se tiene un conteo de
    una vez visitados, una vez se visiten `n` nodos se
    aumenta el contador de nivel. Una vez el contador
    de nivel sea mayor al nivel limite se finaliza el
    recorrido
- [ ] Pensar en como hacer el algoritmo con limite de
      nivel en `DFS`
  - Se podría asumir que cada que agregamos al contenedor
    estamos bajando un nivel, sólo necesitamos tener un
    conteo de cuánto bajamos y dejar de agregar al contenedor
    si llegamos vamos a sobrepasar el nivel límite, creo
  - Tener una lista de vertices que estoy considerando que
    hay por cada nivel, una vez no se agreguen más vertices
    al nivel empiezo a descontar de la lista hasta finalmente
    sacar de esa lista ese nivel, e ir recorriendo esto
    recursivamente y mirando el nivel máximo que estoy por
    ramificación
  1. Inicia algoritmo. Nivel 0, 0 en pila
  2. Agrego un nodo a la pila, nivel actual 0,
  3. Agrego 3 a la pila, nivel actual 1
  4.
