"""Contrato del adaptador: respeta el SYSTEM del modelo personalizado."""

import unittest
from unittest.mock import patch

from logica.cliente_ollama import consultar


class TestClienteOllama(unittest.TestCase):
    @patch("ollama.Client")
    def test_conserva_instrucciones_del_modelfile(self, cliente):
        cliente.return_value.chat.return_value = {"message": {"content": "respuesta del modelo"}}
        self.assertEqual(consultar("ficha específica", "futbolia", 0.3), "respuesta del modelo")
        argumentos = cliente.return_value.chat.call_args.kwargs
        self.assertEqual(argumentos["messages"], [{"role": "user", "content": "ficha específica"}])
        self.assertEqual(argumentos["model"], "futbolia")
        self.assertEqual(argumentos["options"]["temperature"], 0.3)
        self.assertEqual(cliente.call_args.kwargs["timeout"], 60)
