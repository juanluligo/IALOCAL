"""Pruebas de árbol, fichas, validación, API de prompts y configuración."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from logica.ApiLocal import MODELO, armar_prompt
from logica.arbol import bajar, cargar_arbol, contar, validar_nodo
from logica.generar_arbol import generar
from logica.guia import guia_verificada, validar_guia


class TestFutbolIA(unittest.TestCase):
    def setUp(self):
        self.arbol = cargar_arbol()

    def hojas(self):
        def walk(n):
            if not n.get("hijos"):
                yield n
            else:
                for h in n["hijos"]:
                    yield from walk(h)

        return list(walk(self.arbol))

    def test_raiz_y_cuatro_areas(self):
        self.assertEqual(self.arbol["id"], "futbolia")
        areas = [x["valor"].lower() for x in self.arbol["hijos"]]
        for expected in ["física", "técnica", "táctica", "psicológica"]:
            self.assertTrue(any(expected in a for a in areas))

    def test_arbol_amplio_y_hojas_completas(self):
        nodos, hojas = contar(self.arbol)
        self.assertGreater(nodos, 400)
        self.assertGreaterEqual(hojas, 190)
        for h in self.hojas():
            for k in [
                "area",
                "tema",
                "objetivo",
                "acciones",
                "progresion",
                "adaptaciones",
                "evaluacion",
                "precaucion",
            ]:
                self.assertTrue(h.get(k), f"Falta {k}: {h.get('id')}")

    def test_combinaciones_nivel_y_contexto(self):
        h = self.hojas()
        self.assertEqual(len(h), 192)
        self.assertEqual(len({x["id"] for x in h}), 192)
        from collections import Counter

        self.assertEqual(set(Counter(x["area"] for x in h).values()), {48})
        self.assertEqual(
            {x["nivel_jugador"] for x in h},
            {
                "Principiante / estoy empezando",
                "Tengo algo de experiencia",
                "Tengo experiencia y busco progresar",
            },
        )

    def test_ruta_invalida(self):
        with self.assertRaises(ValueError):
            bajar(self.arbol, [999])
        with self.assertRaises(ValueError):
            bajar(self.arbol, [True])

    def test_prompt_contiene_ruta_y_seguridad(self):
        hoja, camino = bajar(self.arbol, [0, 0, 0, 0, 0])
        prompt = armar_prompt(camino, hoja)
        self.assertIn("FutbolIA", prompt)
        self.assertIn("No diagnostiques", prompt)
        self.assertIn("FICHA ESTRUCTURADA", prompt)
        self.assertIn("CONOCIMIENTO AMPLIADO ESPECÍFICO", prompt)
        self.assertIn(hoja.get("conocimiento_ampliado", ""), prompt)

    def test_modelo_personalizado_y_sin_txt(self):
        self.assertEqual(MODELO, "futbolia")
        mf = (ROOT / "modelo" / "Modelfile").read_text(encoding="utf-8")
        self.assertIn("FROM llama3.2:1b", mf)
        self.assertIn("fútbol inclusivo", mf.lower())
        self.assertFalse((ROOT / "modelo" / "conocimiento_futbolia.txt").exists())
        self.assertFalse(list((ROOT / "modelo").glob("*.txt")))

    def test_ficha_respaldo_completa(self):
        hoja = self.hojas()[0]
        ficha = guia_verificada(hoja)
        for k in ["Objetivo", "Progresión", "Adaptaciones inclusivas", "Precauciones"]:
            self.assertIn(k, ficha)

    def test_validador_rechaza_frase_insegura(self):
        hoja = self.hojas()[0]
        texto = (
            "Para mejorar "
            + hoja["tema"]
            + ", entrena con dolor y no pares aunque te duela. "
            + ("Haz ejercicios de manera gradual y revisa tu progreso. " * 3)
        )
        ok, motivos = validar_guia(texto, hoja)
        self.assertFalse(ok)
        self.assertTrue(motivos)

    def test_validador_acepta_respuesta_relevante(self):
        hoja = self.hojas()[0]
        texto = f"El objetivo de {hoja['tema']} es practicar de forma progresiva. Realiza el ejercicio en un espacio seguro, empieza con una versión sencilla, descansa cuando lo necesites y ajusta la actividad a tus preferencias. Revisa tu comodidad y detente ante síntomas inusuales."
        ok, _ = validar_guia(texto, hoja)
        self.assertTrue(ok)

    def test_generador_reproducible_y_json_valido(self):
        tree = generar()
        validar_nodo(tree)
        self.assertEqual(contar(tree), contar(self.arbol))
        json.dumps(tree, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
