"""Spanish-only language-directive test for the question followup agent."""

from __future__ import annotations

from typing import Any

import pytest

from deeptutor.agents.question.agents.followup_agent import FollowupAgent


class CaptureFollowupAgent(FollowupAgent):
    """``FollowupAgent`` subclass that records every system prompt sent to
    the LLM (so the language-directive injection can be asserted), while
    short-circuiting the actual network call."""

    def __init__(self, language: str = "es") -> None:
        self.language = language
        self.prompts: dict[str, Any] = {
            "system": "Sistema de seguimiento",
            "answer_followup": (
                "Contexto de la pregunta:\n{question_context}\n\n"
                "Historial de conversación:\n{history_context}\n\n"
                "Seguimiento del usuario:\n{user_message}\n"
            ),
        }
        self.captured_system_prompts: list[str] = []

    async def stream_llm(self, **kwargs):  # type: ignore[override]
        self.captured_system_prompts.append(str(kwargs["system_prompt"]))
        yield "Respondido"


@pytest.mark.asyncio
async def test_followup_agent_appends_language_directive_to_system_prompt() -> None:
    agent = CaptureFollowupAgent(language="es")

    reply = await agent.process(
        user_message="¿Por qué esta es la respuesta?",
        question_context={
            "question_id": "q_1",
            "question_type": "choice",
            "question": "¿Cuándo está definida la multiplicación de matrices?",
            "correct_answer": "Cuando las dimensiones internas coinciden.",
            "explanation": "El número de columnas de A debe ser igual al número de filas de B.",
        },
        history_context="",
    )

    assert reply == "Respondido"
    assert agent.captured_system_prompts
    assert "Sistema de seguimiento" in agent.captured_system_prompts[0]
    assert "Write ALL reader-facing text strictly in Español" in agent.captured_system_prompts[0]
