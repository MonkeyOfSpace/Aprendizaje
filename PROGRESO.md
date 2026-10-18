# Progreso

## Fases

- [x] Fase 0: Montar el taller (19-25 oct 2026) · **aprobada el 17 oct**: proyecto con primer commit (15 oct), "Building effective agents" y Ousterhout 1-2 leídos (16 oct), reflexión "qué es un agente" escrita en el diario del 15 (17 oct). Las docs de Claude Code quedan como lectura pendiente para la semana 2
- [ ] Fase 1: Fundamentos del modelo (26 oct - 8 nov) · empezada el 17 oct: `01_una_herramienta.py` con `leer_fichero`; 18 oct: `02_loop.py`, el loop agente con `leer_fichero` y `listar_directorio` encadenándose solas. Queda `escribir_fichero` y la prueba de aprobado (crear y leer de vuelta), el parser de Aircall, los criterios JEV y la nota
- [ ] Fase 2: Context engineering (9-22 nov)
- [ ] Fase 3: Skills (23 nov - 6 dic)
- [ ] Fase 4: Harness: hooks, permisos y MCP (7-20 dic)
- [ ] Colchón (21 dic - 3 ene)
- [ ] Fase 5: Agentes y subagentes (4-17 ene 2027)
- [ ] Fase 6: Loop engineering (18-31 ene)
- [ ] Fase 7: Tu propio harness (1-14 feb)
- [ ] Fase 8: Consolidar y enseñar (15-21 feb)

## Autoevaluación por competencia (1 a 4, ver PLAN.md sección 2)

| Competencia | Inicio (14 oct) | Tras fase 2 | Tras fase 4 | Tras fase 6 | Final |
|---|---|---|---|---|---|
| Fundamentos del modelo | 1 | | | | |
| Context engineering | 1 | | | | |
| Skills | 1 | | | | |
| Harness | 1 | | | | |
| Agentes | 1 | | | | |
| Loop engineering | 1 | | | | |

## Artefactos construidos

(Se añaden al aprobar cada fase: ruta y una línea de qué hace.)

- `proyecto/` (15 oct): Jorgharness, entorno Python con el SDK de Anthropic y README con la primera hipótesis de qué piezas tiene un harness.
- `proyecto/01_una_herramienta.py` (17 oct): una llamada a la API con la herramienta `leer_fichero`; imprime el JSON de ida y vuelta, el `stop_reason` y los tokens. Todavía no es un agente: no hay loop.
- `proyecto/02_loop.py` (18 oct): el loop agente mínimo. Dos herramientas (`leer_fichero`, `listar_directorio`), ejecución por `name`, `tool_result` con el `id`, acta que crece, frenos de `max_tokens` y `MAX_VUELTAS`, tokens acumulados. Ya es un agente: encadena listar y leer sin intervención.

## Temas aparcados

(Cosas interesantes que surgieron fuera de la fase actual. Se revisan en la fase 8.)

- (18 oct, del loop) La descripción de una herramienta es un consejo que el modelo lee, no una regla que el harness aplica: con `NOTAS.md` inexistente el modelo preguntó en vez de listar. Dónde poner cada garantía (texto frente a código) es tema de las fases 4 y 6, y conecta con la herramienta `decidir` del hilo JEV.
- (16 oct, de Ousterhout caps. 1-2) Si el software ahora lo construyen agentes, ¿el diseño debe pensarse para que lo entienda un agente antes que un desarrollador humano? Conecta con la fase 2 (CLAUDE.md como documentación para el modelo) y con la fase 8.

## Hilo paralelo: fundamentos de diseño (1 h/semana, ver PLAN.md 8.5)

- [ ] Ousterhout caps. 1-5 (fases 0-1) · caps. 1-2 leídos el 16 oct
- [ ] Ousterhout caps. 6-10 (fases 2-3)
- [ ] Ousterhout caps. 11-15 (fases 4-5)
- [ ] Fowler caps. 1-4 (fases 6-7)

## Hilo: modelos de decisión (JEV y similares, ver PLAN.md 8.6)

- [ ] Criterios de decisión para el caso Aircall, escritos por el alumno antes de mirar ningún proveedor (antes de la sesión de la semana 2)
- [ ] Research conjunto del panorama: el tutor trae la tabla, el alumno la cruza con sus criterios (fase 1, semana 2)
- [ ] Parser de Aircall etiquetado tres veces (fase 1, semana 2)
- [ ] Herramienta `decidir` con umbral en código en el loop de juguete (fases 4-6)
- [ ] Mini-eval Haiku / JEV / modelo abierto sobre llamadas reales (fase 7)

## Rutas posteriores al plan

- [ ] Hugging Face y modelos abiertos (PLAN.md 8.4)
- [ ] Fundamentos de desarrollo de software, ruta completa (PLAN.md 8.5)
