"""Fachada compatible; cada operación se implementa en su módulo responsable."""

from logica.navegacion import avanzar, bajar, contar, profundidad, retroceder
from logica.repositorio_arbol import cargar_arbol
from logica.validacion_arbol import validar_nodo

__all__ = [
    "avanzar",
    "bajar",
    "contar",
    "profundidad",
    "retroceder",
    "cargar_arbol",
    "validar_nodo",
]
