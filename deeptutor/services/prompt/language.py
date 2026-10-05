"""Spanish-only prompt language helpers for DeepTutor.

All functions default to ``"es"`` (Spanish). Any language code different from
``"es"`` (including ``"en"``, ``"zh"``, ``"fr"``, etc.) is treated as Spanish
so the system never falls back to English or Chinese scaffolding — it stays in
Spanish or degrades gracefully without crashing.
"""

from __future__ import annotations

from typing import Any


def normalize_language(language: Any) -> str:
    """Always return ``"es"`` — Spanish is the only supported locale."""
    return "es"


def is_chinese(language: str | None) -> bool:
    """Spanish-only: never Chinese."""
    return False


def is_spanish(language: str | None) -> bool:
    """Always True in Spanish‑only mode."""
    return True


def language_label(language: str | None) -> str:
    """Return the language label, always Spanish in this mode."""
    return "Español"


def language_directive(language: str | None, *, allow_user_override: bool = False) -> str:
    """Return a reader-facing language instruction for prompts.

    In Spanish-only mode, always instructs the model to write in Spanish.
    ``allow_user_override`` is accepted for API compatibility but has no effect
    since Spanish is the only locale.
    """
    code = normalize_language(language)
    # Always Spanish directive.
    body = (
        "\n\n[Language] Write ALL reader-facing text strictly in Español. "
        "Do NOT switch languages even if the source material, "
        "JSON keys, or examples in this prompt are in a different language. "
        "Keep proper nouns (people, products, formula symbols) in their "
        "original form."
    )
    override = (
        "This is the default output language, not a restriction on the reader: "
        "if the user explicitly asks you to answer in another language, honour that "
        "request and keep to it for the rest of the conversation."
        if allow_user_override
        else ""
    )
    return f"{body} {override}".strip()


def append_language_directive(
    system_prompt: str | None,
    language: str | None,
    *,
    allow_user_override: bool = False,
) -> str:
    """Append the language directive to an existing system prompt."""
    base = (system_prompt or "").rstrip()
    directive = language_directive(language, allow_user_override=allow_user_override).strip()
    if not base:
        return directive
    return f"{base}\n\n{directive}"


# ── Prompt asset locale ──────────────────────────────────────────────────
#
# Spanish-only: prompt_locale always returns ``"es"``.  No ``"en"``/``"zh"``
# fallback trees exist, so the scaffolding text is always the same regardless
# of the request language.  The language directive (``language_directive``)
# is what makes the model answer in the reader's chosen language.
PROMPT_LOCALE: str = "es"
DEFAULT_PROMPT_LOCALE: str = "es"


def prompt_locale(language: str | None) -> str:
    """Return the on‑disk prompt locale for *language*.

    Spanish‑only: always returns ``"es"``.  No English/Chinese trees are
    consulted, so the scaffolding text is always the same regardless of the
    request language.
    """
    return PROMPT_LOCALE


def load_packaged_prompt(package: str, filename: str, language: str | None) -> str:
    """Read ``<package>/prompts/<locale>/<filename>``.

    Spanish‑only mode: always looks in the ``es`` tree.  If the file does not
    exist, returns an empty string rather than raising an error so that missing
    translations degrade gracefully.
    """
    from importlib import resources

    try:
        text_file = resources.files(package).joinpath("prompts", "es", filename)
        return text_file.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def load_packaged_prompts(package: str, filename: str, language: str | None) -> dict[str, Any]:
    """The YAML form of :func:`load_packaged_prompt`; ``{}`` when unavailable."""
    import yaml

    text = load_packaged_prompt(package, filename, language)
    data = yaml.safe_load(text) if text else None
    return data if isinstance(data, dict) else {}


__all__ = [
    "append_language_directive",
    "is_chinese",
    "is_spanish",
    "language_directive",
    "language_label",
    "normalize_language",
    "prompt_locale",
    "load_packaged_prompt",
    "load_packaged_prompts",
]
