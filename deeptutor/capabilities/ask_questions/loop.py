"""Chat-loop hooks for the Ask Questions capability."""

from __future__ import annotations

from typing import Any

from deeptutor.capabilities.protocol import PromptBlock
from deeptutor.core.context import UnifiedContext
from deeptutor.services.prompt.language import load_packaged_prompt


class AskQuestionsLoopCapability:
    """Contribute an adaptive questioning policy to the normal chat loop."""

    name = "ask_questions"
    owned_tools: tuple[str, ...] = ()

    def is_active(self, context: UnifiedContext) -> bool:
        return bool(context.metadata.get("ask_questions_mode"))

    def system_block(
        self,
        context: UnifiedContext,
        *,
        language: str,
        prompts: dict[str, Any],
    ) -> PromptBlock | None:
        _ = prompts
        if not self.is_active(context):
            return None
        return PromptBlock("ask_questions", _load_system_prompt(language))

    def augment_kwargs(
        self,
        tool_name: str,
        kwargs: dict[str, Any],
        context: UnifiedContext,
    ) -> dict[str, Any]:
        _ = tool_name, context
        return kwargs

    def pre_loop_seed(self, context: UnifiedContext) -> str:
        _ = context
        return ""


def _load_system_prompt(language: str) -> str:
    return load_packaged_prompt(__package__, "system.md", language)


__all__ = ["AskQuestionsLoopCapability"]
