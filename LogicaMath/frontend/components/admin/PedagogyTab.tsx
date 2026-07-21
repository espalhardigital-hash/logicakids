import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings, Layers, Loader2, Cpu, Minimize2, Maximize2 } from 'lucide-react';
import { 
  getAdminSettings, saveAdminSettings, 
  getModularConfigs, saveModularConfig, createModularConfig 
} from '../../services/storageService';
import { useAutoSave } from './useAutoSave';
import { PedagogyConfig, ConfiguracionProgreso } from '../../types';
import { PhaseFlowDesigner } from './PhaseFlowDesigner';
import { ProgressConfigTable } from './ProgressConfigTable';
import { ConfigForm } from './ConfigForm';

// ==========================================
// INTERFACES
// ==========================================
interface StaticSubLevel {
  id: number;
  name: string;
}

interface StaticChallenge {
  id: number;
  name: string;
  defaultTime: number;
  defaultQty: number;
}

interface StaticModule {
  seccion: number;
  modulo_id?: number;
  operacion: string;
  name: string;
  levels?: StaticSubLevel[];
  challenges?: StaticChallenge[];
  isFinalExam?: boolean;
}

interface StaticPhase {
  id: number;
  name: string;
  description: string;
  modules: StaticModule[];
}

// ==========================================
// STATIC MAP OF PHASES
// ==========================================
const fase1Levels = [
  { id: 1, name: "Nivel 1: Fácil" },
  { id: 2, name: "Nivel 2: Medio-Fácil" },
  { id: 3, name: "Nivel 3: Medio" },
  { id: 4, name: "Nivel 4: Medio-Difícil" },
  { id: 5, name: "Nivel 5: Difícil" },
];

const fase1LevelsConTablas = [
  ...fase1Levels,
  { id: 6, name: "Nivel 6: Tablas Aleatorias" }
];

const STATIC_PHASES: StaticPhase[] = [
  {
    id: 1,
    name: "Fase 1: Aritmética Básica",
    description: "Sumas, restas, multiplicaciones y divisiones. ¡Calentamiento mental!",
    modules: [
      { seccion: 1, modulo_id: 1, operacion: "suma", name: "Suma Directa", levels: fase1Levels },
      { seccion: 1, modulo_id: 2, operacion: "resta", name: "Resta Directa", levels: fase1Levels },
      { seccion: 1, modulo_id: 3, operacion: "multiplicacion", name: "Multiplicación Directa", levels: fase1LevelsConTablas },
      { seccion: 1, modulo_id: 4, operacion: "division", name: "División Directa", levels: fase1Levels },
      { seccion: 1, modulo_id: 5, operacion: "mixta", name: "Desafío Mixto", levels: fase1Levels }
    ]
  },
  {
    id: 2,
    name: "Fase 2: Desarrollo Numérico",
    description: "Cálculo mental rápido, sistema monetario real y problemas matemáticos iniciales.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "suma",
        name: "Módulo 1: Gimnasio Numérico Mental",
        levels: [
          { id: 1, name: "Multiplicadores de Tamaño" },
          { id: 2, name: "Jerarquía Lógica" },
          { id: 3, name: "Traducción Lógica" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 25, defaultQty: 25 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 40, defaultQty: 25 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 50, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "multiplicacion",
        name: "Módulo 2: Tablas en Acción",
        levels: [
          { id: 1, name: "Suma e Inversa" },
          { id: 2, name: "Multiplicación e Inversa" },
          { id: 3, name: "El Número Faltante" },
          { id: 4, name: "Gran Integración" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 25, defaultQty: 25 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 40, defaultQty: 25 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 50, defaultQty: 10 }
        ]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta",
        name: "Módulo 3: Tienda Matemática",
        levels: [
          { id: 1, name: "Reconozco el Dinero" },
          { id: 2, name: "Pago y Cambio" },
          { id: 3, name: "Carrito de Compras" },
          { id: 4, name: "Comprador Inteligente" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 25, defaultQty: 25 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 40, defaultQty: 25 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 50, defaultQty: 10 }
        ]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta",
        name: "Módulo 4: Constructor de Soluciones",
        levels: [
          { id: 1, name: "Dos Pasos Guiados" },
          { id: 2, name: "Encadenamiento" },
          { id: 3, name: "Error de Arrastre" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 25, defaultQty: 25 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 40, defaultQty: 25 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 50, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 3,
    name: "Fase 3: Problemas de Texto y Sistemas Simples",
    description: "Selección de datos, elección reflexiva de operación y resolución de problemas de texto complejos.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta",
        name: "Módulo 1: El Detective Literario",
        levels: [
          { id: 1, name: "Aislamiento de Variables Críticas" },
          { id: 2, name: "Datos Útiles vs. Datos Basura" },
          { id: 3, name: "Descarte por Incongruencia" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta",
        name: "Módulo 2: Secuencia Temporal",
        levels: [
          { id: 1, name: "Operaciones aditivas acumulativas" },
          { id: 2, name: "Álgebra retrospectiva" },
          { id: 3, name: "Resolución de textos complejos" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta",
        name: "Módulo 3: Deducción de Precios",
        levels: [
          { id: 1, name: "Deducción de valores unitarios por diferencia" },
          { id: 2, name: "Completado analítico de tablas matriciales" },
          { id: 3, name: "Sistemas simples de dos variables" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta",
        name: "Módulo 4: Reparto y Residuos",
        levels: [
          { id: 1, name: "Cálculo de repartos exactos" },
          { id: 2, name: "Interpretación lógica del residuo" },
          { id: 3, name: "Patrones modulares y congruencias cíclicas" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 5, modulo_id: 5, operacion: "mixta",
        name: "Módulo 5: Ciclos y Agrupaciones Máximas",
        levels: [
          { id: 1, name: "Visualización de Saltos y Empaques" },
          { id: 2, name: "Encuentros Periódicos - MCM" },
          { id: 3, name: "División Máxima Exacta - MCD" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 4,
    name: "Fase 4: Fracciones y Proporciones",
    description: "Comprensión visual y numérica de fracciones, áreas y asimetrías.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta", name: "Módulo 1: La Fracción Visual",
        levels: [{ id: 1, name: "Lectura de Fracciones" }, { id: 2, name: "Fracciones Equivalentes" }, { id: 3, name: "Áreas y Asimetrías" }],
        challenges: [{ id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 }, { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 }, { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta", name: "Módulo 2: Fracción de Cantidad",
        levels: [{ id: 1, name: "Porciones de un Grupo" }, { id: 2, name: "El Motor de Dos Pasos" }, { id: 3, name: "Lógica del Complemento" }],
        challenges: [{ id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 }, { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 }, { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta", name: "Módulo 3: Porcentajes Rápidos",
        levels: [{ id: 1, name: "Porcentajes Intuitivos" }, { id: 2, name: "Gráficos Circulares" }, { id: 3, name: "Gráficos de Barras" }],
        challenges: [{ id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 }, { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 }, { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta", name: "Módulo 4: Razón y Mezclas",
        levels: [{ id: 1, name: "Razones y Proporciones" }, { id: 2, name: "Reparto de Volúmenes" }, { id: 3, name: "Mezclas Complejas" }],
        challenges: [{ id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 }, { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 }, { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 5,
    name: "Fase 5: Geometría Plana y Medidas",
    description: "Perímetros, áreas, figuras compuestas, simetría y conversión de unidades lineales y de superficie.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta",
        name: "Módulo 1: Perímetro y Borde",
        levels: [
          { id: 1, name: "Conteo directo de unidades lineales" },
          { id: 2, name: "Cálculo analítico de perímetros" },
          { id: 3, name: "Conversión de unidades de longitud" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta",
        name: "Módulo 2: Área en Malha",
        levels: [
          { id: 1, name: "Conteo analítico de unidades (u²)" },
          { id: 2, name: "Fusión de sectores triangulares" },
          { id: 3, name: "Estimación de áreas irregulares" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta",
        name: "Módulo 3: Figuras Compuestas y Simetría",
        levels: [
          { id: 1, name: "Descomposición de polígonos" },
          { id: 2, name: "Conservación del área (Tangram)" },
          { id: 3, name: "Cálculo de áreas sombreadas" },
          { id: 4, name: "Identificación de Ejes de Simetría" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta",
        name: "Módulo 4: Conversión y Pantallas",
        levels: [
          { id: 1, name: "Escala gráfica: unidades reales" },
          { id: 2, name: "Diagonal como medida estándar" },
          { id: 3, name: "Conversión de unidades de superficie (m², cm², dm²)" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 6,
    name: "Fase 6: Geometría Espacial, Volumen y Magnitudes Físicas",
    description: "Visualización tridimensional, razonamiento abstracto analítico y medición de magnitudes.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta",
        name: "Módulo 1: Reconocimiento 3D",
        levels: [
          { id: 1, name: "Identificación de poliedros (caras, aristas, vértices)" },
          { id: 2, name: "Detección de bloques ocultos por perspectiva" },
          { id: 3, name: "Planificaciones (moldes desplegados) y sólidos 3D" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta",
        name: "Módulo 2: Patrones de Crecimiento",
        levels: [
          { id: 1, name: "Sucesiones geométricas tridimensionales" },
          { id: 2, name: "Conteo volumétrico estratificado por capas" },
          { id: 3, name: "Generalización algebraica: bloques en etapa N" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta",
        name: "Módulo 3: Cubos Unitarios",
        levels: [
          { id: 1, name: "Volumen: suma de unidades cúbicas (u³)" },
          { id: 2, name: "Cálculo en prismas: Largo × Ancho × Alto" },
          { id: 3, name: "Conversión: volumen cúbico y capacidad en litros" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta",
        name: "Módulo 4: Medidas de Masa y Temperatura",
        levels: [
          { id: 1, name: "Balanzas y Termómetros analógicos (kg, g, °C)" },
          { id: 2, name: "Variaciones térmicas lineales en Celsius" },
          { id: 3, name: "La Máquina Kelvin: conversión °C ↔ K (±273)" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 7,
    name: "Fase 7: Coordenadas, Rutas y Tiempo",
    description: "Orientación en el plano de referencia, vectorización del movimiento y aritmética del tiempo.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta",
        name: "Módulo 1: Orientación Cardinal y Ángulos",
        levels: [
          { id: 1, name: "Puntos Cardinales y giros de 90° y 180°" },
          { id: 2, name: "Instrucciones verbales a trayectos vectoriales" },
          { id: 3, name: "Trayectorias críticas y distancias en grillas" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta",
        name: "Módulo 2: Plano Cartesiano",
        levels: [
          { id: 1, name: "Lectura y ubicación de pares ordenados (X, Y)" },
          { id: 2, name: "Traslación de figuras en el plano" },
          { id: 3, name: "Cálculo de Distancia Manhattan" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 3, modulo_id: 3, operacion: "mixta",
        name: "Módulo 3: La Mecánica del Tiempo",
        levels: [
          { id: 1, name: "Lectura analógica y digital del reloj" },
          { id: 2, name: "Duración de eventos cruzando AM/PM y husos de 24h" },
          { id: 3, name: "Aritmética sexagesimal: adición y sustracción" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 4, modulo_id: 4, operacion: "mixta",
        name: "Módulo 4: Horarios y Apps",
        levels: [
          { id: 1, name: "Lectura de tablas de horarios de transporte" },
          { id: 2, name: "Cálculo de tiempos compuestos y transbordos" },
          { id: 3, name: "Optimización: comparar opciones de transporte" }
        ],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 8,
    name: "Fase 8: Probabilidad y Lógica",
    description: "Análisis combinatorio, probabilidad y problemas de lógica pura.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta", name: "Módulo 1: Combinatoria",
        levels: [{ id: 1, name: "Arreglos Simples" }, { id: 2, name: "Permutaciones" }],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 2, modulo_id: 2, operacion: "mixta", name: "Módulo 2: Probabilidad Básica",
        levels: [{ id: 1, name: "Sucesos Posibles" }, { id: 2, name: "Eventos Compuestos" }],
        challenges: [
          { id: 11, name: "Desafío 1 (Estándar)", defaultTime: 60, defaultQty: 20 },
          { id: 12, name: "Desafío 2 (Avanzado)", defaultTime: 90, defaultQty: 20 },
          { id: 13, name: "Desafío Final (Maestría)", defaultTime: 120, defaultQty: 10 }
        ]
      },
      {
        seccion: 99099, modulo_id: 99, operacion: "mixta",
        name: "🏆 Examen Final de Fase",
        isFinalExam: true,
        challenges: [
          { id: 99, name: "Desafío Mixto (Graduación)", defaultTime: 180, defaultQty: 30 }
        ]
      }
    ]
  },
  {
    id: 9,
    name: "Fase 9: Simulador Pedro II",
    description: "Banco de preguntas y simulacros estilo Colegio Pedro II.",
    modules: [
      {
        seccion: 1, modulo_id: 1, operacion: "mixta", name: "Módulo 1: Simulacros Oficiales",
        levels: [{ id: 1, name: "Exámenes Anteriores" }, { id: 2, name: "Prueba de Velocidad" }],
        challenges: [{ id: 11, name: "Simulacro Completo", defaultTime: 3600, defaultQty: 50 }, { id: 13, name: "Simulacro Maestro", defaultTime: 2400, defaultQty: 50 }]
      }
    ]
  }
];

const DEFAULT_GLOBAL_CONFIG: PedagogyConfig = {
  practica_libre: {
    cantidad_requerida: 15,
    porcentaje_aprobacion: 80,
    usa_cronometro: false,
    tiempo_default_segundos: 15,
    tipo_feedback: 'simple',
  },
  desafios: {
    cantidad_requerida: 20,
    porcentaje_aprobacion: 90,
    usa_cronometro: true,
    tiempo_default_segundos_11: 25,
    tiempo_default_segundos_12: 40,
    tiempo_default_segundos_13: 50,
    tipo_feedback: 'simple',
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 15 },
  show: { opacity: 1, y: 0, transition: { type: 'spring' as const, stiffness: 300, damping: 24 } }
} as const;

const PedagogyTab: React.FC = () => {
  // Navigation
  const [selectedPhaseId, setSelectedPhaseId] = useState<number>(1);
  const [selectedModule, setSelectedModule] = useState<StaticModule | null>(null);
  const [selectedSubLevelId, setSelectedSubLevelId] = useState<number | null>(null);
  const [isSelectedChallenge, setIsSelectedChallenge] = useState<boolean>(false);

  // Accordion state for operation categories
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>(() => {
    const saved = localStorage.getItem('pedagogyExpandedCategories');
    return saved ? JSON.parse(saved) : { basicas: true, avanzadas: true, desafios: true, final_exam: true };
  });

  const toggleCategory = (cat: string) => {
    setExpandedCategories(prev => {
      const next = { ...prev, [cat]: !prev[cat] };
      localStorage.setItem('pedagogyExpandedCategories', JSON.stringify(next));
      return next;
    });
  };

  // Collapse/Expand all config sections
  const [sectionsCollapsed, setSectionsCollapsed] = useState(false);

  // Main config states
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const [globalConfig, setGlobalConfig] = useState<PedagogyConfig>(DEFAULT_GLOBAL_CONFIG);
  const [dbModularConfigs, setDbModularConfigs] = useState<ConfiguracionProgreso[]>([]);

  // Draft editing states (local modifications tracking)
  const [draftGlobalConfig, setDraftGlobalConfig] = useState<PedagogyConfig>(DEFAULT_GLOBAL_CONFIG);
  const [draftModularConfigs, setDraftModularConfigs] = useState<ConfiguracionProgreso[]>([]);

  // Load configs on mount
  useEffect(() => {
    loadAllConfigs();
  }, []);

  const loadAllConfigs = async () => {
    try {
      setLoading(true);
      const [settingsData, modularData] = await Promise.all([
        getAdminSettings(),
        getModularConfigs()
      ]);

      if (settingsData) {
        const mergedGlobal: PedagogyConfig = {
          practica_libre: { ...DEFAULT_GLOBAL_CONFIG.practica_libre, ...(settingsData.practica_libre || {}) },
          desafios: { ...DEFAULT_GLOBAL_CONFIG.desafios, ...(settingsData.desafios || {}) }
        };
        setGlobalConfig(mergedGlobal);
        setDraftGlobalConfig(mergedGlobal);
      }
      if (modularData) {
        setDbModularConfigs(modularData);
        setDraftModularConfigs(JSON.parse(JSON.stringify(modularData)));
      }
    } catch (error) {
      console.error("Failed to load platform configurations:", error);
    } finally {
      setLoading(false);
    }
  };

  // Selectors
  const selectPhase = (phaseId: number) => {
    setSelectedPhaseId(phaseId);
    setSelectedModule(null);
    setSelectedSubLevelId(null);
    setIsSelectedChallenge(false);
  };

  const selectModule = (phaseId: number, mod: StaticModule) => {
    setSelectedPhaseId(phaseId);
    setSelectedModule(mod);
    if (mod.isFinalExam) {
      setSelectedSubLevelId(99);
      setIsSelectedChallenge(true);
    } else if (mod.levels && mod.levels.length > 0) {
      setSelectedSubLevelId(mod.levels[0].id);
      setIsSelectedChallenge(false);
    } else {
      setSelectedSubLevelId(null);
      setIsSelectedChallenge(false);
    }
  };

  // Resolve custom records (active draft)
  const activePhase = STATIC_PHASES.find(p => p.id === selectedPhaseId) || STATIC_PHASES[0];

  // Search if a custom override exists for the active selected Phase & Module
  const activePhaseDefaultRecord = draftModularConfigs.find(
    c => c.fase_id === selectedPhaseId && c.seccion === 0 && c.operacion === 'mixta' && c.activo !== false
  );

  // Mapped DB keys for selected sub-item
  const getSelectedSubItemKeys = () => {
    if (!selectedModule) return { seccion: 0, operacion: '' };
    const modId = selectedModule.modulo_id || 1;
    if (modId === 99) {
      return { seccion: 99099, operacion: 'mixta' };
    }
    if (selectedSubLevelId === null) {
      return { seccion: selectedModule.seccion, operacion: selectedModule.operacion };
    }
    let oper = selectedModule.operacion;
    
    // CRITICAL FIX: Fase 5-9 use a different ID structure for their sections
    if (selectedPhaseId >= 5) {
      if (isSelectedChallenge) {
        return { seccion: selectedPhaseId * 10000 + modId * 100 + selectedSubLevelId, operacion: 'mixta' };
      } else {
        return { seccion: selectedPhaseId * 1000 + modId * 10 + selectedSubLevelId, operacion: oper };
      }
    }

    if (isSelectedChallenge) {
      return { seccion: modId * 1000 + selectedSubLevelId, operacion: 'mixta' };
    } else {
      return { seccion: modId * 100 + selectedSubLevelId, operacion: oper };
    }
  };

  const { seccion: activeSeccion, operacion: activeOperacion } = getSelectedSubItemKeys();

  const activeModuleRecord = selectedModule ? draftModularConfigs.find(
    c => c.fase_id === selectedPhaseId && 
         c.seccion === activeSeccion && 
         c.operacion === activeOperacion && 
         c.activo !== false
  ) : null;

  // Resolve current active parameters applying inheritance
  const getInheritedQuestionsCount = (): number => {
    if (activePhaseDefaultRecord) return activePhaseDefaultRecord.cantidad_requerida;
    return isSelectedChallenge 
      ? draftGlobalConfig.desafios.cantidad_requerida
      : draftGlobalConfig.practica_libre.cantidad_requerida;
  };

  const getInheritedPassingScore = (): number => {
    if (activePhaseDefaultRecord) return activePhaseDefaultRecord.porcentaje_aprobacion;
    return isSelectedChallenge 
      ? draftGlobalConfig.desafios.porcentaje_aprobacion
      : draftGlobalConfig.practica_libre.porcentaje_aprobacion;
  };

  const getInheritedUseTimer = (): boolean => {
    if (activePhaseDefaultRecord) return activePhaseDefaultRecord.usa_cronometro;
    return isSelectedChallenge 
      ? draftGlobalConfig.desafios.usa_cronometro
      : draftGlobalConfig.practica_libre.usa_cronometro;
  };

  const getInheritedFeedbackType = (): string => {
    if (activePhaseDefaultRecord) return activePhaseDefaultRecord.tipo_feedback;
    return isSelectedChallenge 
      ? draftGlobalConfig.desafios.tipo_feedback
      : draftGlobalConfig.practica_libre.tipo_feedback;
  };

  const getInheritedTimerForLevel = (): number => {
    if (activePhaseDefaultRecord && activePhaseDefaultRecord.tiempo_default_segundos !== null) {
      return activePhaseDefaultRecord.tiempo_default_segundos;
    }
    if (isSelectedChallenge) {
      if (selectedSubLevelId === 11) return draftGlobalConfig.desafios.tiempo_default_segundos_11;
      if (selectedSubLevelId === 12) return draftGlobalConfig.desafios.tiempo_default_segundos_12;
      if (selectedSubLevelId === 13) return draftGlobalConfig.desafios.tiempo_default_segundos_13;
      return 25;
    }
    return draftGlobalConfig.practica_libre.tiempo_default_segundos;
  };

  // Handle Updates
  const updateGlobalField = (section: 'practica_libre' | 'desafios', field: string, val: any) => {
    setDraftGlobalConfig(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: val
      }
    }));
  };

  const handleUpdatePhaseDefault = (field: keyof ConfiguracionProgreso, val: any) => {
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(c => c.fase_id === selectedPhaseId && c.seccion === 0 && c.operacion === 'mixta');
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], [field]: val, activo: true };
        return updated;
      } else {
        const newRecord: ConfiguracionProgreso = {
          fase_id: selectedPhaseId,
          seccion: 0,
          operacion: 'mixta',
          cantidad_requerida: field === 'cantidad_requerida' ? val : draftGlobalConfig.practica_libre.cantidad_requerida,
          porcentaje_aprobacion: field === 'porcentaje_aprobacion' ? val : draftGlobalConfig.practica_libre.porcentaje_aprobacion,
          orden_desbloqueo: 0,
          tipo_feedback: field === 'tipo_feedback' ? val : draftGlobalConfig.practica_libre.tipo_feedback,
          usa_cronometro: field === 'usa_cronometro' ? val : draftGlobalConfig.practica_libre.usa_cronometro,
          tiempo_default_segundos: field === 'tiempo_default_segundos' ? val : draftGlobalConfig.practica_libre.tiempo_default_segundos,
          activo: true
        };
        return [...prev, newRecord];
      }
    });
  };

  const handleUpdateModuleField = (field: keyof ConfiguracionProgreso, val: any) => {
    if (!selectedModule) return;
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(
        c => c.fase_id === selectedPhaseId && 
             c.seccion === activeSeccion && 
             c.operacion === activeOperacion
      );
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], [field]: val, activo: true };
        return updated;
      } else {
        const newRecord: ConfiguracionProgreso = {
          fase_id: selectedPhaseId,
          seccion: activeSeccion,
          operacion: activeOperacion,
          cantidad_requerida: field === 'cantidad_requerida' ? val : getInheritedQuestionsCount(),
          porcentaje_aprobacion: field === 'porcentaje_aprobacion' ? val : getInheritedPassingScore(),
          orden_desbloqueo: isSelectedChallenge ? (selectedSubLevelId || 11) : (selectedSubLevelId || 1),
          tipo_feedback: field === 'tipo_feedback' ? val : getInheritedFeedbackType(),
          usa_cronometro: field === 'usa_cronometro' ? val : getInheritedUseTimer(),
          tiempo_default_segundos: field === 'tiempo_default_segundos' ? val : getInheritedTimerForLevel(),
          activo: true
        };
        return [...prev, newRecord];
      }
    });
  };

  const togglePhaseOverride = (enable: boolean) => {
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(c => c.fase_id === selectedPhaseId && c.seccion === 0 && c.operacion === 'mixta');
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], activo: enable };
        return updated;
      } else if (enable) {
        const newRecord: ConfiguracionProgreso = {
          fase_id: selectedPhaseId,
          seccion: 0,
          operacion: 'mixta',
          cantidad_requerida: draftGlobalConfig.practica_libre.cantidad_requerida,
          porcentaje_aprobacion: draftGlobalConfig.practica_libre.porcentaje_aprobacion,
          orden_desbloqueo: 0,
          tipo_feedback: draftGlobalConfig.practica_libre.tipo_feedback,
          usa_cronometro: draftGlobalConfig.practica_libre.usa_cronometro,
          tiempo_default_segundos: draftGlobalConfig.practica_libre.tiempo_default_segundos,
          activo: true
        };
        return [...prev, newRecord];
      }
      return prev;
    });
  };

  const toggleModuleOverride = (enable: boolean) => {
    if (!selectedModule) return;
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(
        c => c.fase_id === selectedPhaseId && 
             c.seccion === activeSeccion && 
             c.operacion === activeOperacion
      );
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], activo: enable };
        return updated;
      } else if (enable) {
        let defaultTime = getInheritedTimerForLevel();
        let defaultQty = getInheritedQuestionsCount();
        if (isSelectedChallenge && selectedSubLevelId) {
          const chDef = selectedModule.challenges?.find(c => c.id === selectedSubLevelId);
          if (chDef) {
            defaultTime = chDef.defaultTime;
            defaultQty = chDef.defaultQty;
          }
        }
        
        const newRecord: ConfiguracionProgreso = {
          fase_id: selectedPhaseId,
          seccion: activeSeccion,
          operacion: activeOperacion,
          cantidad_requerida: defaultQty,
          porcentaje_aprobacion: isSelectedChallenge ? 90 : getInheritedPassingScore(),
          orden_desbloqueo: isSelectedChallenge ? (selectedSubLevelId || 11) : (selectedSubLevelId || 1),
          tipo_feedback: isSelectedChallenge ? 'simple' : getInheritedFeedbackType(),
          usa_cronometro: isSelectedChallenge ? true : getInheritedUseTimer(),
          tiempo_default_segundos: defaultTime,
          activo: true
        };
        return [...prev, newRecord];
      }
      return prev;
    });
  };

  const onRemoveOverride = (faseId: number, seccion: number, operacion: string) => {
    setDraftModularConfigs(prev => {
      return prev.map(c => {
        if (c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion) {
          return { ...c, activo: false };
        }
        return c;
      });
    });
  };

  const onSelectNode = (faseId: number, seccion: number, operacion: string) => {
    setSelectedPhaseId(faseId);
    if (seccion === 0) {
      setSelectedModule(null);
      setSelectedSubLevelId(null);
      setIsSelectedChallenge(false);
      return;
    }
    
    const phase = STATIC_PHASES.find(p => p.id === faseId);
    if (!phase) return;
    
    for (const mod of phase.modules) {
      const modId = mod.modulo_id || 1;
      
      if (mod.isFinalExam && seccion === 99099) {
        setSelectedModule(mod);
        setSelectedSubLevelId(99);
        setIsSelectedChallenge(true);
        return;
      }
      
      const level = mod.levels?.find(l => {
        const levelSeccion = faseId >= 5 
          ? faseId * 1000 + modId * 10 + l.id
          : modId * 100 + l.id;
        return levelSeccion === seccion;
      });
      if (level) {
        setSelectedModule(mod);
        setSelectedSubLevelId(level.id);
        setIsSelectedChallenge(false);
        return;
      }

      const challenge = mod.challenges?.find(c => {
        const challengeSeccion = faseId >= 5
          ? faseId * 10000 + modId * 100 + c.id
          : modId * 1000 + c.id;
        return challengeSeccion === seccion;
      });
      if (challenge) {
        setSelectedModule(mod);
        setSelectedSubLevelId(challenge.id);
        setIsSelectedChallenge(true);
        return;
      }
    }
  };

  // Compare draft vs database to check for changes
  const hasChanges = () => {
    const globalChanged = JSON.stringify(globalConfig) !== JSON.stringify(draftGlobalConfig);
    const modularChanged = JSON.stringify(dbModularConfigs) !== JSON.stringify(draftModularConfigs);
    return globalChanged || modularChanged;
  };

  const isPhaseModified = (phaseId: number): boolean => {
    const originalPhaseRecord = dbModularConfigs.find(c => c.fase_id === phaseId && c.seccion === 0 && c.operacion === 'mixta');
    const draftPhaseRecord = draftModularConfigs.find(c => c.fase_id === phaseId && c.seccion === 0 && c.operacion === 'mixta');
    if (JSON.stringify(originalPhaseRecord) !== JSON.stringify(draftPhaseRecord)) return true;

    const phaseModules = STATIC_PHASES.find(p => p.id === phaseId)?.modules || [];
    for (const mod of phaseModules) {
      const modId = mod.modulo_id || 1;
      const levelIds = mod.levels?.map(l => l.id) || [];
      const challengeIds = mod.challenges?.map(c => c.id) || [];
      for (const lid of levelIds) {
        const levelSeccion = phaseId >= 5 ? phaseId * 1000 + modId * 10 + lid : modId * 100 + lid;
        if (isModuleModified(phaseId, levelSeccion, mod.operacion)) return true;
      }
      for (const cid of challengeIds) {
        const challengeSeccion = phaseId >= 5 ? phaseId * 10000 + modId * 100 + cid : modId * 1000 + cid;
        if (isModuleModified(phaseId, challengeSeccion, 'mixta')) return true;
      }
    }
    return false;
  };

  const isModuleModified = (phaseId: number, seccion: number, operacion: string): boolean => {
    const orig = dbModularConfigs.find(c => c.fase_id === phaseId && c.seccion === seccion && c.operacion === operacion);
    const draft = draftModularConfigs.find(c => c.fase_id === phaseId && c.seccion === seccion && c.operacion === operacion);
    return JSON.stringify(orig) !== JSON.stringify(draft);
  };

  // Save All Changes (Pushing to backend)
  const handleSaveAll = async () => {
    setSaving(true);
    setSaveStatus('idle');

    try {
      // 1. Save Global Settings
      const globalChanged = JSON.stringify(globalConfig) !== JSON.stringify(draftGlobalConfig);
      if (globalChanged) {
        await saveAdminSettings(draftGlobalConfig);
        setGlobalConfig({ ...draftGlobalConfig });
      }

      // 2. Save Modular configurations
      for (const draft of draftModularConfigs) {
        const original = dbModularConfigs.find(
          c => c.fase_id === draft.fase_id && 
               c.seccion === draft.seccion && 
               c.operacion === draft.operacion
        );

        if (!original) {
          await createModularConfig(draft);
        } else if (JSON.stringify(original) !== JSON.stringify(draft)) {
          if (original.id) {
            await saveModularConfig(original.id, draft);
          }
        }
      }

      const reloadedData = await getModularConfigs();
      if (reloadedData) {
        setDbModularConfigs(reloadedData);
        setDraftModularConfigs(JSON.parse(JSON.stringify(reloadedData)));
      }

      setSaveStatus('success');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } catch (error) {
      console.error("Failed to save advanced settings:", error);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } finally {
      setSaving(false);
    }
  };

  const changesExist = hasChanges();
  const { status: autoSaveStatus } = useAutoSave(changesExist, handleSaveAll, 1500);

  if (loading) {
    return (
      <div className="w-full flex items-center justify-center py-40 select-none">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="text-blue-500 animate-spin" size={48} />
          <p className="text-slate-500 dark:text-slate-400 font-bold text-base">Cargando base de datos pedagógica...</p>
        </div>
      </div>
    );
  }

  return (
    <motion.div variants={itemVariants} className="w-full flex flex-col gap-6 lg:gap-10 select-none">
      
      {/* Auto-Save Status Bar */}
      <div className="flex items-center justify-between px-6 py-3 bg-white/5 dark:bg-slate-900/40 rounded-xl border border-slate-200 dark:border-white/10 shadow-sm">
        <div className="flex items-center gap-3">
          {(autoSaveStatus === 'saving' || saving) && (
            <>
              <div className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse shadow-[0_0_8px_rgba(245,158,11,0.8)]" />
              <span className="text-sm font-bold text-slate-600 dark:text-slate-300">Guardando...</span>
            </>
          )}
          {autoSaveStatus === 'success' && !saving && (
            <>
              <div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]" />
              <span className="text-sm font-bold text-slate-600 dark:text-slate-300">Sincronizado</span>
            </>
          )}
          {autoSaveStatus === 'error' && !saving && (
            <>
              <div className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]" />
              <span className="text-sm font-bold text-red-500">Error al guardar</span>
            </>
          )}
          {autoSaveStatus === 'idle' && !saving && (
            <>
              <div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]" />
              <span className="text-sm font-bold text-slate-600 dark:text-slate-300">Sincronizado</span>
            </>
          )}
        </div>
      </div>

      {/* Top Header Card */}
      <div className="flex items-center justify-between bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-6 lg:p-10 rounded-[2.2rem] lg:rounded-[3rem] shadow-2xl">
        <div>
          <h2 className="text-3xl lg:text-4xl xl:text-5xl font-black text-slate-900 dark:text-white flex items-center gap-3 lg:gap-5">
            <div className="p-2.5 bg-blue-500/20 rounded-2xl border border-blue-500/30">
              <Cpu className="text-blue-400" size={24} />
            </div>
            Gestión Pedagógica Avanzada
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm lg:text-base xl:text-lg mt-2 lg:mt-3 leading-relaxed">Configuración jerárquica con sistema de herencia para las fases del Viaje Matemático.</p>
        </div>

        <button
          type="button"
          onClick={() => setSectionsCollapsed(!sectionsCollapsed)}
          className="px-4 py-3.5 lg:px-5 lg:py-4 rounded-2xl flex items-center gap-2 font-bold text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white bg-white/50 dark:bg-white/5 border border-slate-200 dark:border-white/10 hover:bg-white/80 dark:hover:bg-white/10 transition-all"
          title={sectionsCollapsed ? 'Expandir todas las secciones' : 'Colapsar todas las secciones'}
        >
          {sectionsCollapsed ? <Maximize2 size={16} /> : <Minimize2 size={16} />}
          {sectionsCollapsed ? 'Expandir todo' : 'Colapsar todo'}
        </button>
      </div>

      {/* ========================================================= */}
      {/* LEVEL 1 NAVIGATION (Global vs Fases vs Resumen) */}
      {/* ========================================================= */}
      <div className="flex bg-white/50 dark:bg-slate-900/40 p-2 rounded-3xl mb-4 shadow-sm border border-slate-200 dark:border-white/10">
        <button 
          type="button"
          onClick={() => { setSelectedPhaseId(0); setSelectedModule(null); }}
          className={`flex-1 flex items-center justify-center gap-3 py-4 rounded-2xl font-black text-sm lg:text-base transition-all ${
            selectedPhaseId === 0 
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' 
              : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white hover:bg-white dark:hover:bg-white/5'
          }`}
        >
          <Settings size={20} className={selectedPhaseId === 0 ? "animate-[spin_3s_linear_infinite]" : ""} /> 
          Plataforma Global
        </button>
        <button 
          type="button"
          onClick={() => { setSelectedPhaseId(1); setSelectedModule(null); }}
          className={`flex-1 flex items-center justify-center gap-3 py-4 rounded-2xl font-black text-sm lg:text-base transition-all ${
            selectedPhaseId > 0 
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' 
              : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white hover:bg-white dark:hover:bg-white/5'
          }`}
        >
          <Layers size={20} /> 
          Configuración por Fases
        </button>
      </div>

      <div className="flex flex-col gap-6">
        
        {/* Phase / Module selector */}
        {selectedPhaseId > 0 && (
          <PhaseFlowDesigner
            selectedPhaseId={selectedPhaseId}
            selectedModule={selectedModule}
            selectPhase={selectPhase}
            selectModule={selectModule}
            expandedCategories={expandedCategories}
            toggleCategory={toggleCategory}
            draftModularConfigs={draftModularConfigs}
            isPhaseModified={isPhaseModified}
            isModuleModified={isModuleModified}
            selectedSubLevelId={selectedSubLevelId}
            setSelectedSubLevelId={setSelectedSubLevelId}
            isSelectedChallenge={isSelectedChallenge}
            setIsSelectedChallenge={setIsSelectedChallenge}
            staticPhases={STATIC_PHASES}
          />
        )}

        {/* Content Panels */}
        {!sectionsCollapsed && (
          <ConfigForm
            type={selectedPhaseId === 0 ? 'global' : !selectedModule ? 'phase' : 'module'}
            title={selectedPhaseId === 0 ? 'Configuración de Fallbacks Generales' : !selectedModule ? activePhase.name : `${selectedModule.name.split(':')[0]} (${isSelectedChallenge ? 'Desafío' : 'Nivel'} ${selectedSubLevelId})`}
            description={selectedPhaseId === 0 ? 'Estos valores actúan como fallback unificado para todo el sistema educativo.' : !selectedModule ? activePhase.description : 'Reglas de evaluación y parámetros exclusivos para este contenido.'}
            draftGlobalConfig={draftGlobalConfig}
            updateGlobalField={updateGlobalField}
            activeOverrideRecord={selectedPhaseId === 0 ? null : !selectedModule ? activePhaseDefaultRecord : activeModuleRecord}
            toggleOverride={selectedPhaseId === 0 ? () => {} : !selectedModule ? togglePhaseOverride : toggleModuleOverride}
            updateOverrideField={selectedPhaseId === 0 ? () => {} : !selectedModule ? handleUpdatePhaseDefault : handleUpdateModuleField}
            isSelectedChallenge={isSelectedChallenge}
            selectedSubLevelId={selectedSubLevelId}
            getInheritedQuestionsCount={getInheritedQuestionsCount}
            getInheritedPassingScore={getInheritedPassingScore}
            getInheritedUseTimer={getInheritedUseTimer}
            getInheritedFeedbackType={getInheritedFeedbackType}
            getInheritedTimerForLevel={getInheritedTimerForLevel}
          />
        )}

        {/* Resumen de Sobrescrituras (ProgressConfigTable) */}
        {selectedPhaseId > 0 && (
          <ProgressConfigTable
            draftModularConfigs={draftModularConfigs}
            staticPhases={STATIC_PHASES}
            onRemoveOverride={onRemoveOverride}
            onSelectNode={onSelectNode}
          />
        )}
      </div>

    </motion.div>
  );
};

export default PedagogyTab;
