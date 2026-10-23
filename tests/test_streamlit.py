"""Pruebas de interacción de la interfaz principal, sin depender de Ollama."""

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent


class TestStreamlit(unittest.TestCase):
    def abrir_hoja(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        app.toggle[0].set_value(False).run()
        for profundidad in range(5):
            app.button(key=f"opt_{profundidad}_0").click().run()
        self.assertEqual(len(app.exception), 0)
        return app

    def generar(self, app):
        next(b for b in app.button if b.label == "Generar orientación").click().run()
        self.assertEqual(len(app.exception), 0)

    def test_recorrido_y_respaldo(self):
        app = self.abrir_hoja()
        self.generar(app)
        self.assertTrue(any("Fuente: ficha del sistema" in c.value for c in app.caption))
        next(b for b in app.button if b.label == "⬅️ Elegir otra opción").click().run()
        self.assertEqual(app.session_state["indices"], [0, 0, 0, 0])
        self.assertEqual(len(app.exception), 0)

    def test_cambiar_configuracion_no_muestra_guia_anterior(self):
        app = self.abrir_hoja()
        self.generar(app)
        app.text_input[0].set_value("otro_modelo").run()
        self.assertFalse(any("Fuente: ficha del sistema" in c.value for c in app.caption))

    def test_modelo_vacio_muestra_error_sin_romper_interfaz(self):
        app = self.abrir_hoja()
        app.text_input[0].set_value(" ").run()
        self.generar(app)
        self.assertTrue(any("modelo" in e.value.lower() for e in app.error))

    def test_ruta_obsoleta_se_reinicia(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15).run()
        app.session_state["indices"] = [999]
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["indices"], [])
