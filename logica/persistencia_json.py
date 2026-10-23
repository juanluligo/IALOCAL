"""Codificación JSON estricta y escritura atómica, sin reglas del dominio."""

import json
import math
import os
import tempfile
from pathlib import Path


def _objeto_sin_duplicados(pares):
    objeto = {}
    for clave, valor in pares:
        if clave in objeto:
            raise ValueError(f"Clave JSON duplicada: {clave}")
        objeto[clave] = valor
    return objeto


def _constante_invalida(valor):
    raise ValueError(f"Constante no permitida en JSON: {valor}")


def _decimal_finito(valor):
    numero = float(valor)
    if not math.isfinite(numero):
        raise ValueError(f"Número JSON fuera de rango: {valor}")
    return numero


def decodificar_json(texto):
    """Rechaza claves duplicadas y NaN/Infinity que no pertenecen a JSON."""
    return json.loads(
        texto,
        object_pairs_hook=_objeto_sin_duplicados,
        parse_constant=_constante_invalida,
        parse_float=_decimal_finito,
    )


def leer_json(ruta):
    return decodificar_json(Path(ruta).read_text(encoding="utf-8-sig"))


def guardar_json(ruta, datos):
    """Serializa antes de tocar el destino y reemplaza solo un archivo completo."""
    contenido = json.dumps(datos, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=ruta.parent, suffix=".tmp", delete=False
        ) as archivo:
            temporal = Path(archivo.name)
            archivo.write(contenido)
        os.replace(temporal, ruta)
    finally:
        if temporal is not None:
            temporal.unlink(missing_ok=True)
