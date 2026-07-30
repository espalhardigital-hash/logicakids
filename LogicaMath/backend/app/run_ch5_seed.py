"""
Script de Siembra de Terreno CH-5: Estructura de 4 Módulos × 3 Niveles y Práctica Libre en Input Libre
"""

import asyncio
from app.db.session import AsyncSessionLocal
from app.fase5.seed import clear_fase5_data, seed_practica_pool, seed_configuracion_progreso

async def main():
    print("=== INICIANDO SIEMBRA CH-5 ===")
    async with AsyncSessionLocal() as session:
        await clear_fase5_data(session)
        await seed_practica_pool(session)
        await seed_configuracion_progreso(session)
    print("=== SIEMBRA CH-5 COMPLETADA EXITOSAMENTE ===")

if __name__ == "__main__":
    asyncio.run(main())
