"""Composición pura de una ficha aplicando políticas declaradas en el catálogo."""

from logica.identificadores import identificador


def crear_hoja(base, nivel, contexto, area):
    acciones = list(base["acciones"][: nivel.get("max_acciones_base")])
    acciones = list(nivel.get("acciones_previas", [])) + acciones
    adaptaciones = list(base["adaptaciones"][: contexto.get("max_adaptaciones_base")])
    adaptaciones = list(contexto.get("adaptaciones_previas", [])) + adaptaciones
    ficha = {
        campo: base[campo]
        for campo in (
            "area",
            "tema",
            "detalle",
            "conocimiento",
            "objetivo",
            "estructura",
            "conocimiento_ampliado",
        )
    }
    ficha.update(
        {
            "nivel": "Orientación final",
            "id": f"{identificador(base['area'])}_{identificador(base['tema'])}_{nivel['id']}_{contexto['id']}",
            "valor": f"{base['tema']} — {nivel['valor']}",
            "icono": "⚽",
            "nivel_jugador": nivel["valor"],
            "contexto_practica": contexto["valor"],
            "acciones": acciones,
            "progresion": list(nivel.get("progresion", base["progresion"])),
            "adaptaciones": adaptaciones,
            "evaluacion": list(base["evaluacion"]),
            "precaucion": base["precaucion"] + area.get("precaucion_adicional", ""),
            "limites": "Orientación educativa general; no sustituye al entrenador ni a profesionales sanitarios.",
        }
    )
    return ficha
