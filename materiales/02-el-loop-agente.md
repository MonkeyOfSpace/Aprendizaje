# El loop agente

Material de la Fase 1. Escrito por el tutor el 19 oct 2026 a partir de la sesión del 18. Tu nota "Qué es un agente, explicado con mi loop de 60 líneas" se escribe con esto delante, pero con tus palabras.

## Qué es

Una llamada a la API con herramientas **no es un agente**. El 17 oct lo viste: el modelo pidió leer el README, el script imprimió la petición y terminó. Nadie leyó nada.

Un agente es esa misma llamada metida en un bucle con tres pasos más:

1. **Ejecutar** la función que el modelo pidió, con los datos que rellenó.
2. **Devolver** el resultado al modelo, emparejado con la petición.
3. **Volver a llamar**, y repetir mientras el modelo siga pidiendo herramientas.

La frase que fijamos en la Fase 0: un agente decide **cada paso mirando el resultado del anterior**. El loop es lo que hace posible ese "mirando el resultado": sin él, el modelo nunca ve el resultado de nada.

Claude Code es exactamente esto. Cuando me escribes, Claude Code me llama una vez. Si pido ejecutar un comando, lo ejecuta, me devuelve la salida y me llama otra vez. Yo leo la salida y decido el siguiente paso. Se repite hasta que devuelvo solo texto. Claude Code es un `while` con mucha ropa encima; la ropa son las fases 2 a 6 del plan.

## Ejemplo real: `02_loop.py`, vuelta a vuelta

Pregunta: "¿Qué dice el fichero de requisitos del proyecto?". No se da el nombre del fichero.

```
VUELTA 1  stop_reason: tool_use | entrada: 733 | salida: 94
          -> el modelo pide listar_directorio con {"ruta": "."}
VUELTA 2  stop_reason: tool_use | entrada: 880 | salida: 57
          -> el modelo pide leer_fichero con {"ruta": "requirements.txt"}
VUELTA 3  stop_reason: end_turn | entrada: 966 | salida: 126
          --- RESPUESTA FINAL ---
          El fichero de requisitos del proyecto es `requirements.txt` y contiene
          anthropic==1.14.0 y python-dotenv==1.2.4...
Tokens totales: 2579 entrada, 277 salida, en 3 vuelta(s).
```

Nadie le dijo ese orden. En la vuelta 1 no sabía el nombre y listó. En la vuelta 2 tenía el listado delante y eligió `requirements.txt`. En la vuelta 3 tenía el contenido y contestó. Cada paso se decidió mirando el resultado del anterior.

## El acta: la lista `mensajes`

El modelo **no tiene memoria entre llamadas**. Cada llamada a la API es nueva y el modelo solo sabe lo que va en ella. Por eso el harness mantiene una lista, `mensajes`, que es el acta de la conversación, y la envía entera en cada vuelta.

Así crece el acta en el ejemplo de arriba:

```
Antes de la vuelta 1:
  [user]      "¿Qué dice el fichero de requisitos del proyecto?"

Antes de la vuelta 2:
  [user]      "¿Qué dice el fichero de requisitos del proyecto?"
  [assistant] tool_use: listar_directorio {"ruta": "."}            <- lo que él pidió
  [user]      tool_result (id de arriba): "01_una_herramienta.py\n02_loop.py\nREADME.md\n..."

Antes de la vuelta 3:
  ... todo lo anterior, más:
  [assistant] tool_use: leer_fichero {"ruta": "requirements.txt"}
  [user]      tool_result (id de arriba): "anthropic==1.14.0\npython-dotenv==1.2.4"
```

Tres cosas que sorprenden la primera vez:

- **El `tool_result` va con rol `user`.** Para el modelo, el resultado de una herramienta es algo que le llega desde fuera, igual que un mensaje tuyo. No hay un canal especial.
- **Lo que el modelo escribe en una vuelta se le reenvía como entrada en la siguiente.** Los 94 tokens de salida de la vuelta 1 están dentro de los 880 de entrada de la vuelta 2.
- **El `id` empareja petición y resultado.** El modelo lo inventa en el `tool_use`; el harness lo copia en `tool_use_id` del `tool_result`. Hace falta porque el modelo puede pedir varias herramientas en una misma respuesta.

En código, las dos líneas que hacen crecer el acta:

```python
mensajes.append({"role": "assistant", "content": respuesta.content})   # lo que él pidió
mensajes.append({"role": "user", "content": resultados})               # lo que obtuvo
```

## `stop_reason`: la señal que gobierna el loop

Cada respuesta trae un `stop_reason` que dice por qué el modelo dejó de escribir. El loop es un `if` sobre ese campo:

| `stop_reason` | Qué significa | Qué hace el harness en `02_loop.py` |
|---|---|---|
| `tool_use` | "Quiero usar estas herramientas" | Ejecuta, añade al acta, vuelve a llamar |
| `end_turn` | "He terminado, esta es mi respuesta" | Imprime los bloques `text` y sale |
| `max_tokens` | "Me cortaron a media frase" | Avisa al humano y sale |

El `max_tokens` es peligroso dentro de un loop: si el corte cae en mitad de un `tool_use`, el `input` llega incompleto y no se puede ejecutar. Lo viste el 17 oct con Haiku cortado a mitad de frase. Lo que no vale es ignorarlo y seguir como si fuera `end_turn`.

## Los frenos del harness

El modelo no controla cuándo para el loop; lo controla el harness. En `02_loop.py` hay tres frenos:

1. **`max_tokens`**: cuánto puede escribir el modelo en una vuelta. Lo impone la API, lo eliges tú.
2. **`MAX_VUELTAS`**: cuántas vueltas como máximo. Aunque el modelo siga pidiendo, el harness para a las 10. Sin esto, un modelo que se atasca pidiendo lo mismo gastaría dinero sin fin.
3. **El paso "decidir si ejecuta"**: tú lo colocaste en tu narración del 18 oct sin que te lo pidiera. Entre leer el `tool_use` y ejecutarlo, el harness puede mirar qué pide y negarse. En `02_loop.py` todavía ejecuta todo; en Claude Code es el sistema de permisos que te pregunta antes de un comando. Fase 4.

## Qué se paga: los tokens

Cada vuelta envía el acta completa. Todo lo que entra en el acta se paga en cada vuelta posterior:

| | Vuelta 1 | Vuelta 2 | Diferencia |
|---|---|---|---|
| "¿Qué dice el README?" (18 oct) | 517 entrada | 1189 entrada | 672: el `tool_use` (54) + el README entero en el `tool_result` (~600) |

El README se pagó una vez por leerlo y se habría pagado otra vez en cada vuelta si el agente hubiera seguido. Un agente que lee diez ficheros grandes y luego da veinte vueltas más está reenviando esos diez ficheros veinte veces. Controlar qué entra en el acta y cuánto tiempo se queda es la Fase 2.

## Cómo se diseña: consejos

**Separa las tres piezas.** Fichas (lo que el modelo ve), funciones (lo que el harness ejecuta) y loop (quién llama a quién). En `02_loop.py` son tres secciones numeradas. Cuando el proyecto crezca serán tres ficheros.

**Una tabla une el `name` con la función.** `FUNCIONES = {"leer_fichero": leer_fichero, ...}`. Añadir una herramienta es añadir una ficha, una función y una línea en la tabla. El loop no cambia.

**Ejecuta todos los `tool_use` de una respuesta y devuelve todos los `tool_result` en un solo turno `user`.** El modelo puede pedir dos herramientas a la vez (leer dos ficheros). Cada una lleva su `id`; los resultados van juntos en la misma lista. Si devuelves solo uno, la API rechaza la llamada.

**Salta los bloques que no son `tool_use`.** La respuesta puede traer `thinking` y `text` junto al `tool_use`. Solo se ejecutan los `tool_use`; los demás viajan en el acta porque `respuesta.content` se añade entero.

**Los errores vuelven al modelo, no rompen el loop.** Un `tool_result` puede llevar `"ERROR: no existe el fichero"`. El modelo lo lee y decide: listar, probar otro nombre, o preguntar. Es lo que permite que un agente se recupere.

**Registra cada vuelta.** `stop_reason`, tokens, qué herramienta pidió y con qué. Sin este registro no sabes qué hizo el agente ni cuánto costó, y no puedes depurarlo. Claude Code te lo enseña en pantalla por el mismo motivo.

**Decide qué hacer con `max_tokens` antes de que pase.** Parar y avisar, o subir el límite y reintentar. Nunca seguir.

**Pon un tope de vueltas desde el primer día.** Es la línea más barata del script y la que más dinero te puede ahorrar.

## Lo que tu loop todavía no tiene (y Claude Code sí)

Para que sepas qué viene, no para hacerlo ahora:

- Un **system prompt** que le diga al modelo quién es y cómo trabajar aquí (Fase 2).
- **Permisos**: el paso "decidir si ejecuta" con reglas (Fase 4).
- **Compactación** del acta cuando crece demasiado (Fase 2).
- **Hooks**: código que se ejecuta antes o después de cada herramienta (Fase 4).
- **Subagentes**: un loop que lanza otro loop con su propia acta (Fase 5).
- **Streaming**: ver la respuesta mientras se escribe en vez de al final (Fase 1, si da tiempo).

## Para ampliar

- Docs de Anthropic, "Tool use with Claude", sección sobre el flujo completo y los `stop_reason`.
- Anthropic, "Building effective agents" (ya leído en la Fase 0): vuelve a la sección de agentes con el loop delante; ahora el diagrama se lee distinto.
- El `tool_runner` del SDK de Python hace este loop por ti. Lo hicimos a mano a propósito; cuando lo mires, reconocerás cada pieza.
