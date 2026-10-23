"""Rutas centralizadas del proyecto FutbolIA."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARBOL_JSON = RAIZ / "datos" / "ArbolFutbolIA.json"
# Alias compatible: catálogo y definición del árbol tienen una única fuente.
CATALOGO_JSON = ARBOL_JSON
MODELFILE = RAIZ / "modelo" / "Modelfile"
