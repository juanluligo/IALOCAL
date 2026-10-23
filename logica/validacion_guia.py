"""Filtro heurístico de pertinencia y patrones inseguros; no es validación clínica."""

import re
import unicodedata


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto).replace("–", "-").replace("—", "-"))
    texto = texto.encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", texto).strip()


# Reglas pequeñas independientes: se añaden patrones sin modificar el servicio.
PATRONES_INSEGUROS = (
    r"\b(?:entrena|entrenar|entrenes|continua|sigue|seguir)\s+(?:entrenando\s+)?(?:con|a pesar de(?:l)?)\s+dolor\b",
    r"\b(?:ignora|ignorar|ignores)\s+(?:el\s+)?dolor\b",
    r"\bno\s+(?:pares|te detengas|descanses)\s+(?:aunque|si)\b",
    r"\b(?:fuerza|forzar|fuerces)\s+(?:las\s+)?articulaciones\b",
    r"\bno\s+(?:bebas|tomes)\s+agua\b",
    r"\b(?:toma|tomar|tomes|usa|usar)\s+(?:ibuprofeno|paracetamol|analgesicos|medicamentos)\b",
)
PALABRAS_VACIAS = {"de", "del", "el", "la", "los", "las", "y", "en", "con", "para", "un", "una"}
PATRON_CARGA = re.compile(
    r"\b\d+(?:[.,]\d+)?(?:\s*(?:-|a)\s*\d+(?:[.,]\d+)?)?\s*"
    r"(?:minutos?|segundos?|horas?|repeticiones?|series?|kilometros?|metros?|kg|km|min|seg|%)(?!\w)"
)


def _contiene_patron_inseguro(texto):
    for patron in PATRONES_INSEGUROS:
        for coincidencia in re.finditer(patron, texto):
            # «No entrenes con dolor» y «evita entrenar con dolor» son precauciones.
            # No se permite que la negación atraviese una frase o una conjunción.
            prefijo = texto[max(0, coincidencia.start() - 50) : coincidencia.start()]
            negado = re.search(
                r"(?:\bno|\bnunca|\bevita|\bevitar)\s+(?:(?:debes|deberias|se debe|recomiendo)\s+)?$",
                prefijo,
            )
            if not negado:
                return True
    return False


def validar_guia(texto, hoja):
    if not isinstance(texto, str) or len(texto.strip()) < 80:
        return False, ["La respuesta está vacía o es demasiado breve."]
    normalizado = normalizar(texto)
    motivos = []
    if _contiene_patron_inseguro(normalizado):
        motivos.append("La respuesta contiene una recomendación potencialmente insegura.")
    contenido_ficha = " ".join(
        valor if isinstance(valor, str) else " ".join(valor)
        for valor in hoja.values()
        if isinstance(valor, str)
        or (isinstance(valor, list) and all(isinstance(v, str) for v in valor))
    )
    cargas_respaldadas = set(PATRON_CARGA.findall(normalizar(contenido_ficha)))
    if any(carga not in cargas_respaldadas for carga in PATRON_CARGA.findall(normalizado)):
        motivos.append("La respuesta añade cargas o duraciones numéricas no indicadas en la ficha.")
    tema = set(re.findall(r"[a-z0-9]+", normalizar(hoja.get("tema", "")))) - PALABRAS_VACIAS
    palabras = set(re.findall(r"[a-z0-9]+", normalizado))
    if not tema or not tema.intersection(palabras):
        motivos.append("La respuesta no menciona el tema seleccionado.")
    return not motivos, motivos
