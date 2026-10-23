"""Contrato y carga del catálogo fuente de conocimiento deportivo."""

from logica.identificadores import identificador
from logica.persistencia_json import leer_json
from logica.rutas import CATALOGO_JSON
from logica.validacion_arbol import validar_lista_textos, validar_texto


def validar_catalogo(catalogo):
    if (
        not isinstance(catalogo, dict)
        or type(catalogo.get("version")) is not int
        or catalogo["version"] != 1
        or catalogo.get("formato") != "catalogo_futbolia"
        or catalogo.get("id") != "futbolia"
        or "hijos" in catalogo
    ):
        raise ValueError(
            "Se requiere catalogo_futbolia version: 1, id: futbolia, sin hijos expandidos."
        )
    for seccion in ("areas", "niveles", "contextos", "temas"):
        elementos = catalogo.get(seccion)
        if not isinstance(elementos, list) or not elementos:
            raise ValueError(f"El catálogo requiere una lista no vacía: {seccion}")
        vistos = set()
        for indice, elemento in enumerate(elementos):
            ruta = f"{seccion}/{indice}"
            if not isinstance(elemento, dict):
                raise ValueError(f"{ruta} debe ser un objeto.")
            if seccion == "temas":
                textos = (
                    "area",
                    "tema",
                    "detalle",
                    "conocimiento",
                    "objetivo",
                    "precaucion",
                    "conocimiento_ampliado",
                    "estructura",
                )
                clave = (elemento.get("area"), identificador(str(elemento.get("tema", ""))))
            else:
                textos = (
                    ("id", "icono", "nombre", "pregunta")
                    if seccion == "areas"
                    else ("id", "icono", "valor")
                )
                clave = elemento.get("id")
            for campo in textos:
                validar_texto(elemento.get(campo), f"{ruta}/{campo}")
            if seccion == "areas" and "precaucion_adicional" in elemento:
                validar_texto(elemento["precaucion_adicional"], f"{ruta}/precaucion_adicional")
            listas_opcionales = (
                ("acciones_previas", "progresion")
                if seccion == "niveles"
                else ("adaptaciones_previas",)
                if seccion == "contextos"
                else ()
            )
            for campo in listas_opcionales:
                if campo in elemento:
                    validar_lista_textos(elemento[campo], f"{ruta}/{campo}")
            limite = (
                "max_acciones_base"
                if seccion == "niveles"
                else "max_adaptaciones_base"
                if seccion == "contextos"
                else None
            )
            if limite is not None and limite in elemento:
                if type(elemento[limite]) is not int or elemento[limite] < 1:
                    raise ValueError(f"{ruta}/{limite} debe ser un entero positivo.")
            if seccion == "temas":
                for campo in ("acciones", "progresion", "adaptaciones", "evaluacion"):
                    validar_lista_textos(elemento.get(campo), f"{ruta}/{campo}")
            if clave in vistos:
                raise ValueError(f"Entrada duplicada en {ruta}: {clave}")
            vistos.add(clave)
    areas = [a["nombre"] for a in catalogo["areas"]]
    if len(areas) != len(set(areas)):
        raise ValueError("Los nombres de área deben ser únicos.")
    usadas = {tema["area"] for tema in catalogo["temas"]}
    if usadas != set(areas):
        raise ValueError("Cada tema debe pertenecer a un área y cada área debe tener temas.")
    return True


def cargar_catalogo(ruta=CATALOGO_JSON):
    catalogo = leer_json(ruta)
    validar_catalogo(catalogo)
    return catalogo
