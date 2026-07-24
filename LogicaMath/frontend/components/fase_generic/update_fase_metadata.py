path = r"D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\frontend\components\fase_generic\faseMetadata.ts"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update faseId in reverse order
content = content.replace("export const FASE_9: FaseMetadata = {\n  faseId: 9,\n  nombre: 'Fase 9: Simulados Pedro II'", "export const FASE_11: FaseMetadata = {\n  faseId: 11,\n  nombre: 'Fase 11: Simulacros'")
content = content.replace("export const FASE_8: FaseMetadata = {\n  faseId: 8,\n  nombre: 'Fase 8: Lógica, Combinatoria y Probabilidad'", "export const FASE_9: FaseMetadata = {\n  faseId: 9,\n  nombre: 'Fase 9: Probabilidad, Combinatoria y Lógica'")
content = content.replace("export const FASE_7: FaseMetadata = {\n  faseId: 7,\n  nombre: 'Fase 7: Coordenadas y Desplazamientos'", "export const FASE_8: FaseMetadata = {\n  faseId: 8,\n  nombre: 'Fase 8: Coordenadas, Rutas y Tiempo'")
content = content.replace("export const FASE_6: FaseMetadata = {\n  faseId: 6,\n  nombre: 'Fase 6: Geometría Espacial'", "export const FASE_7: FaseMetadata = {\n  faseId: 7,\n  nombre: 'Fase 7: Geometría Espacial, Volumen y Magnitudes'")
content = content.replace("export const FASE_5: FaseMetadata = {\n  faseId: 5,\n  nombre: 'Fase 5: Geometría Plana y Medidas'", "export const FASE_6: FaseMetadata = {\n  faseId: 6,\n  nombre: 'Fase 6: Geometría Plana Multiforme y Áreas'")

fase5_meta = """export const FASE_5: FaseMetadata = {
  faseId: 5,
  nombre: 'Fase 5: Operatoria Decimal y Conversiones',
  subtitulo: 'Dominio de operaciones con decimales y sistema de unidades',
  descripcion: 'Aprende a alinear la coma, completar ceros, multiplicar y dividir decimales, y convertir unidades de longitud, volumen y superficie.',
  modulos: [
    {
      moduloId: 1, nombre: 'Suma y Resta de Decimales', descripcion: 'Alineación de comas y completado de ceros.', icono: 'plus', color: '#06B6D4',
      niveles: [{ nivelId: 1, nombre: 'Suma alineando la coma', descripcion: 'Práctica', teoria: { titulo: 'Suma Decimal', parrafos: ['Alinea la coma.'], tip_pedagogico: 'Coma sobre coma.' }, preguntas: [] }]
    }
  ]
};

"""

fase10_meta = """export const FASE_10: FaseMetadata = {
  faseId: 10,
  nombre: 'Fase 10: Razonamiento Abstracto y Visual',
  subtitulo: 'Tangram, figuras abstractas y patrones visuales',
  descripcion: 'Fase reservada (Próximamente).',
  modulos: []
};

"""

if "export const FASE_6:" in content:
    idx = content.find("export const FASE_6:")
    content = content[:idx] + fase5_meta + content[idx:]

if "export const FASE_11:" in content:
    idx = content.find("export const FASE_11:")
    content = content[:idx] + fase10_meta + content[idx:]

content = content.replace(
    "export const ALL_FASES: FaseMetadata[] = [FASE_3, FASE_4, FASE_5, FASE_6, FASE_7, FASE_8, FASE_9];",
    "export const ALL_FASES: FaseMetadata[] = [FASE_3, FASE_4, FASE_5, FASE_6, FASE_7, FASE_8, FASE_9, FASE_10, FASE_11];"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("faseMetadata.ts actualizado con FASE_5..FASE_11.")
