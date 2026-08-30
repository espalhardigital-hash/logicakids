"""
conftest.py — Fixtures para la suite de tests de integración de backend.

Fixture `db_session`:
- Usa una transacción externa y savepoints sobre el engine de pruebas.
- Incluso si un endpoint llama `commit()`, el rollback exterior impide persistir
  datos en la BD (deep_analise_pro §15.5).
- Compatible con pytest-asyncio 1.x (asyncio_mode=auto en pytest.ini o pyproject.toml).
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine


@pytest_asyncio.fixture
async def db_session():
    """Fixture de sesión de BD asíncrona.

    ``join_transaction_mode='create_savepoint'`` hace que los ``commit()``
    internos de los routers cierren solo un savepoint. La transacción exterior
    permanece bajo control del fixture y siempre se revierte al finalizar.
    """
    async with engine.connect() as connection:
        outer_transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield session
        finally:
            await session.close()
            if outer_transaction.is_active:
                await outer_transaction.rollback()
    # pytest-asyncio may create a new event loop for the next parametrized
    # case; do not return asyncpg connections bound to the previous loop.
    await engine.dispose()
