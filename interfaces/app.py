"""Adaptador HTTP de FutbolIA. Ejecutar: python interfaces/app.py."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify, render_template
from werkzeug.exceptions import RequestEntityTooLarge

from interfaces.contratos import leer_solicitud, opciones_solicitud
from interfaces.presentacion import presentar_nodo
from logica.ApiLocal import generar_guia
from logica.configuracion import MODELO
from logica.navegacion import bajar, profundidad
from logica.repositorio_arbol import cargar_arbol
from logica.validacion_arbol import validar_arbol


def create_app(arbol=None, generador=None):
    """Raíz de composición: permite sustituir datos y orientación sin cambiar rutas."""
    app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent / "templates"))
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
    arbol = cargar_arbol() if arbol is None else arbol
    validar_arbol(arbol)
    generar = generar_guia if generador is None else generador
    total_niveles = profundidad(arbol) + 1

    @app.get("/")
    def inicio():
        return render_template("index.html", modelo=MODELO)

    @app.errorhandler(RequestEntityTooLarge)
    def solicitud_demasiado_grande(_):
        return jsonify({"error": "La solicitud JSON supera el tamaño permitido."}), 413

    @app.post("/api/nodo")
    def api_nodo():
        try:
            datos = leer_solicitud()
            indices = datos.get("indices", [])
            nodo, camino = bajar(arbol, indices)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify(presentar_nodo(nodo, camino, indices, total_niveles))

    @app.post("/api/explicar")
    def api_explicar():
        try:
            datos = leer_solicitud()
            modelo, temperatura, usar_ia = opciones_solicitud(datos)
            nodo, camino = bajar(arbol, datos.get("indices", []))
            if nodo.get("hijos"):
                raise ValueError("Selecciona una hoja antes de solicitar orientación.")
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify(generar(camino, nodo, modelo, temperatura, usar_ia))

    return app


app = create_app()

if __name__ == "__main__":
    print("Abre http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
