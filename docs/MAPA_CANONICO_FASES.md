# Mapa Canónico de Fases — LogicaKids Pro

> **Versión:** 1.0  
> **Fecha de Congelamiento:** 2026-07-25  
> **Propósito:** Documento rector de equivalencia entre Base de Datos, Backend, Frontend y Contenido Pedagógico para evitar bugs de desalineación o borrado accidental (`Arquetipo H` / `Recomendación R1`).

---

## Tabla Canónica de Equivalencia de Fases

| `fase_id` (DB) | Orden | Nombre Pedagógico Oficial | Backend Path | API Prefix | Frontend Component Main | Modulos |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **0** | 0 | Introducción y Diagnóstico Inicial | `app/fase1/` | `/api/fase1` | `Fase1GameScreen.tsx` | 1 |
| **1** | 1 | Pre-Conteo y Cantidades | `app/fase1/` | `/api/fase1` | `Fase1GameScreen.tsx` | 4 |
| **2** | 2 | Operaciones Básicas y Tienda | `app/fase2/` | `/api/fase2` | `Fase2GameScreen.tsx` | 4 |
| **3** | 3 | Multiplicación y División | `app/fase3/` | `/api/fase3` | `Fase3GameScreen.tsx` | 4 |
| **4** | 4 | Fracciones y Porcentajes | `app/fase4/` | `/api/fase4` | `Fase4GameScreen.tsx` | 4 |
| **5** | 5 | Geometría, Perímetros y Áreas | `app/fase5/` | `/api/fase5` | `Fase5GameScreen.tsx` | 4 |
| **6** | 6 | Cubos Unitarios y Razonamiento | `app/fase6/` | `/api/fase6` | `Fase6GameScreen.tsx` | 4 |
| **7** | 7 | Tiempo, Relojes y Calendarios | `app/fase7/` | `/api/fase7` | `Fase7GameScreen.tsx` | 4 |
| **8** | 8 | Probabilidad y Estadística | `app/fase8/` | `/api/fase8` | `Fase8GameScreen.tsx` | 4 |
| **9** | 9 | Simulados y Evaluación Global | `app/fase9/` | `/api/fase9` | `Fase9GameScreen.tsx` *(En Const.)* | 4 |
| **10** | 10 | Avanzado / Lógica Compleja | `app/fase10/` | `/api/fase10` | `Fase10GameScreen.tsx` *(En Const.)* | 4 |
| **11** | 11 | Desafíos TJS y Maestría | `app/fase11/` | `/api/fase11` | `Fase11GameScreen.tsx` *(En Const.)* | 4 |

---

## Reglas Estrictas de Mantenimiento

1. **Invariante de ID:** Bajo ninguna circunstancia se deben modificar o re-numerar los valores de `fase_id` en la tabla `fases` de la Base de Datos en producción.
2. **Purge de Datos:** Cualquier script de re-siembra o limpieza (`clear_faseN_data`) debe usar **exclusivamente** el `fase_id` exacto de esta tabla canónica.
3. **Fases en Construcción:** Fases 9, 10 y 11 se consideran en desarrollo y no forman parte de la suite activa de producción sin auditoría previa.
