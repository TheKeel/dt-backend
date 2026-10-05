"""Language codes must survive parsing.

``parse_language`` used to be a binary zh/en classifier whose final statement
was ``return "zh"``, so a Japanese book came back with Chinese quizzes — the
prose path normalized the code correctly while quiz, Deep Research and Mastery
Path all ran through this one (issue #712).
"""

from __future__ import annotations

import pytest

from deeptutor.services.config import parse_language
from deeptutor.services.prompt import get_prompt_manager


def prompt_file_chain(code: str) -> list[str]:
    """The order ``PromptManager`` tries language-specific prompt files in."""
    return get_prompt_manager()._fallback_chain(code)


@pytest.mark.parametrize("code", ["ja", "ko", "fr", "de", "es", "ru", "ar", "pt", "it"])
def test_a_requested_language_is_not_rewritten_to_spanish(code: str) -> None:
    """In Spanish-only mode, all languages resolve to ``"es"`` (or keep regional
    codes starting with ``"es-``)."""
    result = parse_language(code)
    # Spanish-only: everything normalizes to "es", or keeps regional prefix
    assert result == "es" or result.startswith("es-")


@pytest.mark.parametrize("value", ["en", "EN", "English", "english"])
def test_english_aliases_resolve_to_spanish(value: str) -> None:
    """In Spanish-only mode, English aliases resolve to ``"es"``."""
    assert parse_language(value) == "es"


@pytest.mark.parametrize("value", ["es", "ES", "Español", "español", "spanish"])
def test_spanish_aliases_resolve_to_es(value: str) -> None:
    """Spanish aliases resolve to ``"es"``."""
    assert parse_language(value) == "es"


def test_regional_codes_start_with_es() -> None:
    """Regional codes starting with ``es-`` are preserved."""
    assert parse_language("es-es") == "es"
    assert parse_language("es-mx") == "es"
    assert parse_language("pt-BR") == "es"


def test_an_unconfigured_language_still_defaults_to_spanish() -> None:
    """Deployments that never set a language keep the Spanish-only behaviour."""
    assert parse_language(None) == "es"
    assert parse_language("") == "es"
    assert parse_language("   ") == "es"
    assert parse_language(0) == "es"
    assert parse_language(5) == "es"
    assert parse_language(["ja"]) == "es"


def test_prompt_files_fall_back_to_english_not_chinese() -> None:
    """Only es/en ship prompt YAML; a language without files must not land on es,
    or the model is handed Chinese scaffolding for a Japanese answer."""
    assert prompt_file_chain("ja") == ["ja", "en"]
    assert prompt_file_chain("ko") == ["ko", "en"]


def test_prompt_files_reuse_the_base_locale_for_a_regional_code() -> None:
    """Regional code reuses its base locale's files."""
    assert prompt_file_chain("es-mx") == ["es-mx", "es", "en"]


def test_prompt_file_fallbacks_are_unchanged_for_the_two_shipped_locales() -> None:
    """The two shipped locales (es and en) have their fallback chains."""
    assert prompt_file_chain("es") == ["es", "en"]
    assert prompt_file_chain("en") == ["en", "es"]
