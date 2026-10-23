"""Fachada compatible de la integración local; compone el servicio de orientación."""

from logica.cliente_ollama import consultar
from logica.configuracion import MODELO, TEMPERATURA
from logica.prompts import armar_prompt
from logica.servicio_guia import AVISOS, ServicioGuia

__all__ = ["MODELO", "TEMPERATURA", "AVISOS", "armar_prompt", "consultar", "generar_guia"]


def generar_guia(camino, hoja, modelo=MODELO, temperatura=TEMPERATURA, usar_ia=True):
    return ServicioGuia(consultar=consultar).generar(camino, hoja, modelo, temperatura, usar_ia)


if __name__ == "__main__":
    from logica.arbol import cargar_arbol

    print(f"FutbolIA listo: {cargar_arbol()['valor']}. Ejecute la interfaz para recorrer el árbol.")
