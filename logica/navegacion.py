"""Navegación y métricas de árboles en memoria, sin persistencia."""


def bajar(arbol, indices):
    if not isinstance(indices, (list, tuple)):
        raise ValueError("La ruta debe ser una lista de índices.")
    nodo, camino = arbol, [arbol]
    for posicion, i in enumerate(indices):
        if isinstance(i, bool) or not isinstance(i, int):
            raise ValueError(f"Índice inválido: {i}")
        hijos = nodo.get("hijos", [])
        if not 0 <= i < len(hijos):
            raise ValueError(f"Índice inválido: {i}")
        nodo = hijos[i]
        camino.append(nodo)
        if not nodo.get("hijos") and posicion < len(indices) - 1:
            raise ValueError("La ruta continúa después de una hoja.")
    return nodo, camino


def avanzar(arbol, indices):
    bajar(arbol, indices)
    return list(indices)


def retroceder(arbol, indices):
    bajar(arbol, indices)
    return list(indices[:-1])


def contar(nodo):
    hijos = nodo.get("hijos", [])
    if not hijos:
        return 1, 1
    res = [contar(h) for h in hijos]
    return 1 + sum(x[0] for x in res), sum(x[1] for x in res)


def profundidad(nodo):
    hijos = nodo.get("hijos", [])
    return 0 if not hijos else 1 + max(profundidad(h) for h in hijos)
