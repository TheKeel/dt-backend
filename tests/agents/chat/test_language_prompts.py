"""Spanish-only prompt language tests for the chat loop.

The system is Spanish-only: ``normalize_language`` maps every input locale
to ``"es"``, so ``en``/``zh`` inputs produce the same Spanish scaffolding.
These tests pin that behaviour.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from deeptutor.agents.chat.agentic_pipeline import AgenticChatPipeline
from deeptutor.agents.loop.prompt_blocks import ChatPromptAssembler
from deeptutor.capabilities.mastery.pipeline import MasteryLoopPipeline
from deeptutor.core.context import UnifiedContext
from deeptutor.runtime.agentic.tool_dispatch import MAX_PARALLEL_TOOL_CALLS


@pytest.fixture(autouse=True)
def _fake_llm_config(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = SimpleNamespace(
        binding="openai",
        model="gpt-test",
        api_key="sk-test",
        base_url="https://example.test/v1",
        api_version=None,
    )
    monkeypatch.setattr(
        "deeptutor.agents.loop.pipeline.get_llm_config",
        lambda: cfg,
    )
    monkeypatch.setattr("deeptutor.agents.base_agent.get_llm_config", lambda: cfg)


@pytest.mark.parametrize("language", ["es", "en", "zh"])
@pytest.mark.parametrize("mode", ["chat", "immersive_reading", "mastery_path"])
def test_tool_call_limit_reaches_each_loop_prompt(language: str, mode: str) -> None:
    pipeline_type = MasteryLoopPipeline if mode == "mastery_path" else AgenticChatPipeline
    pipeline = pipeline_type(language=language)
    context = UnifiedContext(active_capability=mode)
    prompt = pipeline._build_system_prompt([], context)

    assert MAX_PARALLEL_TOOL_CALLS == 15
    assert prompt.count("## tool_call_policy\n") == 1
    assert "{limit}" not in prompt
    # Spanish-only: every locale renders the same Spanish policy text.
    assert "como máximo 15 llamadas a herramientas" in prompt
    assert "límite por ronda" in prompt
    assert "no se ejecutan" in prompt


def test_agentic_chat_final_prompt_uses_selected_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRegistry:
        def build_prompt_text(self, *_args, **_kwargs) -> str:
            return "- tool"

    monkeypatch.setattr(
        "deeptutor.agents.loop.pipeline.get_tool_registry",
        lambda: FakeRegistry(),
    )

    from deeptutor.core.context import UnifiedContext

    ctx = UnifiedContext()
    zh_prompt = AgenticChatPipeline(language="zh")._build_system_prompt([], ctx)
    en_prompt = AgenticChatPipeline(language="en")._build_system_prompt([], ctx)

    # Spanish-only: both locales carry the Spanish directive and persona.
    assert "Write ALL reader-facing text strictly in Español" in zh_prompt
    assert "Write ALL reader-facing text strictly in Español" in en_prompt
    assert "Eres DeepTutor" in zh_prompt
    assert "Eres DeepTutor" in en_prompt


def test_mastery_plugin_system_prompt_uses_localized_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRegistry:
        def build_prompt_text(self, *_args, **_kwargs) -> str:
            return "- tool"

    monkeypatch.setattr(
        "deeptutor.agents.loop.pipeline.get_tool_registry",
        lambda: FakeRegistry(),
    )

    from deeptutor.core.context import UnifiedContext

    ctx = UnifiedContext(metadata={"mastery_mode": True, "mastery_path_id": "p1"})
    zh_prompt = AgenticChatPipeline(language="zh")._build_system_prompt([], ctx)
    en_prompt = AgenticChatPipeline(language="en")._build_system_prompt([], ctx)

    assert "## mastery_tutor" in zh_prompt
    assert "tutor personal de dominio" in zh_prompt
    assert "## mastery_tutor" in en_prompt
    assert "tutor personal de dominio" in en_prompt


def test_ask_questions_plugin_system_prompt_uses_localized_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRegistry:
        def build_prompt_text(self, *_args, **_kwargs) -> str:
            return "- tool"

    monkeypatch.setattr(
        "deeptutor.agents.loop.pipeline.get_tool_registry",
        lambda: FakeRegistry(),
    )

    from deeptutor.core.context import UnifiedContext

    ctx = UnifiedContext(metadata={"ask_questions_mode": True})
    zh_prompt = AgenticChatPipeline(language="zh")._build_system_prompt([], ctx)
    en_prompt = AgenticChatPipeline(language="en")._build_system_prompt([], ctx)

    assert "## ask_questions" in zh_prompt
    assert "Modo de Preguntas" in zh_prompt
    assert "llamando a `ask_user` exactamente una vez" in zh_prompt
    assert "segundo, tercero, décimo" in zh_prompt
    assert "todo el contexto disponible" in zh_prompt
    assert "## ask_questions" in en_prompt
    assert "Modo de Preguntas" in en_prompt
    assert "llamando a `ask_user` exactamente una vez" in en_prompt


def test_prompt_blocks_include_localized_optional_context() -> None:
    from deeptutor.core.context import UnifiedContext

    prompts = {
        "general": "General",
        "runtime_policy": "Política",
        "loop": {
            "system": "Bucle",
            "user": "El usuario dice: {user_message}",
            "finish_exhausted": "Presupuesto agotado, responde directamente.",
        },
    }
    ctx = UnifiedContext(
        user_message="Explica la fotosíntesis",
        sidebar_context="[contenido seleccionado]\nCarga el código y los datos estáticos en memoria",
        persona_context="Usa preguntas socráticas",
        memory_context="Al estudiante le gustan los ejemplos",
    )
    assembler = ChatPromptAssembler(prompts=prompts, language="es")

    blocks = assembler.blocks(context=ctx, tool_manifest="", workspace_note="Espacio de trabajo disponible")

    names = [block.name for block in blocks]
    assert names[:4] == ["general", "runtime_context", "runtime_policy", "loop"]
    assert "sidebar_tutor_context" in names
    assert "persona_style" in names
    assert "memory" in names
    assert "workspace" in names
    assert assembler.user_message(context=ctx) == "El usuario dice: Explica la fotosíntesis"
    assert assembler.finish_exhausted_instruction() == "Presupuesto agotado, responde directamente."
    system_prompt = assembler.render(blocks)
    assert "## sidebar_tutor_context" in system_prompt
    assert "Carga el código y los datos estáticos en memoria" in system_prompt
