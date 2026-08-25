> ✅ **Reestructuración de la Fase 4 completada.**
> `docs/reestructuraciondefases.md` se conserva como referencia histórica; para la Fase 4 manda el estado real ya implementado en código y BD local.

# Guía de Arquitectura y Construcción: Nueva Fase (Basado en Fase 2)

> **Alcance actualizado (2026-08-23):** toda referencia de esta guía a Bucle Espejo, Rescate, `es_espejo`, clones por error o `/cerrar-rescate` está **derogada para Fases 5 y 6**. Para esas fases prevalece [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](../ESTADO_IMPLEMENTACION_FASES_5_6.md): corrección obligatoria de 10 segundos, nueva pregunta tras el error y progreso solo por acierto. Esta guía conserva esas secciones como diseño histórico de fases anteriores.

Este documento detalla la lógica, estructura y los pasos técnicos necesarios para construir una nueva Fase (por ejemplo, Fase 3 o Fase 4) dentro del proyecto "Lógica Matemáticas Kids", tomando como modelo la arquitectura madura de la Fase 2.

---

## 1. Visión General y Conceptos Pedagógicos

Cada Fase funciona como un micro-ecosistema aislado pero integrado en el progreso global del alumno. Está compuesta por:
*   **Módulos**: Grandes bloques temáticos (ej. "Gimnasio Numérico").
*   **Niveles**: Práctica guiada con preguntas infinitas o un set definido para alcanzar la "dominancia" (ej. 10 aciertos).
*   **Desafíos**: Evaluaciones finales del módulo (Estándar, Avanzado, Maestría). Tienen tiempo límite y un máximo de errores permitidos.

### Estructura Canónica de Fase (4 Módulos × 3 Niveles)
Toda nueva fase debe organizarse en una estructura canónica de **4 Módulos Temáticos × 3 Niveles de Práctica Libre** por módulo, siguiendo la progresión didáctica innegociable:
- **Nivel 1 (Aislar microconcepto A):** Concepto básico descompuesto sin distracciones.
- **Nivel 2 (Aislar microconcepto B):** Segundo concepto o variante descompuesta sin distracciones.
- **Nivel 3 (Integrar A + B / TJS ligero):** Integración práctica de ambos conceptos en un solo marco.

### Reglas Innegociables de UI/UX (T3 & T4)
- **T3 (Cero Scroll Vertical):** Ninguna interfaz de teoría, práctica o desafío puede generar scrollbar vertical. Todo el contenido debe ser visible dentro del marco.
- **T4 (Viewport Fijo 950×620 px):** Maquetación objetivo para desktop y tablet horizontal (móviles excluidos).
- **Regla de Evaluación:** No se evalúa una convención o formato que no haya sido enseñado previamente en la teoría del módulo.

### Mecánicas Core (El Tutor Invisible)
1.  **Bucle Espejo (Mirror Loop)**: Si el alumno falla repetidamente (ej. 3 veces), la progresión se congela. El sistema entra en "modo rescate" (espejo), mostrando un modal de explicación teórica detallada. La siguiente pregunta será un clon exacto de la que falló, obligándolo a aplicar lo aprendido.
2.  **Early Exit**: En los Desafíos, si el alumno comete más errores de los tolerados (ej. `max_errores_tolerados = 3`), el desafío termina inmediatamente con una pantalla de fallo, obligándolo a reiniciar desde cero.
3.  **Teoría Dinámica (Lectura)**: Antes de comenzar un nivel nuevo, se muestra un modal interactivo con teoría, vocabulario y ejemplos obtenidos de la base de datos.

---

## 2. Arquitectura del Backend (FastAPI)

El código debe residir en un directorio aislado: `backend/app/faseX/`.

### A. Modelos de Base de Datos (`models.py`)
No modifiques el núcleo de la base de datos (`app/models/sql_models.py`) a menos que sea algo global. Crea modelos locales que referencien al `Alumno` y a la `Pregunta`:
*   `IntentoPregunta`: Rastrea la sesión de resolución de una pregunta.
*   `IntentoPaso`: Registra cada intento del teclado/respuesta del niño. Útil para medir tiempos de reacción.
*   `NivelTeoria`: Almacena el JSON con los textos explicativos, diccionarios y ejemplos para la Fase.

### B. Schemas de Comunicación (`schemas.py`)
Define Pydantic models estrictos para la API. Las interfaces clave son:
*   **Dashboard**: `FaseXDashboard`, `FaseXModuloInfo`, `FaseXNivelInfo`.
*   **Pregunta (`FaseXPreguntaParaAlumno`)**: Lo que se envía al Front. **Regla de oro**: NUNCA enviar la respuesta correcta en el JSON si es una pregunta de opción múltiple, para evitar trampas en el cliente.
*   **Respuesta (`FaseXResponderPregunta`)**: Payload del cliente (respuesta dada, ID alternativa, tiempo tomado, paso actual).
*   **Resultado (`FaseXResultadoRespuesta`)**: Feedback post-evaluación (`es_correcta`, `aciertos_acumulados`, banderas como `es_espejo`, `early_exit`, `bloque_completado`).

### C. Generadores y Servicios (`generators.py`)
El motor de la fase. Dependiendo de la materia, aquí se escriben los algoritmos para generar ecuaciones aleatorias balanceadas o extraer problemas de texto basados en un `seed`.

### D. Enrutador (`router.py`)
El controlador principal. Debe implementar los siguientes endpoints:
1.  `GET /faseX/dashboard`: Estado actual, módulos y niveles desbloqueados.
2.  `GET /faseX/modulo/{id}/nivel/{id}/pregunta`: Obtiene la siguiente pregunta (ya sea generada al vuelo o el "espejo" si el alumno está en rescate).
3.  `POST /faseX/responder`: La lógica más densa. Evalúa la respuesta, actualiza el estado de dominio del nivel, dispara el Bucle Espejo si los errores superan el umbral, y guarda la analítica.
4.  `GET /faseX/lectura/...`: Entrega la teoría del nivel.
5.  `POST /faseX/graduate`: Marca la fase como completada y desbloquea la `Fase X+1` a nivel global.

---

## 3. Arquitectura del Frontend (React)

Ubicación: `frontend/components/faseX/`.

### A. Tipos y Servicios API
*   **`FaseXTypes.ts`**: Debe ser un espejo 1:1 de los Schemas Pydantic. Usa TypeScript Interfaces para `FaseXDashboard`, `FaseXPregunta`, `FaseXAnswerResult`, etc.
*   **`FaseXService.ts`**: Wrapper alrededor de `fetch` o `axios` para comunicarse con `/api/faseX/...`.

### B. Componentes Principales
1.  **`WelcomeScreenPhaseX.tsx`**: Introducción narrativa o cinemática a la Fase.
2.  **`FaseXDashboard.tsx`**: Vista de progreso. Muestra módulos, niveles bloqueados/desbloqueados, y permite lanzar el juego.
3.  **`FaseXGameScreen.tsx`**: El componente más complejo (el motor del frontend).
    *   **Estado**: Debe gestionar el cronómetro, el valor del teclado en pantalla (si aplica), la animación de framer-motion de la pregunta saliente/entrante, y el estado de feedback.
    *   **Orquestación**: 
        1. Pide la pregunta (API). 
        2. Renderiza la UI adaptativa (Teclado numérico, Selección Múltiple, Arrastrar y Soltar). 
        3. Envía respuesta. 
        4. Si el backend devuelve `es_espejo = true`, levanta el Modal de Rescate de inmediato.
        5. Avanza a la siguiente pregunta o gradúa el nivel.

### C. Componentes Reutilizables y Modales
*   **`FaseXTheoryModal.tsx`**: Renderizador de las explicaciones previas al nivel.
*   **`FaseXMirrorModal.tsx`**: Componente de alta prioridad. Cuando se activa, oscurece la pantalla de juego y obliga al niño a leer la explicación detallada de por qué se equivocó, antes de dejarlo volver a intentar.

---

## 4. Flujo de Trabajo Sugerido para Implementación

Construir una fase completa puede ser abrumador si se intenta hacer todo a la vez. El siguiente flujo de trabajo está diseñado para construir de manera incremental, asegurando que el frontend y el backend se integren suavemente sin bloqueos.

### Paso 1: Diseño Pedagógico y Lógico (Mockups)
Antes de escribir código, define las reglas del juego:
*   **Mapeo de Módulos**: ¿Cuántos módulos tendrá la fase? (ej. Módulo 1: Sumas, Módulo 2: Restas).
*   **Mapeo de Niveles**: Define cuántos niveles tiene cada módulo y qué requiere para ganarse (ej. 10 aciertos).
*   **Tipo de Input**: Define si el niño usará un teclado numérico (`respuesta_numerica`), elegirá opciones (`multiple_opcion`) o si será un juego de arrastrar/tocar.
*   **Teoría (JSON)**: Redacta en papel o en un archivo temporal los textos de ayuda y diccionario que irán en la base de datos (`NivelTeoria`).

### Paso 2: Setup Backend Inicial (Contratos y Mocks)
Crea la estructura base para que el frontend pueda empezar a trabajar, incluso si la lógica matemática real aún no existe.
1.  **Esquemas (`schemas.py`)**: Define exactamente qué JSON enviará el servidor al cliente (Pregunta) y qué JSON espera recibir (Respuesta).
2.  **Endpoints Mockeados (`router.py`)**: Crea las rutas (`/dashboard`, `/pregunta`, `/responder`) devolviendo **datos falsos y fijos** (hardcoded). 
    * *Ejemplo:* El endpoint de pregunta siempre devuelve "2 + 2" y el endpoint de responder siempre dice "es_correcta: true".

### Paso 3: Integración Frontend (UI y Animaciones)
Con el backend mockeado, el desarrollo del frontend se vuelve puro diseño y experiencia de usuario (UX).
1.  **Tipos (`FaseXTypes.ts`)**: Copia los contratos del backend.
2.  **Dashboard**: Construye la pantalla de selección de niveles con sus colores e íconos.
3.  **Game Screen**: Construye la pantalla de juego. 
    *   Asegúrate de que el input (teclado/botones) funcione bien.
    *   Añade las animaciones de Framer Motion para cuando entra una nueva pregunta y cuando el usuario acierta o falla (feedback visual).

### Paso 4: Lógica Dura en Backend (El Motor)
Ahora reemplaza los mocks en el backend por código real.
1.  **Generadores (`generators.py`)**: Escribe el código en Python que genera preguntas matemáticas aleatorias y calcula sus respuestas correctas basándose en la dificultad del nivel.
2.  **Evaluación (`router.py`)**: En el endpoint `/responder`, implementa la lógica para leer la respuesta del niño, compararla con la correcta y guardar el progreso real en las tablas `IntentoPregunta` y `ProgresoAlumno`.

### Paso 5: El "Tutor Invisible" y Refinamiento (UX/Pedagogía)
Esta es la capa de calidad que hace que la app sea educativa y no solo un test.
1.  **Bucle Espejo**: En el backend, programa que si el niño lleva 3 errores seguidos, el resultado devuelva `es_espejo: true`. En el frontend, haz que esto dispare inmediatamente el modal de ayuda (`FaseXMirrorModal`).
2.  **Teoría Dinámica**: Conecta el endpoint de lectura para que muestre la teoría antes de comenzar.
3.  **Early Exit (Desafíos)**: Si es un nivel tipo Desafío, configura el límite de errores que expulsa al usuario al dashboard.

### Paso 6: QA y Pruebas Extremas
Juega la fase completa prestando especial atención a:
*   **El camino feliz**: Jugar perfecto y ver que el progreso llegue al 100% y se gradúe la fase.
*   **El camino de errores**: Falla a propósito 3 veces para asegurar que el modal de Rescate (Espejo) aparece, bloquea el avance, y que la siguiente pregunta es exactamente del mismo tipo.

---

## 5. Manteniendo la Consistencia Visual y UX (Estilos y Animaciones)

Para garantizar que la nueva fase se sienta idéntica a la Fase 2 (animaciones fluidas, destellos rojos de error, destellos verdes de acierto, teclado numérico), debes re-utilizar la infraestructura visual ya establecida:

### A. Variables de Diseño y CSS Core (Dark Space)
La Fase 2 utiliza un tema "Dark Space" con acentos neón y "glassmorphism". Al crear una nueva fase, el desarrollador (o el LLM) debe definir y utilizar exactamente este diccionario visual en el CSS de la fase (`FaseXStyles.css`):

1. **Paleta de Colores Base**:
   ```css
   :root {
     --f2-bg-deep:       #0b0f1a;
     --f2-bg-card:       #131929;
     --f2-bg-glass:      rgba(255, 255, 255, 0.04);
     --f2-border:        rgba(255, 255, 255, 0.08);
     --f2-text-primary:  #e8edf5;
     --f2-text-secondary:#8a9bbf;
     --f2-correct:       #10B981; /* Verde Neón */
     --f2-error:         #EF4444; /* Rojo Alerta */
   }
   ```
2. **Estructura del Wrapper y Tarjetas (Glassmorphism)**:
   * **Pantalla Principal (`.f2-screen`)**: Debe tener `background: var(--f2-bg-deep);` con un ligero `radial-gradient` para darle volumen espacial.
   * **Tarjetas (`.f2-question-card`)**: Fondo oscuro `var(--f2-bg-card)`, bordes sutiles `border: 1px solid var(--f2-border)`, esquinas muy redondeadas `border-radius: 20px` y opcionalmente sombra paralela.

3. **Diseño del Teclado Numérico**:
   Para los teclados en pantalla, usa CSS grid (ej: `grid-template-columns: repeat(3, 1fr)`) y estiliza los botones (`.f2-key`) obligatoriamente así:
   ```css
   .f2-key {
     background: rgba(255, 255, 255, 0.05);
     border: 1px solid rgba(255, 255, 255, 0.1);
     color: white;
     border-radius: 16px;
     font-size: 1.8rem;
     font-weight: 700;
     transition: all 0.2s ease;
   }
   /* Efecto hover vibrante al tocar */
   .f2-key:active { background: rgba(255,255,255, 0.15); transform: scale(0.95); }
   ```

### B. Lógica de Feedback con Framer Motion (Rojo / Verde)
La regla estricta de UX al responder es pintar el fondo de verde para un acierto o de rojo con un efecto de "Shake" (temblor lateral) para un error. **Esta es la receta exacta que el LLM debe seguir en React**:

1. **Control de Estado de Feedback**:
   ```tsx
   const [feedback, setFeedback] = useState({ visible: false, esCorrecta: false });
   ```

2. **Capa Superpuesta Animada (Overlay con Shake)**:
   Usa `framer-motion` envolviendo el componente principal o la tarjeta de juego para generar el destello visual de acierto/error:
   ```tsx
   <motion.div 
     className="fase-container"
     animate={{
       // Transición suave al verde o rojo
       backgroundColor: feedback.visible 
         ? (feedback.esCorrecta ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)') 
         : 'transparent',
       // Shake animation (temblor) solo si es error
       x: (feedback.visible && !feedback.esCorrecta) ? [-10, 10, -10, 10, 0] : 0
     }}
     transition={{ duration: 0.3 }}
   >
     {/* Contenido de la pregunta... */}
   </motion.div>
   ```

3.  **Teclado Numérico Animado (Keypad Variants)**:
    Si la fase usa entrada numérica, debes copiar las constantes de animación del teclado de la Fase 2 para mantener esa sensación de aparición elástica (efecto *spring*):
    ```tsx
    const keypadVariants = {
      hidden: { opacity: 0, scale: 0.9 },
      show: {
        opacity: 1, scale: 1,
        transition: { staggerChildren: 0.05, type: "spring", stiffness: 300, damping: 20 }
      }
    };
    ```

### C. Presentación de la Información (Layout UI)
Para que la interfaz no desoriente al niño, mantén siempre la misma jerarquía visual de la Fase 2:
1.  **Barra Superior (Top Bar)**: Botón de salir a la izquierda, título del Nivel en el centro, y los indicadores de progreso (estrellas, rachas) y cronómetro a la derecha.
2.  **Enunciado (Centro)**: El texto debe tener una fuente grande y legible, dentro de un contenedor con fondo oscuro semitransparente (`background: rgba(0,0,0,0.4)`) y texto blanco o resaltado.
3.  **Área de Interacción (Abajo)**: Ya sea el teclado de 9 botones, cajas de selección o bloques para arrastrar, colócalo siempre anclado a la parte inferior. Esto lo hace amigable para los pulgares en dispositivos móviles y tabletas.

---

## 6. Referencia Técnica para IAs (Contratos y Esqueletos)

Si eres un LLM leyendo este documento para generar una nueva fase (ej. Fase 3), **utiliza los siguientes esqueletos** como base exacta para no romper la integración con la base de datos principal y el frontend.

### A. Esqueleto de Schemas (`schemas.py`)
Para que el frontend entienda la pregunta y el backend procese la respuesta, implementa esta estructura Pydantic:

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FaseXPreguntaParaAlumno(BaseModel):
    modulo_id: int
    nivel_id: int
    enunciado: str
    tipo_pregunta: str # ej: 'respuesta_numerica', 'multiple_opcion'
    # NUNCA incluyas la respuesta_correcta aquí a menos que sea estrictamente interno
    tiene_cronometro: bool = False
    tiempo_limite_segundos: Optional[int] = None
    
    # Progreso en vivo
    aciertos_acumulados: int = 0
    intentos_totales: int = 0
    porcentaje_actual: int = 0

class FaseXResponderPregunta(BaseModel):
    modulo_id: int
    nivel_id: int
    respuesta_dada: str
    tiempo_respuesta_segundos: float

class FaseXResultadoRespuesta(BaseModel):
    es_correcta: bool
    respuesta_correcta: Optional[str] = None
    feedback_error: Optional[str] = None # Mensaje pedagógico si falló
    
    aciertos_acumulados: int
    porcentaje_actual: int
    bloque_completado: bool = False
    
    # Bucle Espejo y Early Exit
    es_espejo: bool = False
    early_exit: bool = False
```

### B. Esqueleto del Router (`router.py`)
Utiliza la inyección de dependencias estándar del proyecto para el usuario y la base de datos:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# Asume que las dependencias de auth y bd están en app.auth y app.db.session
# from app.auth import get_current_student
# from app.db.session import get_db

router = APIRouter(prefix="/faseX", tags=["faseX"])

@router.get("/modulo/{modulo_id}/nivel/{nivel_id}/pregunta", response_model=FaseXPreguntaParaAlumno)
async def get_pregunta(modulo_id: int, nivel_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_student)):
    # Lógica del generador aquí...
    pass

@router.post("/responder", response_model=FaseXResultadoRespuesta)
async def responder(payload: FaseXResponderPregunta, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_student)):
    # 1. Validar respuesta
    # 2. Actualizar intentos
    # 3. Disparar es_espejo si lleva 3 errores
    pass
```

### C. Esqueleto de Componente React (`FaseXGameScreen.tsx`)
El componente principal SIEMPRE debe recibir estos Props básicos y manejar estos estados internos:

```tsx
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
// import { FaseXPregunta, FaseXAnswerResult } from './FaseXTypes';

interface Props {
  moduloId: number;
  nivelId: number;
  onComplete: () => void; // Disparado cuando el nivel llega al 100%
  onBack: () => void;     // Disparado al presionar salir
}

export const FaseXGameScreen: React.FC<Props> = ({ moduloId, nivelId, onComplete, onBack }) => {
  const [pregunta, setPregunta] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState({ visible: false, esCorrecta: false, msg: '' });

  // Al montar, solicitar pregunta a la API...
  
  return (
    <motion.div className="fase-container" /*...lógica del color vista en sección 5...*/>
       {/* Barra superior con onBack */}
       {/* UI del Enunciado */}
       {/* Teclado / Botones de Input */}
    </motion.div>
  );
}
```

---

## 7. Piezas Clave de Integración y Persistencia

Para que la Fase funcione en el mundo real, no basta con la lógica aislada. Debes integrarla en el entorno global de la aplicación (tomando como ejemplo la Fase 2):

### A. Inyección de Datos Iniciales (`seed.py`)
El frontend fallará si intenta buscar teoría o niveles que no existen en la base de datos.
*   **Requisito**: Debes crear un script `backend/app/faseX/seed.py`.
*   **Función**: Este script contiene diccionarios JSON en bruto con los párrafos, el diccionario y los ejemplos de cada nivel. Debe poseer una función asíncrona `seed_faseX(db: AsyncSession)` que haga un `UPSERT` (Insertar o Actualizar) en la tabla `NivelTeoria` (y `Fase`, `Pregunta` si aplica).
*   Asegúrate de invocar este `seed_faseX` en el script principal de inicialización de la base de datos (`seed_global.py` o similar).

### B. Enrutamiento Global (Frontend y Backend)
La fase no existe si no es accesible por el usuario.
*   **En Backend (`main.py`)**: 
    Asegúrate de importar e incluir el router para habilitar los endpoints:
    ```python
    from app.faseX.router import router as fasex_router
    app.include_router(fasex_router)
    ```
*   **En Frontend (`App.tsx` o enrutador principal)**: 
    Debes registrar las rutas para el Dashboard y para jugar la nueva fase:
    ```tsx
    import { FaseXDashboard } from './components/faseX/FaseXDashboard';
    // ...
    <Route path="/faseX" element={<FaseXDashboard />} />
    ```

### C. Persistencia de Sesión (Manejo de Recargas)
¿Qué ocurre si el usuario presiona "F5" o recarga la pestaña a mitad de un Desafío?
*   El backend gestiona el progreso con tablas como `IntentoPregunta`, pero **el frontend debe ser resiliente**.
*   Al montar `FaseXGameScreen.tsx`, la llamada inicial a la API (`get_pregunta`) no debe crear un nivel desde cero automáticamente; el backend debe detectar si hay un intento en curso y devolver la pregunta en la que se quedó el alumno junto con su porcentaje de progreso previo.
*   No guardes la lógica de "cuántos errores llevo" únicamente en estados de React, o se perderá al recargar. Siempre depende de lo que dicte el backend.

---

## 8. Checklist Final de Calidad (QA para IA / Desarrolladores)

Antes de declarar que la Fase X está terminada, verifica obligatoriamente los siguientes puntos:

- [ ] **Data Contracts**: ¿El archivo `FaseXTypes.ts` en frontend coincide 100% con los modelos Pydantic en `schemas.py`?
- [ ] **El Bucle Espejo**: ¿Al fallar reiteradamente (ej. 3 veces), el sistema bloquea el progreso, levanta el modal de ayuda y la siguiente pregunta evalúa el mismo concepto?
- [ ] **Teoría Dinámica**: ¿Las lecturas y ejemplos provienen de la BD (vía `seed.py`) y no están fijas (hardcoded) en los archivos `.tsx`?
- [ ] **Consistencia UI/UX**: ¿La fase respeta el tema *Dark Space* (fondos, botones de cristal) y usa Framer Motion para los destellos Rojo (shake) y Verde al responder?
- [ ] **Mecánica Early Exit**: En los niveles marcados como *Desafío*, ¿el sistema expulsa al usuario al dashboard si supera el límite de errores permitidos?
- [ ] **Seguridad Anti-Trampas**: ¿Te aseguraste de que el Backend NUNCA envíe el campo `respuesta_correcta` en el JSON para preguntas de opción múltiple?
- [ ] **Graduación Global**: ¿El endpoint de graduación desbloquea la siguiente fase en la tabla global de progreso del usuario?
