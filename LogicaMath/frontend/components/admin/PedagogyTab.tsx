import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Lock, Loader2, Save } from 'lucide-react';
import {
  getAdminSettings, saveAdminSettings,
  getModularConfigs, saveModularConfig, createModularConfig
} from '../../services/storageService';
import { PedagogyConfig, ConfiguracionProgreso } from '../../types';
import { StaticModule, StaticPhase, getModuleRows, findRowBySeccion, CHALLENGE_ORDER_SECCIONES } from './pedagogyHelpers';
import { PedagogyNavTree } from './PedagogyNavTree';
import { GlobalConfigPanel } from './GlobalConfigPanel';
import { PhaseDefaultPanel } from './PhaseDefaultPanel';
import { ModuleGridPanel } from './ModuleGridPanel';
import { OverridesSummaryPanel } from './OverridesSummaryPanel';
import { PRACTICE_REQUIRED_CORRECT_ANSWERS } from '../common/progression';

// ==========================================
// STATIC MAP OF PHASES
// Fases 1 a 8 tienen su estructura pedagógica definitiva.
// La Fase 9 (Simulador Pedro II) todavía está en diseño y usa otra
// lógica de configuración: se muestra bloqueada en el panel (ver LOCKED_PHASE_ID).
// ==========================================
const LOCKED_PHASE_ID = 9;

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
    name: "Fase 4: Operatoria Decimal y Conversiones",
    description: "Suma, resta, multiplicación, división con decimales y conversiones métricas.",
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
    cantidad_requerida: PRACTICE_REQUIRED_CORRECT_ANSWERS,
    porcentaje_aprobacion: 100,
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
  // Navigation: selectedPhaseId 0 = Plataforma Global
  const [selectedPhaseId, setSelectedPhaseId] = useState<number>(1);
  const [selectedModule, setSelectedModule] = useState<StaticModule | null>(null);

  // Main config states
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(false);

  const [globalConfig, setGlobalConfig] = useState<PedagogyConfig>(DEFAULT_GLOBAL_CONFIG);
  const [dbModularConfigs, setDbModularConfigs] = useState<ConfiguracionProgreso[]>([]);

  const [draftGlobalConfig, setDraftGlobalConfig] = useState<PedagogyConfig>(DEFAULT_GLOBAL_CONFIG);
  const [draftModularConfigs, setDraftModularConfigs] = useState<ConfiguracionProgreso[]>([]);

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

  // ==========================================
  // Navigation handlers
  // ==========================================
  const selectGlobal = () => {
    setSelectedPhaseId(0);
    setSelectedModule(null);
  };

  const selectPhase = (phaseId: number) => {
    setSelectedPhaseId(phaseId);
    setSelectedModule(null);
  };

  const selectModule = (phaseId: number, mod: StaticModule) => {
    if (phaseId === LOCKED_PHASE_ID) return;
    setSelectedPhaseId(phaseId);
    setSelectedModule(mod);
  };

  // ==========================================
  // Inheritance resolution (Global -> Fase -> Módulo/Nivel/Desafío)
  //
  // La fase tiene DOS familias de defaults independientes:
  // - "Niveles" (seccion 0): cascada a todo nivel de práctica libre de la fase.
  // - "Desafíos" (secciones sentinela negativas, una por orden 11/12/13): cada una
  //   cascada de forma independiente al Desafío 1/2/Final de TODOS los módulos de
  //   la fase. El Examen Final de Fase tiene su propia fila directa (seccion 99099),
  //   no es un sentinel: solo hay un examen final por fase.
  // ==========================================
  const getPhaseDefaultRecord = (faseId: number): ConfiguracionProgreso | null => {
    const rec = draftModularConfigs.find(c => c.fase_id === faseId && c.seccion === 0 && c.operacion === 'mixta');
    return rec && rec.activo !== false ? rec : null;
  };

  const getPhaseChallengeRecord = (faseId: number, order: number): ConfiguracionProgreso | null => {
    const seccion = CHALLENGE_ORDER_SECCIONES[order];
    if (seccion === undefined) return null;
    const rec = draftModularConfigs.find(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === 'mixta');
    return rec && rec.activo !== false ? rec : null;
  };

  const getInheritedQuestionsCount = (faseId: number, isChallenge: boolean, subId: number = 0): number => {
    if (isChallenge) {
      const challengeDefault = getPhaseChallengeRecord(faseId, subId);
      if (challengeDefault) return challengeDefault.cantidad_requerida;
      return draftGlobalConfig.desafios.cantidad_requerida;
    }
    const phaseDefault = getPhaseDefaultRecord(faseId);
    if (phaseDefault) return phaseDefault.cantidad_requerida;
    return draftGlobalConfig.practica_libre.cantidad_requerida;
  };

  const getInheritedPassingScore = (faseId: number, isChallenge: boolean, subId: number = 0): number => {
    if (isChallenge) {
      const challengeDefault = getPhaseChallengeRecord(faseId, subId);
      if (challengeDefault) return challengeDefault.porcentaje_aprobacion;
      return draftGlobalConfig.desafios.porcentaje_aprobacion;
    }
    const phaseDefault = getPhaseDefaultRecord(faseId);
    if (phaseDefault) return phaseDefault.porcentaje_aprobacion;
    return draftGlobalConfig.practica_libre.porcentaje_aprobacion;
  };

  const getInheritedUseTimer = (faseId: number, isChallenge: boolean, subId: number = 0): boolean => {
    if (isChallenge) {
      const challengeDefault = getPhaseChallengeRecord(faseId, subId);
      if (challengeDefault) return challengeDefault.usa_cronometro;
      return draftGlobalConfig.desafios.usa_cronometro;
    }
    const phaseDefault = getPhaseDefaultRecord(faseId);
    if (phaseDefault) return phaseDefault.usa_cronometro;
    return draftGlobalConfig.practica_libre.usa_cronometro;
  };

  const getInheritedFeedbackType = (faseId: number, isChallenge: boolean, subId: number = 0): string => {
    if (isChallenge) {
      const challengeDefault = getPhaseChallengeRecord(faseId, subId);
      if (challengeDefault) return challengeDefault.tipo_feedback;
      return draftGlobalConfig.desafios.tipo_feedback;
    }
    const phaseDefault = getPhaseDefaultRecord(faseId);
    if (phaseDefault) return phaseDefault.tipo_feedback;
    return draftGlobalConfig.practica_libre.tipo_feedback;
  };

  const getInheritedTimer = (faseId: number, isChallenge: boolean, subId: number): number => {
    if (!isChallenge) {
      const phaseDefault = getPhaseDefaultRecord(faseId);
      if (phaseDefault && phaseDefault.tiempo_default_segundos !== null) return phaseDefault.tiempo_default_segundos;
      return draftGlobalConfig.practica_libre.tiempo_default_segundos;
    }
    const challengeDefault = getPhaseChallengeRecord(faseId, subId);
    if (challengeDefault && challengeDefault.tiempo_default_segundos !== null) return challengeDefault.tiempo_default_segundos;
    if (subId === 11) return draftGlobalConfig.desafios.tiempo_default_segundos_11;
    if (subId === 12) return draftGlobalConfig.desafios.tiempo_default_segundos_12;
    if (subId === 13) return draftGlobalConfig.desafios.tiempo_default_segundos_13;
    return 25;
  };

  // ==========================================
  // Mutations
  // ==========================================
  const updateGlobalField = (section: 'practica_libre' | 'desafios', field: string, val: any) => {
    setDraftGlobalConfig(prev => ({
      ...prev,
      [section]: { ...prev[section], [field]: val }
    }));
  };

  // Auto-override: editar cualquier campo crea/activa la regla propia de ese nodo.
  const upsertModularField = (
    faseId: number, seccion: number, operacion: string,
    field: keyof ConfiguracionProgreso, val: any,
    ctx: { isChallenge: boolean; subId: number }
  ) => {
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion);
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], [field]: val, activo: true };
        return updated;
      }
      const newRecord: ConfiguracionProgreso = {
        fase_id: faseId,
        seccion,
        operacion,
        cantidad_requerida: field === 'cantidad_requerida' ? val : getInheritedQuestionsCount(faseId, ctx.isChallenge, ctx.subId),
        porcentaje_aprobacion: field === 'porcentaje_aprobacion' ? val : getInheritedPassingScore(faseId, ctx.isChallenge, ctx.subId),
        orden_desbloqueo: ctx.subId,
        tipo_feedback: field === 'tipo_feedback' ? val : getInheritedFeedbackType(faseId, ctx.isChallenge, ctx.subId),
        usa_cronometro: field === 'usa_cronometro' ? val : getInheritedUseTimer(faseId, ctx.isChallenge, ctx.subId),
        tiempo_default_segundos: field === 'tiempo_default_segundos' ? val : getInheritedTimer(faseId, ctx.isChallenge, ctx.subId),
        activo: true
      };
      return [...prev, newRecord];
    });
  };

  const removeModularOverride = (faseId: number, seccion: number, operacion: string) => {
    setDraftModularConfigs(prev => prev.map(c => (
      c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion ? { ...c, activo: false } : c
    )));
  };

  const applyValuesToRow = (
    faseId: number, seccion: number, operacion: string, subId: number, isChallenge: boolean,
    values: { cantidad_requerida: number; porcentaje_aprobacion: number; usa_cronometro: boolean; tiempo_default_segundos: number }
  ) => {
    setDraftModularConfigs(prev => {
      const idx = prev.findIndex(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion);
      if (idx !== -1) {
        const updated = [...prev];
        updated[idx] = { ...updated[idx], ...values, activo: true };
        return updated;
      }
      const newRecord: ConfiguracionProgreso = {
        fase_id: faseId,
        seccion,
        operacion,
        cantidad_requerida: values.cantidad_requerida,
        porcentaje_aprobacion: values.porcentaje_aprobacion,
        orden_desbloqueo: subId,
        tipo_feedback: getInheritedFeedbackType(faseId, isChallenge, subId),
        usa_cronometro: values.usa_cronometro,
        tiempo_default_segundos: values.tiempo_default_segundos,
        activo: true
      };
      return [...prev, newRecord];
    });
  };

  const handleApplyToAllRows = (values: { cantidad_requerida: number; porcentaje_aprobacion: number; usa_cronometro: boolean; tiempo_default_segundos: number }) => {
    if (!selectedModule) return;
    const rows = getModuleRows(selectedPhaseId, selectedModule);
    rows.forEach(row => applyValuesToRow(selectedPhaseId, row.seccion, row.operacion, row.subId, row.isChallenge, values));
  };

  // ==========================================
  // Change tracking (badges + save)
  // ==========================================
  const isRowChanged = (faseId: number, seccion: number, operacion: string): boolean => {
    const orig = dbModularConfigs.find(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion);
    const draft = draftModularConfigs.find(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion);
    return JSON.stringify(orig) !== JSON.stringify(draft);
  };

  const isModuleChanged = (faseId: number, mod: StaticModule): boolean => {
    return getModuleRows(faseId, mod).some(row => isRowChanged(faseId, row.seccion, row.operacion));
  };

  const isPhaseModified = (faseId: number): boolean => {
    if (isRowChanged(faseId, 0, 'mixta')) return true;
    if (Object.values(CHALLENGE_ORDER_SECCIONES).some(seccion => isRowChanged(faseId, seccion, 'mixta'))) return true;
    const phase = STATIC_PHASES.find(p => p.id === faseId);
    if (!phase) return false;
    return phase.modules.some(mod => isModuleChanged(faseId, mod));
  };

  const moduleHasOverride = (faseId: number, mod: StaticModule): boolean => {
    return getModuleRows(faseId, mod).some(row =>
      draftModularConfigs.some(c => c.fase_id === faseId && c.seccion === row.seccion && c.operacion === row.operacion && c.activo !== false)
    );
  };

  const onSelectNode = (faseId: number, seccion: number, operacion: string) => {
    if (faseId === LOCKED_PHASE_ID) {
      setSelectedPhaseId(LOCKED_PHASE_ID);
      setSelectedModule(null);
      return;
    }
    setSelectedPhaseId(faseId);
    if (seccion === 0) {
      setSelectedModule(null);
      return;
    }
    const phase = STATIC_PHASES.find(p => p.id === faseId);
    if (!phase) return;
    const found = findRowBySeccion(phase, seccion);
    if (found) setSelectedModule(found.mod);
  };

  const hasChanges = () => {
    const globalChanged = JSON.stringify(globalConfig) !== JSON.stringify(draftGlobalConfig);
    const modularChanged = JSON.stringify(dbModularConfigs) !== JSON.stringify(draftModularConfigs);
    return globalChanged || modularChanged;
  };

  // ==========================================
  // Save All Changes (Pushing to backend)
  // ==========================================
  const handleSaveAll = async () => {
    setSaving(true);
    setSaveError(false);

    try {
      const globalChanged = JSON.stringify(globalConfig) !== JSON.stringify(draftGlobalConfig);
      if (globalChanged) {
        await saveAdminSettings(draftGlobalConfig);
        setGlobalConfig({ ...draftGlobalConfig });
      }

      for (const draft of draftModularConfigs) {
        const original = dbModularConfigs.find(
          c => c.fase_id === draft.fase_id &&
               c.seccion === draft.seccion &&
               c.operacion === draft.operacion
        );

        const targetId = draft.id || original?.id;
        if (targetId) {
          if (JSON.stringify(original) !== JSON.stringify(draft)) {
            await saveModularConfig(targetId, draft);
          }
        } else {
          await createModularConfig(draft);
        }
      }

      const reloadedData = await getModularConfigs();
      if (reloadedData) {
        setDbModularConfigs(reloadedData);
        setDraftModularConfigs(JSON.parse(JSON.stringify(reloadedData)));
      }
    } catch (error) {
      console.error("Failed to save advanced settings:", error);
      setSaveError(true);
    } finally {
      setSaving(false);
    }
  };

  const changesExist = hasChanges();

  // Advierte antes de cerrar/recargar si hay cambios sin guardar (no hay autoguardado).
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (changesExist) {
        e.preventDefault();
        e.returnValue = '';
      }
    };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [changesExist]);

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

  const activePhase = STATIC_PHASES.find(p => p.id === selectedPhaseId) || null;
  const scope: 'global' | 'locked' | 'fase' | 'module' =
    selectedPhaseId === 0 ? 'global' : selectedPhaseId === LOCKED_PHASE_ID ? 'locked' : selectedModule ? 'module' : 'fase';

  return (
    <motion.div variants={itemVariants} className="w-full flex flex-col gap-4 select-none">

      {/* Slim header */}
      <div className="flex items-center justify-between gap-3 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl px-5 py-3.5">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500/10 rounded-xl">
            <Cpu className="text-blue-500" size={20} />
          </div>
          <div>
            <h2 className="text-lg font-black text-slate-900 dark:text-white">Configuración Pedagógica</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">Herencia: Plataforma Global → Fase → Módulo → Nivel/Desafío</p>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {saving ? (
            <>
              <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Guardando...</span>
            </>
          ) : saveError ? (
            <>
              <div className="w-2 h-2 rounded-full bg-red-500" />
              <span className="text-xs font-bold text-red-500">Error al guardar</span>
            </>
          ) : changesExist ? (
            <>
              <div className="w-2 h-2 rounded-full bg-amber-500" />
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Cambios sin guardar</span>
            </>
          ) : (
            <>
              <div className="w-2 h-2 rounded-full bg-green-500" />
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Sincronizado</span>
            </>
          )}

          <button
            type="button"
            onClick={handleSaveAll}
            disabled={!changesExist || saving}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-black bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-blue-600"
          >
            <Save size={14} /> Guardar cambios
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[260px_minmax(0,1fr)] gap-4 items-start">
        <PedagogyNavTree
          staticPhases={STATIC_PHASES}
          selectedPhaseId={selectedPhaseId}
          selectedModule={selectedModule}
          onSelectGlobal={selectGlobal}
          onSelectPhase={selectPhase}
          onSelectModule={selectModule}
          phaseHasChanges={isPhaseModified}
          moduleHasChanges={isModuleChanged}
          moduleHasOverride={moduleHasOverride}
          lockedPhaseId={LOCKED_PHASE_ID}
        />

        <div className="flex flex-col gap-4 min-w-0">
          {scope === 'global' && (
            <GlobalConfigPanel draftGlobalConfig={draftGlobalConfig} updateGlobalField={updateGlobalField} />
          )}

          {scope === 'locked' && (
            <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-10 flex flex-col items-center text-center gap-3">
              <Lock size={32} className="text-slate-400" />
              <h3 className="text-lg font-black text-slate-900 dark:text-white">Fase 9 en diseño</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md">
                El Simulador Pedro II todavía no tiene su estructura pedagógica definitiva y usará una lógica de configuración distinta. Esta sección se habilitará cuando esté lista.
              </p>
            </div>
          )}

          {scope === 'fase' && activePhase && (
            <PhaseDefaultPanel
              faseId={selectedPhaseId}
              faseName={activePhase.name}
              faseDescription={activePhase.description}
              record={getPhaseDefaultRecord(selectedPhaseId)}
              inheritedQuestionsCount={getInheritedQuestionsCount(selectedPhaseId, false)}
              inheritedPassingScore={getInheritedPassingScore(selectedPhaseId, false)}
              inheritedUseTimer={getInheritedUseTimer(selectedPhaseId, false)}
              inheritedTimer={getInheritedTimer(selectedPhaseId, false, 0)}
              inheritedFeedbackType={getInheritedFeedbackType(selectedPhaseId, false)}
              onUpdateField={(field, val) => upsertModularField(selectedPhaseId, 0, 'mixta', field, val, { isChallenge: false, subId: 0 })}
              onRevert={() => removeModularOverride(selectedPhaseId, 0, 'mixta')}
              draftModularConfigs={draftModularConfigs}
              getInheritedQuestionsCount={(isChallenge, subId) => getInheritedQuestionsCount(selectedPhaseId, isChallenge, subId)}
              getInheritedPassingScore={(isChallenge, subId) => getInheritedPassingScore(selectedPhaseId, isChallenge, subId)}
              getInheritedUseTimer={(isChallenge, subId) => getInheritedUseTimer(selectedPhaseId, isChallenge, subId)}
              getInheritedTimer={(isChallenge, subId) => getInheritedTimer(selectedPhaseId, isChallenge, subId)}
              onUpdateChallengeRowField={(seccion, operacion, isChallenge, subId, field, val) =>
                upsertModularField(selectedPhaseId, seccion, operacion, field, val, { isChallenge, subId })}
              onRevertChallengeRow={(seccion, operacion) => removeModularOverride(selectedPhaseId, seccion, operacion)}
            />
          )}

          {scope === 'module' && selectedModule && (
            <ModuleGridPanel
              faseId={selectedPhaseId}
              mod={selectedModule}
              draftModularConfigs={draftModularConfigs}
              getInheritedQuestionsCount={(isChallenge, subId) => getInheritedQuestionsCount(selectedPhaseId, isChallenge, subId)}
              getInheritedPassingScore={(isChallenge, subId) => getInheritedPassingScore(selectedPhaseId, isChallenge, subId)}
              getInheritedUseTimer={(isChallenge, subId) => getInheritedUseTimer(selectedPhaseId, isChallenge, subId)}
              getInheritedFeedbackType={(isChallenge, subId) => getInheritedFeedbackType(selectedPhaseId, isChallenge, subId)}
              getInheritedTimer={(isChallenge, subId) => getInheritedTimer(selectedPhaseId, isChallenge, subId)}
              onUpdateRowField={(seccion, operacion, isChallenge, subId, field, val) =>
                upsertModularField(selectedPhaseId, seccion, operacion, field, val, { isChallenge, subId })}
              onRevertRow={(seccion, operacion) => removeModularOverride(selectedPhaseId, seccion, operacion)}
              onApplyToAll={handleApplyToAllRows}
            />
          )}

          {scope !== 'locked' && (
            <OverridesSummaryPanel
              draftModularConfigs={draftModularConfigs}
              staticPhases={STATIC_PHASES}
              onRemoveOverride={removeModularOverride}
              onSelectNode={onSelectNode}
            />
          )}
        </div>
      </div>

    </motion.div>
  );
};

export default PedagogyTab;
