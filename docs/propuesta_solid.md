# Propuesta de corrección y separación de responsabilidades

## Objetivo
Corregir errores reproducidos y aplicar SOLID, especialmente responsabilidad única, conservando las interfaces y las 192 orientaciones.

## Diagnóstico verificado
- 17 de 19 pruebas pasan. Fallan el rechazo de recomendaciones inseguras y la ausencia del TXT obsoleto.
- POST /api/nodo con una lista JSON devuelve 500; un JSON malformado se transforma en la ruta raíz y devuelve 200.
- La cadena "false" activa IA porque se convierte con bool().
- validar_nodo acepta un objeto sin estructura y no comprueba tipos de los campos de las fichas.
- generar_arbol.py mezcla contenido deportivo, adaptación, construcción del árbol y escritura de archivos.
- arbol.py mezcla persistencia JSON, validación y navegación; ApiLocal.py mezcla prompt, transporte y coordinación del respaldo.
- crear_modelfile.py lee JSON sin usar la validación central.
- No hay repositorio Git. Flask está instalado; Streamlit y el cliente Ollama no están instalados.

## Enfoques
1. Recomendado: refactorización incremental, conservando contratos públicos. Extraer catálogo editable a JSON, separar lectura/escritura, validación, construcción, navegación, generación de prompts, transporte y coordinación. Permite comprobar equivalencia del árbol y mantener ambas interfaces.
2. Reescritura completa con clases para todos los componentes. Aumenta cambios y complejidad sin una necesidad demostrada en este prototipo.

## Diseño propuesto
- JSON almacena datos; SOLID se aplica a los componentes Python que los consumen. Un catálogo fuente contiene temas, niveles y contextos; el árbol existente continúa como salida generada compatible.
- Persistencia JSON se ocupa exclusivamente de lectura y escritura. Validadores independientes verifican estructura, tipos, campos obligatorios, niveles y duplicados entre hermanos.
- El constructor transforma el catálogo validado en árbol sin efectos sobre archivos. El comando generador coordina carga, construcción, validación y guardado.
- Navegación y métricas no conocen rutas de archivos.
- Separar formato de ficha y filtro heurístico de respuestas; cubrir rechazos inseguros, pertinencia y respuestas válidas con pruebas.
- Separar prompt y cliente Ollama del servicio de orientación. Inyectar dependencias pequeñas donde permita comprobar errores sin IA real, sin crear jerarquías artificiales.
- Flask valida objetos JSON y tipos explícitos; devuelve 400 ante entradas inválidas. Una fábrica permite sustituir árbol y servicio en pruebas.
- El generador de Modelfile reutiliza la carga validada. Actualizar README y arquitectura con las responsabilidades reales.
- Conservar el contenido del TXT obsoleto como documentación histórica fuera de modelo, identificándolo como no utilizado.

## Verificación prevista
Agregar primero pruebas que reproduzcan los errores; ejecutar toda la suite; comprobar igualdad completa del árbol generado, no solo recuentos; generar Modelfile; recorrer todas las hojas sin IA; ejecutar Flask y Streamlit y comprobar su arranque. La inferencia real requiere servidor Ollama y modelo disponibles y se informará por separado.

## Decisiones propuestas
Mantener Python, Flask, Streamlit, rutas públicas y nombres compatibles. No introducir base de datos ni cambiar la experiencia visual. La separación se realiza por motivos reales de cambio, usando funciones y contratos pequeños.
