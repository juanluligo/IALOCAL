"""Contrato de los nodos y transiciones del árbol de decisiones."""

NIVELES = (
    "Raíz",
    "Área",
    "Objetivo",
    "Nivel de experiencia",
    "Contexto de práctica",
    "Orientación final",
)
TEXTOS_HOJA = (
    "area",
    "tema",
    "nivel_jugador",
    "contexto_practica",
    "detalle",
    "conocimiento",
    "objetivo",
    "estructura",
    "conocimiento_ampliado",
    "precaucion",
    "limites",
)
LISTAS_HOJA = ("acciones", "progresion", "adaptaciones", "evaluacion")


def validar_texto(valor, ruta):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{ruta} debe ser texto no vacío.")


def validar_lista_textos(valor, ruta):
    if not isinstance(valor, list) or not valor:
        raise ValueError(f"{ruta} debe ser una lista no vacía de textos.")
    for indice, elemento in enumerate(valor):
        validar_texto(elemento, f"{ruta}/{indice}")


def validar_nodo(nodo, ruta="raíz", *, nivel_esperado=None):
    if not isinstance(nodo, dict):
        raise ValueError(f"{ruta} debe ser un objeto.")
    for campo in ("id", "valor", "nivel", "icono"):
        validar_texto(nodo.get(campo), f"{ruta}/{campo}")
    nivel = nodo["nivel"]
    if nivel not in NIVELES or (nivel_esperado is not None and nivel != nivel_esperado):
        raise ValueError(f"Nivel inválido en {ruta}: {nivel}")
    hijos = nodo.get("hijos", [])
    if not isinstance(hijos, list):
        raise ValueError(f"{ruta}/hijos debe ser una lista.")
    if nivel == "Orientación final":
        if hijos:
            raise ValueError(f"Una orientación final no puede tener hijos: {ruta}")
        for campo in TEXTOS_HOJA:
            validar_texto(nodo.get(campo), f"{ruta}/{campo}")
        for campo in LISTAS_HOJA:
            validar_lista_textos(nodo.get(campo), f"{ruta}/{campo}")
        return True
    validar_texto(nodo.get("pregunta"), f"{ruta}/pregunta")
    if not hijos:
        raise ValueError(f"Rama sin opciones en {ruta}")
    if nivel == "Contexto de práctica" and len(hijos) != 1:
        raise ValueError(f"El contexto debe tener una orientación final: {ruta}")
    ids = set()
    siguiente = NIVELES[NIVELES.index(nivel) + 1]
    for indice, hijo in enumerate(hijos):
        validar_nodo(hijo, f"{ruta}/{indice}", nivel_esperado=siguiente)
        if hijo["id"] in ids:
            raise ValueError(f"Identificador duplicado entre hermanos en {ruta}: {hijo['id']}")
        ids.add(hijo["id"])
    return True


def validar_arbol(arbol):
    validar_nodo(arbol, nivel_esperado="Raíz")
    if arbol["id"] != "futbolia":
        raise ValueError("El árbol no corresponde a FutbolIA.")
    hojas = set()

    def comprobar(nodo, contexto=None):
        contexto = dict(contexto or {})
        campos = {
            "Objetivo": "tema",
            "Nivel de experiencia": "nivel_jugador",
            "Contexto de práctica": "contexto_practica",
        }
        if nodo["nivel"] in campos:
            contexto[campos[nodo["nivel"]]] = nodo["valor"]
        if nodo["nivel"] == "Área":
            contexto["area"] = nodo["valor"].removeprefix("Área ").casefold()
        if nodo["nivel"] == "Orientación final":
            if nodo["id"] in hojas:
                raise ValueError(f"Orientación duplicada: {nodo['id']}")
            hojas.add(nodo["id"])
            if any(
                (nodo[campo].casefold() if campo == "area" else nodo[campo]) != valor
                for campo, valor in contexto.items()
            ):
                raise ValueError(f"La ficha no corresponde a su ruta: {nodo['id']}")
        for hijo in nodo.get("hijos", []):
            comprobar(hijo, contexto)

    comprobar(arbol)
    return True
