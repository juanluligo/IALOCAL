"""Caso de uso: coordinar IA, validación y respaldo con dependencias sustituibles."""

import logging
from typing import Callable

from logica.cliente_ollama import consultar as consultar_ollama
from logica.configuracion import MODELO, TEMPERATURA, validar_opciones
from logica.ficha import guia_verificada
from logica.prompts import armar_prompt
from logica.validacion_guia import validar_guia

log = logging.getLogger("futbolia")
AVISOS = {
    "ollama": "La IA local no está disponible o devolvió un error. Se muestra la orientación educativa del sistema.",
    "desactivada": "La IA está desactivada. Se muestra la orientación educativa del sistema.",
    "validacion": "La respuesta de la IA no superó las comprobaciones básicas de seguridad y pertinencia. Se muestra la ficha del sistema.",
}


class ServicioGuia:
    """Depende de funciones pequeñas, no de Flask, Streamlit ni archivos JSON."""

    def __init__(
        self,
        consultar: Callable[[str, str, float], str] = consultar_ollama,
        validar=validar_guia,
        formatear=guia_verificada,
        crear_prompt=armar_prompt,
    ):
        self.consultar = consultar
        self.validar = validar
        self.formatear = formatear
        self.crear_prompt = crear_prompt

    def generar(self, camino, hoja, modelo=MODELO, temperatura=TEMPERATURA, usar_ia=True):
        modelo, temperatura, usar_ia = validar_opciones(modelo, temperatura, usar_ia)
        respaldo = self.formatear(hoja)

        def alternativa(motivo):
            return {
                "texto": respaldo,
                "fuente": "sistema",
                "aviso": AVISOS[motivo],
                "validacion": "respaldo",
            }

        if not usar_ia:
            return alternativa("desactivada")
        prompt = self.crear_prompt(camino, hoja)
        try:
            texto = self.consultar(prompt, modelo, temperatura)
        except Exception as exc:
            log.warning("Consulta Ollama fallida (%s).", type(exc).__name__)
            return alternativa("ollama")
        valida, motivos = self.validar(texto, hoja)
        if not valida:
            log.warning("Respuesta IA no validada: %s", motivos)
            return alternativa("validacion")
        return {
            "texto": texto.strip(),
            "fuente": "ollama",
            "aviso": None,
            "validacion": "basica_aprobada",
        }
