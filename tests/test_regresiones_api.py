"""Entradas HTTP inválidas deben producir 400 JSON, nunca errores internos."""

import unittest
from unittest.mock import patch

from interfaces.app import app


class TestContratosHTTP(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = False
        self.client = app.test_client()

    def test_cuerpo_debe_ser_objeto_json(self):
        for endpoint in ("/api/nodo", "/api/explicar"):
            for cuerpo in ("null", "[]", "[1]", '"texto"', "42", "true", "{", ""):
                with self.subTest(endpoint=endpoint, cuerpo=cuerpo):
                    res = self.client.post(endpoint, data=cuerpo, content_type="application/json")
                    self.assertEqual(res.status_code, 400)
                    self.assertIn("error", res.get_json())

    def test_sin_content_type_json(self):
        res = self.client.post("/api/nodo", data='{"indices": []}')
        self.assertEqual(res.status_code, 400)

    def test_recursos_de_presentacion_se_sirven_independientes(self):
        for ruta, tipo in (("/static/app.js", "javascript"), ("/static/app.css", "text/css")):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(tipo, respuesta.content_type)
                respuesta.close()

    @patch("logica.ApiLocal.consultar", side_effect=AssertionError("No debe llamar IA"))
    def test_opciones_explicitas(self, consultar):
        casos = (
            {"usar_ia": "false"},
            {"usar_ia": 0},
            {"usar_ia": None},
            {"temperatura": True},
            {"temperatura": "0.3"},
            {"temperatura": float("nan")},
            {"temperatura": float("inf")},
            {"temperatura": 10**400},
            {"modelo": ["futbolia"]},
            {"modelo": " "},
        )
        for opciones in casos:
            with self.subTest(opciones=opciones):
                datos = {"indices": [0, 0, 0, 0, 0], "usar_ia": False, **opciones}
                res = self.client.post("/api/explicar", json=datos)
                self.assertEqual(res.status_code, 400)
        consultar.assert_not_called()

    def test_rechaza_claves_duplicadas(self):
        res = self.client.post(
            "/api/nodo", data='{"indices": [999], "indices": []}', content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

    def test_fabrica_permite_inyectar_servicio(self):
        from interfaces.app import create_app
        from logica.arbol import cargar_arbol

        def servicio(camino, hoja, modelo, temperatura, usar_ia):
            return {"texto": hoja["objetivo"], "fuente": "prueba", "aviso": None}

        client = create_app(arbol=cargar_arbol(), generador=servicio).test_client()
        res = client.post("/api/explicar", json={"indices": [0, 0, 0, 0, 0], "usar_ia": False})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["fuente"], "prueba")

    def test_todas_las_hojas_sin_ia(self):
        for area in range(4):
            for tema in range(4):
                for nivel in range(3):
                    for contexto in range(4):
                        indices = [area, tema, nivel, contexto, 0]
                        with self.subTest(indices=indices):
                            ficha = self.client.post(
                                "/api/nodo", json={"indices": indices}
                            ).get_json()
                            res = self.client.post(
                                "/api/explicar", json={"indices": indices, "usar_ia": False}
                            )
                            self.assertEqual(res.status_code, 200)
                            self.assertEqual(res.get_json()["fuente"], "sistema")
                            self.assertIn(ficha["objetivo"], res.get_json()["texto"])
