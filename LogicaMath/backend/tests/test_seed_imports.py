import importlib

import pytest


SEED_IMPORTS = [
    pytest.param("app.fase7.seed_fase7", "run_fase7_seed", id="fase7"),
    pytest.param(
        "app.fase8.seed_fase8",
        "run_fase8_seed",
        id="fase8-known-renumbering-debt",
        marks=pytest.mark.xfail(
            strict=True,
            reason="Physical phase 7-11 renumbering is incomplete; see docs/MAPA_CANONICO_FASES.md",
        ),
    ),
    pytest.param(
        "app.fase9.seed_fase9",
        "run_fase9_seed",
        id="fase9-known-renumbering-debt",
        marks=pytest.mark.xfail(
            strict=True,
            reason="Physical phase 7-11 renumbering is incomplete; see docs/MAPA_CANONICO_FASES.md",
        ),
    ),
]


@pytest.mark.parametrize(("module_name", "callable_name"), SEED_IMPORTS)
def test_global_seed_import_resolves(module_name: str, callable_name: str) -> None:
    module = importlib.import_module(module_name)
    assert callable(getattr(module, callable_name))
