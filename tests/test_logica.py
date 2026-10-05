import unittest


# ==========================================
# 1. Clase Aislada: ModeloEstudianteSRL
# (La misma lógica inyectada en update.py)
# ==========================================
class ModeloEstudianteSRL:
    def __init__(self, srl_profile: dict = None):
        if srl_profile and "variables" in srl_profile:
            self.variables = srl_profile["variables"]
        else:
            self.variables = {
                "v2_autoeficacia": 3.0,
                "v13_valor_tarea": 3.0,
                "v21_creencias_control": 3.0,
                "v30_metas_intrinsecas": 3.0,
                "v34_elaboracion": 3.0,
                "v38_organizacion": 3.0,
                "v43_pensamiento_critico": 3.0,
                "v49_regulacion_metacognitiva": 3.0,
                "v61_gestion_tiempo": 3.0,
                "v69_regulacion_esfuerzo": 3.0,
                "v71_busqueda_ayuda_docente": 3.0,
                "v79_aprendizaje_autonomo": 3.0,
            }

    def registrar_interaccion(self, accion: str, detalle: str = None):
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

    def calcular_nivel_srl(self):
        promedio = sum(self.variables.values()) / len(self.variables)
        if 1.0 <= promedio <= 2.5:
            nivel = "Bajo"
        elif 2.6 <= promedio <= 3.5:
            nivel = "Medio"
        else:
            nivel = "Alto"
        return nivel, round(promedio, 2)


# ==========================================
# 2. Casos de Prueba (Unit Tests)
# ==========================================
class TestModeloEstudianteSRL(unittest.TestCase):
    def test_inicializacion_por_defecto(self):
        """Verifica que un usuario nuevo comienza con un perfil neutro (Medio)."""
        motor = ModeloEstudianteSRL()
        nivel, promedio = motor.calcular_nivel_srl()

        self.assertEqual(nivel, "Medio")
        self.assertEqual(promedio, 3.0)
        self.assertEqual(len(motor.variables), 12)

    def test_interacciones_positivas_elevan_puntaje(self):
        """Verifica que acciones como pedir pistas o buscar teoría incrementan las variables MSLQ correspondientes."""
        motor = ModeloEstudianteSRL()

        # Simulamos clics del usuario en la interfaz
        motor.registrar_interaccion("clic_boton_ver_mas")
        motor.registrar_interaccion("uso_panel_help", "pedir_pista_tras_fallo")

        # Validamos que los valores específicos se sobrescribieron a puntuaciones altas
        self.assertEqual(motor.variables["v13_valor_tarea"], 5.0)
        self.assertEqual(motor.variables["v79_aprendizaje_autonomo"], 4.0)

        # El promedio general debe ser mayor a 3.0 ahora
        nivel, promedio = motor.calcular_nivel_srl()
        self.assertGreater(promedio, 3.0)

    def test_interacciones_negativas_detonan_nivel_bajo(self):
        """Verifica que un comportamiento desadaptativo clasifica al alumno en nivel 'Bajo' para forzar el andamiaje."""
        motor = ModeloEstudianteSRL()

        # Simulamos que el alumno salta el ejercicio al primer error
        motor.registrar_interaccion("abandono_ejercicio", "salta_al_primer_error")
        self.assertEqual(motor.variables["v69_regulacion_esfuerzo"], 1.0)

        # Simulamos un declive en el resto de variables mediante interacciones previas
        for key in motor.variables:
            motor.variables[key] = 1.0

        nivel, promedio = motor.calcular_nivel_srl()

        self.assertEqual(nivel, "Bajo")
        self.assertLessEqual(promedio, 2.5)

    def test_perfil_autonomo_alcanza_nivel_alto(self):
        """Verifica que un alumno con consistencia reflexiva alcanza el umbral > 3.6 para desactivar ayudas invasivas."""
        motor = ModeloEstudianteSRL()

        # Simulamos puntajes máximos de un alumno autorregulado
        for key in motor.variables:
            motor.variables[key] = 5.0

        nivel, promedio = motor.calcular_nivel_srl()

        self.assertEqual(nivel, "Alto")
        self.assertEqual(promedio, 5.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
