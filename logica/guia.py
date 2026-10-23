"""Fachada compatible para formato de ficha y validación de respuestas."""

from logica.ficha import guia_verificada
from logica.validacion_guia import normalizar, validar_guia

__all__ = ["guia_verificada", "normalizar", "validar_guia"]
