"""Verificación local repetible; no necesita servidor ni modelo de Ollama."""

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main():
    comandos = (
        ("Dependencias", ["-m", "pip", "check"]),
        (
            "Compilación Python",
            [
                "-m",
                "compileall",
                "-q",
                "app.py",
                "logica",
                "interfaces",
                "modelo",
                "tests",
                "docs",
                "scripts",
            ],
        ),
        ("Pruebas", ["-m", "unittest", "discover", "-s", "tests", "-v"]),
    )
    for nombre, argumentos in comandos:
        print(f"\n{nombre}", flush=True)
        subprocess.run([sys.executable, "-X", "utf8", *argumentos], cwd=RAIZ, check=True)
    print("\nVerificación completada correctamente.")


if __name__ == "__main__":
    main()
