"""Opciones compartidas y validación independiente de la interfaz."""

MODELO = "futbolia"
TEMPERATURA = 0.3


def validar_opciones(modelo=MODELO, temperatura=TEMPERATURA, usar_ia=True):
    if not isinstance(modelo, str) or not modelo.strip():
        raise ValueError("El modelo debe ser texto no vacío.")
    if isinstance(temperatura, bool) or not isinstance(temperatura, (int, float)):
        raise ValueError("La temperatura debe ser un número entre 0 y 1.")
    # El rango rechaza también NaN/Infinity sin convertir enteros enormes a float.
    if not 0 <= temperatura <= 1:
        raise ValueError("La temperatura debe estar entre 0 y 1.")
    if not isinstance(usar_ia, bool):
        raise ValueError("usar_ia debe ser un booleano JSON (true o false).")
    return modelo.strip(), float(temperatura), usar_ia
