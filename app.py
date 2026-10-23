"""Punto de entrada de la interfaz gráfica principal."""

import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "interfaces" / "app_streamlit.py"), run_name="__main__"
)
