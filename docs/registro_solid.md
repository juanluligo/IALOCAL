# Registro de implementación SOLID

Plan: docs/superpowers/plans/2026-10-23-solid.md

- Diseño aprobado por el usuario; ejecución directa autorizada.
- Base: 19 pruebas, 17 correctas y 2 fallidas. Errores HTTP y validación reproducidos.
- No existe Git; se conserva una copia de los archivos fuente originales antes de modificarlos.
- Contratos compartidos revisados: constructor produce el mismo árbol que consume el repositorio; fachadas conservan imports existentes; Flask y Streamlit usan el mismo servicio.

## Trabajo completado

- Datos: catálogo JSON fuente con contenido y políticas de adaptación; constructor puro; navegación, validadores, repositorio y escritura atómica separados. Igualdad estructural completa del árbol con el ZIP original confirmada antes y después de regenerar: 453 nodos, 192 hojas.
- Orientación: formato, prompt, filtro, transporte y coordinación separados. El servicio admite sustitución de dependencias mediante funciones pequeñas. Configuración explícita, sin conversiones silenciosas.
- Interfaces: Flask con fábrica, contratos y presentación independientes; HTML, CSS y JavaScript separados; navegación con control de respuestas tardías. Streamlit con copia de datos por revisión, guías asociadas a configuración y control de rutas obsoletas. Contenedores reales reemplazan las cajas HTML vacías de las opciones.
- Modelo: generación desde árbol validado, síntesis de 16 temas en 5.298 bytes y conservación del SYSTEM personalizado. TXT original archivado como Markdown histórico fuera de modelo.
- Entorno: .venv, dependencias instaladas, requirements-lock.txt y scripts/verificar.py para repetir las comprobaciones. Ollama ya estaba instalado; se descargó llama3.2:1b y se creó futbolia sin modificar gpt-oss:20b.

## Revisión independiente

La guía requesting-code-review solicitó una revisión de lectura con contexto independiente. Encontró un desbordamiento al aplicar math.isfinite a enteros enormes enviados como temperatura. Se reprodujo con pruebas HTTP y directas antes de corregirlo; ahora se valida el rango antes de convertir a float. La prueba del entero de 400 dígitos devuelve 400 JSON por HTTP real.

No quedaron hallazgos críticos o importantes pendientes en la revisión. El revisor también confirmó la igualdad estructural con el árbol original.

## Decisiones de implementación

- Se trabajó sobre la carpeta autorizada porque no hay Git; no se inventó un repositorio ni se crearon commits. El original permanece en .respaldo/fuentes_originales.zip.
- Las políticas de adaptación se ampliaron dentro del catálogo JSON para permitir niveles y contextos nuevos sin ramas por identificador en Python. Se conserva exactamente la salida original.
- El Modelfile contiene una síntesis, no todas las variantes, para reducir contexto redundante. La ficha completa sigue en cada consulta.
- Se añadió rechazo de cargas numéricas no respaldadas tras observar una respuesta real que inventaba duraciones. El filtro sigue siendo heurístico; no se relajó para conseguir una respuesta aceptada.
- Se dejó de enviar un SYSTEM genérico desde el transporte para respetar el SYSTEM de futbolia. La prueba del adaptador cubre ese contrato.

## Verificación final — 23 de octubre de 2026

- scripts/verificar.py: dependencias compatibles, compilación Python correcta y 54/54 pruebas correctas, sin pruebas omitidas.
- Ruff: revisión estática correcta y 45 archivos con formato comprobado.
- Pruebas HTTP: las 192 orientaciones funcionan sin IA; entradas inválidas y número enorme se rechazan con 400.
- Streamlit: cuatro pruebas de interacción, incluidas configuración, respaldo, retroceso y ruta obsoleta; inicio y endpoint de salud HTTP 200.
- Navegador: recorrido completo de Flask hasta la ficha, generación sin IA y fuente de respaldo visibles; Streamlit carga con sus cuatro áreas. Captura en docs/evidencias/streamlit_funcionando.png.
- IA real: orientación de confianza deportiva solicitada a la API Flask con futbolia devolvió HTTP 200, fuente ollama y basica_aprobada en 5,09 s. Registro completo en .respaldo/prueba_http_ia_final.json.
- Respaldo real: respuesta de resistencia con cifras no aportadas por la ficha fue rechazada y sustituida por la ficha. Registro en .respaldo/prueba_ia_final.json.
- Los avisos ScriptRunContext del ejecutor de pruebas Streamlit son propios de su ejecución fuera del servidor y no son excepciones de la aplicación.

Aplicaciones locales iniciadas en http://127.0.0.1:8501 y http://127.0.0.1:5000. Registros y procesos de esta ejecución en .respaldo/.

## Actualización: normalización de ArbolFutbolIA.json

Esta actualización sustituye la decisión anterior de persistir un árbol expandido y un catálogo separado. La única fuente vigente es datos/ArbolFutbolIA.json en formato catalogo_futbolia versión 1. El archivo datos/catalogo.json ya no existe; CATALOGO_JSON es un alias de la fuente única.

- Antes: 9.357 líneas, 623.122 bytes, 192 copias de conocimiento ampliado.
- Después: 557 líneas, 28.919 bytes, 16 definiciones de tema; reducción del 95,4 % en bytes.
- El repositorio compone y valida el árbol en memoria, preservando las interfaces. La representación persistida crece con las definiciones y no con el producto de temas × niveles × contextos. La expansión en memoria todavía existe por compatibilidad con la navegación actual.
- Se retiró el catálogo duplicado después de comprobar la fuente normalizada guardada. El original expandido sigue conservado en el ZIP de respaldo de la primera revisión.
- generar_arbol.py valida y compone en memoria: no modifica ni vuelve a expandir el archivo. Modelfile y ambas interfaces usan el repositorio actualizado.
- Compatibilidad: cargar_arbol(ruta) acepta fuentes normalizadas independientes y árboles expandidos antiguos.
- Huella SHA-256 del árbol semántico anterior y actual: f8fa22218eac83ed4036420992b81c6981a5f74790034acd2f7e74c7d2fb0d8e.
- Verificación: 61 pruebas correctas, dependencias y compilación correctas. Revisión independiente de normalización, catálogo y datos: 19 pruebas correctas, sin hallazgos accionables.
- Instrucciones actuales en README.md y docs/arquitectura.md. Las secciones anteriores de este registro describen la evolución histórica.
