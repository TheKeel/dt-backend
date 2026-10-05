"""Self-Regulated Learning model: MSLQ profile -> scaffolding strategy.

Pure logic, no I/O. The 12 MSLQ variables are Likert 1-5, neutral 3.0.
``obtener_estrategia_matriz`` crosses the regulation level (ARR, from the
variables) with the knowledge level (CON, from graded attempts) to pick how
much scaffolding the tutor applies.

Lives beside the consolidator rather than inside it: ``update.py`` is the
memory pipeline, this is a scoring rule both the pipeline and the tests need.
"""

from __future__ import annotations

from typing import Any

#: The 12 MSLQ variables, always present in a profile.
_SRL_VARIABLES = (
    "v2_autoeficacia",
    "v13_valor_tarea",
    "v21_creencias_control",
    "v30_metas_intrinsecas",
    "v34_elaboracion",
    "v38_organizacion",
    "v43_pensamiento_critico",
    "v49_regulacion_metacognitiva",
    "v61_gestion_tiempo",
    "v69_regulacion_esfuerzo",
    "v71_busqueda_ayuda_docente",
    "v79_aprendizaje_autonomo",
)


def default_srl_variables() -> dict[str, float]:
    return {variable: 3.0 for variable in _SRL_VARIABLES}


def _veredicto_de(intento: dict[str, Any]) -> str:
    data = intento.get("data")
    return str(data.get("veredicto_experto") or "") if isinstance(data, dict) else ""


class ModeloEstudianteSRL:
    def __init__(self, srl_profile: dict[str, Any] | None = None) -> None:
        self.variables = (srl_profile or {}).get("variables", default_srl_variables())

    def registrar_interaccion(self, accion: str, detalle: str | None = None) -> None:
        if accion == "clic_boton_ver_mas":
            self.variables["v13_valor_tarea"] = 5.0
        elif accion == "elegir_bifurcacion" and detalle == "ver_paso_a_paso":
            self.variables["v21_creencias_control"] = 5.0
            self.variables["v30_metas_intrinsecas"] = 5.0
        elif accion == "punto_de_control_tras_fallo" and detalle == "revisar_teoria":
            self.variables["v49_regulacion_metacognitiva"] = 5.0
        elif accion == "abandono_ejercicio" and detalle == "salta_al_primer_error":
            self.variables["v69_regulacion_esfuerzo"] = 1.0
        elif accion == "uso_panel_help" and detalle == "pedir_pista_tras_fallo":
            self.variables["v79_aprendizaje_autonomo"] = 4.0

    def calcular_nivel_arr(self) -> tuple[str, float]:
        promedio = sum(self.variables.values()) / len(self.variables)
        if 1.0 <= promedio <= 2.5:
            nivel = "Bajo"
        elif 2.6 <= promedio <= 3.5:
            nivel = "Medio"
        else:
            nivel = "Alto"
        return nivel, round(promedio, 2)

    def evaluar_conocimiento(self, intentos: list) -> str:
        """Knowledge level from graded attempts.

        Reads the persisted assessment shape (``is_correct`` / ``result``); a
        nested ``data.veredicto_experto`` marker is also accepted so a caller
        holding raw trace records still scores. No attempts means unknown, not
        failing, so it returns the neutral "Medio".
        """
        aciertos = 0
        for intento in intentos:
            if not isinstance(intento, dict):
                continue
            if intento.get("is_correct") is True or intento.get("result") == "correct":
                aciertos += 1
            elif intento.get("result") == "incorrect":
                continue
            elif _veredicto_de(intento) == "correcto":
                aciertos += 1

        tasa_exito = aciertos / len(intentos) if intentos else 0.5
        if tasa_exito < 0.4:
            return "Bajo"
        if tasa_exito <= 0.75:
            return "Medio"
        return "Alto"

    def obtener_estrategia_matriz(self, nivel_arr: str, nivel_con: str) -> str:
        matriz = {
            "Bajo": {
                "Bajo": "Máximo (Directivo/Explicativo)",
                "Medio": "Alto (Guía Estructurada)",
                "Alto": "Medio (Sugerencias Orientadas)",
            },
            "Medio": {
                "Bajo": "Alto (Monitoreo Estricto)",
                "Medio": "Medio (Facilitador)",
                "Alto": "Bajo (Autónomo Supervisado)",
            },
            "Alto": {
                "Bajo": "Medio (Retos con Soporte)",
                "Medio": "Bajo (Desafíos Autónomos)",
                "Alto": "Mínimo (Laissez-faire / Mentoría)",
            },
        }
        return matriz.get(nivel_con, {}).get(nivel_arr, "Medio (Facilitador)")


#: Estrategia de andamiaje -> dificultad que el motor impone en mastery_quiz.
#: La matriz decide; el LLM propone contenido pero no elige nivel.
ESTRATEGIA_A_DIFICULTAD = {
    "Máximo (Directivo/Explicativo)": "easy",
    "Alto (Guía Estructurada)": "easy",
    "Alto (Monitoreo Estricto)": "easy",
    "Medio (Facilitador)": "medium",
    "Medio (Sugerencias Orientadas)": "medium",
    "Medio (Retos con Soporte)": "medium",
    "Bajo (Autónomo Supervisado)": "hard",
    "Bajo (Desafíos Autónomos)": "hard",
    "Mínimo (Laissez-faire / Mentoría)": "hard",
}

_DIFICULTAD_POR_DEFECTO = "medium"


def dificultad_por_estrategia(estrategia: str | None) -> str:
    """Dificultad autoritativa para una estrategia de andamiaje.

    Desconocida o ausente -> medium, nunca vacío: la pregunta siempre
    lleva badge aunque el perfil SRL aún no exista.
    """
    if not isinstance(estrategia, str):
        return _DIFICULTAD_POR_DEFECTO
    return ESTRATEGIA_A_DIFICULTAD.get(estrategia.strip(), _DIFICULTAD_POR_DEFECTO)


def scaffolding_para_estrategia(estrategia: str | None) -> dict[str, str]:
    """Bloque scaffolding para exponer en mastery_status y auditar overrides."""
    dificultad = dificultad_por_estrategia(estrategia)
    return {
        "estrategia": estrategia if isinstance(estrategia, str) and estrategia.strip() else "Medio (Facilitador)",
        "difficulty": dificultad,
    }


__all__ = [
    "ESTRATEGIA_A_DIFICULTAD",
    "ModeloEstudianteSRL",
    "default_srl_variables",
    "dificultad_por_estrategia",
    "scaffolding_para_estrategia",
]
