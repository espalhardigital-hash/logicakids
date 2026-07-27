"""Tests unitarios de helpers de sync (bd_minio.md) — sin red ni DB real."""

import json
import os
import sys

import pytest

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from sync_helpers import (  # noqa: E402
    SVG_INLINE_FASES,
    build_scope_where,
    extract_graphics_filename,
    null_missing_user_fks,
    parse_id_list,
    rewrite_datos_numericos_url,
    rewrite_db_url,
    serialize_jsonb,
    should_skip_minio,
)


def test_rewrite_db_url_strips_asyncpg_and_encodes_hash():
    url = "postgresql+asyncpg://user:p#ass@db:5432/mydb"
    out = rewrite_db_url(url, override_host="localhost", override_port=5433)
    assert "+asyncpg" not in out
    assert "p%23ass" in out
    assert "localhost:5433" in out
    assert out.endswith("/mydb")


def test_extract_graphics_filename():
    assert (
        extract_graphics_filename("https://x/bucket/graphics/abc.png") == "abc.png"
    )
    assert extract_graphics_filename("https://x/bucket/graphics/a/b.png") == "a/b.png"
    assert extract_graphics_filename(None) is None
    assert extract_graphics_filename("") is None


def test_rewrite_datos_numericos_url_preserves_filename():
    datos = {"url": "http://localhost:9100/logicakids/graphics/uuid1.png", "a": 1}
    out = rewrite_datos_numericos_url(
        datos, "https://files.example.com", "logicakids-prod"
    )
    assert out["url"] == "https://files.example.com/logicakids-prod/graphics/uuid1.png"
    assert out["a"] == 1


def test_rewrite_datos_numericos_from_json_string():
    raw = json.dumps({"url": "http://x/b/graphics/f.webp"})
    out = rewrite_datos_numericos_url(raw, "https://cdn.t", "buck")
    assert out["url"] == "https://cdn.t/buck/graphics/f.webp"


def test_null_missing_user_fks():
    c, m, r = null_missing_user_fks(1, 99, 2, {1, 2})
    assert c == 1
    assert m is None
    assert r == 2
    c2, m2, r2 = null_missing_user_fks(None, None, None, {1})
    assert c2 is m2 is r2 is None


def test_build_scope_where_fase_and_ids():
    sql, params = build_scope_where(fase_id=5)
    assert "fase_id = %s" in sql
    assert params == [5]

    sql2, params2 = build_scope_where(ids=[10, 20], fase_id=3)
    assert "id = ANY(%s)" in sql2
    assert params2[0] == [10, 20]
    assert 3 in params2


def test_build_scope_where_total():
    sql, params = build_scope_where()
    assert sql == ""
    assert params == []


def test_should_skip_minio():
    assert should_skip_minio(True, [1, 2, 3]) is True
    assert should_skip_minio(False, [5]) is True
    assert should_skip_minio(False, [5, 6]) is True
    assert should_skip_minio(False, [5, 7]) is False
    assert should_skip_minio(False, []) is False
    assert SVG_INLINE_FASES == frozenset({5, 6})


def test_parse_id_list():
    assert parse_id_list("1, 2,3") == [1, 2, 3]
    assert parse_id_list(None) is None
    assert parse_id_list("  ") is None


def test_serialize_jsonb():
    assert serialize_jsonb(None) is None
    assert json.loads(serialize_jsonb({"a": 1})) == {"a": 1}
    assert serialize_jsonb('{"a": 1}') == '{"a": 1}'
