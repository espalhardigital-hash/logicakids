path = r"D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\frontend\components\admin\phaseMaps.ts"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update IDs in reverse order
content = content.replace('name: "Fase 9: Simulados Pedro II"', 'name: "Fase 11: Simulacros"')
content = content.replace('name: "Fase 8: Lógica, Combinatoria y Probabilidad"', 'name: "Fase 9: Probabilidad, Combinatoria y Lógica"')
content = content.replace('name: "Fase 7: Coordenadas, Rutas y Tiempo"', 'name: "Fase 8: Coordenadas, Rutas y Tiempo"')
content = content.replace('name: "Fase 6: Geometría Espacial, Volumen y Magnitudes Físicas"', 'name: "Fase 7: Geometría Espacial, Volumen y Magnitudes"')
content = content.replace('name: "Fase 5: Geometría Plana y Medidas"', 'name: "Fase 6: Geometría Plana Multiforme y Áreas"')

op_decimal = """  {
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
"""

if 'name: "Fase 6: Geometría Plana Multiforme y Áreas"' in content:
    idx_f6 = content.find('name: "Fase 6: Geometría Plana Multiforme y Áreas"')
    idx_brace = content.rfind('{', 0, idx_f6)
    content = content[:idx_brace] + op_decimal + content[idx_brace:]

fase_10 = """  {
    id: 10,
    name: "Fase 10: Razonamiento Abstracto y Visual",
    modules: [
      {
        id: 1,
        name: "Módulo 1: Razonamiento Visual (Próximamente)",
        levels: [
          { id: 1, name: "Fase Reservada", seccion: 101, operacion: "mixta" }
        ]
      }
    ]
  },
"""

if 'name: "Fase 11: Simulacros"' in content:
    idx_f11 = content.find('name: "Fase 11: Simulacros"')
    idx_brace = content.rfind('{', 0, idx_f11)
    content = content[:idx_brace] + fase_10 + content[idx_brace:]

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("phaseMaps.ts actualizado con las 11 fases.")
