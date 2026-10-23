"""Genera modelo/Modelfile desde un árbol validado; no requiere archivos TXT."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logica.repositorio_arbol import cargar_arbol
from logica.rutas import ARBOL_JSON as ARBOL
from logica.rutas import MODELFILE as SALIDA
from modelo.modelfile import construir_modelfile


def main(entrada=ARBOL, salida=SALIDA):
    arbol = cargar_arbol(entrada)
    contenido = construir_modelfile(arbol)
    salida = Path(salida)
    salida.write_text(contenido, encoding="utf-8")
    print(f"Modelfile actualizado: {salida} ({salida.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
