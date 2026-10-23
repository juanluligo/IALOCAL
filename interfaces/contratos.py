"""Contrato de las solicitudes HTTP JSON de FutbolIA."""

from flask import request

from logica.configuracion import MODELO, TEMPERATURA, validar_opciones
from logica.persistencia_json import decodificar_json


def leer_solicitud():
    if not request.is_json:
        raise ValueError("Envía un objeto con Content-Type: application/json.")
    try:
        datos = decodificar_json(request.get_data(as_text=True))
    except (ValueError, RecursionError) as exc:
        raise ValueError(
            "El cuerpo debe contener JSON válido, sin claves duplicadas ni números no finitos."
        ) from exc
    if not isinstance(datos, dict):
        raise ValueError("El cuerpo JSON debe ser un objeto.")
    indices = datos.get("indices", [])
    if not isinstance(indices, list):
        raise ValueError("indices debe ser una lista de enteros.")
    return datos


def opciones_solicitud(datos):
    return validar_opciones(
        datos.get("modelo", MODELO),
        datos.get("temperatura", TEMPERATURA),
        datos.get("usar_ia", True),
    )
