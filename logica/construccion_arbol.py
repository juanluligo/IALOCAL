"""Construcción pura del árbol desde un catálogo validado."""

from logica.adaptacion_ficha import crear_hoja
from logica.catalogo import validar_catalogo
from logica.identificadores import identificador


def construir_arbol(catalogo):
    validar_catalogo(catalogo)
    raiz = {
        "nivel": "Raíz",
        "id": "futbolia",
        "valor": "FutbolIA: fútbol inclusivo",
        "icono": "⚽",
        "pregunta": "¿Qué área quieres trabajar?",
        "hijos": [],
    }
    for area in catalogo["areas"]:
        nodo_area = {
            "nivel": "Área",
            "id": area["id"],
            "valor": f"Área {area['nombre'].lower()}",
            "icono": area["icono"],
            "pregunta": area["pregunta"],
            "hijos": [],
        }
        for base in (t for t in catalogo["temas"] if t["area"] == area["nombre"]):
            tema = {
                "nivel": "Objetivo",
                "id": identificador(base["tema"]),
                "valor": base["tema"],
                "icono": "🎯",
                "pregunta": "¿Cuál es tu nivel de experiencia?",
                "hijos": [],
            }
            for nivel in catalogo["niveles"]:
                nodo_nivel = {
                    "nivel": "Nivel de experiencia",
                    "id": nivel["id"],
                    "valor": nivel["valor"],
                    "icono": nivel["icono"],
                    "pregunta": "¿En qué contexto vas a practicar?",
                    "hijos": [],
                }
                for contexto in catalogo["contextos"]:
                    nodo_nivel["hijos"].append(
                        {
                            "nivel": "Contexto de práctica",
                            "id": contexto["id"],
                            "valor": contexto["valor"],
                            "icono": contexto["icono"],
                            "pregunta": "Orientación personalizada",
                            "hijos": [crear_hoja(base, nivel, contexto, area)],
                        }
                    )
                tema["hijos"].append(nodo_nivel)
            nodo_area["hijos"].append(tema)
        raiz["hijos"].append(nodo_area)
    return raiz
