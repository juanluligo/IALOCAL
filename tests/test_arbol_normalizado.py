"""El almacenamiento crece por definiciones, no por combinaciones repetidas."""

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from logica.arbol import cargar_arbol, contar
from logica.catalogo import cargar_catalogo
from logica.persistencia_json import guardar_json, leer_json
from logica.rutas import ARBOL_JSON, CATALOGO_JSON, RAIZ


class TestArbolNormalizado(unittest.TestCase):
    def test_conserva_exactamente_el_arbol_previo_a_la_migracion(self):
        contenido = json.dumps(
            cargar_arbol(), sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(contenido).hexdigest(),
            "f8fa22218eac83ed4036420992b81c6981a5f74790034acd2f7e74c7d2fb0d8e",
        )

    def test_archivo_es_fuente_unica_normalizada(self):
        datos = leer_json(ARBOL_JSON)
        self.assertEqual(datos.get("formato"), "catalogo_futbolia")
        self.assertEqual(datos.get("id"), "futbolia")
        self.assertNotIn("hijos", datos)
        self.assertEqual(len(datos["temas"]), 16)
        self.assertEqual(CATALOGO_JSON, ARBOL_JSON)
        self.assertFalse((RAIZ / "datos" / "catalogo.json").exists())

    def test_no_se_repiten_conocimiento_ni_combinaciones(self):
        texto = ARBOL_JSON.read_text(encoding="utf-8")
        self.assertEqual(texto.count('"conocimiento_ampliado"'), 16)
        self.assertNotIn('"nivel_jugador"', texto)
        self.assertLess(len(texto.splitlines()), 1000)
        self.assertLess(ARBOL_JSON.stat().st_size, 35000)
        self.assertEqual(contar(cargar_arbol()), (453, 192))

    def test_carga_una_fuente_normalizada_independiente(self):
        fuente = copy.deepcopy(cargar_catalogo())
        fuente.update(formato="catalogo_futbolia", id="futbolia")
        fuente["temas"][0]["objetivo"] = "Objetivo de prueba independiente"
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "otro_arbol.json"
            guardar_json(ruta, fuente)
            arbol = cargar_arbol(ruta)
            hoja = arbol["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]
            self.assertEqual(hoja["objetivo"], "Objetivo de prueba independiente")

    def test_conserva_lectura_del_formato_expandido(self):
        arbol = cargar_arbol()
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "legado.json"
            guardar_json(ruta, arbol)
            self.assertEqual(cargar_arbol(ruta), arbol)

    def test_comando_no_vuelve_a_expandir_el_archivo(self):
        antes = ARBOL_JSON.read_bytes()
        resultado = subprocess.run(
            [sys.executable, "-X", "utf8", "logica/generar_arbol.py"],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(ARBOL_JSON.read_bytes(), antes)
        self.assertIn("192", resultado.stdout)

    def test_rechaza_formato_desconocido(self):
        fuente = copy.deepcopy(cargar_catalogo())
        fuente.update(formato="desconocido", id="futbolia")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "arbol.json"
            ruta.write_text(json.dumps(fuente), encoding="utf-8")
            with self.assertRaises(ValueError):
                cargar_arbol(ruta)
