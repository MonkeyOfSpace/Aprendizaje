# Las tres capas: humano, harness, modelo

Material de la Fase 1. Escrito por el tutor el 23 oct 2026 a partir de las sesiones del 19 y el 23 (la conversación sobre el artículo de Theo "What is a harness?"). Es el marco en el que viven los materiales 01 (la herramienta) y 02 (el loop). Tu nota de la fase se escribe con esto delante, pero con tus palabras.

## Qué es

Un agente tiene tres capas, y cada pieza de código o texto vive en una sola:

| Capa | Quién la lee | Qué hace | En Jorgharness (`02_loop.py`) |
|---|---|---|---|
| **Interfaz humano ↔ harness** | Tú | Por donde entra tu petición y por donde ves lo que pasa | `sys.argv[1]`, los `print()` de cada vuelta, la "RESPUESTA FINAL" |
| **Interfaz modelo ↔ harness** | El modelo | Lo que el modelo ve del mundo y lo que el harness le devuelve | Las fichas (`HERRAMIENTAS`), los `tool_result`, y en la Fase 2 el system prompt |
| **Harness** | Nadie: se ejecuta | Parsea, decide, ejecuta, devuelve, frena | Las funciones, la tabla `FUNCIONES`, el `for`, los `if` sobre `stop_reason`, `MAX_VUELTAS` |

El modelo solo genera texto. El humano solo escribe y lee. El harness es lo que hay entre los dos, y es lo único de las tres capas que construyes tú. Por eso el plan entero va de harness: el modelo es una caja negra y el humano eres tú.

La definición que da Theo (23 oct 2026) encaja con la de la Fase 0: **agente = harness + modelo**. Ninguno de los dos hace nada solo. Un modelo sin harness escribe `tool_use` que nadie ejecuta (tu script 1 del 17 oct). Un harness sin modelo es un `for` que no sabe qué pedir.

### Las cinco piezas de un harness, según Theo, en tu loop

| Pieza | En `02_loop.py` |
|---|---|
| Herramientas que ejecutan código | `def leer_fichero`, `def listar_directorio` |
| Una sintaxis en texto para pedirlas | El bloque `tool_use` con `name`, `input` e `id` |
| Algo que parsea esa sintaxis y ejecuta | `if bloque.type == "tool_use"` y `FUNCIONES[bloque.name]` |
| Una vía para devolver el resultado | El `tool_result` con el mismo `id`, añadido al acta |
| Una lista de herramientas con descripciones | `HERRAMIENTAS`, las fichas |

Las cinco están en 60 líneas. Claude Code tiene las mismas cinco con mucha ropa encima.

### Interfaz frente a harness, en Claude Code

Theo lo dice de Claude Code y vale para Jorgharness: la terminal (o la pestaña Code del escritorio) es la interfaz; el harness va por debajo (el Agent SDK) y se puede meter en otras interfaces. En tu script, si cambias los `print()` por una ventana con botones, el agente se comporta igual. Truco para ver la costura: tapa con la mano todo lo que lleve `print` o `sys.argv`. Lo que queda es el harness, y funcionaría igual sin lo tapado, solo que a ciegas para ti.

## La interfaz del modelo tiene dos direcciones

Es la capa que más se confunde, porque es la única donde el harness habla en lenguaje natural. Tiene ida y vuelta:

- **De ida, lo que el modelo ve del harness:** las fichas. Y el system prompt, cuando lo haya.
- **De vuelta, lo que el harness le devuelve:** los `tool_result`. Un resultado de herramienta es la única ventana del modelo al mundo. Diseñarlo importa tanto como diseñar la ficha.

Ejemplo del 19 oct. `leer_fichero` con un fichero inexistente devolvía `ERROR: no existe el fichero 'NOTAS.md'`. Es un callejón sin salida: el modelo paró y te preguntó. La alternativa, que el harness enriquezca el error con lo que el modelo iba a pedir de todos modos:

```python
except FileNotFoundError:
    carpeta = os.path.dirname(ruta) or "."
    return (f"ERROR: no existe el fichero '{ruta}'. "
            f"Contenido de '{carpeta}':\n{listar_directorio(carpeta)}")
```

Ahora el error es una bifurcación. El harness no adivina qué busca el modelo; solo le da contexto para el siguiente paso. Gana una vuelta (más barato, determinista). Pierde tokens en cada error aunque el modelo no los necesite, y le quita al modelo la opción de no listar.

Y esta interfaz tiene una propiedad que la del humano no tiene: **se paga**. Cada carácter de ficha y cada `tool_result` entra en el acta y cuesta tokens en cada vuelta posterior (material 02, "Qué se paga"). La segunda ficha de tu loop cuesta unos 216 tokens en cada llamada. Por eso Claude Code carga algunas herramientas en diferido: la ficha completa solo entra en el acta cuando el modelo la pide. Es la Fase 2.

## Texto o código: dónde va cada garantía

Cuando quieres que el agente haga algo (por ejemplo, listar el directorio si el fichero no existe), tienes dos sitios donde actuar, uno en cada capa:

| | En la interfaz del modelo (texto) | En el harness (código) |
|---|---|---|
| Qué es | La ficha dice "si no lo encuentras, lista" | `leer_fichero` devuelve el listado junto al error |
| Qué ganas | Flexibilidad, cero código, el modelo decide con el objetivo en la cabeza | Garantía, una vuelta menos, comportamiento determinista |
| Qué pierdes | No es garantía: el 18 oct la ficha ya lo decía y el modelo preguntó igual | Tokens en cada error, y el modelo pierde la opción de no hacerlo |

**La regla:** si equivocarse es barato, texto. Si es caro o irreversible, código.

Claude Code hace las dos cosas, según lo que quiera garantizar:

- La ficha de `Grep` dice "prefiere esta herramienta a `grep` por Bash". Consejo en texto. Si el modelo usa `grep` por Bash, nada lo impide. Tendencia.
- La ficha de `Write` dice "sobrescribir un fichero que no has leído fallará". No es un consejo: el harness lo comprueba en código y la llamada falla. Garantía.

`escribir_fichero`, tu primera herramienta con efectos, es donde esta regla se aplica por primera vez en Jorgharness: qué pasa si el fichero ya existe es una decisión de garantía, no de tendencia.

## Cómo se diseña: consejos

**Pregunta "para quién es" antes de colocar una pieza.** Si lo lee el humano, interfaz. Si lo lee el modelo, interfaz del modelo. Si no lo lee nadie, harness. Cada pieza en una sola capa.

**Diseña el `tool_result` como diseñas la ficha.** Cuándo va bien, qué texto devuelve (nunca vacío). Cuándo falla, qué contexto lleva el error para que el modelo tenga un siguiente paso.

**Decide dónde va cada garantía con la regla barato/irreversible.** Lo que puede costar dinero o romper algo, en código. Lo demás, en texto, y acepta que es tendencia.

**Responde desde el harness.** Cuando algo sale raro, la pregunta útil no es "qué pensó el modelo" (no se puede saber) sino "qué le di y qué hice con lo que devolvió". Las dos cosas están en tu código.

**Trata la interfaz del modelo como un presupuesto.** Cada ficha y cada resultado se pagan en todas las vueltas siguientes. Antes de añadir una herramienta o alargar un resultado, pregúntate si vale lo que cuesta.

## Errores vistos en sesión

- **18 oct: responder desde el modelo.** En la narración del flujo en 10 pasos, tres veces se contestó "qué piensa el modelo" cuando la pregunta era qué hace el harness. El modelo es una caja negra; lo que se construye y lo que se depura es el harness.
- **19 oct: creer que cambiar la ficha resuelve el problema.** La ficha de `listar_directorio` ya decía "solo cuando no lo encuentres" y el modelo preguntó en vez de listar. El texto sube la probabilidad, no la asegura. La respuesta completa a "ficha o código" incluye siempre qué se pierde.
- **19 oct: "el harness no puede saber qué fichero busca el modelo".** Cierto, pero no necesita saberlo: puede enriquecer el error con el contexto que el modelo iba a pedir. Confundir "no puede adivinar" con "no puede ayudar".
- **23 oct: colocar las fichas en la interfaz del humano.** Las fichas parecen interfaz porque están en lenguaje natural, pero el humano nunca las ve: las lee el modelo. Son interfaz del modelo con el harness, y por tanto parte del harness. La corrección: la interfaz es para el humano; para el modelo, fichas más `tool_result`.

## Para ampliar

- Theo (t3.gg), "What is a harness?", artículo en X del 23 oct 2026: https://x.com/theo/status/2113424203345265053. Las cinco piezas, interfaz frente a harness, y la analogía de la cocina (modelo = chef, harness = cocina). Lo que no dice: que el harness también decide (frenos, permisos, errores enriquecidos); eso es lo que separa un harness de juguete de uno serio y es el trabajo de las Fases 4 y 6.
- Anthropic Engineering, "Writing effective tools for agents – with agents" (2025): la sección sobre qué devolver en los errores es la versión larga del ejemplo de `leer_fichero`.
- El código de pi (`pi-agent-core`), lectura de la Fase 4: un harness mínimo donde las tres capas se ven a simple vista.
- Las fichas de las herramientas de Claude Code (`Read`, `Write`, `Edit`, `Grep`, `Bash`). Pídemelas en sesión y léelas con la lista de comprobación del material 01.
