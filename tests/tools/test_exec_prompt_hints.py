"""The exec prompt must not teach one operating system's shell on another."""

from __future__ import annotations

from deeptutor.tools.exec_tool import ExecTool


def test_exec_prompt_does_not_recommend_posix_filters_as_portable_commands() -> None:
    hints = ExecTool().get_prompt_hints(language="es")
    rendered = "\n".join((hints.input_format, hints.guideline, hints.note))
    for fragment in ("head", "grep", "tail"):
        assert fragment not in rendered


def test_exec_prompt_requires_real_access_error_before_claiming_denial() -> None:
    es = ExecTool().get_prompt_hints(language="es")

    assert "No describas fallos de sintaxis o de dependencias como denegación del sandbox" in es.note
