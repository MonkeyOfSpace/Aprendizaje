# Semana 2 de Jorgharness: UNA llamada a la API con UNA herramienta.
# No es un agente todavía: no hay loop. Solo queremos ver el JSON de ida y vuelta.

import json
import sys
import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8 por defecto
load_dotenv()                  # carga ANTHROPIC_API_KEY desde proyecto/.env
client = anthropic.Anthropic()  # el cliente la coge del entorno

MODELO = "claude-haiku-5-5"    # el más barato; cambiar aquí si hace falta

# La ficha de la herramienta. Es lo ÚNICO que el modelo ve de ella: no hay código detrás todavía.
leer_fichero = {
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
            "ruta": {
                "type": "string",
                "description": "La ruta relativa del archivo a leer",
            },
        },
        "required": ["ruta"],
    },
}

# La pregunta viene del primer argumento; si no hay, usamos una por defecto.
pregunta = sys.argv[1] if len(sys.argv) > 1 else "¿Qué dice el README?"
mensajes = [{"role": "user", "content": pregunta}]

# ---- IDA: esto es lo que enviamos ----
print("=" * 20, "IDA (lo que enviamos)", "=" * 20)
print(json.dumps({"model": MODELO, "tools": [leer_fichero], "messages": mensajes},
                 indent=2, ensure_ascii=False))

respuesta = client.messages.create(
    model=MODELO,
    max_tokens=1024,
    tools=[leer_fichero],
    messages=mensajes,
)

# ---- VUELTA: esto es lo que responde el modelo ----
print("=" * 20, "VUELTA (lo que responde)", "=" * 20)
print(respuesta.model_dump_json(indent=2))
print()
print("stop_reason:", respuesta.stop_reason)
print("tokens entrada:", respuesta.usage.input_tokens, "| tokens salida:", respuesta.usage.output_tokens)
