"""Valida la fuente normalizada y construye el árbol únicamente en memoria.

Uso: python logica/generar_arbol.py
"""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logica.catalogo import cargar_catalogo
from logica.construccion_arbol import construir_arbol
from logica.navegacion import contar
from logica.validacion_arbol import validar_arbol


def generar(catalogo=None):
    arbol = construir_arbol(cargar_catalogo() if catalogo is None else catalogo)
    validar_arbol(arbol)
    return arbol


def main():
    arbol = generar()
    nodos, hojas = contar(arbol)
    print(f"Árbol validado en memoria: {nodos} nodos, {hojas} orientaciones finales.")
    print("La fuente JSON permanece normalizada; no se guardan combinaciones duplicadas.")


if __name__ == "__main__":
    main()
