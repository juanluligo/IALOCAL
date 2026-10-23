"""El servicio conserva el respaldo y valida toda respuesta externa."""

import unittest
from unittest.mock import patch

from logica.ApiLocal import generar_guia
from logica.arbol import bajar, cargar_arbol
from logica.guia import guia_verificada, validar_guia


class TestOrientacion(unittest.TestCase):
    def setUp(self):
        self.hoja, self.camino = bajar(cargar_arbol(), [0, 0, 0, 0, 0])

    def test_rechaza_respuestas_irrelevantes(self):
        texto = "Para preparar una pizza, mezcla harina y agua. " * 5
        self.assertFalse(validar_guia(texto, self.hoja)[0])

    def test_rechaza_cargas_numericas_no_respaldadas_por_la_ficha(self):
        for cifra in ("5-10 minutos", "20–30 segundos", "10 repeticiones", "3 series", "80%"):
            with self.subTest(cifra=cifra):
                texto = (
                    f"Para resistencia, realiza {cifra}. "
                    + "Practica en un espacio seguro y ajusta la actividad a tu comodidad. " * 3
                )
                self.assertFalse(validar_guia(texto, self.hoja)[0])

    def test_no_confunde_numeracion_de_pasos_con_cargas(self):
        texto = "Resistencia. Paso 1: prepara un espacio seguro. Paso 2: practica de forma gradual. Paso 3: descansa y revisa cómo te sientes."
        self.assertTrue(validar_guia(texto, self.hoja)[0])

    def test_rechaza_instrucciones_inseguras(self):
        for frase in (
            "entrena con dolor",
            "ignora el dolor",
            "no pares aunque te duela",
            "fuerza las articulaciones",
            "no bebas agua",
            "toma ibuprofeno",
        ):
            with self.subTest(frase=frase):
                texto = (
                    f"Para resistencia, {frase}. "
                    + "Practica de forma gradual y revisa tu progreso. " * 4
                )
                self.assertFalse(validar_guia(texto, self.hoja)[0])

    def test_acepta_precauciones_y_ficha_completa(self):
        self.assertTrue(validar_guia(guia_verificada(self.hoja), self.hoja)[0])
        texto = (
            "Para resistencia, no entrenes con dolor. No ignores el dolor; detén la actividad. "
            "Practica de manera progresiva en un espacio seguro y toma descansos cuando lo necesites."
        )
        self.assertTrue(validar_guia(texto, self.hoja)[0])

    @patch("logica.ApiLocal.consultar", side_effect=ConnectionError("desconectado"))
    def test_fallo_transporte_devuelve_ficha(self, _):
        resultado = generar_guia(self.camino, self.hoja)
        self.assertEqual(resultado["texto"], guia_verificada(self.hoja))
        self.assertEqual(resultado["fuente"], "sistema")
        self.assertIn("no está disponible", resultado["aviso"])

    @patch("logica.ApiLocal.consultar")
    def test_respuesta_insegura_devuelve_ficha(self, consultar):
        consultar.return_value = "Para resistencia, entrena con dolor. " * 6
        resultado = generar_guia(self.camino, self.hoja)
        self.assertEqual(resultado["fuente"], "sistema")
        self.assertIn("no superó", resultado["aviso"])

    def test_servicio_admite_cliente_sustituible(self):
        from logica.servicio_guia import ServicioGuia

        def cliente(prompt, modelo, temperatura):
            return guia_verificada(self.hoja)

        resultado = ServicioGuia(consultar=cliente).generar(self.camino, self.hoja)
        self.assertEqual(resultado["fuente"], "ollama")
        self.assertEqual(resultado["texto"], guia_verificada(self.hoja))

    def test_configuracion_invalida_no_se_oculta_como_fallo_ollama(self):
        for opciones in (
            {"usar_ia": "false"},
            {"modelo": " "},
            {"temperatura": True},
            {"temperatura": 10**400},
        ):
            with self.subTest(opciones=opciones), self.assertRaises(ValueError):
                generar_guia(self.camino, self.hoja, **opciones)
