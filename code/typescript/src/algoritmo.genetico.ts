import { randomInt } from "crypto";

/**
 * Tipo de dato que presenta un elemento de un algoritmo
 * genetico capaz de tener un valor, codificacion y fitness
 */
export type Pueblerino<V, C> = {
  valor: V;
  codificacion: C;
  fitness: number;
};

export enum MetodoSeleccion {
  ELITISMO,
  RANGOS,
  RULETA,
}

export class AlgoritmoGenetico<V, C> {
  private cruza: (poblacion: Pueblerino<V, C>[]) => Pueblerino<V, C>[];
  private muta: (poblacion: Pueblerino<V, C>[]) => Pueblerino<V, C>[];
  private paro: (poblacion: Pueblerino<V, C>[]) => boolean;

  constructor() {
    const notImp = () => {
      throw Error("Method undefined");
    };

    this.cruza = notImp;
    this.muta = notImp;
    this.paro = notImp;
  }

  public onCruza(fn: (poblacion: Pueblerino<V, C>[]) => Pueblerino<V, C>[]) {
    this.cruza = fn;
  }

  public onMuta(fn: (poblacion: Pueblerino<V, C>[]) => Pueblerino<V, C>[]) {
    this.muta = fn;
  }

  public onEvalParo(fn: (poblacion: Pueblerino<V, C>[]) => boolean) {
    this.paro = fn;
  }

  public ejecutarAlgoritmo(
    poblacion: Pueblerino<V, C>[],
    seleccion: MetodoSeleccion,
    limiteGeneracion?: number,
  ) {
    let poblacionCpy = [...poblacion];
    let generacion = 0;

    // Tipo para el prototipo de funcion que hace la selección
    type FuncionSeleccion<V, C> = (
      pueblerinos: Pueblerino<V, C>[],
    ) => Pueblerino<V, C>[];

    // Crear un diccionario que contenga una funcion dado un enum
    // para evitar usar un switch en lugar de usar un switch
    const seleccionMatcher: {
      [key in MetodoSeleccion]: FuncionSeleccion<V, C>;
    } = {
      [MetodoSeleccion.RULETA]: this.ruleta.bind(this),
      [MetodoSeleccion.ELITISMO]: this.elitismo.bind(this),
      [MetodoSeleccion.RANGOS]: this.rangos.bind(this),
    };

    while (
      this.paro(poblacionCpy) != true &&
      (limiteGeneracion === undefined || generacion <= limiteGeneracion)
    ) {
      //Seleccionar mejores
      poblacionCpy = seleccionMatcher[seleccion](poblacionCpy);
      poblacionCpy = this.cruza(poblacionCpy);
      poblacionCpy = this.muta(poblacionCpy);

      console.log(`Generacion: ${generacion}`);
      console.log(poblacionCpy);

      generacion += 1;
    }
  }

  public elitismo(poblacion: Pueblerino<V, C>[]): Pueblerino<V, C>[] {
    const nuevaPoblacion: Pueblerino<V, C>[] = [];

    const mejor = poblacion.reduce((a, b) => (a.fitness > b.fitness ? a : b));

    nuevaPoblacion.push(mejor);

    const maxIndex = poblacion.length - 1;
    for (let i = 0; i < maxIndex; i++) {
      const ind1 = randomInt(0, maxIndex);
      let ind2;
      do {
        ind2 = randomInt(0, maxIndex);
      } while (ind1 === ind2);

      const p1 = poblacion[ind1];
      const p2 = poblacion[ind2];
      if (p1.fitness > p2.fitness) {
        nuevaPoblacion.push(p1);
      } else {
        nuevaPoblacion.push(p2);
      }
    }

    return nuevaPoblacion;
  }

  public rangos(poblacion: Pueblerino<V, C>[]): Pueblerino<V, C>[] {
    const nuevaPoblacion = [];

    const poblacionOrdenada = [...poblacion].sort(
      (a, b) => a.fitness - b.fitness,
    );

    const size = poblacion.length;
    const sumatoria_ranking = (size * (size + 1)) / 2;

    const rangos = [0];

    for (let i = 0; i < size; i++) {
      const porcentaje = (i + 1) / sumatoria_ranking;
      const porcentajeAcumulado = rangos[i] + porcentaje;
      const redondeo = parseFloat(porcentajeAcumulado.toFixed(2));
      rangos.push(redondeo);
    }

    for (let i = 0; i < size; i++) {
      const randomNum = Math.random();

      for (let i = 1; i < rangos.length; i++) {
        if (rangos[i - 1] <= randomNum && randomNum < rangos[i]) {
          const seleccionado = poblacionOrdenada[i - 1];
          nuevaPoblacion.push(seleccionado);
          break;
        }
      }
    }

    return nuevaPoblacion;
  }

  public ruleta(poblacion: Pueblerino<V, C>[]): Pueblerino<V, C>[] {
    const nuevaPoblacion = [];

    const poblacionOrdenada = [...poblacion]
      .sort((a, b) => a.fitness - b.fitness)
      .reverse();

    const aptitudTotal = poblacionOrdenada.reduce(
      (acumulador, valor) => acumulador + valor.fitness, // Operacion por iteracion
      0, // Valor inicial del acumulador
    );

    const size = poblacionOrdenada.length;
    const rangos = [0];
    for (let i = 0; i < size; i++) {
      const p = poblacionOrdenada[i];
      const porcentaje = p.fitness / aptitudTotal;
      const porcentajeAcumulado = rangos[i] + porcentaje;
      const redondeo = parseFloat(porcentajeAcumulado.toFixed(2));
      rangos.push(redondeo);
    }

    for (let i = 0; i < size; i++) {
      const randomNum = Math.random();

      for (let i = 1; i < rangos.length; i++) {
        if (rangos[i - 1] <= randomNum && randomNum < rangos[i]) {
          const seleccionado = poblacionOrdenada[i - 1];
          nuevaPoblacion.push(seleccionado);
          break;
        }
      }
    }

    return nuevaPoblacion;
  }
}
