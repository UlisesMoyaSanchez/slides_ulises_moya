# Agente simple con LLM local

Demo mínima de un agente con tool-calling corriendo 100% local, usando
[Ollama](https://ollama.com). Acompaña la sección final de la presentación
"Agentes LLM".

## 1. Instalar Ollama

- Linux: `curl -fsSL https://ollama.com/install.sh | sh`
- macOS / Windows: descargar el instalador desde https://ollama.com/download

Verifica que el servicio esté corriendo:

```bash
ollama serve   # si no arranca solo como servicio de sistema
```

## 2. Descargar un modelo con soporte de tool-calling

```bash
ollama pull qwen2.5
# alternativa: ollama pull llama3.1
```

Si usas otro modelo, actualiza la variable `MODELO` en `agente_simple.py`.

## 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

## 4. Ejecutar

```bash
python agente_simple.py
```

Deberías ver algo como:

```
Pregunta: ¿Qué día es hoy y cuánto es el día del mes multiplicado por 7?

  [Action] fecha_actual({})
  [Observation] 2026-07-02 10:15:00
  [Action] calculadora({'expresion': '2 * 7'})
  [Observation] 14

Respuesta final: Hoy es 2 de julio de 2026; 2 * 7 = 14.
```

## Qué mirar en el código

`agente_simple.py` está dividido en los mismos pasos que se explican en la
charla:

1. **Herramientas**: funciones Python normales (`calculadora`, `fecha_actual`,
   `leer_archivo`).
2. **Tool schemas**: la descripción de esas funciones en el formato que
   entiende Ollama, para que el modelo sepa que existen.
3. **Loop del agente**: el ciclo ReAct — el modelo pide una herramienta,
   nosotros la ejecutamos, le devolvemos el resultado, y repetimos hasta que
   ya no pida más herramientas.

El notebook `../notebook/agente_llm_local.ipynb` recorre exactamente lo mismo,
celda por celda con explicaciones.
