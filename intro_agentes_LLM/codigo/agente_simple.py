"""
Agente simple con un LLM local (Ollama) y tres herramientas.

Requisitos previos (ver README.md de esta carpeta):
    1. Tener Ollama instalado y corriendo (`ollama serve`).
    2. Haber descargado un modelo con soporte de tool-calling, por ejemplo:
       `ollama pull qwen2.5` o `ollama pull llama3.1`
    3. `pip install -r requirements.txt`

Ejecutar con:  python agente_simple.py
"""

import ollama
import datetime
import os

MODELO = "qwen2.5"  # cambia esto si usas otro modelo con tool-calling

# ------------------------------------------------------------------
# Paso 1: las herramientas. Son funciones Python normales, nada especial.
# El agente solo puede usar lo que nosotros exponemos aquí.
# ------------------------------------------------------------------

def calculadora(expresion: str) -> str:
    """Evalua una expresion aritmetica simple, ej. '3 * (4 + 2)'."""
    permitidos = set("0123456789+-*/(). ")
    if not set(expresion) <= permitidos:
        return "Error: la expresion contiene caracteres no permitidos."
    try:
        return str(eval(expresion, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error al evaluar: {e}"


def fecha_actual() -> str:
    """Devuelve la fecha y hora actual del sistema."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def leer_archivo(ruta: str) -> str:
    """Lee y devuelve el contenido de un archivo de texto local."""
    if not os.path.isfile(ruta):
        return f"Error: no existe el archivo '{ruta}'."
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()[:2000]  # recortamos por si el archivo es muy grande


# Diccionario para poder llamar a la funcion correcta a partir de su nombre
# (que es justo lo que nos va a devolver el modelo).
HERRAMIENTAS_DISPONIBLES = {
    "calculadora": calculadora,
    "fecha_actual": fecha_actual,
    "leer_archivo": leer_archivo,
}

# ------------------------------------------------------------------
# Paso 2: el "schema" de cada herramienta. Es la descripcion que le
# damos al modelo para que sepa que herramientas existen, que hacen
# y que argumentos esperan. El modelo NUNCA ejecuta la funcion: solo
# decide "quiero llamar a X con estos argumentos".
# ------------------------------------------------------------------

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "calculadora",
            "description": "Evalua una expresion aritmetica y devuelve el resultado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expresion": {
                        "type": "string",
                        "description": "Expresion aritmetica, ej. '12 * 7'",
                    }
                },
                "required": ["expresion"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fecha_actual",
            "description": "Devuelve la fecha y hora actual del sistema.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "leer_archivo",
            "description": "Lee el contenido de un archivo de texto local dada su ruta.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta al archivo a leer",
                    }
                },
                "required": ["ruta"],
            },
        },
    },
]


# ------------------------------------------------------------------
# Paso 3: el loop del agente (ciclo ReAct simplificado).
#
#   1. Mandamos el historial + las tools disponibles al modelo.
#   2. Si el modelo pide una tool call -> la ejecutamos, agregamos el
#      resultado al historial como mensaje de rol "tool", y volvemos
#      a preguntarle al modelo (vuelve al paso 1).
#   3. Si el modelo ya da una respuesta final (sin tool calls) -> la
#      mostramos y terminamos.
# ------------------------------------------------------------------

def ejecutar_agente(pregunta: str, max_iteraciones: int = 6) -> str:
    mensajes = [
        {
            "role": "system",
            "content": (
                "Eres un asistente que puede usar herramientas para responder "
                "con precision. Usa una herramienta cuando la necesites en vez "
                "de adivinar datos como fechas o resultados de calculos."
            ),
        },
        {"role": "user", "content": pregunta},
    ]

    for _ in range(max_iteraciones):
        respuesta = ollama.chat(model=MODELO, messages=mensajes, tools=TOOLS_SCHEMA)
        mensaje = respuesta["message"]
        mensajes.append(mensaje)

        tool_calls = mensaje.get("tool_calls")
        if not tool_calls:
            # El modelo ya no quiere usar herramientas: esta es la respuesta final.
            return mensaje["content"]

        # El modelo pidio una o mas herramientas: las ejecutamos una por una.
        for llamada in tool_calls:
            nombre = llamada["function"]["name"]
            argumentos = llamada["function"]["arguments"]

            print(f"  [Action] {nombre}({argumentos})")
            funcion = HERRAMIENTAS_DISPONIBLES.get(nombre)
            if funcion is None:
                resultado = f"Error: la herramienta '{nombre}' no existe."
            else:
                resultado = funcion(**argumentos)

            print(f"  [Observation] {resultado}")
            mensajes.append(
                {"role": "tool", "content": str(resultado), "name": nombre}
            )

    return "No se alcanzo una respuesta final dentro del limite de iteraciones."


if __name__ == "__main__":
    pregunta = (
        "¿Qué día es hoy y cuánto es el día del mes multiplicado por 7?"
    )
    print(f"Pregunta: {pregunta}\n")
    respuesta_final = ejecutar_agente(pregunta)
    print(f"\nRespuesta final: {respuesta_final}")
