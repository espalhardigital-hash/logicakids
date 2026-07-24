export interface LevelMap {
  id: number;
  name: string;
  seccion: number;
  operacion: string;
  isChallenge?: boolean;
}

export interface ModuleMap {
  id: number;
  name: string;
  levels: LevelMap[];
}

export interface PhaseMap {
  id: number;
  name: string;
  modules: ModuleMap[];
  levels?: LevelMap[]; // Optional: direct levels (used in ContentTab for Fase 1 compatibility)
}

export const PHASE_MAPS: PhaseMap[] = [
  {
    id: 1,
    name: "Fase 1: Aritmética Básica",
    modules: [
      {
        id: 1,
        name: "Operaciones Directas",
        levels: [
          {
            id: 1,
            name: "Suma Directa",
            seccion: 1,
            operacion: "suma"
          },
          {
            id: 2,
            name: "Resta Directa",
            seccion: 1,
            operacion: "resta"
          },
          {
            id: 3,
            name: "Multiplicación Directa",
            seccion: 1,
            operacion: "multiplicacion"
          },
          {
            id: 4,
            name: "División Directa",
            seccion: 1,
            operacion: "division"
          },
          {
            id: 99,
            name: "Desafío Mixto (Examen Final)",
            seccion: 99099,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      }
    ]
  },
  {
    id: 2,
    name: "Fase 2: Desarrollo Numérico",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Gimnasio Numérico Mental",
        levels: [
          {
            id: 1,
            name: "Multiplicadores de Tamaño",
            seccion: 101,
            operacion: "suma"
          },
          {
            id: 2,
            name: "Jerarquía Lógica",
            seccion: 102,
            operacion: "suma"
          },
          {
            id: 3,
            name: "Traducción Lógica",
            seccion: 103,
            operacion: "suma"
          },
          {
            id: 11,
            name: "Desafío 1 (Estándar)",
            seccion: 1011,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 12,
            name: "Desafío 2 (Avanzado)",
            seccion: 1012,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 13,
            name: "Desafío Final (Maestría)",
            seccion: 1013,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Tablas en Acción",
        levels: [
          {
            id: 1,
            name: "Suma e Inversa",
            seccion: 201,
            operacion: "multiplicacion"
          },
          {
            id: 2,
            name: "Multiplicación e Inversa",
            seccion: 202,
            operacion: "multiplicacion"
          },
          {
            id: 3,
            name: "El Número Faltante",
            seccion: 203,
            operacion: "multiplicacion"
          },
          {
            id: 4,
            name: "Gran Integración",
            seccion: 204,
            operacion: "multiplicacion"
          },
          {
            id: 11,
            name: "Desafío 1 (Estándar)",
            seccion: 2011,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 12,
            name: "Desafío 2 (Avanzado)",
            seccion: 2012,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 13,
            name: "Desafío Final (Maestría)",
            seccion: 2013,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Tienda Matemática",
        levels: [
          {
            id: 1,
            name: "Reconozco el Dinero",
            seccion: 301,
            operacion: "mixta"
          },
          {
            id: 2,
            name: "Pago y Cambio",
            seccion: 302,
            operacion: "mixta"
          },
          {
            id: 3,
            name: "Carrito de Compras",
            seccion: 303,
            operacion: "mixta"
          },
          {
            id: 4,
            name: "Comprador Inteligente",
            seccion: 304,
            operacion: "mixta"
          },
          {
            id: 11,
            name: "Desafío 1 (Estándar)",
            seccion: 3011,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 12,
            name: "Desafío 2 (Avanzado)",
            seccion: 3012,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 13,
            name: "Desafío Final (Maestría)",
            seccion: 3013,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Constructor de Soluciones",
        levels: [
          {
            id: 1,
            name: "Dos Pasos Guiados",
            seccion: 401,
            operacion: "mixta"
          },
          {
            id: 2,
            name: "Encadenamiento",
            seccion: 402,
            operacion: "mixta"
          },
          {
            id: 3,
            name: "Error de Arrastre",
            seccion: 403,
            operacion: "mixta"
          },
          {
            id: 11,
            name: "Desafío 1 (Estándar)",
            seccion: 4011,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 12,
            name: "Desafío 2 (Avanzado)",
            seccion: 4012,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 13,
            name: "Desafío Final (Maestría)",
            seccion: 4013,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          {
            id: 99,
            name: "Desafío Mixto (Examen Final)",
            seccion: 99099,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      }
    ]
  },
  {
    id: 3,
    name: "Fase 3: Problemas de Texto y Sistemas Simples",
    modules: [
      {
        id: 1,
        name: "Módulo 1: El Detective Literario",
        levels: [
          { id: 1, name: "Aislamiento de Variables Críticas", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Datos Útiles vs. Datos Basura", seccion: 102, operacion: "mixta" },
          { id: 3, name: "Descarte por Incongruencia", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Secuencia Temporal",
        levels: [
          { id: 1, name: "Operaciones Cronológicas", seccion: 201, operacion: "mixta" },
          { id: 2, name: "Álgebra Retrospectiva", seccion: 202, operacion: "mixta" },
          { id: 3, name: "Mutaciones Sucesivas", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Deducción de Precios",
        levels: [
          { id: 1, name: "Comparación de Carritos", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Grilla de Doble Entrada", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Álgebra Visual", seccion: 303, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Reparto y Residuos",
        levels: [
          { id: 1, name: "Agrupación Visual", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Análisis de Resto", seccion: 402, operacion: "mixta" },
          { id: 3, name: "Sucesión Circular", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 5,
        name: "Módulo 5: Ciclos y Agrupaciones Máximas",
        levels: [
          { id: 1, name: "Visualización de Saltos y Empaques", seccion: 501, operacion: "mixta" },
          { id: 2, name: "Encuentros Periódicos - MCM", seccion: 502, operacion: "mixta" },
          { id: 3, name: "División Máxima Exacta - MCD", seccion: 503, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 5011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 5012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 5013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Desafío Mixto (Examen Final)", seccion: 99099, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
  {
    id: 4,
    name: "Fase 4: Fracciones y Proporciones",
    modules: [
      {
        id: 1,
        name: "Módulo 1: La Fracción Visual",
        levels: [
          { id: 1, name: "Lectura de Fracciones", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Fracciones Equivalentes", seccion: 102, operacion: "mixta" },
          { id: 3, name: "Áreas y Asimetrías", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Fracción de Cantidad",
        levels: [
          { id: 1, name: "Porciones de un Grupo", seccion: 201, operacion: "mixta" },
          { id: 2, name: "El Motor de Dos Pasos", seccion: 202, operacion: "mixta" },
          { id: 3, name: "Lógica del Complemento", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Porcentajes Rápidos",
        levels: [
          { id: 1, name: "Porcentajes Intuitivos", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Gráficos Circulares", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Gráficos de Barras", seccion: 303, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Razón y Mezclas",
        levels: [
          { id: 1, name: "Razones y Proporciones", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Reparto de Volúmenes", seccion: 402, operacion: "mixta" },
          { id: 3, name: "Mezclas Complejas", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Examen Final Fase 4", seccion: 999, operacion: "mixta" }
        ]
      }
    ]
  },
    {
    id: 5,
    name: "Fase 5: Operatoria Decimal y Conversiones",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Suma y Resta de Decimales",
        levels: [
          { id: 1, name: "Suma alineando la coma", seccion: 101, operacion: "suma" },
          { id: 2, name: "Resta con completado de ceros", seccion: 102, operacion: "resta" },
          { id: 3, name: "Combinadas en contexto", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Multiplicación y División de Decimales",
        levels: [
          { id: 1, name: "Multiplicación con conteo de posiciones", seccion: 201, operacion: "multiplicacion" },
          { id: 2, name: "División con desplazamiento de la coma", seccion: 202, operacion: "division" },
          { id: 3, name: "Repartición y costo unitario", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Medidas de Longitud",
        levels: [
          { id: 1, name: "Escalera métrica lineal", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Operaciones con unidades mixtas", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Escalas de mapas y rutas por tramos", seccion: 303, operacion: "mixta" },
          { id: 11, name: "Desafío 1", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Medidas de Volumen",
        levels: [
          { id: 1, name: "Escalera cúbica", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Volumen y capacidad: dm³=L, cm³=mL", seccion: 402, operacion: "mixta" },
          { id: 3, name: "Problemas de capacidad en contexto", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 5,
        name: "Módulo 5: Unidades de Superficie",
        levels: [
          { id: 1, name: "Escalera cuadrada", seccion: 501, operacion: "mixta" },
          { id: 2, name: "Pulgadas y pies a cm", seccion: 502, operacion: "mixta" },
          { id: 3, name: "Hectáreas, m² y reparto en lotes", seccion: 503, operacion: "mixta" },
          { id: 11, name: "Desafío 1", seccion: 5011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2", seccion: 5012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final", seccion: 5013, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
{
    id: 5,
    name: "Fase 6: Geometría Plana Multiforme y Áreas",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Perímetro y Borde",
        levels: [
          { id: 1, name: "Conteo directo de unidades lineales", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Cálculo analítico de perímetros", seccion: 102, operacion: "mixta" },
          { id: 3, name: "Conversión de unidades de longitud", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Área en Malha",
        levels: [
          { id: 1, name: "Conteo analítico de unidades (u²)", seccion: 201, operacion: "mixta" },
          { id: 2, name: "Fusión de sectores triangulares", seccion: 202, operacion: "mixta" },
          { id: 3, name: "Estimación de áreas irregulares", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Figuras Compuestas y Simetría",
        levels: [
          { id: 1, name: "Descomposición de polígonos", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Conservación del área (Tangram)", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Cálculo de áreas sombreadas", seccion: 303, operacion: "mixta" },
          { id: 4, name: "Identificación de Ejes de Simetría", seccion: 304, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Conversión y Pantallas",
        levels: [
          { id: 1, name: "Escala gráfica: unidades reales", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Diagonal como medida estándar", seccion: 402, operacion: "mixta" },
          { id: 3, name: "Conversión de unidades de superficie (m², cm², dm²)", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Desafío Mixto (Examen Final)", seccion: 99099, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
  {
    id: 6,
    name: "Fase 7: Geometría Espacial, Volumen y Magnitudes",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Reconocimiento 3D",
        levels: [
          { id: 1, name: "Identificación de poliedros (caras, aristas, vértices)", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Detección de bloques ocultos por perspectiva", seccion: 102, operacion: "mixta" },
          { id: 3, name: "Planificaciones (moldes desplegados) y sólidos 3D", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Patrones de Crecimiento",
        levels: [
          { id: 1, name: "Sucesiones geométricas tridimensionales", seccion: 201, operacion: "mixta" },
          { id: 2, name: "Conteo volumétrico estratificado por capas", seccion: 202, operacion: "mixta" },
          { id: 3, name: "Generalización algebraica: bloques en etapa N", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Cubos Unitarios",
        levels: [
          { id: 1, name: "Volumen: suma de unidades cúbicas (u³)", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Cálculo en prismas: Largo × Ancho × Alto", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Conversión: volumen cúbico y capacidad en litros", seccion: 303, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Medidas de Masa y Temperatura",
        levels: [
          { id: 1, name: "Balanzas y Termómetros analógicos (kg, g, °C)", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Variaciones térmicas lineales en Celsius", seccion: 402, operacion: "mixta" },
          { id: 3, name: "La Máquina Kelvin: conversión °C ↔ K (±273)", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Desafío Mixto (Examen Final)", seccion: 99099, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
  {
    id: 7,
    name: "Fase 8: Coordenadas, Rutas y Tiempo",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Orientación Cardinal y Ángulos",
        levels: [
          { id: 1, name: "Puntos Cardinales y giros de 90° y 180°", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Instrucciones verbales a trayectos vectoriales", seccion: 102, operacion: "mixta" },
          { id: 3, name: "Trayectorias críticas y distancias en grillas", seccion: 103, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Plano Cartesiano",
        levels: [
          { id: 1, name: "Lectura y ubicación de pares ordenados (X, Y)", seccion: 201, operacion: "mixta" },
          { id: 2, name: "Traslación de figuras en el plano", seccion: 202, operacion: "mixta" },
          { id: 3, name: "Cálculo de Distancia Manhattan", seccion: 203, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: La Mecánica del Tiempo",
        levels: [
          { id: 1, name: "Lectura analógica y digital del reloj", seccion: 301, operacion: "mixta" },
          { id: 2, name: "Duración de eventos cruzando AM/PM y husos de 24h", seccion: 302, operacion: "mixta" },
          { id: 3, name: "Aritmética sexagesimal: adición y sustracción", seccion: 303, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 3011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 3012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 3013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 4,
        name: "Módulo 4: Horarios y Apps",
        levels: [
          { id: 1, name: "Lectura de tablas de horarios de transporte", seccion: 401, operacion: "mixta" },
          { id: 2, name: "Cálculo de tiempos compuestos y transbordos", seccion: 402, operacion: "mixta" },
          { id: 3, name: "Optimización: comparar opciones de transporte", seccion: 403, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 4011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 4012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 4013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Desafío Mixto (Examen Final)", seccion: 99099, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
  {
    id: 8,
    name: "Fase 8: Probabilidad y Lógica",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Combinatoria",
        levels: [
          { id: 1, name: "Arreglos Simples", seccion: 101, operacion: "mixta" },
          { id: 2, name: "Permutaciones", seccion: 102, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 1012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 1013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Probabilidad Básica",
        levels: [
          { id: 1, name: "Sucesos Posibles", seccion: 201, operacion: "mixta" },
          { id: 2, name: "Eventos Compuestos", seccion: 202, operacion: "mixta" },
          { id: 11, name: "Desafío 1 (Estándar)", seccion: 2011, operacion: "mixta", isChallenge: true },
          { id: 12, name: "Desafío 2 (Avanzado)", seccion: 2012, operacion: "mixta", isChallenge: true },
          { id: 13, name: "Desafío Final (Maestría)", seccion: 2013, operacion: "mixta", isChallenge: true }
        ]
      },
      {
        id: 99,
        name: "Graduación y Examen Final",
        levels: [
          { id: 99, name: "Desafío Mixto (Examen Final)", seccion: 99099, operacion: "mixta", isChallenge: true }
        ]
      }
    ]
  },
  {
    id: 9,
    name: "Fase 9: Simulados Colegio Pedro II",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Simulados Cortos",
        levels: [
          {
            id: 1,
            name: "Descubrimiento",
            seccion: 9011,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 2,
            name: "Consolidación",
            seccion: 9012,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 3,
            name: "Fluidez",
            seccion: 9013,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 4,
            name: "Desafío 1: Filtro de Tiempo",
            seccion: 9014,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 5,
            name: "Desafío 2: Enunciados Largos",
            seccion: 9015,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 6,
            name: "Desafío Final: Candado Corto",
            seccion: 9016,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 2,
        name: "Módulo 2: Simulados Completos",
        levels: [
          {
            id: 1,
            name: "Descubrimiento",
            seccion: 9021,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 2,
            name: "Consolidación",
            seccion: 9022,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 3,
            name: "Fluidez",
            seccion: 9023,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 4,
            name: "Desafío 1: Corte Resistencia",
            seccion: 9024,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 5,
            name: "Desafío 2: Banco Error",
            seccion: 9025,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 6,
            name: "Desafío Final: Maestro",
            seccion: 9026,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      },
      {
        id: 3,
        name: "Módulo 3: Revisión Dirigida y Tutoría IA",
        levels: [
          {
            id: 1,
            name: "Descubrimiento",
            seccion: 9031,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 2,
            name: "Consolidación",
            seccion: 9032,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 3,
            name: "Fluidez",
            seccion: 9033,
            operacion: "mixta",
            isChallenge: false
          },
          {
            id: 4,
            name: "Desafío 1: Filtro Corrección",
            seccion: 9034,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 5,
            name: "Desafío 2: Trampa Recurrente",
            seccion: 9035,
            operacion: "mixta",
            isChallenge: true
          },
          {
            id: 6,
            name: "Desafío Final: Graduación",
            seccion: 9036,
            operacion: "mixta",
            isChallenge: true
          }
        ]
      }
    ]
  }
];
