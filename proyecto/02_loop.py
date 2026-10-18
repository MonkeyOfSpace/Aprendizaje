# Semana 3 de Jorgharness: el LOOP agente mínimo.
# El modelo pide herramientas; el harness las ejecuta y le devuelve el resultado;
# se repite hasta que el modelo deja de pedir. Esto ya es un agente.

import json
import os
import sys
import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
client = anthropic.Anthropic()

MODELO = "claude-haiku-5-5"
MAX_TOKENS = 1024
MAX_VUELTAS = 10   # freno del harness: aunque el modelo siga pidiendo, paramos aquí

# ---------- 1. Las fichas: lo que el modelo VE de las herramientas ----------

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

# Ficha escrita por Jorge (18 oct), con dos retoques: la descripción del parámetro
# decía "archivo a leer" (copiada de leer_fichero) y le faltaba una comilla.
listar_directorio_ficha = {
    "name": "listar_directorio",
    "description": (
        "Devuelve el listado completo de archivos de un directorio. "
        "La ruta debe ser relativa a la carpeta donde se ejecuta el script. "
        "Úsalo para encontrar archivos que te pide el usuario o que necesitas para resolver la tarea. "
        "No lo uses si ya tienes el nombre del fichero; solo cuando no lo encuentres."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ruta": {"type": "string", "description": "La ruta relativa del directorio a listar"},
        },
        "required": ["ruta"],
    },
}

HERRAMIENTAS = [leer_fichero_ficha, listar_directorio_ficha]

# ---------- 2. Las funciones: lo que el harness EJECUTA ----------
# El modelo nunca ve este código. Solo ve la ficha de arriba.

def leer_fichero(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: no existe el fichero '{ruta}'"   # el error también se devuelve al modelo

def listar_directorio(ruta):
    try:
        nombres = sorted(os.listdir(ruta))
    except FileNotFoundError:
        return f"ERROR: no existe el directorio '{ruta}'"
    # Marcamos las carpetas con "/" para que el modelo distinga fichero de directorio.
    lineas = [n + "/" if os.path.isdir(os.path.join(ruta, n)) else n for n in nombres]
    return "\n".join(lineas) if lineas else "(directorio vacío)"

# Tabla que une el `name` que escribe el modelo con la función Python que lo ejecuta.
FUNCIONES = {
    "leer_fichero": leer_fichero,
    "listar_directorio": listar_directorio,
}

# ---------- 3. El loop ----------

pregunta = sys.argv[1] if len(sys.argv) > 1 else "¿Qué dice el README?"
mensajes = [{"role": "user", "content": pregunta}]   # el acta: crece en cada vuelta
tokens_entrada_total = 0
tokens_salida_total = 0

for vuelta in range(1, MAX_VUELTAS + 1):
    print(f"\n{'=' * 20} VUELTA {vuelta} {'=' * 20}")

    respuesta = client.messages.create(
        model=MODELO,
        max_tokens=MAX_TOKENS,
        tools=HERRAMIENTAS,
        messages=mensajes,
    )
    tokens_entrada_total += respuesta.usage.input_tokens
    tokens_salida_total += respuesta.usage.output_tokens
    print("stop_reason:", respuesta.stop_reason,
          "| entrada:", respuesta.usage.input_tokens,
          "| salida:", respuesta.usage.output_tokens)

    # --- Paso 8: el modelo ha terminado ---
    if respuesta.stop_reason == "end_turn":
        print("\n--- RESPUESTA FINAL ---")
        for bloque in respuesta.content:
            if bloque.type == "text":
                print(bloque.text)
        break   # salimos del loop: el agente ha terminado

    # --- Paso 10: el modelo se quedó sin tokens ---
    if respuesta.stop_reason == "max_tokens":
        print(f"\nAVISO: el modelo se quedó sin tokens ({MAX_TOKENS}). Respuesta cortada, paro aquí.")
        break

    # --- Pasos 5, 6 y 7: el modelo pide herramientas ---
    if respuesta.stop_reason == "tool_use":
        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue   # puede haber bloques `text` o `thinking` mezclados; los saltamos
            print(f"-> el modelo pide {bloque.name} con {json.dumps(bloque.input, ensure_ascii=False)}")

            funcion = FUNCIONES[bloque.name]
            salida = funcion(**bloque.input)   # paso 6: ejecutar con el input desempaquetado

            # Paso 7: el resultado vuelve emparejado con el id de la petición.
            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,   # el mismo id que escribió el modelo en su tool_use
                "content": salida,          # lo que devolvió la función, tal cual (texto o error)
            })

        # El acta crece dos turnos: lo que él pidió y lo que obtuvo.
        mensajes.append({"role": "assistant", "content": respuesta.content})
        mensajes.append({"role": "user", "content": resultados})

else:
    # Este `else` del `for` solo se ejecuta si el loop agotó MAX_VUELTAS sin un `break`.
    print(f"\nParado por el harness: {MAX_VUELTAS} vueltas sin terminar.")

print(f"\nTokens totales: {tokens_entrada_total} entrada, {tokens_salida_total} salida, "
      f"en {vuelta} vuelta(s).")
