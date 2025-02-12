use std::{cell::RefCell, marker::PhantomData, rc::Rc};

/// Alias para una instancia de un vértice.
///
/// Se utiliza `Rc<RefCell<...>>` para permitir el uso compartido y la modificación interna
/// del vértice.
pub type VertexInstance<T, A> = Rc<RefCell<Vertex<T, A>>>;

/// Define la relación de adyacencia entre vértices.
///
/// Este trait abstrae el concepto de conexión entre vértices, permitiendo implementar
/// diferentes tipos de adyacencias (por ejemplo, ponderadas y no ponderadas).
pub trait Adjacency<T>
where
    T: Clone,
{
    /// Retorna la instancia del vértice conectado por esta adyacencia.
    fn vertex(&self) -> VertexInstance<T, Self>
    where
        Self: Sized;
}

/// Representa un vértice en un grafo.
///
/// Un vértice almacena un valor de tipo `T` y mantiene una lista de adyacencias (aristas)
/// de tipo `A`. Se requiere que `T` implemente `Clone` y que `A` implemente el trait
/// [`Adjacency<T>`](trait.Adjacency.html).
#[derive(Debug)]
pub struct Vertex<T, A>
where
    T: Clone,
    A: Adjacency<T>,
{
    /// Valor almacenado en el vértice.
    pub value: T,
    /// Lista de adyacencias (conexiones a otros vértices).
    adjacencies: Vec<A>,
}

impl<T, A> Vertex<T, A>
where
    T: Clone,
    A: Adjacency<T>,
{
    /// Crea un nuevo vértice con el valor especificado.
    ///
    /// # Argumentos
    ///
    /// * `value` - Valor que se asignará al vértice.
    ///
    /// # Retorna
    ///
    /// Una instancia de `Vertex` envuelta en `Rc<RefCell<...>>` para manejo compartido.
    pub fn new(value: T) -> VertexInstance<T, A> {
        Rc::new(RefCell::new(Self {
            value,
            adjacencies: Vec::new(),
        }))
    }

    /// Agrega múltiples adyacencias al vértice.
    ///
    /// # Argumentos
    ///
    /// * `adjacencies` - Colección de adyacencias a agregar.
    pub fn add_adjacencies<I>(&mut self, adjacencies: I)
    where
        I: IntoIterator<Item = A>,
    {
        self.adjacencies.extend(adjacencies);
    }

    /// Obtiene una referencia a la adyacencia en la posición indicada.
    ///
    /// # Argumentos
    ///
    /// * `index` - Posición de la adyacencia deseada.
    ///
    /// # Retorna
    ///
    /// * `Some(&A)` si existe una adyacencia en el índice indicado.
    /// * `None` en caso contrario.
    pub fn get(&self, index: usize) -> Option<&A> {
        self.adjacencies.get(index)
    }

    /// Remueve la adyacencia en la posición indicada y la retorna.
    ///
    /// # Argumentos
    ///
    /// * `index` - Posición de la adyacencia a remover.
    ///
    /// # Retorna
    ///
    /// * `Some(A)` si la adyacencia fue removida.
    /// * `None` si el índice no es válido.
    pub fn remove(&mut self, index: usize) -> Option<A> {
        if index < self.adjacencies.len() {
            Some(self.adjacencies.remove(index))
        } else {
            None
        }
    }

    /// Devuelve una slice con todas las adyacencias del vértice.
    pub fn adjacencies(&self) -> &[A] {
        &self.adjacencies
    }
}

/// Representa una adyacencia no ponderada.
///
/// Se utiliza para conectar vértices sin asignarles un peso adicional.
pub struct NonWeightedAdjacency<T>
where
    T: Clone,
{
    /// Instancia del vértice conectado por esta adyacencia.
    pub vertex: VertexInstance<T, NonWeightedAdjacency<T>>,
}

impl<T> NonWeightedAdjacency<T>
where
    T: Clone,
{
    /// Crea una nueva adyacencia no ponderada.
    ///
    /// # Argumentos
    ///
    /// * `vertex` - Instancia del vértice al que se conecta.
    pub fn new(vertex: VertexInstance<T, Self>) -> Self {
        Self { vertex }
    }
}

impl<T> Adjacency<T> for NonWeightedAdjacency<T>
where
    T: Clone,
{
    /// Retorna la instancia del vértice conectado por esta adyacencia.
    fn vertex(&self) -> VertexInstance<T, Self> {
        self.vertex.clone()
    }
}

/// Representa una adyacencia ponderada.
///
/// Se utiliza para conectar vértices asignándoles un peso a la conexión.
pub struct WeightedAdjacency<T>
where
    T: Clone,
{
    /// Instancia del vértice conectado por esta adyacencia.
    pub vertex: VertexInstance<T, WeightedAdjacency<T>>,
    /// Peso asignado a la conexión.
    pub weight: f64,
}

impl<T> WeightedAdjacency<T>
where
    T: Clone,
{
    /// Crea una nueva adyacencia ponderada.
    ///
    /// # Argumentos
    ///
    /// * `vertex` - Instancia del vértice al que se conecta.
    /// * `weight` - Peso de la conexión.
    pub fn new(vertex: VertexInstance<T, Self>, weight: f64) -> Self {
        Self { vertex, weight }
    }
}

impl<T> Adjacency<T> for WeightedAdjacency<T>
where
    T: Clone,
{
    /// Retorna la instancia del vértice conectado por esta adyacencia.
    fn vertex(&self) -> VertexInstance<T, Self> {
        self.vertex.clone()
    }
}

/// Tipo que representa la ausencia de un valor en el vértice.
///
/// Se utiliza en el patrón builder para indicar que aún no se ha asignado un valor.
#[derive(Debug, Clone, Default)]
pub struct NoValue;

/// Wrapper para encapsular un valor en el vértice.
#[derive(Debug, Clone)]
pub struct Value<T: Clone>(T);

/// Builder para la creación de vértices con adyacencias ponderadas.
///
/// Este builder permite construir de manera encadenada un vértice, asignándole
/// un valor y agregando una o más adyacencias ponderadas.
pub struct WVertexBuilder<T, V>
where
    T: Clone,
{
    _p: PhantomData<T>,
    /// Valor del vértice. Puede ser `NoValue` o `Value<T>`.
    value: V,
    /// Lista de adyacencias ponderadas a agregar al vértice.
    adjacencies: Vec<WeightedAdjacency<T>>,
}

impl<T> WVertexBuilder<T, Value<T>>
where
    T: Clone,
{
    /// Construye el vértice a partir de los datos acumulados en el builder.
    ///
    /// # Retorna
    ///
    /// Una instancia de `Vertex` envuelta en `Rc<RefCell<...>>`.
    pub fn build(self) -> VertexInstance<T, WeightedAdjacency<T>> {
        Rc::new(RefCell::new(Vertex {
            value: self.value.0,
            adjacencies: self.adjacencies,
        }))
    }
}

impl<T, V> WVertexBuilder<T, V>
where
    T: Clone,
{
    /// Agrega una adyacencia ponderada al vértice.
    ///
    /// # Argumentos
    ///
    /// * `vertex` - Instancia del vértice al que se conecta.
    /// * `weight` - Peso de la adyacencia.
    ///
    /// # Retorna
    ///
    /// El builder actualizado, permitiendo encadenar más llamadas.
    pub fn adjacency(
        self,
        vertex: VertexInstance<T, WeightedAdjacency<T>>,
        weight: f64,
    ) -> WVertexBuilder<T, V> {
        let mut builder = WVertexBuilder {
            value: self.value,
            _p: self._p,
            adjacencies: self.adjacencies,
        };

        builder
            .adjacencies
            .push(WeightedAdjacency::new(vertex, weight));
        builder
    }

    /// Agrega múltiples adyacencias ponderadas al vértice.
    ///
    /// # Argumentos
    ///
    /// * `adjacencies` - Colección de adyacencias ponderadas.
    ///
    /// # Retorna
    ///
    /// El builder actualizado.
    pub fn adjacencies<I>(mut self, adjacencies: I) -> Self
    where
        I: IntoIterator<Item = WeightedAdjacency<T>>,
    {
        self.adjacencies.extend(adjacencies);
        self
    }
}

impl<T> WVertexBuilder<T, NoValue>
where
    T: Clone,
{
    /// Crea un nuevo builder para vértices ponderados sin un valor asignado.
    pub fn new() -> WVertexBuilder<T, NoValue> {
        WVertexBuilder {
            value: NoValue::default(),
            adjacencies: Vec::new(),
            _p: PhantomData::default(),
        }
    }
}

impl<T> WVertexBuilder<T, NoValue>
where
    T: Clone,
{
    /// Asigna un valor al vértice en el builder.
    ///
    /// # Argumentos
    ///
    /// * `value` - Valor a asignar al vértice.
    ///
    /// # Retorna
    ///
    /// Un builder con el valor establecido, permitiendo posteriormente agregar adyacencias.
    pub fn value(self, value: T) -> WVertexBuilder<T, Value<T>> {
        WVertexBuilder {
            value: Value(value),
            adjacencies: self.adjacencies,
            _p: self._p,
        }
    }
}

/// Builder para la creación de vértices con adyacencias no ponderadas.
///
/// Este builder permite construir un vértice sin pesos en sus conexiones.
pub struct NWVertexBuilder<T, V>
where
    T: Clone,
{
    _p: PhantomData<T>,
    /// Valor del vértice. Puede ser `NoValue` o `Value<T>`.
    value: V,
    /// Lista de adyacencias no ponderadas a agregar al vértice.
    adjacencies: Vec<NonWeightedAdjacency<T>>,
}

impl<T> NWVertexBuilder<T, Value<T>>
where
    T: Clone,
{
    /// Construye el vértice a partir de los datos acumulados en el builder.
    ///
    /// # Retorna
    ///
    /// Una instancia de `Vertex` envuelta en `Rc<RefCell<...>>`.
    pub fn build(self) -> VertexInstance<T, NonWeightedAdjacency<T>> {
        Rc::new(RefCell::new(Vertex {
            value: self.value.0,
            adjacencies: self.adjacencies,
        }))
    }
}

impl<T, V> NWVertexBuilder<T, V>
where
    T: Clone,
{
    /// Agrega una adyacencia no ponderada al vértice.
    ///
    /// # Argumentos
    ///
    /// * `vertex` - Instancia del vértice al que se conecta.
    ///
    /// # Retorna
    ///
    /// El builder actualizado, permitiendo encadenar llamadas.
    pub fn adjacency(
        self,
        vertex: VertexInstance<T, NonWeightedAdjacency<T>>,
    ) -> NWVertexBuilder<T, V> {
        let mut builder = NWVertexBuilder {
            value: self.value,
            _p: self._p,
            adjacencies: self.adjacencies,
        };

        builder.adjacencies.push(NonWeightedAdjacency::new(vertex));
        builder
    }

    /// Agrega múltiples adyacencias no ponderadas al vértice.
    ///
    /// # Argumentos
    ///
    /// * `adjacencies` - Colección de adyacencias no ponderadas.
    ///
    /// # Retorna
    ///
    /// El builder actualizado.
    pub fn adjacencies<I>(mut self, adjacencies: I) -> Self
    where
        I: IntoIterator<Item = NonWeightedAdjacency<T>>,
    {
        self.adjacencies.extend(adjacencies);
        self
    }
}

impl<T> NWVertexBuilder<T, NoValue>
where
    T: Clone,
{
    /// Crea un nuevo builder para vértices no ponderados sin un valor asignado.
    pub fn new() -> NWVertexBuilder<T, NoValue> {
        NWVertexBuilder {
            value: NoValue::default(),
            adjacencies: Vec::new(),
            _p: PhantomData::default(),
        }
    }
}

impl<T> NWVertexBuilder<T, NoValue>
where
    T: Clone,
{
    /// Asigna un valor al vértice en el builder.
    ///
    /// # Argumentos
    ///
    /// * `value` - Valor a asignar al vértice.
    ///
    /// # Retorna
    ///
    /// Un builder con el valor establecido, permitiendo posteriormente agregar adyacencias.
    pub fn value(self, value: T) -> NWVertexBuilder<T, Value<T>> {
        NWVertexBuilder {
            value: Value(value),
            adjacencies: self.adjacencies,
            _p: self._p,
        }
    }
}
