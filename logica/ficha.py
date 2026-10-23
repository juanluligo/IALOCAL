"""Presentación textual de la ficha de respaldo, sin IA ni reglas de filtrado."""


def guia_verificada(hoja):
    lineas = []

    campos = [
        ("Área", "area"),
        ("Tema", "tema"),
        ("Nivel", "nivel_jugador"),
        ("Contexto", "contexto_practica"),
        ("Conocimiento", "conocimiento"),
        ("Conocimiento ampliado", "conocimiento_ampliado"),
        ("Objetivo", "objetivo"),
        ("Detalle", "detalle"),
        ("Estructura sugerida", "estructura"),
    ]

    for titulo, campo in campos:
        valor = hoja.get(campo)
        if valor:
            lineas.append(f"**{titulo}:** {valor}")

    listas = [
        ("acciones", "Pasos sugeridos"),
        ("progresion", "Progresión"),
        ("adaptaciones", "Adaptaciones inclusivas"),
        ("evaluacion", "Seguimiento educativo"),
    ]

    for campo, titulo in listas:
        elementos = hoja.get(campo, [])
        if elementos:
            lineas.append(f"**{titulo}:**")
            lineas.extend(f"- {elemento}" for elemento in elementos)

    if hoja.get("precaucion"):
        lineas.append(f"**Precauciones:** {hoja['precaucion']}")

    if hoja.get("limites"):
        lineas.append(f"**Límites:** {hoja['limites']}")

    lineas.append(
        "Esta orientación es educativa y general; debe adaptarse "
        "con la persona. No es una valoración médica ni un "
        "diagnóstico psicológico."
    )

    return "\n\n".join(lineas)
