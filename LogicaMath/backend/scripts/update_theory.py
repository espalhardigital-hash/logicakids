import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, update
from app.db.session import AsyncSessionLocal
from app.fase2.models import NivelTeoria
from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase4

# Textos actualizados y formales para Módulo 4
TEORIA_MODULO_4 = {
    1: {
        "titulo": "Razones y Proporciones",
        "texto_descubrimiento": "Una **razón** es una comparación matemática entre dos cantidades mediante una división. Nos indica cuántas partes de un elemento se necesitan en relación con otro elemento. Por ejemplo, si una receta de limonada requiere 3 tazas de agua por cada 1 taza de zumo de limón, la razón es **3 a 1 (o 3:1)**.\n---\nPara preparar cantidades más grandes conservando el sabor original, aplicamos una **proporción**. Esto significa multiplicar o dividir ambos términos de la razón por un mismo número, al cual llamamos **factor de escala**. ¡Si duplicas la cantidad de limón, también debes duplicar la de agua para que la mezcla no se arruine!",
        "diccionario": {
            "Razón (a:b)": "La comparación matemática que relaciona dos cantidades e indica cuántas veces una contiene a la otra.",
            "Factor de Escala": "El multiplicador común por el cual aumentamos o disminuimos proporcionalmente todos los elementos de la mezcla."
        },
        "advertencia": "¡Cuidado! Una proporción se amplía multiplicando, nunca sumando. Si la receta es 3:1 y pasas a 2 de limón, debes multiplicar el agua por 2 (3 × 2 = 6). No le sumes simplemente 1."
    },
    2: {
        "titulo": "Reparto de Volúmenes",
        "texto_descubrimiento": "Cuando necesitamos preparar una mezcla a gran escala pero solo conocemos la proporción de sus partes y el **volumen total deseado (volumen macro)**, aplicamos el reparto proporcional. Imagina que para obtener una pintura verde mezclamos 2 litros de azul y 3 de amarillo, lo que produce 5 litros de verde en total (la receta base).\n---\nSi un cliente nos pide 30 litros de verde, el cálculo es simple: primero sumamos las partes para hallar el rendimiento de la receta base (2 + 3 = 5 litros). Luego, dividimos el volumen total pedido entre el volumen de la receta base para obtener el factor de escala (30 ÷ 5 = 6 veces). Finalmente, multiplicamos cada ingrediente por este factor: 2 azul × 6 = 12 litros de azul, y 3 amarillo × 6 = 18 litros de amarillo.",
        "diccionario": {
            "Volumen Macro": "La cantidad total final requerida al juntar todos los componentes de la mezcla.",
            "Receta Base": "La suma de las partes iniciales de cada ingrediente, que indica cuánto produce una sola dosis de la mezcla."
        },
        "advertencia": "Suma primero todas las partes de la receta original para saber el total que rinde. Luego divide el volumen macro entre ese total para hallar tu factor de escala."
    },
    3: {
        "titulo": "Mezclas Complejas",
        "texto_descubrimiento": "En muchas mezclas es crucial determinar qué parte del volumen total representa un único ingrediente. Esto nos permite entender la **concentración** o **fracción de mezcla**. Por ejemplo, si mezclas 1 gota de esencia de flores con 4 gotas de alcohol, tendrás 5 gotas de perfume en total. La esencia representa 1 de las 5 partes totales (fracción 1/5).\n---\nSi convertimos esta fracción a porcentaje dividiendo 1 entre 5 y multiplicando por 100, descubrimos que la esencia representa el **20% del volumen total**. El porcentaje nos ayuda a comparar la concentración de diferentes sustancias de forma estandarizada y directa.",
        "diccionario": {
            "Fracción de Mezcla": "La relación matemática entre la cantidad de un ingrediente y el volumen total de la mezcla.",
            "Homogeneidad": "La propiedad por la cual los componentes de una mezcla están distribuidos de forma uniforme en cualquier porción."
        },
        "advertencia": "¡Ojo! La fracción de un ingrediente se calcula dividiendo su porción entre el TOTAL de todas las partes juntas, no entre la cantidad del otro ingrediente."
    }
}

async def main():
    async with AsyncSessionLocal() as session:
        # 1. Primero actualizamos Módulo 3 Nivel 4 (ejemplos solamente)
        print("Obteniendo ejemplos para Modulo 3, Nivel 4...")
        theory_data_3_4 = obtener_ejemplos_expandidos_fase4(3, 4)
        if theory_data_3_4:
            print("Actualizando NivelTeoria Fase 4 Modulo 3 Nivel 4...")
            stmt = update(NivelTeoria).where(
                NivelTeoria.fase_id == 4,
                NivelTeoria.modulo_id == 3,
                NivelTeoria.nivel_id == 4
            ).values(ejemplos=theory_data_3_4)
            await session.execute(stmt)
            await session.commit()
            print("Módulo 3 Nivel 4 actualizado.")

        # 2. Actualizamos los 3 niveles del Módulo 4
        for nivel_id, info in TEORIA_MODULO_4.items():
            print(f"Obteniendo ejemplos para Modulo 4, Nivel {nivel_id}...")
            ejemplos = obtener_ejemplos_expandidos_fase4(4, nivel_id)
            
            if ejemplos:
                print(f"Actualizando toda la teoría de Fase 4 Modulo 4 Nivel {nivel_id} en BD...")
                stmt = update(NivelTeoria).where(
                    NivelTeoria.fase_id == 4,
                    NivelTeoria.modulo_id == 4,
                    NivelTeoria.nivel_id == nivel_id
                ).values(
                    titulo=info["titulo"],
                    texto_descubrimiento=info["texto_descubrimiento"],
                    diccionario=info["diccionario"],
                    advertencia=info["advertencia"],
                    ejemplos=ejemplos
                )
                await session.execute(stmt)
                await session.commit()
                print(f"Módulo 4 Nivel {nivel_id} actualizado por completo.")
            else:
                print(f"No se pudieron obtener ejemplos para Módulo 4 Nivel {nivel_id}")

if __name__ == "__main__":
    asyncio.run(main())
