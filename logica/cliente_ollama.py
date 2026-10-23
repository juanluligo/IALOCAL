"""Adaptador de transporte Ollama con espera acotada."""

from logica.configuracion import MODELO, TEMPERATURA, validar_opciones


def consultar(prompt, modelo=MODELO, temperatura=TEMPERATURA):
    from ollama import Client

    modelo, temperatura, _ = validar_opciones(modelo, temperatura)
    respuesta = Client(timeout=60).chat(
        model=modelo,
        # Ollama utiliza el SYSTEM del Modelfile; no lo sustituimos por otro genérico.
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperatura, "num_ctx": 8192, "num_predict": 1200},
    )
    return respuesta["message"]["content"]
