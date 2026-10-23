"""El Modelfile se produce únicamente desde un árbol validado."""

import tempfile
import unittest
from pathlib import Path

from logica.arbol import cargar_arbol


class TestModelfile(unittest.TestCase):
    def test_sintesis_tiene_un_bloque_por_tema_y_cabe_en_contexto(self):
        from modelo.modelfile import construir_modelfile

        contenido = construir_modelfile(cargar_arbol())
        self.assertEqual(contenido.count("ÁREA:"), 16)
        self.assertIn("FROM llama3.2:1b", contenido)
        self.assertIn("No diagnostiques", contenido)
        self.assertLess(len(contenido), 16000)

    def test_rechaza_arbol_invalido_sin_sobrescribir_salida(self):
        from modelo.crear_modelfile import main

        with tempfile.TemporaryDirectory() as carpeta:
            entrada = Path(carpeta) / "arbol.json"
            salida = Path(carpeta) / "Modelfile"
            entrada.write_text('{"id":"futbolia","valor":"incompleto"}', encoding="utf-8")
            salida.write_text("modelo anterior", encoding="utf-8")
            with self.assertRaises(ValueError):
                main(entrada, salida)
            self.assertEqual(salida.read_text(encoding="utf-8"), "modelo anterior")
