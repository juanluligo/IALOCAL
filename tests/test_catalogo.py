"""La ampliación del catálogo no requiere modificar el constructor."""

import copy
import unittest

from logica.catalogo import cargar_catalogo, validar_catalogo
from logica.generar_arbol import generar


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = cargar_catalogo()

    def test_admite_nivel_nuevo_con_politica_de_datos(self):
        self.catalogo["niveles"].append(
            {
                "id": "retorno",
                "valor": "Retomo la práctica",
                "icono": "⚽",
                "acciones_previas": ["Revisar comodidad antes de comenzar"],
                "max_acciones_base": 1,
                "progresion": ["Aumentar la práctica gradualmente"],
            }
        )
        arbol = generar(self.catalogo)
        nivel = arbol["hijos"][0]["hijos"][0]["hijos"][-1]
        self.assertEqual(nivel["id"], "retorno")
        hoja = nivel["hijos"][0]["hijos"][0]
        self.assertEqual(hoja["acciones"][0], "Revisar comodidad antes de comenzar")
        self.assertEqual(hoja["progresion"], ["Aumentar la práctica gradualmente"])

    def test_construir_no_modifica_catalogo(self):
        copia = copy.deepcopy(self.catalogo)
        generar(self.catalogo)
        self.assertEqual(copia, self.catalogo)

    def test_rechaza_catalogos_inconsistentes(self):
        for mutar in (
            lambda c: c.update(version=True),
            lambda c: c["temas"][0].update(area="Desconocida"),
            lambda c: c["temas"].append(copy.deepcopy(c["temas"][0])),
            lambda c: c["temas"][0].update(acciones="correr"),
            lambda c: c["niveles"][0].update(max_acciones_base=True),
        ):
            catalogo = copy.deepcopy(self.catalogo)
            mutar(catalogo)
            with self.subTest(catalogo=catalogo["version"]), self.assertRaises(ValueError):
                validar_catalogo(catalogo)
