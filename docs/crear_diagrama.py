"""Genera un diagrama SVG de la arquitectura de FutbolIA sin dependencias externas."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "diagrama_futbolia.svg"
W, H = 1200, 820
boxes = [
    (420, 35, 360, 76, "Usuario / jugador", "Selecciona área, tema, nivel y contexto", "#174e70"),
    (420, 160, 360, 76, "Interfaz Streamlit o Flask", "Navegación y presentación", "#1d5b55"),
    (
        420,
        285,
        360,
        76,
        "Árbol de decisiones JSON",
        "192 orientaciones finales · 4 áreas",
        "#174e70",
    ),
    (
        70,
        420,
        320,
        90,
        "Sistema experto de respaldo",
        "Ficha estructurada + reglas básicas",
        "#6b4c1f",
    ),
    (
        440,
        420,
        320,
        90,
        "Servicio de orientación",
        "Prompt, transporte y respaldo separados",
        "#1d5b55",
    ),
    (810, 420, 320, 90, "Modelfile + Ollama", "Instrucciones generales + modelo local", "#5b3d79"),
    (250, 600, 320, 90, "Filtro de respuesta", "Pertinencia y patrones de seguridad", "#6b4c1f"),
    (640, 600, 320, 90, "Orientación al usuario", "Respuesta IA o ficha de respaldo", "#174e70"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="100%" height="100%" fill="#0b1220"/>',
    '<text x="600" y="20" text-anchor="middle" fill="#edf3fa" font-family="Arial" font-size="1"> </text>',
]
# arrows behind boxes
arrows = [
    ((600, 111), (600, 160)),
    ((600, 236), (600, 285)),
    ((500, 361), (230, 420)),
    ((600, 361), (600, 420)),
    ((700, 361), (970, 420)),
    ((600, 510), (410, 600)),
    ((230, 510), (370, 600)),
    ((970, 510), (800, 600)),
    ((570, 645), (640, 645)),
]
for (x1, y1), (x2, y2) in arrows:
    svg.append(
        f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#8ba5bc" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'
    )
svg.append(
    '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#8ba5bc"/></marker></defs>'
)
for x, y, w, h, title, subtitle, color in boxes:
    svg.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{color}" stroke="#9cb5c9" stroke-width="1.5"/>'
    )
    svg.append(
        f'<text x="{x + w / 2}" y="{y + 31}" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="19" font-weight="bold">{esc(title)}</text>'
    )
    svg.append(
        f'<text x="{x + w / 2}" y="{y + 56}" text-anchor="middle" fill="#edf3fa" font-family="Arial" font-size="13">{esc(subtitle)}</text>'
    )
svg.append(
    '<text x="600" y="770" text-anchor="middle" fill="#b7c8d9" font-family="Arial" font-size="16">Conocimiento estructurado sin archivo TXT: Modelfile + catálogo fuente JSON</text>'
)
svg.append("</svg>")
OUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Diagrama creado: {OUT}")
