"""Interfaz gráfica de FutbolIA. Ejecutar desde la raíz: python -m streamlit run interfaces/app_streamlit.py"""

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import streamlit as st

from logica.ApiLocal import MODELO, TEMPERATURA, generar_guia
from logica.arbol import bajar, cargar_arbol, contar, profundidad, retroceder
from logica.rutas import ARBOL_JSON

st.set_page_config(page_title="FutbolIA", page_icon="⚽", layout="wide")
st.markdown(
    """
<style>
.stApp{background:#0b1220;color:#edf3fa}
section[data-testid="stSidebar"]{background:#111c2e}
.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(120deg,#123d37,#174e70);border:1px solid #2b6a69;margin-bottom:1rem}
.hero h1{color:white;margin:0;font-size:2.4rem}.hero p{color:#d8eee8;margin:.4rem 0 0}
.small{color:#a9bbcf;font-size:.92rem}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def get_tree(version):
    """Cada revisión del archivo tiene su caché; cada sesión recibe su copia."""
    return cargar_arbol()


try:
    revision = ARBOL_JSON.stat()
    arbol = get_tree((revision.st_mtime_ns, revision.st_size))
except Exception as exc:
    st.error(f"No se pudo cargar el árbol de FutbolIA: {exc}")
    st.info("Revisa datos/ArbolFutbolIA.json y valídalo con: python logica/generar_arbol.py")
    st.stop()
st.session_state.setdefault("indices", [])
st.session_state.setdefault("guias", {})
nodos, hojas = contar(arbol)
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    usar_ia = st.toggle("Usar IA local (Ollama)", value=True)
    modelo = st.text_input("Modelo de Ollama", value=MODELO)
    temperatura = st.slider("Creatividad", 0.0, 1.0, TEMPERATURA, 0.1)
    st.markdown("---")
    st.markdown("## 🌳 Árbol de decisiones")
    st.caption(f"{profundidad(arbol) + 1} niveles máximos · {nodos} nodos · {hojas} hojas")
    st.markdown("**Cómo se alimenta la IA**")
    st.write(
        "La app entrega la ruta elegida y la ficha JSON al modelo en cada consulta. Esto contextualiza la respuesta, no reentrena el modelo."
    )
    if st.button("🔄 Recargar árbol", use_container_width=True):
        get_tree.clear()
        st.session_state.indices = []
        st.session_state.guias = {}
        st.rerun()
    if st.button("🏠 Volver al inicio", use_container_width=True):
        st.session_state.indices = []
        st.session_state.guias = {}
        st.rerun()

st.markdown(
    '<div class="hero"><h1>⚽ FutbolIA</h1><p>Orientación futbolística inclusiva · Árbol de decisiones · Inteligencia artificial local</p></div>',
    unsafe_allow_html=True,
)
st.write(
    "Explora una necesidad, revisa la información del catálogo y solicita una orientación personalizada. Puedes avanzar a tu ritmo y volver a cualquier paso."
)
try:
    nodo, camino = bajar(arbol, st.session_state.indices)
except ValueError:
    st.session_state.indices = []
    st.session_state.guias = {}
    nodo, camino = bajar(arbol, [])
    st.info("El recorrido anterior ya no está disponible. Vuelve a elegir un área.")
st.progress(
    min(len(st.session_state.indices) / max(1, profundidad(arbol)), 1.0),
    text=f"Recorrido: {len(st.session_state.indices)} decisiones",
)
st.markdown("**Ruta:** " + "  ›  ".join(n.get("valor", "") for n in camino))

if nodo.get("hijos"):
    st.subheader(nodo.get("pregunta", "Elige una opción"))
    hijos = nodo["hijos"]
    cols = st.columns(2 if len(hijos) > 2 else max(1, len(hijos)))
    for i, h in enumerate(hijos):
        with cols[i % len(cols)]:
            with st.container(border=True):
                st.markdown(f"### {h.get('icono', '⚽')} {h['valor']}")
                st.markdown(
                    f'<div class="small">{escape(h.get("pregunta", "Explorar esta opción"))}</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"Explorar {h['valor']}",
                    key=f"opt_{len(st.session_state.indices)}_{i}",
                    use_container_width=True,
                ):
                    st.session_state.indices = st.session_state.indices + [i]
                    st.session_state.guias = {}
                    st.rerun()
    if st.session_state.indices and st.button("⬅️ Paso anterior"):
        st.session_state.indices = retroceder(arbol, st.session_state.indices)
        st.session_state.guias = {}
        st.rerun()
else:
    st.subheader(f"🎯 {nodo.get('valor', 'Orientación')}")
    area = nodo.get("area", "Fútbol")
    st.caption(f"Área: {area} · Estado: orientación educativa general")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📘 Ficha del proyecto")
        st.write(nodo.get("detalle", ""))
        if nodo.get("nivel_jugador"):
            st.write("**Nivel:**", nodo["nivel_jugador"])
        if nodo.get("contexto_practica"):
            st.write("**Contexto:**", nodo["contexto_practica"])
        if nodo.get("conocimiento"):
            st.write("**Conocimiento:**", nodo["conocimiento"])
        if nodo.get("objetivo"):
            st.write("**Objetivo:**", nodo["objetivo"])
        if nodo.get("acciones"):
            st.write("**Pasos sugeridos:**")
            for a in nodo["acciones"]:
                st.markdown(f"- {a}")
        for campo, titulo in [
            ("progresion", "Progresión"),
            ("adaptaciones", "Adaptaciones inclusivas"),
            ("evaluacion", "Seguimiento educativo"),
        ]:
            if nodo.get(campo):
                st.write(f"**{titulo}:**")
                for item in nodo[campo]:
                    st.markdown(f"- {item}")
        if nodo.get("precaucion"):
            st.warning("Precaución: " + nodo["precaucion"])
    with col2:
        st.markdown("### 🤖 Orientación con IA")
        st.write("La IA recibe la ruta del árbol y esta ficha para elaborar una respuesta.")
        clave = (
            tuple(n["id"] for n in camino),
            modelo.strip(),
            temperatura,
            usar_ia,
            revision.st_mtime_ns,
            revision.st_size,
        )
        if st.button("Generar orientación", type="primary", use_container_width=True):
            try:
                with st.spinner("Preparando orientación…"):
                    st.session_state.guias = {
                        clave: generar_guia(camino, nodo, modelo, temperatura, usar_ia)
                    }
            except ValueError as exc:
                st.error(str(exc))
        resultado = st.session_state.guias.get(clave)
        if resultado:
            if resultado.get("aviso"):
                st.info(resultado["aviso"])
            st.markdown(resultado["texto"])
            st.caption(
                "Fuente: "
                + ("Ollama" if resultado["fuente"] == "ollama" else "ficha del sistema")
                + " · Validación: "
                + resultado.get("validacion", "no indicada")
            )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Elegir otra opción", use_container_width=True):
            st.session_state.indices = retroceder(arbol, st.session_state.indices)
            st.session_state.guias = {}
            st.rerun()
    with c2:
        if st.button("🏠 Volver al inicio", use_container_width=True):
            st.session_state.indices = []
            st.session_state.guias = {}
            st.rerun()

st.divider()
with st.expander("🧠 Cómo funciona todo el proyecto"):
    st.markdown("""
    1. **Árbol JSON:** guarda preguntas, opciones y fichas de conocimiento.
    2. **Interfaz:** muestra las opciones y registra el recorrido de la persona.
    3. **Lógica Python:** localiza la hoja elegida y prepara la ficha.
    4. **Ollama:** recibe la ruta y el contexto para redactar una orientación.
    5. **Respaldo:** si Ollama falla o está desactivado, se muestra la ficha del sistema.
    6. **Mejora del conocimiento:** edita `datos/ArbolFutbolIA.json`, ejecuta `python logica/generar_arbol.py` para validarlo y pulsa «Recargar árbol».

    La IA no reentrena sus parámetros con los cambios del JSON. El contenido se le proporciona como contexto en cada consulta.
    """)
st.caption(
    "FutbolIA es un prototipo educativo. No sustituye orientación deportiva o atención profesional."
)
