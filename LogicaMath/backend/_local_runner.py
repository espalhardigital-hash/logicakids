"""
Runner local (sin Docker backend) para crear el esquema y ejecutar seeds/consultas
contra el Postgres local del stack docker-compose.local.yml (puerto 5433).

Uso:
    python _local_runner.py create        -> crea todas las tablas (create_all)
    python _local_runner.py seed <fase>   -> ejecuta el seed de una fase (5..9)

NO se commitea. Herramienta de verificación local.
"""
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import app.main  # noqa: F401  -> registra todos los modelos en Base.metadata
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[create_all] OK")


async def run_seed(fase: str):
    # Entrypoints reales según app/seed.py (algunos manejan su propia sesión).
    if fase == "4":
        from app.fase4.seed import run_fase4_seed
        await run_fase4_seed()
    elif fase == "5":
        from app.fase5.seed import run_fase5_seed
        async with AsyncSessionLocal() as session:
            await run_fase5_seed(session)
    elif fase == "6":
        from app.fase6.seed import seed_fase6_full
        await seed_fase6_full()
    elif fase == "7":
        from app.fase7.seed_fase7 import run_fase7_seed
        await run_fase7_seed()
    elif fase == "8":
        # El seed de Fase 8 vive (por un desajuste histórico) en app/fase9/seed_fase8.py
        from app.fase9.seed_fase8 import run_fase8_seed
        await run_fase8_seed()
    elif fase == "9":
        # Simulados (fase_id=9): el seed vive en app/fase11/seed_fase9.py
        from app.fase11.seed_fase9 import run_fase9_seed
        await run_fase9_seed()
    else:
        raise SystemExit(f"Fase desconocida: {fase}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "create"

    async def _main():
        if cmd == "create":
            await create_all()
        elif cmd == "seed":
            await create_all()
            await run_seed(sys.argv[2])
        else:
            raise SystemExit(f"Comando desconocido: {cmd}")

    asyncio.run(_main())
