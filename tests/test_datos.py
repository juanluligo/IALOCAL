"""Regresiones de los límites JSON y la integridad del árbol."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from logica.arbol import cargar_arbol, validar_nodo
from logica.generar_arbol import generar


class TestDatos(unittest.TestCase):
    def setUp(self):
        self.arbol = cargar_arbol()

    def test_generacion_conserva_todo_el_contenido(self):
        self.assertEqual(generar(), self.arbol)

    def test_rechaza_nodos_incompletos(self):
        for nodo in ({"valor": "sin estructura"}, {"valor": " "}):
            with self.subTest(nodo=nodo), self.assertRaises(ValueError):
                validar_nodo(nodo)

    def test_rechaza_rama_truncada(self):
        self.arbol["hijos"][0]["hijos"] = []
        with self.assertRaises(ValueError):
            validar_nodo(self.arbol)

    def test_rechaza_hermanos_duplicados(self):
        self.arbol["hijos"].append(copy.deepcopy(self.arbol["hijos"][0]))
        with self.assertRaises(ValueError):
            validar_nodo(self.arbol)

    def test_rechaza_campos_de_hoja_mal_tipados(self):
        for campo, valor in (
            ("acciones", "correr"),
            ("objetivo", 3),
            ("evaluacion", [None]),
            ("adaptaciones", [" "]),
        ):
            arbol = copy.deepcopy(self.arbol)
            hoja = arbol["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]
            hoja[campo] = valor
            with self.subTest(campo=campo), self.assertRaises(ValueError):
                validar_nodo(arbol)

    def test_rechaza_claves_json_duplicadas(self):
        contenido = json.dumps(self.arbol, ensure_ascii=False)
        contenido = contenido.replace('"id": "futbolia"', '"id": "otro", "id": "futbolia"', 1)
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "arbol.json"
            ruta.write_text(contenido, encoding="utf-8")
            with self.assertRaises(ValueError):
                cargar_arbol(ruta)

    def test_no_acepta_numeros_no_finitos_ni_exponentes_desbordados(self):
        from logica.persistencia_json import decodificar_json

        for numero in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(numero=numero), self.assertRaises(ValueError):
                decodificar_json('{"valor": ' + numero + "}")

    def test_serializacion_fallida_conserva_archivo_anterior(self):
        from logica.persistencia_json import guardar_json, leer_json

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            guardar_json(ruta, {"texto": "Fútbol inclusivo"})
            with self.assertRaises(ValueError):
                guardar_json(ruta, {"numero": float("nan")})
            self.assertEqual(leer_json(ruta), {"texto": "Fútbol inclusivo"})
            self.assertEqual(list(Path(carpeta).glob("*.tmp")), [])

    def test_ficha_debe_coincidir_con_area_de_la_ruta(self):
        hoja = self.arbol["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]["hijos"][0]
        hoja["area"] = "Táctica"
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "arbol.json"
            ruta.write_text(json.dumps(self.arbol, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                cargar_arbol(ruta)
