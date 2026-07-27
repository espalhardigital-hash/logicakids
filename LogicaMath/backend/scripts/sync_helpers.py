#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers puros para sincronización local → VPS (preguntas + MinIO).

Alineados con RULES AGENTES/bd_minio.md:
- reescritura de URLs de graphics/
- codificación de contraseñas con '#'
- alcance por fase / sección / operación / IDs
- Fases 5–6 (SVG inline) no requieren MinIO graphics/ por defecto
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Iterable, Optional, Sequence
from urllib.parse import urlparse

# Fases cuya figura va embebida en enunciado (SVG), no en MinIO graphics/
SVG_INLINE_FASES = frozenset({5, 6})


def load_env_file(filepath: str) -> dict[str, str]:
    """Lee un archivo .env simple (KEY=VALUE) y retorna un dict."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo .env en: {filepath}")

    env_data: dict[str, str] = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                env_data[key.strip()] = val.strip()
    return env_data


def rewrite_db_url(
    db_url: str,
    override_host: Optional[str] = None,
    override_port: Optional[int] = None,
) -> str:
    """Convierte URL asyncpg → psycopg2 y codifica '#' en la contraseña."""
    url = db_url.replace("+asyncpg", "")

    if "://" in url:
        scheme, rest = url.split("://", 1)
        if "@" in rest:
            auth, host_path = rest.split("@", 1)
            auth = auth.replace("#", "%23")
            url = f"{scheme}://{auth}@{host_path}"

    if not override_host and not override_port:
        return url

    parsed = urlparse(url)
    scheme = parsed.scheme
    netloc = parsed.netloc
    path = parsed.path

    auth = ""
    host_port = netloc
    if "@" in netloc:
        auth, host_port = netloc.split("@", 1)
        auth += "@"

    host = host_port
    port = ""
    if ":" in host_port:
        host, port = host_port.split(":", 1)

    new_host = override_host if override_host else host
    new_port = str(override_port) if override_port else port

    new_netloc = auth + new_host
    if new_port:
        new_netloc += f":{new_port}"

    return f"{scheme}://{new_netloc}{path}"


def extract_graphics_filename(url: Optional[str]) -> Optional[str]:
    """Extrae el nombre de archivo bajo graphics/ de una URL (o None)."""
    if not url or not isinstance(url, str):
        return None
    if "graphics/" in url:
        return url.split("graphics/", 1)[-1].split("?", 1)[0].strip() or None
    # último segmento si parece un asset con extensión
    tail = url.rstrip("/").split("/")[-1]
    if re.search(r"\.(png|jpe?g|gif|webp|svg)$", tail, re.I):
        return tail
    return None


def rewrite_datos_numericos_url(
    datos: Any,
    public_base: str,
    bucket: str,
) -> Any:
    """
    Reescribe datos_numericos.url al dominio/bucket destino, conservando el filename.

    public_base: p.ej. https://files.example.com (sin slash final)
    bucket: nombre del bucket remoto
    """
    if datos is None:
        return None

    if isinstance(datos, str):
        try:
            datos = json.loads(datos)
        except (json.JSONDecodeError, TypeError):
            return datos

    if not isinstance(datos, dict):
        return datos

    out = dict(datos)
    url = out.get("url")
    filename = extract_graphics_filename(url) if url else None
    if filename:
        base = public_base.rstrip("/")
        bucket = bucket.strip("/")
        out["url"] = f"{base}/{bucket}/graphics/{filename}"
    return out


def serialize_jsonb(value: Any) -> Optional[str]:
    """Serializa un valor Python a JSON string para columnas JSONB (o None)."""
    if value is None:
        return None
    if isinstance(value, str):
        # Ya es JSON textual — devolver tal cual si parsea, si no envolver
        try:
            json.loads(value)
            return value
        except (json.JSONDecodeError, TypeError):
            return json.dumps(value)
    return json.dumps(value)


def null_missing_user_fks(
    creado_por: Any,
    modificado_por: Any,
    revisado_por: Any,
    existing_user_ids: set[int],
) -> tuple[Any, Any, Any]:
    """
    Pone a NULL las FK a users que no existen en el destino (bd_minio §7.2).
    Nunca crea usuarios.
    """
    def _fix(uid: Any) -> Any:
        if uid is None:
            return None
        try:
            i = int(uid)
        except (TypeError, ValueError):
            return None
        return i if i in existing_user_ids else None

    return _fix(creado_por), _fix(modificado_por), _fix(revisado_por)


def build_scope_where(
    fase_id: Optional[int] = None,
    seccion: Optional[int] = None,
    operacion: Optional[str] = None,
    ids: Optional[Sequence[int]] = None,
    table_alias: str = "",
) -> tuple[str, list[Any]]:
    """
    Construye cláusula WHERE + params para filtrar preguntas por alcance.
    Retorna ('', []) si no hay filtro (alcance total).
    """
    prefix = f"{table_alias}." if table_alias else ""
    clauses: list[str] = []
    params: list[Any] = []

    if ids:
        clauses.append(f"{prefix}id = ANY(%s)")
        params.append(list(ids))
    if fase_id is not None:
        clauses.append(f"{prefix}fase_id = %s")
        params.append(fase_id)
    if seccion is not None:
        clauses.append(f"{prefix}seccion = %s")
        params.append(seccion)
    if operacion is not None:
        clauses.append(f"{prefix}operacion = %s")
        params.append(operacion)

    if not clauses:
        return "", []
    return "WHERE " + " AND ".join(clauses), params


def should_skip_minio(
    no_minio_flag: bool,
    fase_ids_in_scope: Iterable[int],
) -> bool:
    """
    True si no se debe sincronizar MinIO graphics/.

    - Flag explícito --no-minio
    - O el alcance está contenido solo en Fases 5 y/o 6 (SVG inline)
    """
    if no_minio_flag:
        return True
    fases = set(int(f) for f in fase_ids_in_scope)
    if not fases:
        return False
    return fases.issubset(SVG_INLINE_FASES)


def parse_id_list(raw: Optional[str]) -> Optional[list[int]]:
    """Parsea '1,2,3' → [1,2,3]."""
    if not raw or not raw.strip():
        return None
    out: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part:
            out.append(int(part))
    return out or None


def repo_root_from_scripts() -> str:
    """Raíz del monorepo: .../APP_Logica_Matematicas_kids desde backend/scripts/."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def resolve_env_path(env_name: str, repo_root: Optional[str] = None) -> str:
    """
    Resuelve ruta al .env de un entorno.
    env_name: local | dev | prod
    """
    root = repo_root or repo_root_from_scripts()
    mapping = {
        "local": os.path.join(root, "Datos_localhost", ".env.local"),
        "dev": os.path.join(root, "Datos_Desarrollo", ".env"),
        "prod": os.path.join(root, "Datos_Producion", ".env"),
    }
    if env_name not in mapping:
        raise ValueError(f"Entorno desconocido: {env_name}. Use local|dev|prod.")
    path = mapping[env_name]
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No se encontró .env para '{env_name}' en {path}. "
            "Suministre la ruta o cree el archivo de entorno (no se hardcodean secretos)."
        )
    return path


# Puertos túnel convencionales (confirmables; no son secretos)
DEFAULT_TUNNEL_PORTS = {
    "local": 5433,
    "dev": 5434,
    "prod": 5435,
}
