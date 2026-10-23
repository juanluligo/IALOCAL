"use strict";

// Estado de navegación exclusivo de esta página; los datos deportivos vienen de la API.
let indices = [];
let cargando = false;
let revision = 0;
const $ = (id) => document.getElementById(id);

async function post(url, datos) {
  const respuesta = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const contenido = await respuesta.json();
  if (!respuesta.ok) throw new Error(contenido.error || "Error en la solicitud");
  return contenido;
}

function texto(etiqueta, contenido, padre, clase) {
  const elemento = document.createElement(etiqueta);
  elemento.textContent = contenido;
  if (clase) elemento.className = clase;
  padre.appendChild(elemento);
  return elemento;
}

function lista(titulo, elementos, padre) {
  if (!elementos?.length) return;
  texto("h3", titulo, padre);
  const ul = document.createElement("ul");
  elementos.forEach((elemento) => texto("li", elemento, ul));
  padre.appendChild(ul);
}

function actualizarNavegacion() {
  $("atras").disabled = cargando || !indices.length;
  $("inicio").disabled = cargando || !indices.length;
  $("opciones").querySelectorAll("button").forEach((b) => { b.disabled = cargando; });
}

function mostrarFicha(ficha) {
  const caja = $("resultado");
  texto("h3", ficha.valor || "Orientación", caja);
  texto("p", ficha.detalle || "", caja);
  lista("Objetivo", [ficha.objetivo], caja);
  lista("Pasos sugeridos", ficha.acciones, caja);
  lista("Progresión", ficha.progresion, caja);
  lista("Adaptaciones inclusivas", ficha.adaptaciones, caja);
  lista("Seguimiento educativo", ficha.evaluacion, caja);
  if (ficha.precaucion) texto("p", `Precaución: ${ficha.precaucion}`, caja, "warning");
  const boton = texto("button", "Generar orientación", caja);
  boton.type = "button";
  const respuesta = texto("div", "", caja);
  boton.onclick = async () => {
    const revisionConsulta = revision;
    const ruta = [...indices];
    boton.disabled = true;
    boton.textContent = "Generando…";
    respuesta.replaceChildren();
    try {
      const resultado = await post("/api/explicar", { indices: ruta, usar_ia: $("usar-ia").checked });
      if (revisionConsulta !== revision) return;
      if (resultado.aviso) texto("p", resultado.aviso, respuesta, "warning");
      texto("pre", resultado.texto, respuesta);
      texto("small", `Fuente: ${resultado.fuente === "ollama" ? "Ollama" : "ficha del sistema"}`, respuesta);
    } catch (error) {
      if (revisionConsulta === revision) texto("p", error.message, respuesta, "warning");
    } finally {
      boton.disabled = false;
      boton.textContent = "Generar orientación";
    }
  };
}

async function cargar(nuevaRuta = []) {
  if (cargando) return;
  cargando = true;
  actualizarNavegacion();
  try {
    const ficha = await post("/api/nodo", { indices: nuevaRuta });
    indices = [...nuevaRuta];
    revision += 1;
    $("ruta").textContent = ficha.camino.join(" › ");
    $("pregunta").textContent = ficha.pregunta || ficha.valor;
    $("opciones").replaceChildren();
    $("resultado").replaceChildren();
    if (ficha.hoja) {
      mostrarFicha(ficha);
    } else {
      ficha.opciones.forEach((opcion, indice) => {
        const boton = texto("button", `${opcion.icono || "⚽"} ${opcion.valor}`, $("opciones"));
        boton.type = "button";
        boton.onclick = () => cargar([...indices, indice]);
      });
    }
  } catch (error) {
    $("resultado").replaceChildren();
    texto("p", error.message, $("resultado"), "warning");
  } finally {
    cargando = false;
    actualizarNavegacion();
  }
}

$("atras").onclick = () => cargar(indices.slice(0, -1));
$("inicio").onclick = () => cargar([]);
$("usar-ia").onchange = () => cargar([...indices]);
cargar();
