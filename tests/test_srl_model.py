import unittest

from deeptutor.services.memory.srl import ModeloEstudianteSRL


class TestModeloEstudianteSRL(unittest.TestCase):
    def test_inicializacion_por_defecto(self):
        motor = ModeloEstudianteSRL()
        nivel, promedio = motor.calcular_nivel_arr()
        self.assertEqual(nivel, "Medio")
        self.assertEqual(promedio, 3.0)

    def test_matriz_estrategia_extremos(self):
        motor = ModeloEstudianteSRL()
        # Escenario Crítico: ARR Bajo, CON Bajo
        estrategia_critica = motor.obtener_estrategia_matriz("Bajo", "Bajo")
        self.assertEqual(estrategia_critica, "Máximo (Directivo/Explicativo)")

        # Escenario Óptimo: ARR Alto, CON Alto
        estrategia_optima = motor.obtener_estrategia_matriz("Alto", "Alto")
        self.assertEqual(estrategia_optima, "Mínimo (Laissez-faire / Mentoría)")

    def test_evaluacion_conocimiento(self):
        motor = ModeloEstudianteSRL()

        # The persisted attempt shape: is_correct, as assessment_attempts stores it.
        intentos_fallidos = [
            {"is_correct": False},
            {"is_correct": False},
            {"is_correct": True},
        ]
        self.assertEqual(motor.evaluar_conocimiento(intentos_fallidos), "Bajo")

        intentos_exitosos = [{"is_correct": True}, {"is_correct": True}]
        self.assertEqual(motor.evaluar_conocimiento(intentos_exitosos), "Alto")

        # No attempts is unknown, not failing.
        self.assertEqual(motor.evaluar_conocimiento([]), "Medio")

    def test_recalculo_tras_interacciones(self):
        motor = ModeloEstudianteSRL()
        # El estudiante pide la respuesta directa (comportamiento evasivo)
        motor.registrar_interaccion("abandono_ejercicio", "salta_al_primer_error")
        motor.calcular_nivel_arr()

        # Al disminuir la variable v69, el promedio puede seguir en "Medio"
        # si las demás variables están en 3.0, validemos que el valor v69 bajó.
        self.assertEqual(motor.variables["v69_regulacion_esfuerzo"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
