"""Read-only inventory of Phase 4 configuration and progression integrity."""

import argparse
import asyncio
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.db.session import AsyncSessionLocal, DATABASE_URL
from app.fase4.topology import FASE4_ID, PLAYABLE_SECTIONS
from app.models.sql_models import ConfiguracionProgreso, ProgresoMaestria


def _database_identity() -> dict:
    url = make_url(DATABASE_URL)
    return {
        "driver": url.drivername,
        "host": url.host,
        "port": url.port,
        "database": url.database,
    }


async def build_inventory() -> dict:
    async with AsyncSessionLocal() as session:
        config_result = await session.execute(
            select(ConfiguracionProgreso).where(
                ConfiguracionProgreso.fase_id == FASE4_ID
            )
        )
        configs = list(config_result.scalars().all())

        progress_result = await session.execute(
            select(ProgresoMaestria).where(ProgresoMaestria.fase_id == FASE4_ID)
        )
        progresses = list(progress_result.scalars().all())

    config_sections = Counter(config.seccion for config in configs)
    progress_sections = Counter(progress.seccion for progress in progresses)
    progress_states = Counter(
        str(getattr(progress.estado, "value", progress.estado)) for progress in progresses
    )
    phantom_progress = [
        {
            "id": progress.id,
            "alumno_id": progress.alumno_id,
            "seccion": progress.seccion,
            "estado": str(getattr(progress.estado, "value", progress.estado)),
        }
        for progress in progresses
        if progress.seccion not in PLAYABLE_SECTIONS
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": _database_identity(),
        "phase_id": FASE4_ID,
        "canonical_playable_sections": sorted(PLAYABLE_SECTIONS),
        "configurations": {
            "total_rows": len(configs),
            "global_rows": config_sections.get(0, 0),
            "by_section": dict(sorted(config_sections.items())),
            "missing_playable_sections": sorted(PLAYABLE_SECTIONS - set(config_sections)),
            "noncanonical_sections": sorted(
                set(config_sections) - PLAYABLE_SECTIONS - {0}
            ),
        },
        "progress": {
            "total_rows": len(progresses),
            "by_section": dict(sorted(progress_sections.items())),
            "by_state": dict(sorted(progress_states.items())),
            "phantom_rows": phantom_progress,
        },
        "reconciliation_executed": False,
        "reconciliation_note": (
            "This command is read-only. Reconciliation requires an identified "
            "development snapshot and an explicit archive/delete decision."
        ),
    }


async def main(snapshot_path: str | None) -> int:
    inventory = await build_inventory()
    rendered = json.dumps(inventory, ensure_ascii=False, indent=2)
    print(rendered)
    if snapshot_path:
        path = Path(snapshot_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Snapshot written to: {path.resolve()}")
    return 1 if inventory["progress"]["phantom_rows"] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        help="Optional JSON output path. No database rows are modified.",
    )
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.snapshot)))
