"""Conversión de nodos de dominio a respuestas públicas de la API."""


def presentar_nodo(nodo, camino, indices, total_niveles):
    hijos = nodo.get("hijos", [])
    resultado = {
        "indices": indices,
        "pregunta": nodo.get("pregunta"),
        "valor": nodo["valor"],
        "camino": [paso["valor"] for paso in camino],
        "total_niveles": total_niveles,
        "hoja": not hijos,
        "opciones": [{"valor": hijo["valor"], "icono": hijo["icono"]} for hijo in hijos],
    }
    for campo in (
        "detalle",
        "area",
        "tema",
        "objetivo",
        "precaucion",
        "conocimiento",
        "conocimiento_ampliado",
        "nivel_jugador",
        "contexto_practica",
        "estructura",
        "limites",
    ):
        resultado[campo] = nodo.get(campo)
    for campo in ("acciones", "progresion", "adaptaciones", "evaluacion"):
        resultado[campo] = nodo.get(campo, [])
    return resultado
