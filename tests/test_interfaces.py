"""Pruebas de la API Flask y del comportamiento de respaldo."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from interfaces.app import app


class TestInterfaces(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_carga(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"FutbolIA", response.data)

    def test_api_raiz_devuelve_cuatro_areas(self):
        response = self.client.post("/api/nodo", json={"indices": []})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data["hoja"])
        self.assertEqual(len(data["opciones"]), 4)

    def test_api_ruta_invalida(self):
        response = self.client.post("/api/nodo", json={"indices": [999]})
        self.assertEqual(response.status_code, 400)

    def test_api_rechaza_indices_que_no_son_lista(self):
        response = self.client.post("/api/nodo", json={"indices": "0,1"})
        self.assertEqual(response.status_code, 400)

    def test_api_muestra_detalle_de_hoja(self):
        response = self.client.post("/api/nodo", json={"indices": [0, 0, 0, 0, 0]})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["hoja"])
        self.assertTrue(data["objetivo"])
        self.assertTrue(data["adaptaciones"])

    def test_api_explicar_con_respaldo_sin_ia(self):
        response = self.client.post(
            "/api/explicar", json={"indices": [0, 0, 0, 0, 0], "usar_ia": False}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["fuente"], "sistema")
        self.assertIn("Objetivo", data["texto"])

    def test_api_explicar_rechaza_nodo_no_final(self):
        response = self.client.post("/api/explicar", json={"indices": [0]})
        self.assertEqual(response.status_code, 400)

    def test_api_rechaza_temperatura_fuera_de_rango(self):
        response = self.client.post(
            "/api/explicar", json={"indices": [0, 0, 0, 0, 0], "usar_ia": False, "temperatura": 2}
        )
        self.assertEqual(response.status_code, 400)

    @patch("logica.ApiLocal.consultar")
    def test_api_usa_ia_si_respuesta_valida(self, consultar):
        consultar.return_value = (
            "El objetivo de resistencia es practicar de forma progresiva. "
            "Realiza el ejercicio en un espacio seguro, empieza con una versión sencilla, "
            "descansa cuando lo necesites y ajusta la actividad a tus preferencias. "
            "Revisa tu comodidad y detente ante síntomas inusuales."
        )
        response = self.client.post(
            "/api/explicar", json={"indices": [0, 0, 0, 0, 0], "usar_ia": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["fuente"], "ollama")


if __name__ == "__main__":
    unittest.main()
