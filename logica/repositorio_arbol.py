"""Carga de árboles persistidos aplicando el contrato del dominio."""

from logica.construccion_arbol import construir_arbol
from logica.persistencia_json import leer_json
from logica.rutas import ARBOL_JSON
from logica.validacion_arbol import validar_arbol


def cargar_arbol(ruta=ARBOL_JSON):
    datos = leer_json(ruta)
    # El formato normalizado conserva las definiciones una sola vez. La expansión
    # pertenece al dominio en memoria, nunca a los archivos persistidos.
    normalizado = isinstance(datos, dict) and ("formato" in datos or "temas" in datos)
    arbol = construir_arbol(datos) if normalizado else datos
    validar_arbol(arbol)
    return arbol
