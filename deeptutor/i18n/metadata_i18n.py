"""Localized display metadata for built-in tools and capabilities."""

from __future__ import annotations

from deeptutor.services.prompt.language import prompt_locale

_CAPABILITY_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "chat": {
        "es": "Chat agéntico por defecto con tools, recuperación, memoria y adjuntos.",
    },
    "deep_solve": {
        "es": "Resolución multi-paso con planificación, razonamiento y redacción final.",
    },
    "deep_question": {
        "es": "Genera preguntas de calidad desde plantillas, fuentes u objetivos.",
    },
    "deep_research": {
        "es": "Investigación profunda iterativa que descompone tema y redacta informe.",
    },
    "math_animator": {
        "es": "Genera animaciones matemáticas o storyboards con Manim.",
    },
    "mastery_path": {
        "es": "Aprendizaje estructurado por dominio con repetición espaciada.",
    },
    "visualize": {
        "es": "Crea explicaciones visuales SVG, charts, Mermaid, HTML o Manim.",
    },
    "immersive_reading": {
        "es": "Lee documento con asistente, citado página por página.",
    },
}

_TOOL_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "brainstorm": {
        "es": "Explora ideas en amplitud y organiza con rationale.",
    },
    "exec": {
        "es": "Ejecuta código o scripts shell en workspace aislado.",
    },
    "kb_files": {
        "es": "Lista documentos de base conocimiento con conteo total.",
    },
    "paper_search": {
        "es": "Busca preprints arXiv y devuelve metadata.",
    },
    "zotero_search": {
        "es": "Busca referencias en librería Zotero aportada.",
    },
    "reason": {
        "es": "Llamada razonamiento dedicado para tareas duras.",
    },
    "web_search": {
        "es": "Busca web y devuelve resultados con fuentes.",
    },
    "imagegen": {
        "es": "Genera imágenes desde prompt con modelo configurado.",
    },
    "videogen": {
        "es": "Genera videos cortos desde prompt con modelo configurado.",
    },
}


def capability_description_i18n(name: str, fallback: str = "") -> dict[str, str]:
    values = _CAPABILITY_DESCRIPTIONS.get(name)
    if values:
        return dict(values)
    return {"es": fallback}


def tool_description_i18n(name: str, fallback: str = "") -> dict[str, str]:
    values = _TOOL_DESCRIPTIONS.get(name)
    if values:
        return dict(values)
    return {"es": fallback}


def localized_description(values: dict[str, str], language: str) -> str:
    lang = prompt_locale(language)
    return values.get(lang) or values.get("es") or ""


__all__ = [
    "capability_description_i18n",
    "localized_description",
    "tool_description_i18n",
]
