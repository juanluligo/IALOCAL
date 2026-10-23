"""Formato puro del Modelfile; la ficha específica se envía en cada consulta."""

from logica.validacion_arbol import validar_arbol
from modelo.instrucciones import SISTEMA

BASE = "llama3.2:1b"


def _temas(nodo):
    if nodo["nivel"] == "Orientación final":
        yield nodo
    for hijo in nodo.get("hijos", []):
        yield from _temas(hijo)


def construir_modelfile(arbol):
    validar_arbol(arbol)
    temas = {}
    for ficha in _temas(arbol):
        temas.setdefault((ficha["area"], ficha["tema"]), ficha)
    # Evita duplicar todas las variantes de acciones en el contexto permanente.
    # La ficha completa seleccionada se adjunta siempre en el prompt de usuario.
    secciones = [
        f"ÁREA: {area} | TEMA: {tema}\nConcepto: {ficha['conocimiento']}\nObjetivo: {ficha['objetivo']}"
        for (area, tema), ficha in sorted(temas.items())
    ]
    conocimiento = "\n\n".join(secciones)
    sistema = (
        SISTEMA
        + conocimiento
        + "\n\nREGLA FINAL: prioriza la ficha específica de la consulta y respeta siempre las reglas de seguridad.\n"
    )
    if '"""' in sistema:
        raise ValueError("El contenido no puede cerrar el bloque SYSTEM del Modelfile.")
    return (
        f"FROM {BASE}\n"
        "PARAMETER temperature 0.3\n"
        "PARAMETER num_ctx 8192\n"
        "PARAMETER num_predict 1200\n\n"
        f'SYSTEM """{sistema}"""\n'
    )
