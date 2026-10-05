"""Guards against StatusI18n status-message drift for the visualize capability.

Spanish-only: a capability that calls ``i18n.t("some_key", "default", ...)``
must have ``some_key`` defined in ``agents/<module>/prompts/es/<capability>.yaml``
under the ``status:`` section. If it isn't, ``StatusI18n.t`` silently falls back
to the Spanish ``default``. These tests keep the yaml and the code in sync.

Scoped to ``visualize`` for now; the checks are written generically and
can be parametrized over more capabilities once their yamls use the same
``status:`` layout.
"""

from __future__ import annotations

from pathlib import Path
import re

import yaml

_REPO = Path(__file__).resolve().parents[2]
_PROMPTS = _REPO / "deeptutor" / "agents" / "visualize" / "prompts"
_CODE = _REPO / "deeptutor" / "agents" / "visualize" / "capability.py"


def _status_keys(lang: str = "es") -> set[str]:
    data = yaml.safe_load((_PROMPTS / lang / "visualize.yaml").read_text(encoding="utf-8")) or {}
    status = data.get("status") if isinstance(data, dict) else None
    return set((status or {}).keys())


def _code() -> str:
    return _CODE.read_text(encoding="utf-8")


def test_es_status_pack_exists() -> None:
    """The Spanish status pack must exist and carry keys."""
    assert _status_keys("es"), "prompts/es/visualize.yaml has no status keys"


def test_code_i18n_keys_exist_in_yaml() -> None:
    """Every literal i18n.t("key", ...) used in code must exist in the yaml,
    otherwise users silently get the default."""
    used = set(re.findall(r'i18n\.t\(\s*"([^"]+)"', _code()))
    yaml_keys = _status_keys("es")
    missing = used - yaml_keys
    assert not missing, (
        "i18n keys used in visualize.py but missing from visualize.yaml "
        f"(fall back to default): {sorted(missing)}"
    )


def test_no_orphan_yaml_keys() -> None:
    """Every yaml status key must be referenced as a string literal somewhere in
    the module. Tolerates dynamic dispatch (e.g.
    ``artifact_key = "manim_artifacts_one" if ... else "manim_artifacts_many"``)
    while still catching dead copy left behind by deleted code paths."""
    code = _code()
    orphans = {k for k in _status_keys("es") if f'"{k}"' not in code}
    assert not orphans, (
        f"yaml status keys never referenced in visualize.py (dead copy): {sorted(orphans)}"
    )
