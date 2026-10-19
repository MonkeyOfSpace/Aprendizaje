# Anatomía de una herramienta

Material de la Fase 1. Escrito por el tutor el 19 oct 2026 a partir de las sesiones del 17 y 18. Tu nota de la fase se escribe con esto delante, pero con tus palabras.

## Qué es

Una herramienta tiene dos mitades que viven en sitios distintos:

| Mitad | Quién la ve | Qué es | En Jorgharness |
|---|---|---|---|
| La **ficha** | El modelo | Un JSON con `name`, `description` e `input_schema` | `leer_fichero_ficha` |
| La **función** | El harness | Código que hace el trabajo | `def leer_fichero(ruta)` |

El modelo **nunca ve la función**. Solo lee la ficha, decide si la usa, y rellena el formulario que describe `input_schema`. El harness recibe ese formulario relleno, busca la función por el `name` y la ejecuta. Es un contrato: la ficha promete algo y la función lo cumple.

Analogía de PM: la ficha es la historia de usuario con sus criterios de aceptación. El desarrollador (la función) la implementa. Si la historia está mal escrita, el que la lee hace algo distinto de lo que querías, aunque el código sea perfecto.

## Ejemplo real: `leer_fichero`

La ficha que escribiste tú el 17 oct, tras tres iteraciones:

```python
leer_fichero_ficha = {
    "name": "leer_fichero",
    "description": (
        "Lee un archivo concreto cuando el usuario pide explícitamente información "
        "sobre el mismo o cuando es necesario para completar una tarea. "
        "No la uses para preguntas generales o conceptuales que no dependen de "
        "ningún fichero del proyecto. "
        "La ruta debe ser relativa a la carpeta donde se ejecuta el script. "
        "Devuelve el texto completo del fichero."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ruta": {"type": "string", "description": "La ruta relativa del archivo a leer"},
        },
        "required": ["ruta"],
    },
}
```

Las cuatro frases de la descripción hacen cuatro trabajos distintos:

1. **Cuándo sí**: "cuando el usuario pide explícitamente información sobre el mismo". Anclado en algo observable de la petición.
2. **Cuándo no**: "No la uses para preguntas generales o conceptuales".
3. **Una regla de uso**: "La ruta debe ser relativa".
4. **Qué devuelve**: "el texto completo del fichero".

Y lo que el modelo escribe cuando decide usarla (de la ejecución del 17 oct):

```json
{
  "type": "tool_use",
  "id": "toolu_01ABC...",
  "name": "leer_fichero",
  "input": { "ruta": "README.md" }
}
```

Fíjate: `name` es el de la ficha, `input` tiene exactamente las claves de `properties`, y el `id` lo inventa el modelo para que el harness pueda emparejar el resultado con la petición.

## Ejemplo real: la herramienta `Read` de Claude Code

Claude Code me da unas 20 herramientas con esta misma forma. La de leer ficheros tiene un parámetro obligatorio (`file_path`, ruta absoluta) y dos opcionales (`offset`, `limit`, para leer un trozo). Su descripción incluye una restricción ("la ruta debe ser absoluta") y consejos de uso ("si ya sabes qué parte necesitas, lee solo esa parte"). Es la misma estructura que la tuya, con más parámetros porque resuelve más casos. No la copies: el 17 oct copiaste "ruta absoluta" y "2000 líneas" para una herramienta que no tenía esos parámetros.

## Cómo se diseña: consejos

**Empieza por la función, no por la ficha.** Pregúntate qué es lo mínimo que necesita el código para hacer el trabajo. Para leer un fichero: la ruta. Lo demás (desde qué línea, cuántas) se queda fuera hasta que haga falta. Una herramienta con dos parámetros se usa mejor que una con seis.

**El disparador tiene que ser observable.** Tu primera versión decía "úsala solo si no tienes ya la respuesta". Eso deja la decisión en lo que el modelo *cree* saber, y ante "¿qué dice el README?" puede inventarse uno. La versión buena se ancla en la petición: "cuando el usuario pide información sobre un fichero". Es la diferencia entre un criterio de aceptación verificable y "cuando el dev se sienta seguro".

**Escribe el "cuándo no".** Es la mitad del contrato y la que más se olvida. Sin ella, el modelo tiende a usar la herramienta de más (cada uso cuesta una vuelta del loop y sus tokens).

**Todas las herramientas hablan el mismo idioma.** Si `leer_fichero` usa rutas relativas, `listar_directorio` también. El 18 oct escribiste "ruta absoluta" en la segunda y relativa en la primera: el modelo habría listado con una convención y leído con otra, y las rutas no casarían.

**El nombre del parámetro aparece en tres sitios y tiene que ser el mismo.** En `properties`, en `required` y en la firma de la función Python. El harness ejecuta `funcion(**bloque.input)`, que convierte `{"ruta": "README.md"}` en `leer_fichero(ruta="README.md")`. Si en la ficha pone `ruta` y en `required` pone `file_path`, falla.

**Los errores se devuelven como texto, no se lanzan.** Si el fichero no existe, la función devuelve `"ERROR: no existe el fichero 'x'"` y eso viaja al modelo en el `tool_result`. El modelo lee el error y puede recuperarse (listar el directorio, probar otro nombre). Si lanzaras una excepción, el agente moriría sin opción de arreglarlo.

**La descripción es un consejo, no una regla.** El 18 oct, con `NOTAS.md` inexistente, el modelo tenía el error delante, tenía `listar_directorio` y su ficha decía "solo cuando no lo encuentres". Aun así prefirió preguntarte. Lo que pones en texto es una tendencia; lo que necesitas garantizado va en código del harness. Dónde poner cada cosa es tema de las fases 4 y 6.

**Cada ficha se paga en cada llamada.** Con una herramienta, la vuelta 1 entraban 517 tokens. Con dos, 733. Los 216 de diferencia son la ficha de `listar_directorio`, y se pagan en cada vuelta aunque el modelo no la use. Diez herramientas con descripciones largas son miles de tokens por llamada. Es el primer motivo de la Fase 2 (context engineering).

**No copies fichas. O si copias, relee cada campo como si lo escribieras de cero.** Tres errores en dos días, los tres en lo copiado: `required: ["file_path"]` con el parámetro llamado `ruta`; `"name": "leer_fichero"` en la ficha de listar; "archivo a leer" en la descripción del parámetro de un directorio.

## Lista de comprobación antes de dar una herramienta al modelo

- [ ] `name` único y en el mismo idioma que la función que lo ejecuta.
- [ ] La descripción dice cuándo sí, cuándo no, las reglas de uso y qué devuelve.
- [ ] El "cuándo sí" se puede verificar mirando la petición del usuario.
- [ ] Cada parámetro tiene descripción propia, no copiada de otra herramienta.
- [ ] `required` lista exactamente los nombres de `properties` que son obligatorios.
- [ ] La función Python acepta esos mismos nombres como argumentos.
- [ ] La función devuelve texto siempre, también cuando falla.
- [ ] Las convenciones (rutas, formatos) coinciden con las demás herramientas.
- [ ] Has leído la descripción como si fueras el modelo: ¿sabrías cuándo usarla ante "¿qué dice el README?" y ante "explícame qué es un harness"?

## Para ampliar

- Docs de Anthropic, "Tool use with Claude": la referencia del formato de la ficha y del JSON de ida y vuelta.
- Anthropic Engineering, "Writing effective tools for agents – with agents" (2025): cómo escribir descripciones, qué errores devolver, cuántas herramientas dar. Lectura recomendada para la semana 3.
- Las fichas de las herramientas de Claude Code. Pídeme que te enseñe cualquiera en sesión.
