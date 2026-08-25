> ✅ **Reestructuración de la Fase 4 completada.**
> `docs/reestructuraciondefases.md` se conserva como referencia histórica; la tabla canónica de este documento refleja el estado real de la BD local.
# Mapa Canónico de Fases — LogicaKids Pro

> **Versión:** 2.1 (Fases 5 y 6 verificadas localmente)
> **Fecha de Actualización:** 2026-08-23
> **Propósito:** Documento rector de equivalencia entre Base de Datos, Backend, Frontend y Contenido Pedagógico para evitar bugs de desalineación o borrado accidental (`Arquetipo H` / `Recomendación R1`).

> **DEUDA VERIFICADA (2026-07-30):** la tabla representa el objetivo canónico, pero el código de Fases 7–11 todavía no lo cumple por completo. Existen routers, constantes, seeders y componentes heredados con números cruzados. No ejecutar movimientos o borrados parciales en esas carpetas hasta completar una migración integral con pruebas de importación, endpoints y seeding.

---

## Tabla Canónica de Equivalencia de Fases

| `fase_id` (DB) | Orden | Nombre Pedagógico Oficial (`app/seed.py`) | Backend Path | API Prefix | Frontend Component Main | Modulos |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | 1 | Aritmética Básica | `app/fase1/` | `/api/fase1` | `Fase1GameScreen.tsx` | 4 |
| **2** | 2 | Desarrollo Numérico y Razonamiento | `app/fase2/` | `/api/fase2` | `Fase2GameScreen.tsx` | 4 |
| **3** | 3 | Problemas de Texto y Sistemas Simples | `app/fase3/` | `/api/fase3` | `Fase3GameScreen.tsx` | 4 |
| **4** | 4 | Operatoria Decimal y Conversiones | `app/fase4/` | `/fase4` | `Fase4GameScreen.tsx` | 4 |
| **5** | 5 | Fracciones, Porcentajes y Proporciones | `app/fase5/` | `/fase5` | `Fase5GameScreen.tsx` | 4 |
| **6** | 6 | Geometría Plana Multiforme y Áreas | `app/fase6/` | `/fase6` | `Fase6GameScreen.tsx` | 4 |
| **7** | 7 | Geometría Espacial, Volumen y Magnitudes | `app/fase7/` | `/fase7` | `Fase7GameScreen.tsx` | 4 |
| **8** | 8 | Coordenadas, Rutas y Tiempo | `app/fase8/` | `/fase8` | `Fase8GameScreen.tsx` | 4 |
| **9** | 9 | Probabilidad, Combinatoria y Lógica | `app/fase9/` | `/fase9` | `Fase9GameScreen.tsx` | 4 |
| **10** | 10 | Razonamiento Abstracto y Visual | `app/fase10/` | `/fase10` | `Fase10GameScreen.tsx` *(En Const.)* | 4 |
| **11** | 11 | Simulacros | `app/fase11/` | `/fase11` | `Fase11GameScreen.tsx` | 4 |

---

## Reglas Estrictas de Mantenimiento

1. **Invariante de ID (Acotación a Producción):**
   > 🔴 **DEROGACIÓN NORMATIVA (A0 #4):** La prohibición absoluta de re-numerar `fase_id` queda acotada exclusivamente a entornos de **Producción VPS**. El intercambio seguro de `fase_id` entre Fase 4 (Decimales) y Fase 5 (Fracciones) se ejecutó localmente en la reestructuración de la Fase 4 sin afectar bases de datos activas de alumnos en producción. En desarrollo local o migraciones planeadas, la re-numeración es legítima mediante script de migración verificado.
2. **Purge de Datos:** Cualquier script de re-siembra o limpieza (`clear_faseN_data`) debe usar **exclusivamente** el `fase_id` exacto de esta tabla canónica.
3. **Fases en Construcción:** La Fase 10 se considera en desarrollo reservado sin diseño interno activo.
4. **Estado operativo F5/F6:** ambas fases siguen este mapa, fueron resembradas y auditadas localmente. Su regla común es corrección obligatoria de 10 segundos tras error, sin preguntas espejo y sin scroll vertical. Ver [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](./ESTADO_IMPLEMENTACION_FASES_5_6.md).
