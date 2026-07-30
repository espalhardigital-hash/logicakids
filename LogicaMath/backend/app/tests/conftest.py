"""
conftest.py — Fixtures para la suite de tests de integración de backend.

Fixture `db_session`:
- Usa AsyncSessionLocal de app/db/session.py.
- Hace rollback al terminar: los tests NO persisten nada en la BD (deep_analise_pro §15.5).
- Compatible con pytest-asyncio 1.x (asyncio_mode=auto en pytest.ini o pyproject.toml).
"""

import pytest
import pytest_asyncio
from app.db.session import AsyncSessionLocal


@pytest_asyncio.fixture
async def db_session():
    """Fixture de sesión de BD asíncrona.

    Crea una sesión, la cede al test y hace rollback al finalizar.
    El test nunca escribe datos permanentes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
