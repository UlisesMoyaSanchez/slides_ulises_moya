# Agentes LLM — material de la charla

Este directorio contiene los tres entregables de la presentación "Agentes LLM":

```
intro_agentes_LLM/
├── presentacion/     # Slides en LaTeX Beamer (con diagramas TikZ)
├── codigo/            # Script Python de un agente simple con LLM local
└── notebook/          # Mismo agente, paso a paso en un notebook Jupyter
```

## Presentación

Compilar con `pdflatex` (dos pasadas, para que el índice y las referencias
queden bien resueltos):

```bash
cd presentacion
pdflatex main.tex
pdflatex main.tex
```

Genera `presentacion/main.pdf`. Requiere una instalación de TeX Live con
`beamer` y `tikz` (usa el tema `Madrid` con la paleta institucional del IIEG).

## Código y notebook (demo de agente local)

Ver `codigo/README.md` para instrucciones detalladas de instalación de
Ollama y ejecución. En resumen:

```bash
ollama pull qwen2.5
cd codigo
pip install -r requirements.txt
python agente_simple.py
```

Para el notebook:

```bash
cd notebook
jupyter notebook agente_llm_local.ipynb
```
