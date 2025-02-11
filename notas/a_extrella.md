# A estrella

## Pseudocodigo de clase

```
Algoritmo A*
    f(n)=g(n)+h(n) //solución actual
    f’(n)= g(n)+h(n) //solución nueva vecina

Crea una agenda de un elemento (el nodo raíz)
hasta que la agenda este vacía o se alcance la meta y los demás nodos sean de costos mayores o iguales a la meta
    if el primer elemento es la meta y los demás nodos son de menor o igual costo a la meta then
        acaba
    else
        elimina el primer elemento y
        agrega sus sucesores a la agenda
        ordena todos los elementos de la agenda de acuerdo a
        f(n)=g(n)+h(n)

    end if
Fin Repetir
```

## Pregunta a DeepSeek ¿El pseudocódigo es correcto?

El pseudocódigo presentado **no es completamente correcto** para el algoritmo A\* estándar. Aunque captura algunas ideas clave, tiene errores críticos que afectan su optimalidad y funcionamiento. Aquí el análisis detallado:

---

### **Problemas identificados**

1. **Condición de terminación incorrecta**:

   - El código verifica si el primer elemento es la meta y los demás nodos tienen un costo **menor o igual**. Esto está invertido.
   - **Corrección**: Cuando el nodo objetivo es seleccionado (primer elemento de la agenda), todos los demás nodos deben tener un costo \( f(n) \geq f(\text{meta}) \). La condición debe ser:  
     `if el primer elemento es la meta then acaba`  
     (sin necesidad de verificar los demás nodos, ya que A\* garantiza optimalidad si \( h(n) \) es admisible y consistente).

2. **Manejo de nodos repetidos y actualización de costos**:

   - El pseudocódigo no verifica si un nodo ya está en la agenda o ha sido visitado previamente, ni actualiza \( g(n) \) si se encuentra un camino mejor.
   - **Consecuencia**: Puede generar rutas subóptimas en grafos (no árboles) o entrar en bucles infinitos.

3. **Ineficiencia al ordenar toda la agenda**:

   - Ordenar toda la lista en cada iteración tiene complejidad \( O(n \log n) \). En A\* estándar se usa una **cola de prioridad** para inserción eficiente (\( O(\log n) \)).

4. **Expansión innecesaria del nodo meta**:
   - En A\*, si el primer elemento es la meta, se detiene inmediatamente. El código actual permite expandirla (agregar sus sucesores), lo cual es incorrecto.

---

### **Pseudocódigo Corregido (Esquemático)**

```plaintext
Algoritmo A*:
    Inicializar agenda como una cola de prioridad ordenada por f(n) = g(n) + h(n).
    Agregar nodo raíz a la agenda.

    Mientras la agenda no esté vacía:
        Extraer el nodo con menor f(n) (primero en la agenda).

        Si el nodo es la meta:
            Terminar (solución óptima encontrada).

        Expandir el nodo, generando sus sucesores.
        Para cada sucesor:
            Calcular g(nuevo) = g(nodo actual) + costo del paso.
            Si el sucesor ya está en la agenda o fue visitado:
                Si g(nuevo) < g(anterior):
                    Actualizar g(nuevo) y f(nuevo).
                    Reinsertar en la agenda.
            Sino:
                Agregar el sucesor a la agenda.

        Marcar el nodo actual como visitado.
```

---

### **Conclusión**

El pseudocódigo original:

- **No garantiza optimalidad** por no manejar nodos repetidos.
- **Es ineficiente** al ordenar toda la agenda en cada paso.
- **Tiene una condición de parada errónea**.

Para que A\* funcione correctamente, se requiere una **cola de prioridad**, una **heurística admisible/consistente**, y un mecanismo para actualizar costos en nodos ya explorados (usando una estructura como la **lista cerrada**).
