"""Identificadores estables compatibles con el árbol publicado."""


def identificador(texto):
    return "".join(c.lower() if c.isalnum() else "_" for c in texto).strip("_")
