# Plan de estudio: de "uso IA para programar" a ingeniero de agentes

> Creado el 14 de octubre de 2026. Este documento es vivo: lo revisamos juntos al final de cada fase.

## 1. Punto de partida y meta

**Quién eres hoy**
- Background de Product Manager, programas a diario.
- Usas Claude Code y Copilot para chatear y generar código.
- Nunca has montado skills, hooks, subagentes ni un harness propio.
- Entre 6 y 10 horas semanales reales.
- Campos de práctica: GA_Tools_Front en el trabajo (React 19 + Vite + Tailwind, sin tests) y un proyecto personal nuevo.

**Quién quieres ser en 4 meses**
Alguien que no "usa IA" sino que **diseña sistemas de IA**: sabe qué entra en el contexto y por qué, encapsula conocimiento en skills, automatiza con hooks, delega en agentes, construye loops que se verifican a sí mismos y es capaz de montar su propio harness desde cero. Y además lo sabe explicar, que es lo que diferencia al experto del usuario avanzado.

Tu perfil de PM es una ventaja, no un obstáculo: el diseño de agentes es en gran parte diseño de producto (definir el trabajo, los límites, los criterios de "hecho", la experiencia del usuario del agente).

## 2. Mapa de competencias

Seis competencias, cada una con cuatro niveles. Nos autoevaluamos al final de cada fase en PROGRESO.md.

| Competencia | Nivel 1: usuario | Nivel 2: configura | Nivel 3: construye | Nivel 4: diseña y enseña |
|---|---|---|---|---|
| **Fundamentos del modelo** | Sabe chatear | Entiende tokens, contexto, tool use | Escribe un loop agente a mano contra la API | Explica trade-offs de coste, latencia y caché |
| **Context engineering** | Pega todo el código | Escribe un CLAUDE.md útil | Diseña memoria, progressive disclosure y compactación | Mide y optimiza el contexto de un equipo |
| **Skills** | Invoca skills ajenas | Crea una skill con instrucciones | Crea skills con scripts, recursos y evals | Mantiene una librería de skills del equipo |
| **Harness (hooks, permisos, MCP)** | Acepta cada prompt | Configura permisos y un hook | Escribe hooks y un servidor MCP propio | Diseña el harness de un equipo con seguridad |
| **Agentes** | Usa el agente por defecto | Lanza subagentes | Define agentes especializados y workflows | Construye un agente propio con el Agent SDK |
| **Loop engineering** | Pide y espera | Usa /loop y tareas programadas | Diseña loops con verificación y parada | Diseña loops autónomos con evals y costes acotados |

Meta del plan: **nivel 3 en todas, nivel 4 en al menos dos** (tú eliges cuáles en la fase 7).

## 3. Método semanal

Una semana tipo de 8 horas:

| Bloque | Horas | Qué |
|---|---|---|
| Lectura | 2 | Las fuentes de la fase, con notas en `notas/` |
| Construcción | 4 | El ejercicio de la fase, en el trabajo o en el proyecto personal |
| Sesión conmigo | 1 | Explicación del concepto y aplicación guiada en el momento |
| Escribir | 1 | Entrada en `diario/` y, al final de fase, una nota explicativa en `notas/` |

Reglas que nos damos:
1. **Nada se aprueba sin algo funcionando.** Cada fase termina con un artefacto real que usas después.
2. **Nada se aprueba sin explicarlo.** Cada fase termina con una nota escrita como si se la contaras a un compañero del equipo.
3. **En el trabajo, solo cosas reversibles.** Lo experimental va al proyecto personal.
4. **Una semana colchón** por Navidad. Si te retrasas, se consume el colchón, no se recorta el plan.

### Protocolo de las sesiones conmigo

Abre Claude Code en esta carpeta (`Aprendizaje`) y escribe, por ejemplo, "sesión de la semana 3". El `CLAUDE.md` de esta carpeta me dice cómo actuar:
1. Leo el diario y PROGRESO.md para saber dónde estás.
2. Te propongo la agenda de la sesión (30 min de concepto, 30 min de aplicarlo).
3. Te hago preguntas antes de darte respuestas. Si me pides que lo haga yo, lo hago pero te explico qué hice y por qué.
4. Cerramos actualizando el diario y marcando lo conseguido en PROGRESO.md.

## 4. Itinerario: 16 semanas en 8 fases

Fechas orientativas empezando el lunes 19 de octubre de 2026.

---

### Fase 0: Montar el taller (semana 1, 19-25 oct)

**Objetivo:** tener el entorno, la rutina y el proyecto personal listos.

**Construir**
- Crear el proyecto personal en `proyecto/` (ver propuesta en sección 5), con git y un README que diga qué es.
- Configurar Claude Code para ti: revisar `~/.claude/settings.json`, entender permisos y modos (default, acceptEdits, plan, auto).
- Escribir tu primera entrada en `diario/`.

**Leer**
- Documentación de Claude Code: visión general, permisos, memoria (CLAUDE.md), settings.
- "Building effective agents" (Anthropic Engineering). Léelo entero; es la base conceptual de todo el plan.

**Aprobado cuando:** proyecto personal con primer commit, y has escrito en el diario qué significa para ti "agente" tras leer el artículo.

---

### Fase 1: Fundamentos del modelo (semanas 2-3, 26 oct - 8 nov)

**Objetivo:** entender qué es un agente por dentro: modelo + loop + herramientas. Sin esto todo lo demás es magia.

**Conceptos:** tokens y ventana de contexto, mensajes system/user/assistant, tool use (defines la herramienta, el modelo pide llamarla, tú la ejecutas, devuelves el resultado), prompt caching, streaming, coste.

**Construir (proyecto personal)**
- Semana 2: un script en Node o Python que llama a la API de Claude con una herramienta definida por ti (por ejemplo `leer_fichero`). Observa el JSON de ida y vuelta.
- Semana 3: convertirlo en un **loop agente mínimo** de 50-80 líneas: el modelo pide herramientas hasta que deja de pedirlas. Añade `listar_directorio` y `escribir_fichero`. Ya tienes un Claude Code de juguete.

**Leer**
- Docs de la API: Messages, Tool use, Prompt caching.
- Skill `claude-api` dentro de Claude Code (pídeme que te la muestre).

**Escribir:** nota "Qué es un agente, explicado con mi loop de 60 líneas".

**Aprobado cuando:** tu loop puede crear un fichero y leerlo de vuelta sin que tú intervengas, y sabes decir cuántos tokens costó.

---

### Fase 2: Context engineering (semanas 4-5, 9-22 nov)

**Objetivo:** controlar qué ve el modelo. Es la competencia que más separa a quien obtiene buenos resultados de quien no.

**Conceptos:** qué entra en el contexto en cada turno de Claude Code (system prompt, CLAUDE.md, memoria, resultados de herramientas, resúmenes), progressive disclosure (dar poco y dejar que el agente pida más), compactación, memoria persistente, el coste de un contexto sucio, "just enough context".

**Construir (trabajo)**
- Auditar el CLAUDE.md actual de GA_Tools_Front: qué sobra, qué falta, qué debería estar en un fichero aparte que se lea bajo demanda.
- Añadir una sección de "cómo se hace X aquí" para las dos tareas más repetidas (por ejemplo: nueva página con ruta, nueva llamada al backend con el patrón data/loading/error).
- Medir: misma tarea antes y después del cambio, comparando tokens usados y calidad del resultado (`/explain-usage` en Claude Code).

**Construir (proyecto personal)**
- Añadir a tu loop un system prompt que se construye a partir de un fichero tipo CLAUDE.md del directorio actual. Ya entiendes cómo lo hace Claude Code.

**Leer**
- "Effective context engineering for AI agents" (Anthropic Engineering).
- Docs de Claude Code sobre memoria y CLAUDE.md. "Claude Code best practices".

**Escribir:** nota "Qué pongo en un CLAUDE.md y qué no, con ejemplos del nuestro".

**Aprobado cuando:** el CLAUDE.md del trabajo ha mejorado de forma medible y puedes dibujar en una pizarra qué entra en el contexto en un turno.

---

### Fase 3: Skills (semanas 6-7, 23 nov - 6 dic)

**Objetivo:** encapsular conocimiento reutilizable. Una skill es un procedimiento que el agente carga cuando toca.

**Conceptos:** anatomía de una skill (SKILL.md, descripción que dispara la carga, recursos, scripts), skills de usuario vs de proyecto vs plugin, cuándo una skill y cuándo CLAUDE.md, evals de skills (¿se dispara cuando debe? ¿hace lo que debe?).

**Construir (trabajo)**
- Semana 6: skill `nueva-pagina` para GA_Tools_Front: crea la página, la ruta en App.jsx, el enlace en Layout.jsx y el fetch con el patrón de la casa. Usa `/skill-creator`.
- Semana 7: skill `revisar-pr-front`: checklist de revisión propio del proyecto (español en UI, sin estado global, patrón de fetch, Tailwind v4). Probarla contra tres cambios reales.

**Construir (proyecto personal)**
- Hacer que tu loop lea un directorio `skills/` y añada al system prompt solo las descripciones; el contenido completo se carga con una herramienta `cargar_skill`. Acabas de implementar progressive disclosure.

**Leer**
- Docs de Claude Code: Skills. Skill `skill-creator` y sus evals.

**Escribir:** nota "Cómo decidir entre CLAUDE.md, skill y hook" (la reutilizarás en la fase 8).

**Aprobado cuando:** las dos skills funcionan, se disparan solas con la petición adecuada y has corrido al menos una eval sobre ellas.

---

### Fase 4: El harness: hooks, permisos y MCP (semanas 8-9, 7-20 dic)

**Objetivo:** entender que el "harness" es todo lo que rodea al modelo: herramientas, permisos, hooks, observabilidad. El modelo propone, el harness dispone.

**Conceptos:** hooks (PreToolUse, PostToolUse, Stop...) y por qué son deterministas mientras que las instrucciones no lo son; permisos y allowlists; MCP (Model Context Protocol) como forma estándar de dar herramientas; diferencia entre herramienta, skill y hook.

**Construir (trabajo)**
- Hook PostToolUse que lanza `npm run lint` tras cada edición de `.jsx` y devuelve los errores al agente. Tu primer hook de verdad.
- Hook que impide tocar `src/config.js` sin confirmación.
- Añadir Vitest al proyecto (sin tests el agente no puede verificar nada) con 3 tests sobre utilidades puras. Esto alimenta la fase 6.

**Construir (proyecto personal)**
- Un servidor MCP mínimo (una herramienta, por ejemplo "leer mis notas") y conectarlo a Claude Code.
- Añadir a tu loop un sistema de permisos: antes de `escribir_fichero` pregunta, y una lista de rutas prohibidas.

**Leer**
- Docs de Claude Code: Hooks, Settings, MCP. Skill `update-config`. Especificación de MCP (modelcontextprotocol.io), solo la introducción y "tools".

**Escribir:** nota "Instrucción vs hook: cuándo quiero que algo pase siempre".

**Aprobado cuando:** el lint se ejecuta solo tras cada edición, tu MCP aparece en Claude Code y tu loop rechaza escribir en una ruta prohibida.

---

### Semana colchón (21 dic - 3 ene)

Dos semanas de Navidad que cuentan como una de trabajo. Repaso, poner al día el diario, o recuperar retraso.

---

### Fase 5: Agentes y subagentes (semanas 10-11, 4-17 ene)

**Objetivo:** delegar bien. Un subagente es un contexto limpio con un encargo acotado; saber cuándo usarlo es la mitad del valor.

**Conceptos:** por qué delegar (aislamiento de contexto, paralelismo), coste de la delegación (lo que se pierde en el resumen), definiciones de agente (`.claude/agents/*.md`: modelo, herramientas, prompt), orquestador vs trabajador, workflows deterministas vs agentes autónomos (volver a "Building effective agents").

**Construir (trabajo)**
- Agente `revisor-ux` (solo lectura, modelo barato) que revisa coherencia de UI en español y responsive, y agente `revisor-datos` que revisa el patrón de fetch y errores. Lanzarlos en paralelo sobre un cambio real.
- Usar sesiones paralelas de Claude Code para dos tareas independientes y comparar con hacerlo en serie.

**Construir (proyecto personal)**
- Añadir a tu loop una herramienta `delegar(encargo)` que arranca un sub-loop con contexto nuevo y devuelve solo el resumen. Mide cuánto contexto ahorras.

**Leer**
- Docs de Claude Code: Subagents. Capítulo de orquestación de "Building effective agents". Artículos de Anthropic sobre sistemas multiagente.

**Escribir:** nota "Cuándo delegar y cuándo no: tres casos reales".

**Aprobado cuando:** dos agentes especializados producen revisiones útiles de un cambio real, y sabes explicar un caso en el que delegar fue peor.

---

### Fase 6: Loop engineering (semanas 12-13, 18-31 ene)

**Objetivo:** diseñar bucles que avanzan solos y saben parar. Aquí se junta todo lo anterior: contexto, skills, hooks y agentes.

**Conceptos:** el loop interno (modelo-herramienta-resultado) vs el loop externo (tarea-verificar-corregir-repetir), criterios de parada, verificación objetiva (tests, lint, build) frente a autoevaluación del modelo, presupuesto de iteraciones y coste, loops programados, el peligro de un loop sin verificación (converge en basura con confianza).

**Construir (trabajo)**
- Loop "ponlo en verde": dado un lint o test en rojo, el agente itera hasta verde con máximo N intentos, y si no lo consigue deja un informe. Con `/loop` primero, luego como hook + script.
- Tarea programada semanal: resumen de qué cambió en el repo y qué partes no tienen tests.

**Construir (proyecto personal)**
- Añadir a tu loop un loop externo: recibe una tarea y un comando de verificación (`npm test`), itera hasta que pasa o se agota el presupuesto, y registra cada intento. Esto es el corazón de un harness.

**Leer**
- Docs de Claude Code: `/loop`, tareas programadas, Agent SDK (visión general). Artículos sobre agentic loops y verificación.

**Escribir:** nota "Anatomía de un loop que sabe parar".

**Aprobado cuando:** tu loop externo arregla solo un test que tú rompes a propósito, y para cuando no puede.

---

### Fase 7: Tu propio harness (semanas 14-15, 1-14 feb)

**Objetivo:** construir un agente propio de principio a fin con el Agent SDK, aplicado a un problema tuyo. El capstone técnico.

**Construir (proyecto personal, propuesta)**
Un **agente de release notes y PRD inverso**: lee el historial de git de GA_Tools_Front (o de cualquier repo), agrupa cambios por funcionalidad, pregunta lo que no sabe, y escribe notas de versión en español para negocio. Une tu perfil de PM con todo lo aprendido:
- Context engineering: qué parte del diff enseñar al modelo.
- Skills: formato de notas de la casa.
- Hooks/permisos: solo lectura sobre el repo.
- Subagente: uno por área funcional.
- Loop: itera hasta que las notas cubren todos los commits.
- Evals: un conjunto de 5 releases pasadas con notas "buenas" escritas por ti para comparar.

Si prefieres otro problema, lo elegimos juntos al terminar la fase 5. Lo importante es que use las seis competencias.

**Leer**
- Docs del Agent SDK (TypeScript o Python, el que uses). Docs de evals de Anthropic.

**Aprobado cuando:** el agente corre de principio a fin en un repo real y tienes una tabla de evals con resultados.

---

### Fase 8: Consolidar y enseñar (semana 16, 15-21 feb)

**Objetivo:** convertir lo aprendido en algo que otros puedan usar. Aquí es donde pasas de nivel 3 a nivel 4.

**Construir**
- Elegir las dos competencias donde quieres el nivel 4 y escribir una guía corta para tu equipo de cada una (reutilizando las notas de cada fase).
- Presentación de 20 minutos para el equipo de Grupo Alquila: "cómo usamos IA en el front y qué hemos automatizado".
- Autoevaluación final en PROGRESO.md y diseño del plan de los siguientes 3 meses (ya lo harás tú; yo reviso).

**Aprobado cuando:** has dado la presentación o la has grabado, y las guías están en el repo del trabajo.

---

## 5. El proyecto personal: "mi propio Claude Code"

A lo largo del plan construyes, pieza a pieza, un agente de código de juguete:

| Fase | Pieza que añades |
|---|---|
| 1 | Loop modelo-herramientas con leer, listar y escribir ficheros |
| 2 | System prompt desde un fichero de contexto del directorio |
| 3 | Directorio de skills con carga bajo demanda |
| 4 | Permisos, rutas prohibidas, y un servidor MCP conectado |
| 5 | Herramienta `delegar` que crea un sub-loop |
| 6 | Loop externo con verificación y presupuesto |
| 7 | Reescritura o ampliación con el Agent SDK para el capstone |

Al final no habrás "leído sobre harnesses": habrás construido uno y sabrás por qué Claude Code está hecho como está. Lenguaje recomendado: **Node/TypeScript**, porque es lo que ya usas en el front y el Agent SDK lo soporta. Python es igual de válido si lo prefieres.

## 6. Fuentes principales

Las URLs exactas pueden cambiar; te las confirmo en cada sesión.
- Anthropic Engineering: "Building effective agents", "Effective context engineering for AI agents", "Claude Code best practices", artículos sobre sistemas multiagente.
- Documentación de Claude Code (docs.claude.com): memoria, settings, hooks, skills, subagents, MCP, Agent SDK.
- Documentación de la API de Claude: Messages, Tool use, Prompt caching, Evals.
- Especificación de MCP: modelcontextprotocol.io.
- Skills instaladas en tu Claude Code que puedes leer como ejemplos reales: `skill-creator`, `claude-api`, `update-config`, `code-review`, `loop`.

## 7. Cómo sabrás que lo has conseguido

No por haber leído el plan, sino porque:
1. Ante una tarea nueva, lo primero que piensas es "¿qué contexto necesita el agente y cómo verificará que está bien?", no "¿qué le escribo en el prompt?".
2. Tienes skills, hooks y agentes en el trabajo que usan otros, no solo tú.
3. Has construido un agente completo que resuelve un problema real.
4. Puedes explicar cada pieza a alguien del equipo, y lo has hecho.

## 8. Rutas adicionales y contexto que aprovecha el plan

Añadido el 14 de octubre tras revisar el plan. Las 16 semanas no cambian; esto dice dónde encaja cada cosa nueva y qué queda para después.

### 8.1 Ya usas la API con Haiku: úsalo en la fase 1

En `aircall-inquilinos` (y `witei_db`) ya hay código tuyo que llama a la API de Anthropic con Haiku para parsear llamadas. Es el mejor punto de partida posible para la fase 1:
- Semana 2: antes de escribir nada nuevo, leemos ese parser juntos y lo etiquetamos: dónde está el system prompt, dónde el contexto, qué le falta para ser un agente (no hay loop ni herramientas, es una llamada única). Esa es la diferencia entre "llamada a un LLM" y "agente".
- Semana 2 también: calculamos lo que cuesta al mes y probamos prompt caching sobre él. Es tu primer ejercicio de coste real, no de juguete.
- Fase 7 (evals): el parser es candidato perfecto para un conjunto de evals, porque tienes llamadas reales con las que comparar.

### 8.2 Grupo Alquila es más que GA_Tools_Front

El workspace `ga_tools` tiene tres proyectos con una jerarquía de CLAUDE.md (uno raíz y uno por proyecto): `GA_Tools_Back` (FastAPI, Python), `GA_Tools_Front` (en vías de jubilación) y `captacion` (el CRM que el equipo usa a diario). Además están `alquila_portfolio`, `augur`, `aircall-*`, `witei_db` y otros.

Ajustes que implica, sin cambiar el calendario:
- **Fase 2:** la auditoría de contexto se hace sobre la jerarquía completa de `ga_tools`, no solo sobre un fichero. Ya tienes progressive disclosure montada (raíz corto, detalle por proyecto); vamos a entender por qué funciona y qué se puede medir.
- **Fase 3:** la skill `nueva-pagina` tiene más sentido en `captacion` que en GA_Tools_Front, porque es lo que va a seguir vivo. Pero `captacion` es crítico: la desarrollamos en GA_Tools_Front y la portamos cuando funcione.
- **Fase 4:** los hooks de lint van primero en GA_Tools_Front. En `captacion` solo cuando los hayas probado. Si quieres el ejercicio de tests en Python, `GA_Tools_Back` con pytest es la alternativa a Vitest.
- **Fase 5:** los agentes revisores se prueban contra cambios reales de `captacion`, que es donde hay movimiento.

### 8.3 nan.builders y pi: la ruta del harness abierto

nan.builders expone modelos de pesos abiertos (Qwen, GLM, Gemma, DeepSeek) por una API compatible con OpenAI. pi es un agente de código de terminal, de código abierto y deliberadamente mínimo: un loop, lectura y escritura de ficheros, ejecución de comandos, y poco más. Juntos son la mejor herramienta didáctica que podías tener para este plan:
- **Fase 4, lectura obligatoria:** el código de pi (el paquete del loop del agente, `pi-agent-core`). Claude Code es demasiado grande para leerlo; pi cabe en una tarde y es exactamente "un harness". Comparas lo que tiene y lo que no (sin MCP, sin subagentes, sin permisos) y entiendes qué decisiones son del harness y cuáles del modelo.
- **Fase 6 o 7, experimento:** apuntar tu loop de juguete a `api.nan.builders/v1` con Qwen o GLM en vez de a Claude. Si tu harness está bien diseñado, cambiar de modelo es cambiar una línea. Verás también qué modelos siguen bien las herramientas y cuáles no, que es una lección que no se puede leer, solo vivir.
- **Comparativa útil para el trabajo:** Haiku contra un modelo abierto en el parser de `aircall-inquilinos`, con los evals de la fase 7. Es una decisión de producto real con datos.

### 8.4 Hugging Face: ruta posterior (3-4 semanas tras el plan)

Hugging Face es el "GitHub de los modelos": hub de modelos y datasets, librerías para ejecutarlos y afinarlos, y la comunidad donde se publica lo abierto. Tiene más sentido después del plan, cuando ya sepas qué es un harness y hayas probado modelos abiertos vía nan.builders. Esbozo:
1. El hub: leer model cards, entender licencias, pesos, cuantización, qué significa "7B" o "MoE".
2. Ejecutar un modelo pequeño en local (Transformers o un servidor tipo llama.cpp o Ollama) y conectarlo a tu loop de juguete. Tercer proveedor para el mismo harness.
3. Datasets y evals: subir tu conjunto de evals del parser como dataset propio y correr una eval reproducible.
4. Fine-tuning ligero (LoRA) de un modelo pequeño con tus datos de llamadas. Solo para entender el proceso, no para producción.

Lo detallamos cuando llegues a la fase 7.

### 8.5 Fundamentos de desarrollo de software: hilo paralelo, no otro curso

Tienes razón y es más importante de lo que parece: la IA escribe el código, pero las decisiones de diseño (qué módulo, qué límite, qué se testea, qué es demasiado complejo) siguen siendo tuyas, y un agente amplifica tanto las buenas como las malas. Propongo un hilo paralelo de **una hora a la semana**, de lectura con una pregunta aplicada, dentro del presupuesto de 6-10 horas:

| Fases | Lectura | Pregunta que te llevas al ejercicio de la fase |
|---|---|---|
| 0-1 | "A Philosophy of Software Design" (Ousterhout), caps. 1-5: complejidad, módulos profundos | ¿Mi loop de juguete es un módulo profundo o una bolsa de funciones? |
| 2-3 | Ousterhout caps. 6-10: información oculta, interfaces generales, errores | ¿Qué debería ocultar una skill de quien la usa? |
| 4-5 | Ousterhout caps. 11-15: diseñarlo dos veces, comentarios, nombres | ¿Cómo se nombra y documenta un hook para que otro lo entienda? |
| 6-7 | "Refactoring" (Fowler), caps. 1-4: qué es, cuándo, los "code smells" | ¿Qué smells tiene lo que el agente ha escrito en el loop externo? |
| 8 | Repaso y elección de la siguiente ruta | |

Es un libro corto y otro del que solo lees la introducción. Después del plan, si quieres, montamos una ruta de fundamentos de verdad (testing como disciplina, arquitectura, patrones, sistemas distribuidos) ya con el criterio que te habrá dado construir un harness.

Tu perfil de PM vuelve a ayudar aquí: diseñar software es decidir qué no construir, qué exponer y qué ocultar. Ya lo haces con producto.

### 8.6 Modelos de decisión (JEV y similares): hilo corto, no fase nueva

Añadido el 14 de octubre a propuesta del alumno. Modelos como JEV (TypeSafe AI) no generan texto: reciben un estado y devuelven decisiones estructuradas con probabilidad calibrada (`choice`, `score`, `noul`). Su promesa frente a un generativo como Haiku es velocidad y precio, y su tesis de diseño es la del harness: "el modelo se ocupa de la incertidumbre; el código, de la política". Caso de uso real: clasificar y decidir urgencia o derivación de las llamadas de `aircall-inquilinos`.

Presupuesto: 3-4 horas en total, repartidas. El calendario no cambia.

| Dónde | Qué | Entregable |
|---|---|---|
| Fase 1, semana 2 | Research conjunto del panorama: JEV y los modelos del mismo estilo que vayan saliendo, frente a Haiku con salida estructurada y frente a un modelo abierto vía nan.builders. Criterios fijados antes de mirar proveedores, como una evaluación de proveedor de producto. | Nota en `notas/` con tabla de criterios y veredicto provisional |
| Fase 1, semana 2 | Al leer el parser de Aircall, etiquetarlo tres veces: llamada generativa, salida estructurada con tool use, modelo de decisión. Qué cambia en coste, latencia y garantías. | Sección en la nota de la fase 1 |
| Fases 4 y 6 | En el loop de juguete, herramienta `decidir(estado, pregunta)` que devuelve probabilidad, y en código el umbral que decide si el loop sigue, delega o para (flujo de tres niveles por confianza). | Pieza del harness |
| Fase 7, evals | Mini-eval con 20-30 llamadas reales de Aircall: Haiku actual contra JEV contra modelo abierto. Medir acierto, coste, latencia y calibración (cuando dice 0,9, ¿acierta el 90 %?). | Tabla de evals |

Avisos que nos damos: es un proveedor único, cerrado y con semanas de vida; la evidencia independiente es escasa y en inglés, y nuestras llamadas están en español. Lo que se aprende es el concepto (decisión calibrada con la política en código); el proveedor es intercambiable y el harness lo tratará así. La documentación de referencia es la de TypeSafe AI, no sitios comunitarios.
